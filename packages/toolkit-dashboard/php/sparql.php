<?php
header('Access-Control-Allow-Headers: X-Requested-With, Authorization,Content-Type');
header('Access-Control-Allow-Methods: POST');
header('Content-Type: application/json');

require_once 'app.php';

$req = json_decode(file_get_contents('php://input'));

$path = $req->path;
$data = isset($req->data) ? $req->data : '';
$language = isset($req->language) ? strtolower($req->language) : 'en';

// Map language codes to SPARQL language tags
$lang_tag = array(
    'de' => 'de',
    'fr' => 'fr', 
    'it' => 'it',
    'en' => 'en'
);
$lang = isset($lang_tag[$language]) ? $lang_tag[$language] : 'en';

$q1 = 'PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX qcsm: <https://quantifarm.eu/ontology/>
SELECT DISTINCT ?year ?product ?name ?unit ?absDiff ?percDiff ?title ?subtitle ?higherIsBetter ?impactLevel
WHERE {
    GRAPH <https://quantifarm.eu/graphs/testcase{{NN}}> {
    ?uri rdf:type qcsm:Testcase .
    ?uri qcsm:hasYearlyAssessmentInformation ?info .
    ?info qcsm:hasCultivationYear ?year .
    ?info qcsm:hasParcelComparison ?comparison .
    ?comparison qcsm:hasParcelAssessmentWithDATS ?assessment .
    ?assessment qcsm:hasParcelInformation ?parcel .
    ?parcel qcsm:hasProductType ?productEn .
    ?comparison qcsm:hasMainImpactInformation ?indicatorInfo .
    ?indicatorInfo qcsm:hasMainImpactName ?name .
    ?indicatorInfo qcsm:hasMainImpactUnit ?unit .
    ?indicatorInfo qcsm:hasAbsoluteDifference ?absDiff .
    ?indicatorInfo qcsm:hasPercentageDifference ?percDiff .
    ?indicatorInfo qcsm:hasMainImpactTitle ?titleEn .
    ?indicatorInfo qcsm:hasMainImpactSubtitle ?subtitleEn .
    ?indicatorInfo qcsm:hasHigherIsBetterMeaning ?higherIsBetter .
    ?indicatorInfo qcsm:hasImpactLevel ?impactLevel .
    }
    OPTIONAL {
        GRAPH <https://quantifarm.eu/graphs/testcase-translations> {
            ?parcel qcsm:hasProductType ?productTr .
        }
        FILTER(lang(?productTr) = "{{LANG}}")
    }
    BIND(COALESCE(?productTr, ?productEn) as ?product)
    OPTIONAL {
        GRAPH <https://quantifarm.eu/graphs/testcase-translations> {
            ?indicatorInfo qcsm:hasMainImpactTitle ?titleTr .
        }
        FILTER(lang(?titleTr) = "{{LANG}}")
    }
    OPTIONAL {
        GRAPH <https://quantifarm.eu/graphs/testcase-translations> {
            ?indicatorInfo qcsm:hasMainImpactSubtitle ?subtitleTr .
        }
        FILTER(lang(?subtitleTr) = "{{LANG}}")
    }
    BIND(COALESCE(?titleTr, ?titleEn) as ?title)
    BIND(COALESCE(?subtitleTr, ?subtitleEn) as ?subtitle)
}';

$q2 = 'PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX qcsm: <https://quantifarm.eu/ontology/>
SELECT DISTINCT ?year ?product ?category ?name ?unit ?absDiff ?percDiff ?description ?higherIsBetter ?impactLevel
WHERE {
    GRAPH <https://quantifarm.eu/graphs/testcase{{NN}}> {
    ?uri rdf:type qcsm:Testcase .
    ?uri qcsm:hasYearlyAssessmentInformation ?info .
    ?info qcsm:hasCultivationYear ?year .
    ?info qcsm:hasParcelComparison ?comparison .
    ?comparison qcsm:hasParcelAssessmentWithDATS ?assessment .
    ?assessment qcsm:hasParcelInformation ?parcel .
    ?parcel qcsm:hasProductType ?productEn .
    ?comparison qcsm:hasCostRevenueImpactInformation ?indicatorInfo .
    ?indicatorInfo qcsm:hasCostRevenueImpactCategory ?categoryEn .
    ?indicatorInfo qcsm:hasCostRevenueImpactName ?nameEn .
    ?indicatorInfo qcsm:hasCostRevenueImpactUnit ?unit .
    ?indicatorInfo qcsm:hasAbsoluteDifference ?absDiff .
    ?indicatorInfo qcsm:hasPercentageDifference ?percDiff .
    ?indicatorInfo qcsm:hasCostRevenueImpactShortDescription ?descriptionEn .
    ?indicatorInfo qcsm:hasHigherIsBetterMeaning ?higherIsBetter .
    ?indicatorInfo qcsm:hasImpactLevel ?impactLevel .
    }
    OPTIONAL {
        GRAPH <https://quantifarm.eu/graphs/testcase-translations> {
            ?parcel qcsm:hasProductType ?productTr .
        }
        FILTER(lang(?productTr) = "{{LANG}}")
    }
    BIND(COALESCE(?productTr, ?productEn) as ?product)
    OPTIONAL {
        GRAPH <https://quantifarm.eu/graphs/testcase-translations> {
            ?indicatorInfo qcsm:hasCostRevenueImpactCategory ?categoryTr .
        }
        FILTER(lang(?categoryTr) = "{{LANG}}")
    }
    OPTIONAL {
        GRAPH <https://quantifarm.eu/graphs/testcase-translations> {
            ?indicatorInfo qcsm:hasCostRevenueImpactName ?nameTr .
        }
        FILTER(lang(?nameTr) = "{{LANG}}")
    }
    OPTIONAL {
        GRAPH <https://quantifarm.eu/graphs/testcase-translations> {
            ?indicatorInfo qcsm:hasCostRevenueImpactShortDescription ?descriptionTr .
        }
        FILTER(lang(?descriptionTr) = "{{LANG}}")
    }
    BIND(COALESCE(?categoryTr, ?categoryEn) as ?category)
    BIND(COALESCE(?nameTr, ?nameEn) as ?name)
    BIND(COALESCE(?descriptionTr, ?descriptionEn) as ?description)
}';

$q3 = 'PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX qcsm: <https://quantifarm.eu/ontology/>
SELECT DISTINCT ?year ?product ?name ?unit ?percDiff ?maxRangePercDiff
WHERE {
    GRAPH <https://quantifarm.eu/graphs/testcase{{NN}}> {
    ?uri rdf:type qcsm:Testcase .
    ?uri qcsm:hasYearlyAssessmentInformation ?info .
    ?info qcsm:hasCultivationYear ?year .
    ?info qcsm:hasParcelComparison ?comparison .
    ?comparison qcsm:hasParcelAssessmentWithDATS ?assessment .
    ?assessment qcsm:hasParcelInformation ?parcel .
    ?parcel qcsm:hasProductType ?productEn .
    ?comparison qcsm:hasAggregatedImpactInformation ?indicatorInfo .
    ?indicatorInfo qcsm:hasAggregatedImpactName ?nameEn .
    ?indicatorInfo qcsm:hasAggregatedImpactUnit ?unit .
    ?indicatorInfo qcsm:hasAggregatedImpactValue ?percDiff .
    ?indicatorInfo qcsm:hasAggregatedImpactMaxRangeValue ?maxRangePercDiff .
    }
    OPTIONAL {
        GRAPH <https://quantifarm.eu/graphs/testcase-translations> {
            ?parcel qcsm:hasProductType ?productTr .
        }
        FILTER(lang(?productTr) = "{{LANG}}")
    }
    BIND(COALESCE(?productTr, ?productEn) as ?product)
    OPTIONAL {
        GRAPH <https://quantifarm.eu/graphs/testcase-translations> {
            ?indicatorInfo qcsm:hasAggregatedImpactName ?nameTr .
        }
        FILTER(lang(?nameTr) = "{{LANG}}")
    }
    BIND(COALESCE(?nameTr, ?nameEn) as ?name)
}';

//not used
$q4 = 'PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX qcsm: <https://quantifarm.eu/ontology/>
SELECT *
FROM <https://quantifarm.eu/graphs/dats>
WHERE {
  ?dats qcsm:hasSource "costbenefit" .
}';

function parseSparqlResults($response, $queryName) {
    $decoded = json_decode($response);
    if (!$decoded || !isset($decoded->results->bindings)) {
        http_response_code(502);
        die(json_encode(['error' => 'SPARQL query failed (' . $queryName . ')', 'detail' => substr($response, 0, 200)]));
    }
    return $decoded->results->bindings;
}

switch ($path) {
    case '/tcdata':
        // The testcase number is substituted into a graph IRI — allow digits only (prevents SPARQL injection)
        if (!preg_match('/^\d{1,6}$/', (string)$data)) {
            http_response_code(400);
            die(json_encode(['error' => 'invalid testcase number']));
        }
        $data = (string)(int)$data;

        $obj = new stdClass();
        
        $q = str_replace(['{{NN}}', '{{LANG}}'], [$data, $lang], $q1);
        $r = CallSPARQL($q);
        $obj->q1 = parseSparqlResults($r, 'q1');

        $q = str_replace(['{{NN}}', '{{LANG}}'], [$data, $lang], $q2);
        $r = CallSPARQL($q);
        $obj->q2 = parseSparqlResults($r, 'q2');

        $q = str_replace(['{{NN}}', '{{LANG}}'], [$data, $lang], $q3);
        $r = CallSPARQL($q);
        $obj->q3 = parseSparqlResults($r, 'q3');

        $res = json_encode($obj);

        break;
    case '/costbenefitdats':

        $r = CallSPARQL($q4);
        $res = json_encode(parseSparqlResults($r, 'costbenefitdats'));

        break;
    default: 

        http_response_code(400);
	    $res = json_encode(['error' => 'unknown path']);
}

echo $res;

