const datURL = baseURL + "tool1.php";


function LoadDATDetals(id, isID = true, showCB = true) {
    if (!id) return;

    let par = {
        "path": "/dats/main",
        "data": { }
    };

    if (isID) 
        par.data.dats_uri = id;     //by id
    else 
        par.data.dats_name = id;    //by name

    const lng = getDataLanguage();
    if (lng) par.data.language = lng;

    console.log("POST /dats/main body:", par.data);

    CallAPI(datURL, par, (data) => { CreateDetails(data, showCB); ShowModal('modalDAT'); }, "", "");

    return false;
}

function CreateDetails(data, showCB) {

    console.log("/dats/main return:", data);

    const ms = getDatModalStrings();
    const el = document.getElementById("divDatDetail");
    const na = document.getElementById("modalDATTitle");
    const di = data.dats_info;

    const la = escHtml(getObjPropVal(di.description, "name"));
    const de = escHtml(getObjPropVal(di.description, "description"));
    const tt = escHtml(getObjPropVal(di.description, "title"));
    const kw = escHtml(getObjPropVal(di.description, "keywords"));
    const lyr = escHtml(getObjPropVal(di.properties, "launch_year"));
    const uyr = escHtml(getObjPropVal(di.properties, "update_year"));
    const hp = escHtml(safeUrl(getObjPropVal(di.properties, "web_page")));
    const lng = escHtml(getObjPropVal(di.filterable_properties, "languages"));
    const co = escHtml(getObjPropVal(di.filterable_properties, "countries"));
    const fn = escHtml(getObjPropVal(di.filterable_properties, "functionalities"));
    const bn = escHtml(getObjPropVal(di.filterable_properties, "benefits"));
    const df = escHtml(getObjPropVal(di.filterable_properties, "digital_forms"));
    const cs = escHtml(getObjPropVal(di.filterable_properties, "cost_structures"));
    const se = escHtml(getObjPropVal(di.filterable_properties, "agricultural_sectors"));
    const td = GetTestData(data);
    const cb = showCB ? GetCostBenefitData(data) : "";

    na.innerHTML = `<i class="bi bi-gear fa-lg me-2"></i>${la}`;

    let s = `<div class="card-body">
    ${td}
    ${cb}
    <p class="card-text">${tt}</p>
    <p class="card-text">${de}</p>
    <div><table class="table table-sm w-auto"><tbody>
        <tr><th scope="row"></th><td style="width:100%"></td></tr>`;

    if (se) s += `<tr><th class="text-nowrap" scope="row">${ms.agriculturalSector}</th><td>${se}</td></tr>`;
    if (fn) s += `<tr><th class="text-nowrap" scope="row">${ms.functionality}</th><td>${fn}</td></tr>`;
    if (bn) s += `<tr><th class="text-nowrap" scope="row">${ms.benefits}</th><td>${bn}</td></tr>`;
    if (kw) s += `<tr><th class="text-nowrap" scope="row">${ms.keywords}</th><td>${kw}</td></tr>`;
    if (df) s += `<tr><th class="text-nowrap" scope="row">${ms.digitalForm}</th><td>${df}</td></tr>`;
    if (cs) s += `<tr><th class="text-nowrap" scope="row">${ms.costStructure}</th><td>${cs}</td></tr>`;
    if (lng) s += `<tr><th class="text-nowrap" scope="row">${ms.languages}</th><td>${lng}</td></tr>`;
    if (co) s += `<tr><th class="text-nowrap" scope="row">${ms.country}</th><td>${co}</td></tr>`;
    if (lyr) s += `<tr><th class="text-nowrap" scope="row">${ms.launchYear}</th><td>${lyr}</td></tr>`;
    if (uyr) s += `<tr><th class="text-nowrap" scope="row">${ms.updateYear}</th><td>${uyr}</td></tr>`;
    if (hp) s += `<tr><th class="text-nowrap" scope="row">${ms.link}</th><td><a href="${hp}" target="_blank" class="card-link">${hp}</a></td></tr>`;

    s += `</tbody></table></div></div>`;

    el.innerHTML = s;
}

function GetTestData(data) {
    if (data.test_cases.length == 0) return "";

    const ms = getDatModalStrings();
    data.test_cases.sort((a, b) => a.description.number - b.description.number);    
    
    let s = `<p class="card-text text-danger fw-bold"><i class="bi bi-info-circle fa-lg"></i> ${ms.assessedIntro}</p>
    <table class="table table-sm">
    `;
    let c1="", c2="", c3="", v1=0, v2=0, v3=0, a1="", a2="", a3="";

    data.test_cases.forEach((tc) => {
        tc.assessments.forEach((ass) => {
            if (ass.year === 2026) { //aggregated year
               
                v1 = Math.round(ass.sustainability.economic);
                v2 = Math.round(ass.sustainability.social);
                v3 = Math.round(ass.sustainability.environmental);
                c1 = GetColorByValue(v1);
                c2 = GetColorByValue(v2);
                c3 = GetColorByValue(v3);
                a1 = GetArrowByValue(v1);
                a2 = GetArrowByValue(v2);
                a3 = GetArrowByValue(v3);

                s += `<tr>
                <td class="w-100"><a href="tcreport.html?n=${encodeURIComponent(tc.description.number)}" target="_blank"><i class="fas fa-caret-right mx-2"></i>${escHtml(GetTCdata(tc.description.number, ass.product))} – ${ms.testCase} ${escHtml(tc.description.number)}</a></td>
                <td class="${c1}"><i class="fas fa-coins fa-lg"></i></td><td class="${c1} text-end fw-bold">${v1}%</td><td class="${c1} pe-3"><i class="${a1}"></i></td>
                <td class="${c2}"><i class="fas fa-users fa-lg"></i></td><td class="${c2} text-end fw-bold">${v2}%</td><td class="${c2} pe-3"><i class="${a2}"></i></td>
                <td class="${c3}"><i class="fas fa-leaf-heart fa-lg"></i></td><td class="${c3} text-end fw-bold">${v3}%</td><td class="${c3} pe-3"><i class="${a3}"></i></td>
                </tr>`;
            }
        });
    });

    s += `</table>
    <div class="row my-2"><div class="col-12 fst-italic text-muted">
    <i class="bi bi-info-circle fa-lg"></i>  
    <i class="fas fa-coins mx-1 fa-lg"></i> ${ms.economicLegend}
    <i class="fas fa-users mx-1 fa-lg"></i> ${ms.socialLegend}
    <i class="fas fa-leaf-heart mx-1 fa-lg"></i> ${ms.environmentalLegend}
    ${ms.percentageInfo}
    </div></div>`;

    return s;
}

function GetColorByValue(val) {
    if (val > 0) return "text-success";
    if (val < 0) return "text-danger";
    return "text-primary";
}

function GetArrowByValue(val) {
    if (val > 0) return "fas fa-arrow-alt-up";
    if (val < 0) return "fas fa-arrow-alt-down";
    return "";
}

function GetTCdata(tcID, product) {
    let s = "";

    testCaseData.forEach((tc) => {
        if (tc.id === tcID) 
            s = translateSector(tc.sector) + ": " + product + " in " + translateCountry(tc.country);
    });

    return s;
} 

function GetCostBenefitData(data) {

    if (!(data.dats_info.properties.source.includes("costbenefit") || data.test_cases.length > 0)) return "";

    const ms = getDatModalStrings();
    let s = `<p class="card-text text-danger fw-bold"><i class="bi bi-info-circle fa-lg"></i> ${ms.costBenefitIntro}
    <a href="tool2.html?s=${encodeURIComponent(data.dats_info.description.name)}" target="_blank">${ms.costBenefitLink}</a></p>`;

    s += "";

    return s;
}

