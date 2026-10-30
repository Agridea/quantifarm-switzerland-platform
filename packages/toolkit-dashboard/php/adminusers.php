<?php
header('Access-Control-Allow-Headers: X-Requested-With, Authorization, Content-Type');
header('Access-Control-Allow-Methods: GET, POST');
header('Content-Type: application/json');

require_once 'app.php';

session_start();
CheckSuperAdmin();

require_once 'db.php';

$req = json_decode(file_get_contents('php://input'));
$action = isset($_GET['a']) ? $_GET['a'] : (isset($req->action) ? $req->action : '');

switch ($action) {
    case 'list':
        $rows = $db->execute_query('SELECT id, name, email, createdon, isvalidated, isadmin FROM users WHERE isdel = 0 ORDER BY name');
        $out = array();
        while ($row = $rows->fetch_assoc()) {
            $row['issuperadmin'] = IsSuperAdminEmail($row['email']);
            $out[] = $row;
        }
        $res = $out;
        break;

    case 'setadmin':
        $targetEmail = strtolower(trim($req->email));
        $newIsAdmin = $req->isadmin ? 1 : 0;

        // Super-admin itself is always treated as admin via CheckAdmin(); prevent accidental lockout noise
        $stmt = $db->prepare("UPDATE users SET isadmin = ? WHERE email = ? and isdel = 0");
        $stmt->bind_param("is", $newIsAdmin, $targetEmail);
        $stmt->execute();
        $changed = $stmt->affected_rows;
        $stmt->close();

        if ($changed === 0) {
            http_response_code(404);
            $res = array('error' => 'user not found: ' . $targetEmail);
            break;
        }

        $stmt = $db->prepare("INSERT INTO admin_role_log (actor_email, target_email, new_isadmin, createdon) VALUES (?, ?, ?, ?)");
        $actor = $_SESSION['useremail'];
        $now = date('Y-m-d H:i:s');
        $stmt->bind_param("ssis", $actor, $targetEmail, $newIsAdmin, $now);
        $stmt->execute();
        $stmt->close();

        $res = array('ok' => true);
        break;

    case 'delete':
        $targetEmail = strtolower(trim($req->email));

        if (IsSuperAdminEmail($targetEmail)) {
            http_response_code(400);
            $res = array('error' => 'the super-admin cannot be deleted');
            break;
        }

        // Remove the user's data in the cost-benefit calculators (V1 and V2) first
        $failed = false;
        foreach (array($tool2URL1, $tool2URL2) as $toolURL) {
            foreach (array('crop', 'livestock') as $type) {
                CallAPI('DELETE', $toolURL . '/user_data/' . $type . '?' . http_build_query(array('user_id' => $targetEmail)), null);
                if (http_response_code() >= 400) $failed = true;
            }
        }

        if ($failed) {
            http_response_code(502);
            $res = array('error' => 'could not delete user data in the cost-benefit calculators');
            break;
        }
        http_response_code(200);

        $stmt = $db->prepare("UPDATE users SET isdel = 1 WHERE email = ? and isdel = 0");
        $stmt->bind_param("s", $targetEmail);
        $stmt->execute();
        $changed = $stmt->affected_rows;
        $stmt->close();

        if ($changed === 0) {
            http_response_code(404);
            $res = array('error' => 'user not found: ' . $targetEmail);
            break;
        }

        $res = array('ok' => true);
        break;

    case 'log':
        $rows = $db->execute_query('SELECT actor_email, target_email, new_isadmin, createdon FROM admin_role_log ORDER BY id DESC LIMIT 200');
        $out = array();
        while ($row = $rows->fetch_assoc()) {
            $out[] = $row;
        }
        $res = $out;
        break;

    default:
        http_response_code(400);
        $res = array('error' => 'unknown action: ' . $action);
}

mysqli_close($db);
echo json_encode($res);
