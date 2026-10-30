<?php
header('Access-Control-Allow-Headers: X-Requested-With, Authorization,Content-Type');
header('Access-Control-Allow-Methods: POST');
header('Content-Type: application/json');

require_once 'app.php';

$baseURL = $tool1URL;

$req = json_decode(file_get_contents('php://input'));

$path = $req->path;
$data = $req->data;
if (property_exists($req,'method')) $method = $req->method;

switch ($path) {
    case '/dats/main':

        $url = $baseURL . '/dats/main' . '?' . http_build_query($data);
        $res = CallAPI('GET', $url, null);

        break;
    case '/filters':
      
        $url = $baseURL . '/filters';
        $res = CallAPI('GET', $url, null);

        break;
    case '/profile_entries/':
      
        $url = $baseURL . $path;
        $res = CallAPI('GET', $url, null);

        break;
    case '/dats/recommend':
        
        $url = $baseURL . '/dats/recommend';
        $res = CallAPI('POST', $url, $data);

        break;
    default: 

        http_response_code(400);
	    $res = 'unknown path: ' . $path;
}

echo $res;
