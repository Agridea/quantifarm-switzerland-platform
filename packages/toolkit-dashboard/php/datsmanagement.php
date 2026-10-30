<?php
header('Access-Control-Allow-Headers: X-Requested-With, Authorization, Content-Type');
header('Access-Control-Allow-Methods: GET, POST');
header('Content-Type: application/json');

require_once 'app.php';

session_start();
CheckAdmin();

const QCSM = 'https://quantifarm.eu/ontology/';
const QCSMDATA = 'https://quantifarm.eu/data/dats/';
const QCSMCOUNTRYDATA = 'https://quantifarm.eu/data/countries/';
const RDFS = 'http://www.w3.org/2000/01/rdf-schema#';
const XSD = 'http://www.w3.org/2001/XMLSchema#';

// Form field -> RDF predicate mapping. 'multi' fields are comma-separated and stored
// as one triple per value (matching the dats-loader convention). This is the single
// place that decides which properties a user is allowed to write - no free-form SPARQL
// is ever accepted from the client.
$fieldMap = array(
    'title'          => array('pred' => QCSM . 'hasTitle',                              'multi' => false, 'uri' => false),
    'launchYear'     => array('pred' => QCSM . 'hasLaunchYear',                         'multi' => false, 'uri' => false, 'year' => true),
    'lastUpdateYear' => array('pred' => QCSM . 'lastUpdateYear',                        'multi' => false, 'uri' => false, 'year' => true),
    'description'    => array('pred' => RDFS . 'comment',                                'multi' => false, 'uri' => false),
    'keywords'       => array('pred' => QCSM . 'hasKeyword',                            'multi' => true,  'uri' => false),
    'sector'         => array('pred' => QCSM . 'isTargetedTowardsAgriculturalSector',    'multi' => true,  'uri' => false),
    'country'        => array('pred' => QCSM . 'isTargetedTowardsCountry',               'multi' => true,  'uri' => true, 'country' => true),
    'functionality'  => array('pred' => QCSM . 'hasFunctionality',                       'multi' => true,  'uri' => false),
    'benefits'       => array('pred' => QCSM . 'hasBenefits',                           'multi' => true,  'uri' => false),
    'delivery'       => array('pred' => QCSM . 'hasDigitalForm',                        'multi' => true,  'uri' => false),
    'languages'      => array('pred' => QCSM . 'hasSupportedLanguage',                  'multi' => true,  'uri' => false),
    'cost'           => array('pred' => QCSM . 'hasCostStructure',                      'multi' => false, 'uri' => false),
    'website'        => array('pred' => QCSM . 'hasWebPage',                            'multi' => false, 'uri' => true),
);

$req = json_decode(file_get_contents('php://input'));
$action = isset($_GET['a']) ? $_GET['a'] : (isset($req->action) ? $req->action : '');

switch ($action) {
    case 'list':
        $res = DatList();
        break;
    case 'get':
        $res = DatGet($_GET['uri'], isset($_GET['lang']) ? $_GET['lang'] : 'en');
        if (is_array($res)) $res['editable'] = DatIsOwner($_GET['uri']);
        break;
    case 'save':
        $res = DatSave($req);
        if (is_array($res) && !isset($res['error'])) $res['editable'] = true;
        break;
    case 'delete':
        $res = DatDelete($req->uri, $req->lastModified, isset($req->uiLanguage) ? $req->uiLanguage : '');
        break;
    case 'history':
        $res = DatHistory($_GET['uri']);
        break;
    default:
        http_response_code(400);
        $res = array('error' => 'unknown action: ' . $action);
}

echo json_encode($res);


// A DAT may only be changed by the user who created it (per the change log).
function DatIsOwner($uri) {
    require 'db.php';
    $rows = $db->execute_query("SELECT 1 FROM dat_change_log WHERE dat_uri = ? AND action = 'create' AND user_email = ? LIMIT 1", [$uri, $_SESSION['useremail']]);
    $ok = $rows->fetch_assoc() !== null;
    mysqli_close($db);
    return $ok;
}

// Matches the dats-loader convention (name.replace(" ","_").lower()), plus stripping of
// any character that isn't safe inside a SPARQL IRIREF, to keep DAT URIs injection-safe.
function DatSlug($name) {
    $slug = strtolower(str_replace(' ', '_', trim($name)));
    return preg_replace('/[^a-z0-9_\-]/', '', $slug);
}

function DatUri($name) {
    return QCSMDATA . DatSlug($name);
}

function NowIso() {
    return gmdate('Y-m-d\TH:i:s\Z');
}

// Returns rdfs:label + lastModified for every DAT, for the list/dropdown view.
function DatList() {
    $q = "PREFIX rdfs: <" . RDFS . ">\n"
       . "PREFIX qcsm: <" . QCSM . ">\n"
       . "SELECT ?uri ?label ?lastModified WHERE {\n"
       . "  GRAPH <https://quantifarm.eu/graphs/dats> {\n"
       . "    ?uri a qcsm:DigitalAgriculturalTechnology ;\n"
       . "         rdfs:label ?label .\n"
       . "    OPTIONAL { ?uri qcsm:lastModified ?lastModified }\n"
       . "  }\n"
       . "} ORDER BY LCASE(?label)";

    $data = SparqlAsk($q);
    if ($data === null) {
        http_response_code(502);
        return array('error' => 'triple store query failed');
    }

    $out = array();
    foreach ($data['results']['bindings'] as $b) {
        $out[] = array(
            'uri' => $b['uri']['value'],
            'label' => $b['label']['value'],
            'lastModified' => isset($b['lastModified']) ? $b['lastModified']['value'] : null,
        );
    }
    return $out;
}

// Returns all mapped properties for a single DAT URI.
function DatGet($uri, $language = 'en') {
    global $fieldMap;

    $language = strtolower((string)$language);
    if (!in_array($language, array('en', 'de', 'fr', 'it'), true)) $language = 'en';

    $q = "SELECT ?p ?o WHERE {\n"
       . "  GRAPH <https://quantifarm.eu/graphs/dats> {\n"
       . "    <" . $uri . "> ?p ?o .\n"
       . "  }\n"
       . "}";

    $data = SparqlAsk($q);
    if ($data === null) {
        http_response_code(502);
        return array('error' => 'triple store query failed');
    }

    $byPred = array();
    foreach ($data['results']['bindings'] as $b) {
        $byPred[$b['p']['value']][] = $b['o']['value'];
    }

    $translatedByPred = array();
    if ($language !== 'en') {
        global $datsTranslationsGraphURI;
        $translationQuery = "SELECT ?p ?o WHERE {\n"
            . "  GRAPH <" . $datsTranslationsGraphURI . "> {\n"
            . "    <" . $uri . "> ?p ?o .\n"
            . "    FILTER (lang(?o) = \"" . $language . "\")\n"
            . "  }\n"
            . "}";
        $translationData = SparqlAsk($translationQuery);
        if ($translationData === null) {
            http_response_code(502);
            return array('error' => 'translation graph query failed');
        }
        foreach ($translationData['results']['bindings'] as $b) {
            $translatedByPred[$b['p']['value']][] = $b['o']['value'];
        }
    }

    $out = array('uri' => $uri);
    $out['label'] = isset($byPred[RDFS . 'label']) ? $byPred[RDFS . 'label'][0] : '';
    $out['lastModified'] = isset($byPred[QCSM . 'lastModified']) ? $byPred[QCSM . 'lastModified'][0] : null;
    $out['translationStatus'] = isset($byPred[QCSM . 'translationStatus']) ? $byPred[QCSM . 'translationStatus'][0] : null;
    $out['sourceLanguage'] = isset($byPred[QCSM . 'hasSourceLanguage']) ? $byPred[QCSM . 'hasSourceLanguage'][0] : null;

    foreach ($fieldMap as $field => $def) {
        $values = $language !== 'en' && isset($translatedByPred[$def['pred']])
            ? $translatedByPred[$def['pred']]
            : (isset($byPred[$def['pred']]) ? $byPred[$def['pred']] : array());
        if (!empty($def['country'])) {
            $values = array_map(function ($value) {
                return str_replace('_', ' ', preg_replace('#^' . preg_quote(QCSMCOUNTRYDATA, '#') . '#', '', $value));
            }, $values);
        }
        $out[$field] = $def['multi'] ? implode(', ', $values) : (count($values) ? $values[0] : '');
    }

    return $out;
}

// Strips characters that would break out of a SPARQL IRIREF (<...>) to prevent injection
// via URI-typed fields (e.g. website). Rejects the value entirely if it still isn't a plausible URL.
function SparqlSafeUri($uri) {
    $uri = trim(str_replace(array('<', '>', ' ', '"', '\\'), '', $uri));
    if ($uri !== '' && !preg_match('#^https?://#i', $uri)) return '';
    return $uri;
}

// Builds the triples for a DAT from posted form fields (shared by create/update/undo).
function BuildTriples($uri, $data) {
    global $fieldMap;

    $triples = array();
    $triples[] = "<" . $uri . "> <" . RDFS . "label> \"" . SparqlEscape($data->name) . "\" .";
    $triples[] = "<" . $uri . "> a <" . QCSM . "DigitalAgriculturalTechnology> .";

    foreach ($fieldMap as $field => $def) {
        if (!isset($data->$field) || trim((string)$data->$field) === '') continue;

        if (!empty($def['country'])) {
            foreach (explode(',', $data->$field) as $v) {
                $v = trim($v);
                if ($v === '') continue;
                $countrySlug = preg_replace('/[^A-Za-z0-9_\-]/', '', str_replace(' ', '_', $v));
                $triples[] = "<" . $uri . "> <" . $def['pred'] . "> <" . QCSMCOUNTRYDATA . $countrySlug . "> .";
            }
        } elseif ($def['multi']) {
            foreach (explode(',', $data->$field) as $v) {
                $v = trim($v);
                if ($v === '') continue;
                $triples[] = "<" . $uri . "> <" . $def['pred'] . "> \"" . SparqlEscape($v) . "\" .";
            }
        } elseif ($def['uri']) {
            $safe = SparqlSafeUri((string)$data->$field);
            if ($safe === '') continue;
            $triples[] = "<" . $uri . "> <" . $def['pred'] . "> <" . $safe . "> .";
        } elseif (!empty($def['year'])) {
            $year = trim((string)$data->$field);
            if (!preg_match('/^\d{4}$/', $year) || (int)$year < 1980) continue;
            $triples[] = "<" . $uri . "> <" . $def['pred'] . "> \"" . $year . "\"^^<" . XSD . "gYear> .";
        } else {
            $triples[] = "<" . $uri . "> <" . $def['pred'] . "> \"" . SparqlEscape((string)$data->$field) . "\" .";
        }
    }

    if (!empty($data->sourceLanguage)) {
        $triples[] = "<" . $uri . "> <" . QCSM . "hasSourceLanguage> \"" . SparqlEscape($data->sourceLanguage) . "\" .";
        $triples[] = "<" . $uri . "> <" . QCSM . "translationStatus> \"pending\" .";
    }

    return $triples;
}

// Creates a new DAT or updates an existing one, enforcing optimistic locking via lastModified.
function DatSave($data) {
    if (strtolower((string)$data->sourceLanguage) !== 'en' || strtolower((string)$data->uiLanguage) !== 'en') {
        http_response_code(403);
        return array('error' => 'only English values can be edited');
    }

    if (empty(trim((string)$data->name))) {
        http_response_code(400);
        return array('error' => 'name is required');
    }

    foreach (array('launchYear' => 'launch year', 'lastUpdateYear' => 'last update year') as $field => $label) {
        if (isset($data->$field) && trim((string)$data->$field) !== ''
            && (!preg_match('/^\d{4}$/', trim((string)$data->$field)) || (int)$data->$field < 1980)) {
            http_response_code(400);
            return array('error' => $label . ' must be a year from 1980 onwards');
        }
    }

    $uri = isset($data->uri) && $data->uri !== '' ? $data->uri : DatUri($data->name);
    if (empty($data->uri) && DatSlug($data->name) === '') {
        http_response_code(400);
        return array('error' => 'name must contain at least one letter or digit');
    }
    $isNew = !isset($data->uri) || $data->uri === '';
    $now = NowIso();

    if ($isNew) {
        $existing = DatGet($uri);
        if (!empty($existing['label'])) {
            http_response_code(409);
            return array('error' => 'a DAT with this name already exists');
        }
    }

    if (!$isNew && !DatIsOwner($uri)) {
        http_response_code(403);
        return array('error' => 'only the creator of a DAT can change it');
    }

    if (!$isNew) {
        // Optimistic lock: fail if someone else changed this DAT since the form was loaded
        $clientTs = isset($data->lastModified) ? $data->lastModified : null;
        $ask = "PREFIX qcsm: <" . QCSM . ">\n"
             . "ASK { GRAPH <https://quantifarm.eu/graphs/dats> { <" . $uri . "> qcsm:lastModified "
             . ($clientTs ? ("\"" . SparqlEscape($clientTs) . "\"^^<http://www.w3.org/2001/XMLSchema#dateTime>") : '?any')
             . " } }";
        $res = SparqlAsk($ask);
        if ($res === null) {
            http_response_code(502);
            return array('error' => 'triple store query failed');
        }
        if ($clientTs && !$res['boolean']) {
            http_response_code(409);
            return array('error' => 'conflict: DAT was modified by another user, please reload');
        }
    }

    $oldValue = $isNew ? null : DatGet($uri);

    $triples = BuildTriples($uri, $data);
    $triples[] = "<" . $uri . "> <" . QCSM . "lastModified> \"" . $now . "\"^^<http://www.w3.org/2001/XMLSchema#dateTime> .";

    $update = "PREFIX rdfs: <" . RDFS . ">\n"
            . "PREFIX qcsm: <" . QCSM . ">\n"
            . "DELETE WHERE { GRAPH <https://quantifarm.eu/graphs/dats> { <" . $uri . "> ?p ?o } };\n"
            . "INSERT DATA { GRAPH <https://quantifarm.eu/graphs/dats> {\n" . implode("\n", $triples) . "\n} }";

    $result = CallSPARQLUpdate($update);
    if (!$result['ok']) {
        http_response_code(502);
        return array('error' => 'write failed: ' . $result['code'] . ' ' . $result['error']);
    }

    $newValue = DatGet($uri);
    LogDatChange($uri, $isNew ? 'create' : 'update', $oldValue, $newValue);
    RefreshRecommendationTool();

    return $newValue;
}

// Tells the recommendation tool to reload its in-memory copy of the triple store.
// Best effort: a failure must not fail the save.
function RefreshRecommendationTool() {
    global $tool1URL;
    $token = getenv('REFRESH_TOKEN');
    if (!$token) return;
    $ch = curl_init($tool1URL . '/admin/refresh');
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_POST, true);
    curl_setopt($ch, CURLOPT_HTTPHEADER, array('X-Refresh-Token: ' . $token));
    curl_setopt($ch, CURLOPT_CONNECTTIMEOUT, 2);
    curl_setopt($ch, CURLOPT_TIMEOUT, 5);
    curl_exec($ch);
    if (defined('PHP_VERSION_ID') && PHP_VERSION_ID < 80500) {
        curl_close($ch);
    }
}

// Deletes a DAT after checking it still exists with the expected lastModified (optimistic lock).
function DatDelete($uri, $clientTs, $uiLanguage = 'en') {
    if (strtolower((string)$uiLanguage) !== 'en') {
        http_response_code(403);
        return array('error' => 'only English values can be deleted');
    }
    if (!DatIsOwner($uri)) {
        http_response_code(403);
        return array('error' => 'only the creator of a DAT can delete it');
    }
    $oldValue = DatGet($uri);
    if (empty($oldValue['label'])) {
        http_response_code(404);
        return array('error' => 'DAT not found (already deleted?)');
    }
    if ($clientTs && $oldValue['lastModified'] !== $clientTs) {
        http_response_code(409);
        return array('error' => 'conflict: DAT was modified by another user, please reload');
    }

    $update = "DELETE WHERE { GRAPH <https://quantifarm.eu/graphs/dats> { <" . $uri . "> ?p ?o } }";
    $result = CallSPARQLUpdate($update);
    if (!$result['ok']) {
        http_response_code(502);
        return array('error' => 'delete failed: ' . $result['code'] . ' ' . $result['error']);
    }

    LogDatChange($uri, 'delete', $oldValue, null);
    RefreshRecommendationTool();

    return array('ok' => true);
}

function LogDatChange($uri, $action, $oldValue, $newValue) {
    require_once 'db.php';
    $stmt = $db->prepare("INSERT INTO dat_change_log (user_email, dat_uri, action, old_value, new_value, createdon) VALUES (?, ?, ?, ?, ?, ?)");
    $email = $_SESSION['useremail'];
    $oldJson = $oldValue === null ? null : json_encode($oldValue);
    $newJson = $newValue === null ? null : json_encode($newValue);
    $now = date('Y-m-d H:i:s');
    $stmt->bind_param("ssssss", $email, $uri, $action, $oldJson, $newJson, $now);
    $stmt->execute();
    $stmt->close();
    mysqli_close($db);
}

function DatHistory($uri) {
    require_once 'db.php';
    $rows = $db->execute_query(
        'SELECT id, user_email, action, old_value, new_value, undone_log_id, createdon FROM dat_change_log WHERE dat_uri = ? ORDER BY id DESC',
        [$uri]
    );
    $out = array();
    while ($row = $rows->fetch_assoc()) {
        $out[] = $row;
    }
    mysqli_close($db);
    return $out;
}
