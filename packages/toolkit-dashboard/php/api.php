<?php
header('Access-Control-Allow-Headers: X-Requested-With, Authorization, Content-Type');
header('Access-Control-Allow-Methods: GET, POST');
header('Content-Type: application/json');

require_once 'app.php';

session_start();

$cmd = $_GET['c'];

switch ($cmd) {
    //*****************************
    case 'usr':
        $usr = new stdClass();
        $usr->loggedin = false;

        if (isset($_SESSION['loggedin'])) {
            $usr->user = $_SESSION['username'];
            $usr->email = $_SESSION['useremail'];
            $usr->roles = $_SESSION['userroles'];
            $usr->age = $_SESSION['userage'];
            $usr->gender = $_SESSION['usergender'];
            $usr->country = $_SESSION['usercountry'];
            $usr->isadmin = !empty($_SESSION['isadmin']);
            $usr->issuperadmin = IsSuperAdminEmail($_SESSION['useremail']);
            $usr->loggedin = true;
        }
        
        $res = json_encode($usr);

        break;
    //*****************************
    case 'out':
        session_destroy();
        header('Location: ../index.html');
        exit;

        break;
    //*****************************
    case 'reg':
        
        $name = trim($_POST['name']);
        $email = strtolower(trim($_POST['email']));
        $psw = $_POST['password'];
        $roles = $_POST['roles'];
        $age = $_POST['age'];
        $gender = $_POST['gender'];
        $country = $_POST['country'];

        if ($name == '' || $email == '' ||  $psw == '' ) {
	        exit('ivalid params!');
        }

        require_once 'db.php';

        $rows = $db->execute_query('SELECT id, psw FROM users WHERE email = ? and isdel=0', [$email]);

        if ($rows->num_rows > 0) {
            mysqli_close($db);
	        exit('email already exists!');
        }

        $psw = password_hash($psw, PASSWORD_DEFAULT);
        $t = date('Y-m-d H:i:s', time());
        // isadmin is never accepted from client input - it defaults to 0 and is only ever
        // changed by a super-admin via admin-users.html/adminusers.php
        $stmt = $db->prepare("INSERT INTO users (name, email, psw, createdon, roles, age, gender, country, isvalidated, isdel, isadmin) VALUES(?, ?, ?, ?, ?, ?, ?, ?, 0, 0, 0)");
        $stmt->bind_param("ssssssss", $name, $email, $psw, $t, $roles, $age, $gender, $country);
        $stmt->execute();
        $stmt->close();

        mysqli_close($db);

        UpdateSession($email, $name, $roles, $age, $gender, $country, 0);

        $res = 'ok';

        break;
    //*****************************
    case 'log':
        
        $email = strtolower(trim($_POST['email']));
        $psw = $_POST['password'];

        require_once 'db.php';

        $ok = false;
        $rows = $db->execute_query('SELECT * FROM users WHERE email = ? and isdel=0', [$email]);

        if ($row = $rows->fetch_assoc()) {
	        if (password_verify($psw, $row['psw'])) {
		        UpdateSession($email, $row['name'], $row['roles'], $row['age'], $row['gender'], $row['country'], $row['isadmin']);
		        $ok = true;
	        } 
        }

        mysqli_close($db);

        if (!$ok) {
	        exit('unknown email or password!');
        }

	    $res = 'ok';
        break;
    //*****************************
    case 'upd':

        if (!isset($_SESSION['loggedin'])) {
	        exit('ivalid params!');
        }

        if ($_SESSION['useremail'] != strtolower(trim($_POST['email']))) {
	        exit('ivalid params!');
        }

        $name = trim($_POST['name']);
        $psw1 = $_POST['password1'];
        $psw2 = $_POST['password2'];
        $email = $_SESSION['useremail'];
        $roles = $_POST['roles'];
        $age = $_POST['age'];
        $gender = $_POST['gender'];
        $country = $_POST['country'];

        require_once 'db.php';

        $stmt = $db->prepare("UPDATE users SET name=?, roles=?, age=?, gender=?, country=? WHERE email = ? and isdel=0");
        $stmt->bind_param("ssssss", $name, $roles, $age, $gender, $country, $email);
        $stmt->execute();
        $stmt->close();

        if ($psw1 != '' && $psw2 != '') {
            $rows = $db->execute_query('SELECT psw FROM users WHERE email = ? and isdel=0', [$email]);

            if ($row = $rows->fetch_assoc()) {
	            if (password_verify($psw1, $row['psw'])) {
                    $psw2 = password_hash($psw2, PASSWORD_DEFAULT);
                    $stmt = $db->prepare("UPDATE users SET psw = ? WHERE email = ? and isdel=0");
                    $stmt->bind_param("ss", $psw2, $email);
                    $stmt->execute();
                    $stmt->close();
	            } 
            }
        }

        mysqli_close($db);

        // isadmin is untouched here - keep whatever is already in the session
        UpdateSession($email, $name, $roles, $age, $gender, $country, !empty($_SESSION['isadmin']) ? 1 : 0);

        $res = 'ok';
        break;
    //*****************************
    case 'del':

        if (!isset($_SESSION['loggedin'])) {
	        exit('ivalid params!');
        }

        if ($_SESSION['useremail'] != strtolower(trim($_POST['email']))) {
	        exit('ivalid params!');
        }

        if ($_POST['password3'] == "") {
	        exit('ivalid params!');
        }

        $psw = $_POST['password3'];
        $email = $_SESSION['useremail'];

        require_once 'db.php';

        $ok = false;
        $rows = $db->execute_query('SELECT psw FROM users WHERE email = ? and isdel=0', [$email]);

        if ($row = $rows->fetch_assoc()) {
	        if (password_verify($psw, $row['psw'])) {
                $stmt = $db->prepare("UPDATE users SET isdel = 1 WHERE email = ? and isdel=0");
                $stmt->bind_param("s", $email);
                $stmt->execute();
                $stmt->close();
  		        $ok = true;
	        } 
        }

        mysqli_close($db);

        if (!$ok) {
	        exit('wrong password!');
        }

        //todo: delete user data in tools
        session_destroy();
        $res = 'ok';
        break;
    //*****************************
    case 'fgt':

        $email = $_POST['email'];

        require_once 'db.php';

        $rows = $db->execute_query('SELECT id FROM users WHERE email = ? and isdel=0', [$email]);

        if ($row = $rows->fetch_assoc()) {
            // Cryptographically secure random password (random_int instead of predictable str_shuffle)
            $chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789';
            $psw1 = '';
            for ($i = 0; $i < 12; $i++) {
                $psw1 .= $chars[random_int(0, strlen($chars) - 1)];
            }
            $psw2 = password_hash($psw1, PASSWORD_DEFAULT);
            $stmt = $db->prepare("UPDATE users SET psw = ? WHERE email = ? and isdel=0");
            $stmt->bind_param("ss", $psw2, $email);
            $stmt->execute();
            $stmt->close();

            SendMail($email, 'new password: ' . $psw1);
        }

        mysqli_close($db);

        // Uniform response regardless of account existence (prevents user enumeration)
        $res = 'ok';
        break;
    //*****************************
    default: 

        http_response_code(400);
	    $res = 'unknown cmd: ' . $cmd;
}

echo $res;


//functions
function UpdateSession($email, $name, $roles, $age, $gender, $country, $isadmin = 0){

	session_regenerate_id();
	$_SESSION['loggedin'] = true;
	$_SESSION['useremail'] = $email;
	$_SESSION['username'] = $name;
	$_SESSION['userroles'] = $roles;
	$_SESSION['userage'] = $age;
	$_SESSION['usergender'] = $gender;
	$_SESSION['usercountry'] = $country;
	$_SESSION['isadmin'] = (int)$isadmin === 1;

}

function SendMail($to, $txt) {
    $subject = "QuantiFarm CH Toolkit";
    $headers = "From: quantifarmtoolkit@quantifarmtoolkit.eu";

    $txt .= "\r\n----------------------\r\n";
    $txt .= "This is an automated email. Please, don't reply.";

    $x = mail($to, $subject, $txt, $headers);   // 1 - ok

}