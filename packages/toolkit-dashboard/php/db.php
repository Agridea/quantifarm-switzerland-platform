<?php

// Connect to the database. All settings must come from environment variables.
if (!function_exists('requireEnv')) {
  function requireEnv(string $name): string {
    $value = getenv($name);
    if ($value === false || $value === '') {
      error_log("Missing required environment variable: $name");
      http_response_code(500);
      die('Server configuration error');
    }
    return $value;
  }
}

$db_host = requireEnv('DB_HOST');
$db_user = requireEnv('DB_USER');
$db_password = requireEnv('DB_PASSWORD');
$db_name = requireEnv('DB_NAME');
$db_port = (int) (getenv('DB_PORT') ?: 3306);

$db = new mysqli($db_host, $db_user, $db_password, $db_name, $db_port);

if ($db->connect_errno) {
  error_log('db err: ' . $db->connect_error);
  http_response_code(500);
  die('db err');
}


