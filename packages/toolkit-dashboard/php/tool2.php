<?php
header('Access-Control-Allow-Headers: X-Requested-With, Authorization,Content-Type');
header('Access-Control-Allow-Methods: POST');
header('Content-Type: application/json');

require_once 'app.php';

session_start();
CheckLogin();

$req = json_decode(file_get_contents('php://input'));

$path = $req->path;
$data = $req->data;
$version = $req->version;

// Use container names on quantifarm-network
$baseURL = $tool2URL1;
if($version == 2) $baseURL = $tool2URL2;

switch ($path) {
    case '/dat':
        
        $url = $baseURL . $path;
        $res = CallAPI('GET', $url, null);

        break;
    case '/dat_tree':
        
        $url = $baseURL . $path . '?' . http_build_query($data);
        $res = CallAPI('GET', $url, null);

        break;
    case '/user_data_get':
        
        $data->user_id = $_SESSION['useremail'];
        $url = $baseURL . '/user_data/' . $req->type . '?' . http_build_query($data);
        $res = CallAPI('GET', $url, null);

        break; 
    case '/user_data_post':
        
        $data[0]->user_id = $_SESSION['useremail'];
        $url = $baseURL . '/user_data/' . $req->type;
        $res = CallAPI('POST', $url, $data);

        break;
    case '/totals/':
        
        $data->user_id = $_SESSION['useremail'];
        $url = $baseURL . $path . '?' . http_build_query($data);

        $res = CallAPI('GET', $url, null);

        break;
    case '/dats/all': 
        // call Recommendations tool API
        $url = 'http://' . $host . ':8000/dats/all';
        $res = CallAPI('GET', $url, null);

        break;
    default: 

        http_response_code(400);
	    $res = 'unknown path: ' . $path;
}

echo $res;

