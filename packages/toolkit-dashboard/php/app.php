<?php

// URLs for the API calls
$tool1URL  = "http://recommendation-tool:8000";
$tool2URL1 = "http://quantifarm-cost-benefit-calculator-v1-tool-api:8686";
$tool2URL2 = "http://quantifarm-cost-benefit-calculator-v2-tool-api:8686";
$tool3URL  = "http://quantifarm-cost-benefit-calculator-v2-tool-api:8686";
$sparqlURL = "http://triple-store:3030/quantifarm/query";
$sparqlUpdateURL = "http://triple-store:3030/quantifarm/update";
$datsGraphURI = "https://quantifarm.eu/graphs/dats";
$datsTranslationsGraphURI = "https://quantifarm.eu/graphs/dats-translations";
// Only this account may grant/revoke admin rights (see admin-users.html / adminusers.php)
// SUPER_ADMIN_EMAIL may contain several semicolon-separated addresses
$superAdminEmails = array_values(array_filter(array_map(fn($e) => strtolower(trim($e)), explode(';', getenv('SUPER_ADMIN_EMAIL') ?: ''))));
function IsSuperAdminEmail($email) {
    global $superAdminEmails;
    return in_array(strtolower(trim((string)$email)), $superAdminEmails, true);
}
// *********


function CheckLogin(){
    if (!isset($_SESSION['loggedin'])) {
        http_response_code(401);
        die ('not logged.');
    }
}

// DAT CRUD is restricted to accounts with the isadmin DB flag (never self-assignable, see register/upd in api.php)
function CheckAdmin(){
    CheckLogin();
    if (empty($_SESSION['isadmin'])) {
        http_response_code(403);
        die ('admin rights required.');
    }
}

// Granting/revoking admin rights is restricted to a single hardcoded super-admin account
function CheckSuperAdmin(){
    CheckLogin();
    if (!IsSuperAdminEmail($_SESSION['useremail'])) {
        http_response_code(403);
        die ('super-admin rights required.');
    }
}

function CallAPI($method, $url, $data) {
     
    $ch = curl_init($url);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_FAILONERROR, true);
    curl_setopt($ch, CURLOPT_CUSTOMREQUEST, $method);

    if ($_SERVER['HTTP_HOST'] == 'localhost') {
	    curl_setopt($ch, CURLOPT_SSL_VERIFYHOST, 0);
	    curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, 0);
    }
    
    if (!is_null($data)) {
        curl_setopt($ch, CURLOPT_HTTPHEADER, array('Content-Type: application/json'));
        curl_setopt($ch, CURLOPT_POSTFIELDS, json_encode($data));
    }

    $res = curl_exec($ch);

    $ec = curl_getinfo($ch, CURLINFO_HTTP_CODE);
    if ($ec == 0) $ec = 500;
    http_response_code($ec);

    if (curl_errno($ch)) {
        $res = 'curl error: ' . curl_errno($ch) . '> ' . curl_error($ch);
    }

    if (defined('PHP_VERSION_ID') && PHP_VERSION_ID < 80500) {
        curl_close($ch);
    }

    return $res;
}

function CallSPARQL($data) {
    global $sparqlURL;
    $method="POST";
    
    $ch = curl_init($sparqlURL);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_FAILONERROR, true);
    curl_setopt($ch, CURLOPT_CUSTOMREQUEST, $method);

    if ($_SERVER['HTTP_HOST'] == 'localhost') {
	    curl_setopt($ch, CURLOPT_SSL_VERIFYHOST, 0);
	    curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, 0);
    }
    
    curl_setopt($ch, CURLOPT_HTTPHEADER, array('Content-Type: application/sparql-query'));
    curl_setopt($ch, CURLOPT_POSTFIELDS, $data);

    $res = curl_exec($ch);

    $ec = curl_getinfo($ch, CURLINFO_HTTP_CODE);
    if ($ec == 0) $ec = 500;
    http_response_code($ec);

    if (curl_errno($ch)) {
        $res = 'curl error: ' . curl_errno($ch) . '> ' . curl_error($ch);
    }

    if (defined('PHP_VERSION_ID') && PHP_VERSION_ID < 80500) {
        curl_close($ch);
    }

    return $res;
}

// Executes a SPARQL ASK/SELECT query against the update endpoint's sibling query endpoint,
// returning the decoded JSON result (used for optimistic-lock checks before writing).
function SparqlAsk($query) {
    global $sparqlURL;

    $ch = curl_init($sparqlURL);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_CUSTOMREQUEST, 'POST');
    curl_setopt($ch, CURLOPT_HTTPHEADER, array(
        'Content-Type: application/sparql-query',
        'Accept: application/sparql-results+json'
    ));
    curl_setopt($ch, CURLOPT_POSTFIELDS, $query);

    if ($_SERVER['HTTP_HOST'] == 'localhost') {
        curl_setopt($ch, CURLOPT_SSL_VERIFYHOST, 0);
        curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, 0);
    }

    $res = curl_exec($ch);
    $ec = curl_getinfo($ch, CURLINFO_HTTP_CODE);

    if (defined('PHP_VERSION_ID') && PHP_VERSION_ID < 80500) {
        curl_close($ch);
    }

    if ($ec < 200 || $ec >= 300 || $res === false) {
        return null;
    }

    return json_decode($res, true);
}

// Executes a SPARQL 1.1 Update (INSERT/DELETE) against the /update endpoint.
// Returns true on success (HTTP 2xx), false otherwise - caller must check and abort on failure.
function CallSPARQLUpdate($update) {
    global $sparqlUpdateURL;

    $ch = curl_init($sparqlUpdateURL);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_CUSTOMREQUEST, 'POST');
    curl_setopt($ch, CURLOPT_HTTPHEADER, array('Content-Type: application/sparql-update'));
    curl_setopt($ch, CURLOPT_POSTFIELDS, $update);

    if ($_SERVER['HTTP_HOST'] == 'localhost') {
        curl_setopt($ch, CURLOPT_SSL_VERIFYHOST, 0);
        curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, 0);
    }

    $res = curl_exec($ch);
    $ec = curl_getinfo($ch, CURLINFO_HTTP_CODE);
    $err = curl_errno($ch) ? curl_error($ch) : null;

    if (defined('PHP_VERSION_ID') && PHP_VERSION_ID < 80500) {
        curl_close($ch);
    }

    return array('ok' => ($ec >= 200 && $ec < 300 && !$err), 'code' => $ec, 'error' => $err, 'body' => $res);
}

// Escapes a string for safe embedding as a SPARQL string literal (prevents SPARQL injection).
function SparqlEscape($str) {
    $str = str_replace('\\', '\\\\', $str);
    $str = str_replace('"', '\\"', $str);
    $str = str_replace("\n", '\\n', $str);
    $str = str_replace("\r", '\\r', $str);
    return $str;
}

function UploadFile($url, $file, $fieldName) {
    
    $f = new \CURLFile($file, 'text/csv');

    $ch = curl_init($url);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_FAILONERROR, true);
    curl_setopt($ch, CURLOPT_POST, true);
    curl_setopt($ch, CURLOPT_POSTFIELDS, [$fieldName => $f]);

    if ($_SERVER['HTTP_HOST'] == 'localhost') {
	    curl_setopt($ch, CURLOPT_SSL_VERIFYHOST, 0);
	    curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, 0);
    }
    
    $res = curl_exec($ch);

    $ec = curl_getinfo($ch, CURLINFO_HTTP_CODE);
    if ($ec == 0) $ec = 500;
    http_response_code($ec);

    if (curl_errno($ch)) {
        $res = 'curl error: ' . curl_errno($ch) . '> ' . curl_error($ch);
    }

    if (defined('PHP_VERSION_ID') && PHP_VERSION_ID < 80500) {
        curl_close($ch);
    }

    return $res;
}




