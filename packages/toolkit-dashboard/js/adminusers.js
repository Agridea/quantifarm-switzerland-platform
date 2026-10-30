const adminApiURL = baseURL + "adminusers.php";

document.addEventListener("DOMContentLoaded", setSidebar(null));
SetLoggedUser(InitAdminUsersPage);

function InitAdminUsersPage() {
    const user = JSON.parse(localStorage.getItem(key_usr));

    if (!user.loggedin || !user.issuperadmin) {
        document.getElementById('divNotSuperAdmin').hidden = false;
        document.getElementById('divSuperAdmin').hidden = true;
        return;
    }

    document.getElementById('divNotSuperAdmin').hidden = true;
    document.getElementById('divSuperAdmin').hidden = false;
    LoadUsers();
}

function LoadUsers() {
    fetch(adminApiURL + "?a=list", { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: '{}' })
        .then(function (r) {
            return r.json().then(function (json) {
                if (!r.ok) throw new Error(json.error || ('HTTP ' + r.status));
                return json;
            });
        })
        .then(RenderUsers)
        .catch(function (e) { ShowErr(e); });
}

function RenderUsers(users) {
    const tbl = document.getElementById('tblUsers');
    tbl.textContent = '';

    users.forEach(function (u) {
        const tr = document.createElement('tr');

        function addTextCell(value) {
            const td = document.createElement('td');
            td.textContent = value == null ? '' : String(value);
            tr.appendChild(td);
            return td;
        }

        addTextCell(u.name);
        addTextCell(u.email);
        addTextCell(u.createdon);
        addTextCell(u.isvalidated == 1 ? 'yes' : 'no');

        const adminCell = addTextCell('');
        const adminCheckbox = document.createElement('input');
        adminCheckbox.type = 'checkbox';
        adminCheckbox.className = 'form-check-input';
        adminCheckbox.checked = u.isadmin == 1;
        adminCheckbox.addEventListener('change', function () {
            ToggleAdmin(u.email, adminCheckbox.checked);
        });
        adminCell.appendChild(adminCheckbox);

        const deleteCell = addTextCell('');
        if (!u.issuperadmin) {
            const deleteButton = document.createElement('button');
            deleteButton.type = 'button';
            deleteButton.className = 'btn btn-sm btn-outline-danger';
            deleteButton.addEventListener('click', function () {
                DeleteUser(u.email);
            });

            const deleteIcon = document.createElement('i');
            deleteIcon.className = 'bi bi-trash';
            deleteButton.appendChild(deleteIcon);
            deleteCell.appendChild(deleteButton);
        }

        tbl.appendChild(tr);
    });
}

function ToggleAdmin(email, isAdmin) {
    fetch(adminApiURL + "?a=setadmin", {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ action: 'setadmin', email: email, isadmin: isAdmin })
    })
        .then(function (r) {
            return r.json().then(function (json) {
                if (!r.ok) throw new Error(json.error || ('HTTP ' + r.status));
                return json;
            });
        })
        .then(function () { ShowOk('Updated ' + email + '.'); })
        .catch(function (e) { ShowErr(e); LoadUsers(); });
}

function DeleteUser(email) {
    if (!confirm('Delete user ' + email + '?')) return;

    fetch(adminApiURL + "?a=delete", {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ action: 'delete', email: email })
    })
        .then(function (r) {
            return r.json().then(function (json) {
                if (!r.ok) throw new Error(json.error || ('HTTP ' + r.status));
                return json;
            });
        })
        .then(function () { ShowOk('Deleted ' + email + '.'); LoadUsers(); })
        .catch(function (e) { ShowErr(e); });
}

function ShowErr(e) {
    const d = document.getElementById('divErr');
    d.innerText = e.message || e;
    d.hidden = false;
    document.getElementById('divOk').hidden = true;
}

function ShowOk(msg) {
    const d = document.getElementById('divOk');
    d.innerText = msg;
    d.hidden = false;
    document.getElementById('divErr').hidden = true;
}
