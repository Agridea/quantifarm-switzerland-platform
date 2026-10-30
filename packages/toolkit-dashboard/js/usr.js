
document.addEventListener("DOMContentLoaded", () => {
    document
        .querySelectorAll('[qf-multiselect]')
        .forEach((item) => item.addEventListener('change', handleMultiSelectDropdownCB));

    LoadProfile();
});


function Register() {
    CallAPI2("reg");
}

function Login() {
    CallAPI2("log");
}

function Profile() {
    CallAPI2("upd");
}

function Delete() {
    if (!confirm("Click OK to delete account")) return false;

    CallAPI2("del");
}

function Forgotten() {
    CallAPI2("fgt", "An email with new password has been sent. Check your spam folder as well.");
}

function CallAPI2(cmd, msg) {
    const form = document.forms["formMain"];

    if (!form.reportValidity()) return;

    const url = "php/api.php?c=" + cmd;
    const params = GetQueryParams();
    const redirectUrl = params.has("url") ? params.get("url") : "index.html";

    setButtonState("btnSubmit", true);

    fetch(url, { method: 'POST', body: new FormData(form) })
        .then(function (response) {
            if (response.ok)
                return response.text();
            else
                return response.text();
        })
        .then(function (res) {
            if (res == "ok")
                if (msg)
                    showInfo("divErr", msg);
                else
                    location.href = redirectUrl;
            else
                throw new Error(res);
        })
        .catch(function (error) {
            showErr("divErr", error);
        })
        .finally(function () {
            setButtonState("btnSubmit", false);
        });
}

function LoadProfile() {
    const user = JSON.parse(localStorage.getItem(key_usr));

    if (user && user.loggedin) {
        setUIValue("yourName", user.user);
        setUIValue("yourEmail", user.email);
        setUIValue("yourRoles", user.roles);
        setUIValue("yourAge", user.age);
        setUIValue("yourGender", user.gender);
        setUIValue("yourCountry", user.country);
    }   
}
