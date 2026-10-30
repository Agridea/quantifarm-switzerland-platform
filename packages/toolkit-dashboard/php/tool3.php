<?php
header('Access-Control-Allow-Headers: X-Requested-With, Authorization,Content-Type');
header('Access-Control-Allow-Methods: POST');
header('Content-Type: application/json');

require_once 'app.php';

session_start();
CheckLogin();

// Use container name on quantifarm-network
$baseURL = $tool3URL;


$req = json_decode(file_get_contents('php://input'));

$maxN = 1000;
$path = $req->path;
$data = $req->data;
if (property_exists($req,'method')) $method = $req->method;

switch ($path) {
    case '/event/id/':
    case '/measurement/id/':
        
        $url = $baseURL . $path . urlencode($data->id);
        $res = CallAPI('GET', $url, null);

        break;
    case '/parcel/ids/':
        
        $url = $baseURL . $path . urlencode($data->id);
        $res = CallAPI('GET', $url, null);

        break;
    case '/parcel/user/':
              
        $data->id = $_SESSION['useremail'];
        $url = $baseURL . $path . urlencode($data->id) .  '?' . 'limit=' . $maxN;
        $res = CallAPI('GET', $url, null);

        break;
    case '/event':
    case '/measurement':
        
        if($method == "GET" || $method == "DELETE") {
            $url = $baseURL . $path . '?' . http_build_query($data);
            $res = CallAPI($method, $url, null);
        }
        else if($method == "POST") {
            $url = $baseURL . $path . '?id=' . $data->id;
            $res = CallAPI($method, $url, $data);
        }
        else if($method == "PUT") {
            $url = $baseURL . $path;
            $res = CallAPI($method, $url, $data);
        }

        break;
    case '/parcel':

        $data->user = $_SESSION['useremail'];
        $url = $baseURL . $path . '?' . http_build_query($data);
        $res = CallAPI($method, $url, null);

        break;
    case '/parcel/dat':

        $data->limit = $maxN;
        $url = $baseURL . $path . '?' . http_build_query($data);
        $res = CallAPI('GET', $url, null);

        break;
    case 'aggr':
        $pid = $data->parcelid;
        $q = json_decode(json_encode($data), true);
        unset($q["parcelid"]);

        $url = $baseURL . '/parcels/' . urlencode($pid) . '/aggregations/' . '?' . http_build_query($q);
        $res = CallAPI("GET", $url, null);

        break;
    case 'meteo':
        $pid = $data->parcelid;
        $q = json_decode(json_encode($data), true);
        unset($q["parcelid"]);

        $url = $baseURL . '/parcels/' . urlencode($pid) . '/meteoaggregations/' . '?' . http_build_query($q);
        $res = CallAPI("GET", $url, null);

        break;
    case 'chill':
        $pid = $data->parcelid;
        $q = json_decode(json_encode($data), true);
        unset($q["parcelid"]);

        $url = $baseURL . '/parcels/' . urlencode($pid) . '/chilling-days/' . '?' . http_build_query($q);
        $res = CallAPI("GET", $url, null);

        break;
    case '/parametrics/types/':
        
        $url = $baseURL . $path . urlencode($data->type);
        $res = CallAPI('GET', $url, null);

        break;
    case '/dats/all': 
        // call Recommendations tool API
        $url = $tool1URL . '/dats/all';
        $res = CallAPI('GET', $url, null);

        break;
    default: 

        http_response_code(400);
	    $res = 'unknown path: ' . $path;
}

echo $res;

