let tc_num = 0;
let tc_type = "";
let tc_comp = 0;
let tc_year = 0;
let tc_with = 0;

const refObj = { _main: null, _year: null, _parcel: null };

let fileHandle;

window.addEventListener('beforeunload', (event) => {
    event.preventDefault();
    event.returnValue = '';
});


async function OpenFile() {
    const pickerOpts = {
        types: [
            {
                description: "Test Case JSON files",
                accept: {
                    "application/json": [".json"],
                },
            },
        ],
        excludeAcceptAllOption: true,
    };

    [fileHandle] = await window.showOpenFilePicker(pickerOpts);
    const file = await fileHandle.getFile();
    const contents = await file.text();

    //console.log(contents);
    try {
        const obj = JSON.parse(contents);
        LoadTC(obj);
        ShowToast("Info", "TC data is loaded.");
    } catch (error) {
        ShowError(error);
        console.log(error);
    }
}

async function GetNewFileHandle() {
    const options = {
        types: [
            {
                description: "Test Case JSON files",
                accept: {
                    "application/json": [".json"],
                },
            },
        ],
    };
    const handle = await window.showSaveFilePicker(options);
    return handle;
}

async function WriteFile(fileHandle, contents) {
    const writable = await fileHandle.createWritable();
    await writable.write(contents);
    await writable.close();
}

function NewTC() {
    if (!getUIValue("cboTC")) return;

    const n = getUIValue("cboTC");

    const o = testCaseData[FindIndexByProp(testCaseData, "id", n)];
    const obj = CloneObject(defObj); 
    obj.testcaseNumber = o.id;
    obj.testcaseLeader = o.partner;
    obj.cultivationType = o.cultivation_type;

    LoadTC(obj);
    fileHandle = null;
}

function LoadTC(obj) {

    refObj._main = obj;
    tc_num = refObj._main.testcaseNumber;
    tc_type = refObj._main.cultivationType;

    document.getElementById("butGeneral").hidden = false;
    document.getElementById("but2023").hidden = false;
    document.getElementById("but2024").hidden = false;
    document.getElementById("but2025").hidden = false;
    //document.getElementById("formMain").classList.remove("was-validated");

    ClearUI();
    SetControlsVisibility();
    ChangeYear(2023, true);
    (new bootstrap.Tab(document.getElementById('butGeneral'))).show();  //set tab

}

async function SaveTC() {

    SetObjFromUI();
    RemoveEmptyParcels();

    //console.log(refObj._main);
    //return;

    const obj = JSON.stringify(refObj._main, null, 3);

    if (!fileHandle)
        fileHandle = await GetNewFileHandle();

    await WriteFile(fileHandle, obj);

    ShowToast("Info", "File is saved.");

    LoadTC(refObj._main);
}

function SetObjFromUI() {
    let n, q;

    Object.keys(refObj._parcel).forEach(key => delete refObj._parcel[key]);

    if (IsParcelEmpty())
        q = "[tc_field]:not([tc_field^='_parcel'])";
    else
        q = "[tc_field]";

    document.querySelectorAll(q).forEach((el) => {
        n = el.nodeName.toLowerCase();

        //all fields, not only visible
        if (n === "input")              // && !el.parentElement.parentElement.hidden
            SetObjPropFromUI(el);
        else if (n === "table")         // && !el.hidden
            SetObjArrPropFromUI(el);
    });
}

function SetUIFromObj() {
    let n;
    ClearUI();

    document.querySelectorAll("[tc_field]").forEach((el) => {
        n = el.nodeName.toLowerCase();

        //all fields, not only visible
        if (n === "input")              // && !el.parentElement.parentElement.hidden
            SetCtrlFromObj(el);
        else if (n === "table")         // && !el.hidden
            SetTableFromObj(el);

    });
} 

function IsParcelEmpty() {
    let f = true;
    let n;

    document.querySelectorAll("[tc_field^='_parcel']").forEach((el) => {
        n = el.nodeName.toLowerCase();

        //only visible
        if (n === "input" && !el.parentElement.parentElement.hidden)             
            f = f && !ifEmpty(getUIValue(el));
        else if (n === "table" && !el.hidden)         
            ; //todo?
    });

    return f;
}

function ClearUI() {
    let n;
    document.getElementById("formMain").classList.remove("was-validated");

    document.querySelectorAll("[tc_field]").forEach((el) => {
        n = el.nodeName.toLowerCase();

        //clear all - visible and invisible
        if (n === "input")
            setUIValue(el, null);
        else if (n === "table")
            ClearTable(el);
    });
} 

function ClearTable(t, n = 1) { //clear table and add n empty rows
    const tb = t.firstElementChild.nextElementSibling.nextElementSibling;
    tb.firstElementChild.querySelectorAll("[tc_field2]").forEach((item) => { setUIValue(item, null); });  //clear fields
    const r = tb.firstElementChild.innerHTML;
    tb.innerHTML = ""; //clear table

    for (let i = 0; i < n; i++) {//add n empty rows
        const tr = document.createElement("tr");
        tr.innerHTML = r;
        tb.appendChild(tr);
    }
}

function SetObjPropFromUI(el) {
    const v = getUIValue(el);

    const obj = GetTargetObjRef(el, true);

    obj[GetTargetField(el)] = ifEmpty(v);
}

function SetObjArrPropFromUI(el) {
    let f, f2, els, v, isEmpty;
    const tb = el.firstElementChild.nextElementSibling.nextElementSibling;

    const obj = GetTargetObjRef(el, true);
    f = GetTargetField(el);
    if (!obj[f]) obj[f] = [];
    const arr = obj[f];

    let i = 0;
    for (let tr of tb.children) {
        els = tr.querySelectorAll("[tc_field2]");
        if (els.length > 1) arr[i] = {};

        isEmpty = true;
        els.forEach((item) => {
            f2 = item.getAttribute("tc_field2");
            v = ifEmpty(getUIValue(item));
            if (f2)
                arr[i][f2] = v;
            else
                arr[i] = v;

            isEmpty = isEmpty && !v;
        });

        //remove empty row
        if (isEmpty)
            arr.pop();
        else
            i++;
    }

}

function GetTargetObjRef(el, createIfNull) {
    const arr = el.getAttribute("tc_field").split('.');
    let obj = refObj[arr[0]];

    if (arr.length === 3) {
        if (!obj[arr[1]] && createIfNull)
            obj[arr[1]] = {};

        obj = obj[arr[1]];
    }

    return obj;
}

function GetTargetField(el) {
    const arr = el.getAttribute("tc_field").split('.');
    return arr[arr.length - 1];
}

function SetTableFromObj(el) {
    const tb = el.firstElementChild.nextElementSibling.nextElementSibling;
    let f, els, v;
    let n = 1;

    let obj = GetTargetObjRef(el, false);
    obj = obj[GetTargetField(el)];

    if (obj && obj.length > 1) n = obj.length;

    ClearTable(el, n);

    if (!obj) return;
    if (obj && obj.length === 0) return;

    for (let i = 0; i < tb.children.length; i++) {
        els = tb.children[i].querySelectorAll("[tc_field2]");

        els.forEach((item) => {
            f = item.getAttribute("tc_field2");
            if (f)
                v = obj[i][f];
            else {
                v = obj[i];

                if (item.nodeName.toLowerCase() === "select")  //Array.from(item.options).findIndex((item) => { return item.text === v; })
                    item.innerHTML = "<option></option><option>" + v + "</option>"
            }

            setUIValue(item, v);
        });
    }
}

function SetCtrlFromObj(el) {
    let v = null;
    const obj = GetTargetObjRef(el, false);

    if (obj) v = obj[GetTargetField(el)];
    setUIValue(el, v);
}

function SetControlsVisibility() {

    document.querySelectorAll("[tc_field]").forEach((el) => {
        const f = el.getAttribute("id");
        const n = el.nodeName.toLowerCase();
        const i = FindIndexByProp(fieldsData, "field", f);
        if (i < 0) return;

        const dis = fieldsData[i]["disable"].indexOf(tc_type) >= 0;

        if (n === "input")
            el.parentElement.parentElement.hidden = dis;
        else if (n === "table")
            el.hidden = dis;
        else if(n === "div")
            el.hidden = dis;
    });

}

function AddNewTableRow(e) {
    const tr = document.createElement("tr");
    tr.innerHTML = e.srcElement.parentElement.parentElement.parentElement.nextElementSibling.lastElementChild.innerHTML;
    e.srcElement.parentElement.parentElement.parentElement.nextElementSibling.appendChild(tr);
}

function AddNewPC(ul, b = true) {
    const el = document.getElementById(ul);
    const i = el.children.length;
    const n = "but" + ul + i;

    const li = document.createElement("li");
    el.insertBefore(li, el.lastElementChild);
    el.children[el.children.length - 2].outerHTML = '<li class="nav-item" role="presentation"><button class="nav-link" id="' + n + '" data-bs-toggle="tab" data-bs-target="#tabParcel" type="button" role="tab" aria-controls="tabParcel" aria-selected="false" tabindex="-1" onclick="ChangeComparison(' + i + ')"><b>Parcel Comparison ' + i + '</b></button></li>';

    if (b)
        ChangeComparison(i);

}

function ChangeYear(v, firstLoad = false) {

    if (!firstLoad) SetObjFromUI();
    SetRefObjects(v, 1, 1)
    SetUIFromObj();

    const el = document.getElementById("myTabPC");

    while (el.children.length > 1) {
        el.removeChild(el.firstElementChild);
    }

    while (el.children.length < refObj._year.parcelComparison.length + 1) {
        AddNewPC("myTabPC", false);
    }

    SetTabs();
}

function ChangeComparison(v) {

    SetObjFromUI();
    SetRefObjects(tc_year, v, 1);
    SetUIFromObj();

    SetTabs();
}

function ChangeWith(v) {

    SetObjFromUI();
    SetRefObjects(tc_year, tc_comp, v);
    SetUIFromObj();

    SetTabs();
}

function SetRefObjects(y, c, w) {
    tc_year = y;
    tc_comp = c;
    tc_with = w;

    refObj._year = refObj._main.yearlyAssessmentInformation[FindIndexByProp(refObj._main.yearlyAssessmentInformation, "cultivationYear", tc_year)];

    if (refObj._year.parcelComparison.length < tc_comp)
        refObj._year.parcelComparison.push(CloneObject(emptyPC));

    if (tc_with === 1)
        refObj._parcel = refObj._year.parcelComparison[tc_comp - 1].parcelAssessmentWithDATS;
    else
        refObj._parcel = refObj._year.parcelComparison[tc_comp - 1].parcelAssessmentWithoutDATS;

}

function SetTabs() {

    (new bootstrap.Tab(document.getElementById("butmyTabPC" + tc_comp))).show();  //set tab

    if (tc_with === 1)
        (new bootstrap.Tab(document.getElementById('butWith'))).show();
    else
        (new bootstrap.Tab(document.getElementById('butWithout'))).show();

    document.getElementById("datsUsed").hidden = tc_with === 0;
    SetAlert();
}

function SetAlert() {
    const s = "You enter data for TC " + tc_num + ", Testing period " + tc_year + ", Parcel Comparison " + tc_comp + ", Parcel " + (tc_with ? "with" : "without") + " DATS";
    document.getElementById("alert1").innerHTML = s;
}

function FillDatsUsed(e) {
    e.srcElement.innerHTML = "<option></option>";

    let els, v;
    const tb = document.getElementById("datsInformation").firstElementChild.nextElementSibling.nextElementSibling;

    for (let tr of tb.children) {
        els = tr.querySelectorAll("[tc_field2]");

        els.forEach((item) => {
            if (item.getAttribute("tc_field2") == "datsName") {
                v = ifEmpty(getUIValue(item));
                if (v)
                    e.srcElement.innerHTML += "<option>" + v + "</option>";
            }
        });
    }
}

function RemoveEmptyParcels() {

    for (let o of refObj._main.yearlyAssessmentInformation) {
        o.parcelComparison = o.parcelComparison.filter((pc) =>
            !IsObjectEmpty(pc.parcelAssessmentWithDATS) || !IsObjectEmpty(pc.parcelAssessmentWithoutDATS));
    }

}

function ValidateParcel() {

    console.log("ValidateParcel");
}

function ShowToast(type, msg) {
    const err = "text-danger";
    const info = "text-info";

    const t = document.getElementById("toast1");
    const h = t.querySelector(".me-auto");
    const b = t.querySelector(".toast-body");
    const c = type === "Error" ? err : info;

    h.innerHTML = type;
    b.innerHTML = msg;
    h.classList.remove(err);
    b.classList.remove(err);
    h.classList.remove(info);
    b.classList.remove(info);
    h.classList.add(c);
    b.classList.add(c);

    (new bootstrap.Toast(t)).show();
}

function ShowError(err) {
    const msg = `[${err.name}] ${err.message}`;
    ShowToast("Error", msg);
}

