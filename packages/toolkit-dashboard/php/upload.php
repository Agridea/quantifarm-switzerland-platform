<?php
header('Access-Control-Allow-Methods: POST');

require_once 'app.php';

session_start();
CheckLogin();

if($_FILES["inputFile"]["error"] == 2 ){
	http_response_code(400);
	die ("File too big (err=2)");
}

if($_FILES["inputFile"]["size"] > 5242880){
	http_response_code(400);
	die ("File too big (>5MB)");
}


$f = $_FILES["inputFile"]["tmp_name"];
$q = new stdClass();
// Use container name on quantifarm-network
$baseURL = $tool3URL;

switch ($_POST["objType"]) {
    case 'parcel':
		
		$q->username = $_SESSION['useremail'];
		$url = $baseURL . '/import/parcel?' . http_build_query($q);
		$res = UploadFile($url, $f, 'filedata');
        break;
    case 'event':

		$q->parcelid = $_POST["importParcel"];
		$url = $baseURL . '/import/event?' . http_build_query($q);
		$res = UploadFile($url, $f, 'filedata');
        break;
    case 'meteo':

		$q->parcelid = $_POST["importParcel"];
		$url = $baseURL . '/import/meteo?' . http_build_query($q);
		$res = UploadFile($url, $f, 'filedata');
        break;
    default: 

        http_response_code(400);
	    $res = 'unknown obj';
}

echo $res;

