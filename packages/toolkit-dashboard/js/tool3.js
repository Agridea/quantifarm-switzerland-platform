const tool_key = "tool3";
const apiURL = baseURL + "tool3.php";
let mapFlag = false;
//let refMapPolygon = null;

//data
let dataParcels;
let dataDATs = [];
let user;
let maxRows = 500;

document.addEventListener("DOMContentLoaded", setSidebar(tool_key));

document.addEventListener("DOMContentLoaded", () => {
    document
        .querySelectorAll('[qf-multiselect]')
        .forEach((item) => item.addEventListener('change', handleMultiSelectDropdownCB));
});

SetLoggedUser(SetUI);


function SetUI() {
    user = JSON.parse(localStorage.getItem(key_usr));

    if (!user.loggedin) {
        document.getElementById('lnkLogin').hidden = !true;
        document.getElementById('lockParcels').hidden = !true;
        document.getElementById('lockEvents').hidden = !true;
        document.getElementById('lockMeteo').hidden = !true;
        document.getElementById('lockResults').hidden = !true;
        document.getElementById('btnTabParcels').disabled = !false;
        document.getElementById('btnTabEvents').disabled = !false;
        document.getElementById('btnTabMeteo').disabled = !false;
        document.getElementById('btnTabResult').disabled = !false;
    } else
        LoadData();
}

function LoadData() {
    LoadEnumsData();
    LoadDATsAll();
    LoadParcelsAll();
}

function SetMap() {

    if (!mapFlag) {

        map = L.map('map', { editable: true }).setView([48, 15], 4);
        
        const osm = L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            maxZoom: 18,
            attribution: '&copy; <a href="https://openstreetmap.org" target="_blank">OpenStreetMap</a>',
            id: 'OSM'
        }).addTo(map);

        const gm = L.tileLayer('https://{s}.google.com/vt/lyrs=y&hl=en&x={x}&y={y}&z={z}', {
            maxZoom: 18,
            attribution: '&copy; <a href="https://www.google.com/maps" target=_blank>Google Maps</a>',
            subdomains: ["mt0", "mt1", "mt2", "mt3"],
            id: 'GM'
        }).addTo(map);

        L.control.layers({ "OpenStreetMap": osm, "Google maps": gm }).addTo(map);

        //map.on('editable:editing', function (event) {
        //    console.log("editing",event.layer._latlngs);
        //});

        mapFlag = true;
    }

    const coord = PostgisCoord(getUIValue("txtParcelPoly"));
    DeleteDrawing();

    if (coord != "") {

        let poly = L.polygon(coord, { color: 'red' });
        map.addLayer(poly);
        map.fitBounds(poly.getBounds().pad(0.1));

    }
    else {
        map.setView([48, 15], 4);

    }
}

function StartDrawing() {
    let poly;

    map.editTools.stopDrawing();
    map.eachLayer(function (layer) { if (layer instanceof L.Polygon) poly = layer; });

    if (poly)
        poly.enableEdit();
    else
        map.editTools.startPolygon("", { color: 'red' });
}

function FinishDrawing() {
    let poly;

    map.editTools.commitDrawing();
    map.eachLayer(function (layer) { if (layer instanceof L.Polygon) poly = layer; });

    if (poly) {
        setUIValue("txtParcelPoly", CoordPostgis(poly._latlngs[0]));
        poly.disableEdit();
    }
}

function DeleteDrawing() {
    map.editTools.stopDrawing();
    map.eachLayer(function (layer) { if (layer instanceof L.Polygon) map.removeLayer(layer); });
}

function SaveEvent() {
    //event.preventDefault();
    if (!document.forms["formEvent"].reportValidity()) return;

    const obj = {};
    obj.properties = {};

    obj.id = getUIValue("txtEventID");
    obj.parcelId = ifEmpty(getUIValue("cboEventParcel"));
    obj.dat = ifEmpty(getUIValue("cboEventDats"));
    obj.eventStart = ifEmpty(getUIValue("txtEventDate1"));
    obj.eventEnd = ifEmpty(getUIValue("txtEventDate2"));
    obj.duration = ifEmpty(getUIValue("txtEventDur"));
    obj.type = ifEmpty(getUIValue("cboEventType"));
    obj.crop = ifEmpty(getUIValue("txtEventCrop"));
    obj.variety = ifEmpty(getUIValue("txtEventVar"));
    obj.comments = ifEmpty(getUIValue("txtEventComm"));
    obj.properties.metric = ifEmpty(getUIValue("txtEventSubstance"));
    obj.properties.target = ifEmpty(getUIValue("txtEventTarget"));
    obj.properties.productName = ifEmpty(getUIValue("txtEventProduct"));
    obj.properties.stage = ifEmpty(getUIValue("txtEventStage"));
    obj.properties.amount = ifEmpty(getUIValue("txtEventAmount"));
    obj.properties.unit = ifEmpty(getUIValue("cboEventAmountUnit"));
    obj.properties.unitRef = ifEmpty(getUIValue("cboEventAmountUnitRef"));
    obj.properties.fuelConsumption = ifEmpty(getUIValue("txtEventFuelConsum"));
    obj.properties.fuelType = ifEmpty(getUIValue("cboEventFuelType"));
    obj.properties.fuelUnit = ifEmpty(getUIValue("cboEventFuelUnit"));
    obj.properties.fuelUnitRef = ifEmpty(getUIValue("cboEventFuelUnitRef"));

    const par = {
        "path": "/event",
        "method": obj.id === "" ? "PUT" : "POST",
        "data": obj.id === "" ? [obj] : obj
    };

    CallAPI(apiURL, par, (data) => { CloseModal('modalEvent'); LoadEvents(); }, "eventEditErr", "btnSaveEvent");
}

function SaveMeteo() {
    //event.preventDefault();
    if (!document.forms["formMeteo"].reportValidity()) return;

    const obj = {};
    obj.properties = {};

    obj.id = getUIValue("txtMeteoID");
    obj.parcelId = ifEmpty(getUIValue("cboMeteoParcel"));
    obj.timestamp = ifEmpty(getUIValue("txtMeteoDate"));
    obj.temperature = ifEmpty(getUIValue("txtMeteoTemperature"));
    obj.humidity = ifEmpty(getUIValue("txtMeteoHumidity"));
    obj.windstrength = ifEmpty(getUIValue("txtMeteoWindstrength")); 
    obj.leafwetness = ifEmpty(getUIValue("txtMeteoLeafwetness"));
    obj.rain = ifEmpty(getUIValue("txtMeteoRain"));

    const par = {
        "path": "/measurement",
        "method": obj.id === "" ? "PUT" : "POST",
        "data": obj.id === "" ? [obj] : obj
    };

    CallAPI(apiURL, par, (data) => { CloseModal('modalMeteo'); LoadMeteos(); }, "meteoEditErr", "btnSaveMeteo");
}

function SaveParcel() {
    //event.preventDefault();
    if (!document.forms["formParcel"].reportValidity()) return;

    const obj = {};
    obj.id = getUIValue("txtParcelID");
    obj.name = ifEmpty(getUIValue("txtParcelName"));
    obj.polygon = ifEmpty(getUIValue("txtParcelPoly"));
    obj.user = "";

    const par = {
        "path": "/parcel",
        "method": obj.id === "" ? "PUT" : "POST",
        "data": obj
    };

    CallAPI(apiURL, par, (data) => { CloseModal('modalParcel'); LoadParcelsAll(); }, "parcelEditErr", "btnSaveParcel");
}

function LoadEnumsData() {
    let v = "value";

    const par = {
        "path": "/parametrics/types/",
        "data": { "type": "" }
    };

    par.data.type = "EventType";
    CallAPI(apiURL, par, (data) => { PopulateSelect("eventType", data, v, "", true); PopulateSelect("resultEventType", data, v, ""); PopulateSelect("cboEventType", data, v, "") }, "", "");
    par.data.type = "FuelType";
    CallAPI(apiURL, par, (data) => { PopulateSelect("cboEventFuelType", data, v, "", true); }, "", "");
    par.data.type = "Unit";
    CallAPI(apiURL, par, (data) => { PopulateSelect("cboEventAmountUnit", data, v, "", true); PopulateSelect("cboEventFuelUnit", data, v, "", true); }, "", "");
    par.data.type = "UnitReference";
    CallAPI(apiURL, par, (data) => { PopulateSelect("cboEventAmountUnitRef", data, v, "", true); PopulateSelect("cboEventFuelUnitRef", data, v, "", true); }, "", "");

}

function LoadParcelsAll() {
    const par = {
        "path": "/parcel/user/",
        "data": { "id": "" }
    };

    CallAPI(apiURL, par, (data) => {
        dataParcels = data.sort((a, b) => a.name.localeCompare(b.name));
        LoadParcelDropDowns();
        PopulateParcelList(dataParcels);
        LoadEvents();
        LoadMeteos();
    }, "parcelListBodyErr", "", "");
}

function LoadDATsAll() {
    const par = {
        "path": "/dats/all",
        "data": {}
    };

    CallAPI(apiURL, par, (data) => {
        dataDATs = data.recommendation_list.map((item) => { return { "id" : item.description.ID, "name" : item.description.name.trim() }; });  //trim() is important for sorting
        dataDATs.sort((a, b) => a.name.localeCompare(b.name));

        PopulateSelect("parcelDAT", dataDATs, "name", "id", true);
        PopulateSelect("cboEventDats", dataDATs, "name", "id", true);
    }, "", "");
}

function LoadParcelsFilter() {

    const dat = getUIValue("parcelDAT");

    if (dat) {
        const par = {
            "path": "/parcel/dat",
            "data": { "dat": dat }
        };

        CallAPI(apiURL, par, (data) => {
            //filter only user's parcels 
            const arr = data.filter(p1 => dataParcels.some(p2 => p2.uid === p1.uid));
            arr.sort((a, b) => a.name.localeCompare(b.name));

            PopulateParcelList(arr);
        }, "eventListBodyErr", "", "");
    }
    else
        PopulateParcelList(dataParcels);

}

function LoadParcelDropDowns() {
    const propName = "name";
    const propValue = "uid";

    PopulateSelect("eventParcelName", dataParcels, propName, propValue, false);
    PopulateSelect("meteoParcelName", dataParcels, propName, propValue, false);
    PopulateSelect("cboEventParcel", dataParcels, propName, propValue, true);
    PopulateSelect("cboMeteoParcel", dataParcels, propName, propValue, true);
    PopulateSelect("cboImportParcel", dataParcels, propName, propValue, false);

    PopulateMultiSelect("result1Parcel1", dataParcels, propName, propValue);
    PopulateMultiSelect("result1Parcel2", dataParcels, propName, propValue);

    PopulateSelect("result2Parcel1", dataParcels, propName, propValue, true);
    PopulateSelect("result2Parcel2", dataParcels, propName, propValue, true);

    PopulateMultiSelect("result3Parcel1", dataParcels, propName, propValue);
    PopulateMultiSelect("result3Parcel2", dataParcels, propName, propValue);
}

function LoadEvents() {
    const par = {
        "path": "/event",
        "method": "GET",
        "data": {}
    };

    par.data.parcelid = getUIValue("eventParcelName") ? getUIValue("eventParcelName") : JoinProp(dataParcels, "uid");
    if (getUIValue("eventType")) par.data.event_type = getUIValue("eventType");
    if (getUIValue("eventDate1")) par.data.fromdate = getUIValue("eventDate1");
    if (getUIValue("eventDate2")) par.data.todate = getUIValue("eventDate2");

    CallAPI(apiURL, par, (data) => {
        data.sort((a, b) => a.eventStart.localeCompare(b.eventStart));
        PopulateEventList(data);
    }, "eventListBodyErr", "");
}

function LoadMeteos() {
    const par = {
        "path": "/measurement",
        "method": "GET",
        "data": {}
    };

    par.data.parcelId = getUIValue("meteoParcelName") ? getUIValue("meteoParcelName") : JoinProp(dataParcels, "uid");
    if (getUIValue("meteoDate1")) par.data.fromdate = getUIValue("meteoDate1");
    if (getUIValue("meteoDate2")) par.data.todate = getUIValue("meteoDate2");

    CallAPI(apiURL, par, (data) => {
        data.sort((a, b) => a.timestamp.localeCompare(b.timestamp));
        PopulateMeteoList(data);
    }, "meteoListBodyErr", "");
}

function PopulateParcelList(data) {
    const e = document.getElementById("parcelListBody");
    let html = "";

    data.forEach((item) => {
        const uid = escHtml(String(item.uid).replace(/['\\]/g, ""));
        html += 
    `<tr>
        <td>${escHtml(item.name)}</td>
        <td>${escHtml(item.ektaria)}</td>
        <td>${escHtml(item.country)}</td>
        <td>${escHtml(item.county)}</td>
        <td class="text-end">
            <button type="button" class="btn btn-success qf-bnt-sm" onclick="LoadParcel('${uid}')"><i class="ri-edit-line"></i></button>
            <button type="button" class="btn btn-warning qf-bnt-sm" onclick="DeleteParcel('${uid}')"><i class="ri-delete-bin-2-line"></i></button>
        </td>
    </tr>`
    }); 

    if (html === "") html = "(no parcels found)";

    e.innerHTML = html;
}

function PopulateEventList(data) {
    const e = document.getElementById("eventListBody");
    let html = "";

    data.forEach((item) => {
        //<td>${GetParcelName(item.parcelId)}</td>
        const eid = escHtml(String(item.id).replace(/['\\]/g, ""));
        html += 
    `<tr>
        
        <td>${escHtml(item.type)}</td>
        <td>${escHtml(DateHM(item.eventStart))}</td>
        <td>${escHtml(DateHM(item.eventEnd))}</td>
        <td>${escHtml(item.metric)}</td>
        <td class="text-end">${escHtml(item.amount)}</td>
        <td>${escHtml(item.unit)}/${escHtml(item.unitRef)}</td>
        <td class="text-end">
            <button type="button" class="btn btn-success qf-bnt-sm" onclick="LoadEvent('${eid}')"><i class="ri-edit-line"></i></button>
            <button type="button" class="btn btn-warning qf-bnt-sm" onclick="DeleteEvent('${eid}')"><i class="ri-delete-bin-2-line"></i></button>
        </td>
    </tr>`
    }); 

    if (html === "") html = "(no events found)";

    e.innerHTML = html;
}

function PopulateMeteoList(data) {
    const e = document.getElementById("meteoListBody");
    let html = "";
    let n = 0;

    for (const item of data) {
        if (++n > maxRows) break;

        //<td>${GetParcelName(item.parcelId)}</td>
        html += 
    `<tr>
        <td>${escHtml(DateHM(item.timestamp))}</td>
        <td class="text-end">${escHtml(item.temperature)}</td>
        <td class="text-end">${escHtml(item.humidity)}</td>
        <td class="text-end">${escHtml(item.windstrength)}</td>
        <td class="text-end">${escHtml(item.leafwetness)}</td>
        <td class="text-end">${escHtml(item.rain)}</td>
        
        <td class="text-end">
            <button type="button" class="btn btn-success qf-bnt-sm" onclick="LoadMeteo('${escHtml(String(item.id).replace(/['\\]/g, ""))}')"><i class="ri-edit-line"></i></button>
            <button type="button" class="btn btn-warning qf-bnt-sm" onclick="DeleteMeteo('${escHtml(String(item.id).replace(/['\\]/g, ""))}')"><i class="ri-delete-bin-2-line"></i></button>
        </td>
    </tr>`
    }; 

    if (html === "") html = "(no measurements found)";
    if (n < data.length) html += `<tr><td colspan="8"><span class="text-warning fw-bold">Result is too large: ${data.length} rows. Please, restrict filters. Only the first ${maxRows} rows are shown.</span></td></tr>`;

    console.log(n, data.length);

    e.innerHTML = html;
}

function GetParcelName(id) {
    return FindByProp(dataParcels, "uid", id, "name");
}

function OpenParcel(data) {

    if (!(data instanceof Object)) {
        data = {};
        data.uid = "";
        data.name = "";
        data.polygon = "";
    }

    setUIValue("txtParcelID", data.uid);
    setUIValue("txtParcelName", data.name);
    setUIValue("txtParcelPoly", data.polygon);

    document.getElementById("modalParcelTitle").innerText = (data.uid) ? "Edit Parcel" : "New Parcel";
    document.getElementById("parcelEditErr").innerHTML = '<span class="text-warning">All fields are required</span>';

    ShowModal('modalParcel');
    SetMap();
}

function LoadParcel(id) {
    const par = {
        "path": "/parcel/ids/",
        "data": { "id": id } 
    };

    CallAPI(apiURL, par, (data) => { OpenParcel(data[0]); }, "", "", "");
}

function OpenEvent(data) {

    if (!(data instanceof Object)) {
        data = {};

        data.id = "";
        data.parcelId = "";
        data.dat = "";
        data.eventStart = "";
        data.eventEnd = "";
        data.duration = "";
        data.type = "";
        data.crop = "";
        data.variety = "";
        data.comments = "";
        data.metric = ""; //properties.
        data.target = "";
        data.productName = "";
        data.stage = "";
        data.amount = "";
        data.unit = "";
        data.unitRef = "";
        data.fuelConsumption = "";
        data.fuelType = "";
        data.fuelUnit = "";
        data.fuelUnitRef = "";
    }

    setUIValue("txtEventID", data.id);
    setUIValue("cboEventParcel", data.parcelId);
    setUIValue("cboEventDats", data.dat);
    setUIValue("txtEventDate1", ifNull(data.eventStart).substring(0, 16));
    setUIValue("txtEventDate2", ifNull(data.eventEnd).substring(0, 16));
    setUIValue("txtEventDur", data.duration);
    setUIValue("cboEventType", data.type);
    setUIValue("txtEventCrop", data.crop);
    setUIValue("txtEventVar", data.variety);
    setUIValue("txtEventComm", data.comments);
    setUIValue("txtEventSubstance", data.metric); //properties.
    setUIValue("txtEventTarget", data.target);
    setUIValue("txtEventProduct", data.productName);
    setUIValue("txtEventStage", data.stage);
    setUIValue("txtEventAmount", data.amount);
    setUIValue("cboEventAmountUnit", data.unit);
    setUIValue("cboEventAmountUnitRef", data.unitRef);
    setUIValue("txtEventFuelConsum", data.fuelConsumption);
    setUIValue("cboEventFuelType", data.fuelType);
    setUIValue("cboEventFuelUnit", data.fuelUnit);
    setUIValue("cboEventFuelUnitRef", data.fuelUnitRef);

    document.getElementById("cboEventType").disabled = data.id;
    document.getElementById("cboEventParcel").disabled = data.id;

    document.getElementById("modalEventTitle").innerText = (data.id) ? "Edit Event" : "New Event";
    document.getElementById("eventEditErr").innerHTML = '<span class="text-warning">Fields marked with * are required</span>';

    ShowModal('modalEvent');
}

function OpenMeteo(data) {

    if (!(data instanceof Object)) {
        data = {};

        data.id = "";
        data.parcelId = "";
        data.timestamp = "";
        data.temperature = "";
        data.humidity = "";
        data.windstrength = "";
        data.leafwetness = "";
        data.rain = "";
    }

    setUIValue("txtMeteoID", data.id);
    setUIValue("cboMeteoParcel", data.parcelId);
    setUIValue("txtMeteoDate", data.timestamp.substring(0, 16));
    setUIValue("txtMeteoTemperature", data.temperature);
    setUIValue("txtMeteoHumidity", data.humidity);
    setUIValue("txtMeteoWindstrength", data.windstrength);
    setUIValue("txtMeteoLeafwetness", data.leafwetness);
    setUIValue("txtMeteoRain", data.rain);
    document.getElementById("cboMeteoParcel").disabled = data.id;

    document.getElementById("modalMeteoTitle").innerText = (data.id) ? "Edit Measurement" : "New Measurement";
    document.getElementById("meteoEditErr").innerHTML = '<span class="text-warning">All fields are required</span>';

    ShowModal('modalMeteo');
}

function LoadEvent(id) {
    const par = {
        "path": "/event/id/",
        "data": { "id": id } 
    };

    CallAPI(apiURL, par, (data) => { OpenEvent(data[0]); }, "", "", "");
}

function LoadMeteo(id) {
    const par = {
        "path": "/measurement/id/",
        "data": { "id": id } 
    };

    CallAPI(apiURL, par, (data) => { OpenMeteo(data[0]); }, "", "", "");
}

function DeleteParcel(id) {

    if (!confirm("Click OK to delete parcel")) return;

    const par = {
        "path": "/parcel",
        "method": "DELETE",
        "data": { "id": id } 
    };

    CallAPI(apiURL, par, (data) => { LoadParcelsAll(); }, "", "", "");
}

function DeleteEvent(id) {

    if (!confirm("Click OK to delete event")) return;

    const par = {
        "path": "/event",
        "method": "DELETE",
        "data": { "id": id } 
    };

    CallAPI(apiURL, par, (data) => { LoadEvents(); }, "", "", "");
}

function DeleteMeteo(id) {

    if (!confirm("Click OK to delete measurement")) return;

    const par = {
        "path": "/measurement",
        "method": "DELETE",
        "data": { "id": id } 
    };

    CallAPI(apiURL, par, (data) => { LoadMeteos(); }, "", "", "");
}

function LoadArrg() {
    //event.preventDefault();
    if (!document.forms["formResult1"].reportValidity()) return;

    let obj, par;

    obj = {};
    obj.parcelid = getUIValue("result1Parcel1");
    if (obj.parcelid) {
        obj.aggregation_function = getUIValue("resultAggr");
        obj.evt_type = getUIValue("resultEventType");
        if (getUIValue("result1Date11")) obj.fromdate = getUIValue("result1Date11");
        if (getUIValue("result1Date12")) obj.todate = getUIValue("result1Date12");

        par = {
            "path": "aggr",
            "data": obj
        };

        CallAPI(apiURL, par, (data) => { PopulateResult1List(data, "result1ListBody1"); PopulateDATs("result1ListDATs1", data.dat); PopulateTCs("result1ListTCs1", data.info.crop); }, "result1ListBodyErr1", "");
    }
    else {
        document.getElementById("result1ListBody1").innerHTML = "";
        document.getElementById("result1ListDATs1").innerHTML = "";
    }

    obj = {};
    obj.parcelid = getUIValue("result1Parcel2");
    if (obj.parcelid) {
        obj.aggregation_function = getUIValue("resultAggr");
        obj.evt_type = getUIValue("resultEventType");
        if (getUIValue("result1Date21")) obj.fromdate = getUIValue("result1Date21");
        if (getUIValue("result1Date22")) obj.todate = getUIValue("result1Date22");

        par = {
            "path": "aggr",
            "data": obj
        };

        CallAPI(apiURL, par, (data) => { PopulateResult1List(data, "result1ListBody2"); PopulateDATs("result1ListDATs2", data.dat); PopulateTCs("result1ListTCs2", data.info.crop); }, "result1ListBodyErr2", "");
    }
    else {
        document.getElementById("result1ListBody2").innerHTML = "";
        document.getElementById("result1ListDATs2").innerHTML = "";
    }

}

function LoadChill() {
    //event.preventDefault();
    if (!document.forms["formResult2"].reportValidity()) return;

    let obj, par;

    obj = {};
    obj.parcelid = getUIValue("result2Parcel1");
    if (obj.parcelid) {
        if (getUIValue("result2Date11")) obj.fromdate = getUIValue("result2Date11");
        if (getUIValue("result2Date12")) obj.todate = getUIValue("result2Date12");
        if (getUIValue("resultLow")) obj.chilling_low_threshold = getUIValue("resultLow");
        if (getUIValue("resultHigh")) obj.chilling_high_threshold = getUIValue("resultHigh");

        par = {
            "path": "chill",
            "data": obj
        };

        CallAPI(apiURL, par, (data) => { PopulateResult2List(data, "result2Chart1"); }, "result2ListBodyErr1", "btnShowResult2");
    }
    else {
        document.getElementById("result2Chart1").innerHTML = "";
    }

    obj = {};
    obj.parcelid = getUIValue("result2Parcel2");
    if (obj.parcelid) {
        if (getUIValue("result2Date21")) obj.fromdate = getUIValue("result2Date21");
        if (getUIValue("result2Date22")) obj.todate = getUIValue("result2Date22");
        if (getUIValue("resultLow")) obj.chilling_low_threshold = getUIValue("resultLow");
        if (getUIValue("resultHigh")) obj.chilling_high_threshold = getUIValue("resultHigh");

        par = {
            "path": "chill",
            "data": obj
        };

        CallAPI(apiURL, par, (data) => { PopulateResult2List(data, "result2Chart2"); }, "result2ListBodyErr2", "");
    }
    else {
        document.getElementById("result2Chart2").innerHTML = "";
    }

}

function LoadMeteoArrg() {
    //event.preventDefault();
    if (!document.forms["formResult3"].reportValidity()) return;

    let obj, par;

    const type = getSelectedText("result3EventType");
    const aggr = getSelectedText("result3Aggr");
    const typeID = getUIValue("result3EventType");
    const aggrID = getUIValue("result3Aggr");

    obj = {};
    obj.parcelid = getUIValue("result3Parcel1");
    if (obj.parcelid) {
        obj.aggregation_function = aggrID;
        obj.measurement_type = typeID;
        if (getUIValue("result3Date11")) obj.fromdate = getUIValue("result3Date11");
        if (getUIValue("result3Date12")) obj.todate = getUIValue("result3Date12");

        par = {
            "path": "meteo",
            "data": obj
        };

        CallAPI(apiURL, par, (data) => { PopulateResult3List(data, "result3Chart1", typeID, type, aggr); }, "result3ListBodyErr1", "btnShowResult3");
    }
    else {
        document.getElementById("result3Chart1").innerHTML = "";
    }

    obj = {};
    obj.parcelid = getUIValue("result3Parcel2");
    if (obj.parcelid) {
        obj.aggregation_function = aggrID;
        obj.measurement_type = typeID;
        if (getUIValue("result3Date21")) obj.fromdate = getUIValue("result3Date21");
        if (getUIValue("result3Date22")) obj.todate = getUIValue("result3Date22");

        par = {
            "path": "meteo",
            "data": obj
        };

        CallAPI(apiURL, par, (data) => { PopulateResult3List(data, "result3Chart2", typeID, type, aggr); }, "result3ListBodyErr2", "btnShowResult3");
    }
    else {
        document.getElementById("result3Chart2").innerHTML = "";
    }

}

function ResultTypeChange() {
    const t = getUIValue("resultType");
    document.getElementById('formResult1').hidden = t != 1;
    document.getElementById('divResult1').hidden = t != 1;
    document.getElementById('formResult2').hidden = t != 2;
    document.getElementById('divResult2').hidden = t != 2;
    document.getElementById('formResult3').hidden = t != 3;
    document.getElementById('divResult3').hidden = t != 3;
}

function PopulateResult1List(data, ctrl) {
    const e = document.getElementById(ctrl);
    let html = "";

    //data.npk={};data.npk.N=1;data.npk.P=2;data.npk.K=3;  //test data
    console.log(data);

    data.info.rank.forEach((item) => {
        html +=
   `<tr>
        <td>${escHtml(data.metric[item].metric)}</td>
        <td class="text-end">${escHtml(data.metric[item].total)}</td>
        <td class="text-end">${escHtml(data.metric[item].unit)}</td>
        <td class="text-end">${escHtml(data.metric[item].per_hectar)}</td>
        <td class="text-end">${escHtml(data.metric[item].total_hect)}</td>
    </tr>`
    });

    if (data.npk) {
        html += `
        <tr><td colspan="5">N = ${escHtml(data.npk.N)}%</td></tr>
        <tr><td colspan="5">P = ${escHtml(data.npk.P)}%</td></tr>
        <tr><td colspan="5">K = ${escHtml(data.npk.K)}%</td></tr>`
    }

    if (html === "") html = "(no data)";

    e.innerHTML = html;
}

function PopulateResult2List(data, ctrl) {
    const el = document.getElementById(ctrl);
    const serie = [];
    let m = 0;

    data.data.forEach((item) => {
        serie.push({ x: new Date(item.timestamp), y: item.index });
        m = Math.max(m, item.index);
    });

    const options = {
        series: [{
            name: 'Index',
            data: serie
        }],
        chart: {
            id: ctrl,
            type: 'line',
            stacked: false,
            height: 350,
            zoom: {
                type: 'x',
                enabled: true,
                autoScaleYaxis: true
            },
            toolbar: {
                autoSelected: 'pan'
            }
        },
        dataLabels: {
            enabled: false
        },
        markers: {
            size: 5,
        },
        title: {
            text: 'Chilling hours',
            align: 'left'
        },
        yaxis: {
            labels: {
                formatter: function (val) {
                    return val.toFixed(1);
                }
            },
            title: {
                text: 'index'
            },
            max: ++m,
        },
        xaxis: {
            type: 'datetime',
        },
        tooltip: {
            shared: false,
            y: {
                formatter: function (val) {
                    return val;
                }
            },
            x: {
                formatter: function (val) {
                    return DateHM((new Date(val)).toISOString());
                }
            }
        }
    };

    if (Apex._chartInstances) Apex._chartInstances.forEach((c) => { if (c.id == ctrl) c.chart.destroy() });

    if (serie.length > 0) {
        el.innerHTML = "";
        const chart = new ApexCharts(el, options);
        chart.render();
    } else
        el.innerHTML = "(no data)";

}

function PopulateResult3List(data, ctrl, typeID, type, aggr) {
    const el = document.getElementById(ctrl);
    const serie = [];
    const units = {
        temperature: "°C",
        humidity: "%", 
        windstrength: "km/h",
        leafwetness: "0/1",
        rain: "mm"
    };

    data.forEach((item) => {
        serie.push({ x: item.month.toString() + "'" + item.year.toString(), y: item[typeID] });
    });

    const options = {
        series: [{
            name: 'value',
            data: serie
        }],
        chart: {
            id: ctrl,
            type: 'line',
            stacked: false,
            height: 350,
            zoom: {
                type: 'x',
                enabled: true,
                autoScaleYaxis: true
            },
            toolbar: {
                autoSelected: 'pan'
            }
        },
        dataLabels: {
            enabled: false
        },
        markers: {
            size: 5,
        },
        title: {
            text: aggr + ' ' + type,
            align: 'left'
        },
        yaxis: {
            labels: { },
            title: {
                text: type + ' (' + units[typeID] + ')'
            },
        },
        xaxis: { },
        tooltip: { },
    };

    if (Apex._chartInstances) Apex._chartInstances.forEach((c) => { if (c.id == ctrl) c.chart.destroy() });

    if (serie.length > 0) {
        el.innerHTML = "";
        const chart = new ApexCharts(el, options);
        chart.render();
    } else
        el.innerHTML = "(no data)";

}

function OpenImport(t) {
    if (t == "parcel")
        document.getElementById("modalImportTitle").innerText = "Import Parcels";
    else if (t == "event")
        document.getElementById("modalImportTitle").innerText = "Import Events";
    else if (t == "meteo")
        document.getElementById("modalImportTitle").innerText = "Import Measurements";

    document.getElementById("divImportParcel").hidden = t == "parcel";
    document.getElementById("importErr").innerHTML = '';
    document.getElementById("importObjType").value = t;
    document.getElementById("inputFile").value = '';
    ShowModal('modalImport');
}

function SaveImport() {
    const f = document.forms["formImport"];
    if (!f.reportValidity()) return;

    const payload = new FormData(f);
    const t = document.getElementById("importObjType").value;

    if (t == "parcel")
        CallUploadAPI(payload, (data) => { CloseModal('modalImport'); LoadParcelsAll(); }, "importErr", "btnImport");
    else if (t == "event")
        CallUploadAPI(payload, (data) => { CloseModal('modalImport'); LoadEvents(); }, "importErr", "btnImport");
    else if (t == "meteo")
        CallUploadAPI(payload, (data) => { CloseModal('modalImport'); LoadMeteos(); }, "importErr", "btnImport");

}

function CallUploadAPI(par, funcSuccess, errContainer, startButton) {

    const url = baseURL + "upload.php";

    if (startButton != "") setButtonState(startButton, true);

    fetch(url, { method: 'POST', mode: 'cors', body: par })
        .then(function (response) {
            if (response.ok)
                return response.text();
            else
                return response.text().then(text => { throw new Error(text) });
        })
        .then(function (data) {
            console.log(data);
            funcSuccess(data);

        })
        .catch(function (error) {
            if (errContainer != "") showErr(errContainer, error);
            console.log(error);
        })
        .finally(function () {
            if (startButton != "") setButtonState(startButton, false);
        });
}

function PopulateDATs(ctrl, dats) {
    const div = document.getElementById(ctrl);
    let s = ""; 

    for (let i = 0; i < dats.length; i++) {
        let dat = dataDATs.find((item) => item.id == dats[i]);

        if (dat) {
            s += `<p class="fw-bold"><a href="#" onclick="LoadDATDetals('${dat.id}'); return false; "><i class="bi bi-gear me-2"></i>${dat.name}</a></p>`;
        }
    }

    div.innerHTML = (s === "") ? '<p class="fw-bold">No DATSs used</p>' : '<p class="fw-bold">DATSs used:</p>';
    div.innerHTML += s;
}

function PopulateTCs(ctrl, crops) {
    const div = document.getElementById(ctrl);
    let s = "";     
    
    if (crops && crops.length > 0) {
        for (let i = 0; i < crops.length; i++) {
            for (let j = 0; j < testCaseData.length; j++) {
                if (testCaseData[j].crop.includes(crops[i])) {
                    s += `<p class="fw-bold">
                    <a href="tcreport.html?n=${testCaseData[j].id}" target="_blank">
                    <i class="fas fa-caret-right mx-2"></i>${testCaseData[j].sector}: ${crops[i]} in ${testCaseData[j].country} - Test Case ${testCaseData[j].id}</a></p>`;
                }
            }
        }
    }

    div.innerHTML = (s === "") ? '' : '<p class="fw-bold">Relevant QuantiFarm Test Cases:</p>';
    div.innerHTML += s;
}

