const tool_key = "tool2";
const apiURL = baseURL + "tool2.php";

const crop = "crop";
const live = "livestock";
const cropTC = "cropTC";
const liveTC = "livestockTC";

const modulesMap = {
    arable:     [],
    fruits:     [],
    vineyards:  [],
    vegetables: [],
    orchards:   [],
//
    cattle :        ["livestock_calc_water_usage", "livestock_calc_mortality_cost"],
    pigs:           ["livestock_calc_milk_yield", "livestock_calc_water_usage", "livestock_calc_profit_per_animal"],
    poultry:        ["livestock_calc_milk_yield", "livestock_calc_energy_cost", "livestock_calc_water_usage", "livestock_calc_profit_per_animal", "livestock_calc_feed_cost", "livestock_calc_feed_waste", "livestock_calc_antibiotics_cost", "livestock_calc_mortality_cost"],
    small_ruminants:["livestock_calc_water_usage", "livestock_calc_profit_per_animal", "livestock_calc_antibiotics_cost", "livestock_calc_mortality_cost", "livestock_calc_profitability_increase"],
 //
    TC1:    [],
    TC2:    ["cropTC_calc_fertilizer","cropTC_calc_pesticide", "cropTC_calc_fuel"],
    TC3:    ["cropTC_calc_water","cropTC_calc_electricity"],
    TC4:    ["cropTC_calc_water","cropTC_calc_fuel","cropTC_calc_labor","cropTC_calc_electricity"],
    TC5:    ["cropTC_calc_electricity"],
    TC6:    ["cropTC_calc_fertilizer","cropTC_calc_fuel","cropTC_calc_pesticide"],
    TC7:    ["cropTC_calc_fuel","cropTC_calc_labor","cropTC_calc_electricity","cropTC_calc_pesticide"],
    TC8:    ["cropTC_calc_fuel","cropTC_calc_fertilizer","cropTC_calc_electricity","cropTC_calc_pesticide","cropTC_calc_water"],
    TC9:    ["cropTC_calc_water","cropTC_calc_electricity"],
    TC10:   ["cropTC_calc_water"],
    TC11:   ["cropTC_calc_fertilizer","cropTC_calc_fuel"],
    TC12:   ["cropTC_calc_fertilizer","cropTC_calc_water","cropTC_calc_pesticide"],
    TC13:   ["cropTC_calc_fertilizer","cropTC_calc_electricity"],
    TC14:   [],
    TC15:   [],
    TC16:   ["cropTC_calc_fertilizer","cropTC_calc_pesticide"],
    TC17:   ["cropTC_calc_yield","cropTC_calc_fuel","cropTC_calc_fertilizer","cropTC_calc_electricity","cropTC_calc_water"],
    TC18:   ["cropTC_calc_electricity"],
    TC19:   ["cropTC_calc_fertilizer","cropTC_calc_labor","cropTC_calc_pesticide"],
    TC20:   ["cropTC_calc_fertilizer","cropTC_calc_fuel","cropTC_calc_labor","cropTC_calc_electricity"],
    TC21:   [],
 //   
    TC22:   ["livestockTC_calc_oyster","livestockTC_calc_honey","livestockTC_calc_milk_yield","livestockTC_calc_labor_cost","livestockTC_calc_feed_cost","livestockTC_calc_fuel_cost","livestockTC_calc_antibiotics_cost","livestockTC_calc_mortality_cost"],  
    TC23:   ["livestockTC_calc_oyster","livestockTC_calc_honey","livestockTC_calc_milk_yield","livestockTC_calc_antibiotics_cost"],
    TC24:   ["livestockTC_calc_meat","livestockTC_calc_oyster","livestockTC_calc_honey","livestockTC_calc_milk_yield","livestockTC_calc_labor_cost","livestockTC_calc_electricity_cost","livestockTC_calc_feed_cost"],
    TC25:   ["livestockTC_calc_meat","livestockTC_calc_oyster","livestockTC_calc_honey","livestockTC_calc_water_usage","livestockTC_calc_feed_cost","livestockTC_calc_antibiotics_cost","livestockTC_calc_mortality_cost"],
    TC26:   ["livestockTC_calc_meat","livestockTC_calc_oyster","livestockTC_calc_honey","livestockTC_calc_water_usage","livestockTC_calc_feed_cost","livestockTC_calc_fuel_cost","livestockTC_calc_mortality_cost"],
    TC27:   ["livestockTC_calc_meat","livestockTC_calc_oyster","livestockTC_calc_honey","livestockTC_calc_labor_cost"],
    TC28:   ["livestockTC_calc_meat","livestockTC_calc_oyster","livestockTC_calc_honey","livestockTC_calc_feed_cost","livestockTC_calc_fuel_cost","livestockTC_calc_mortality_cost"],
    TC29:   ["livestockTC_calc_meat","livestockTC_calc_oyster","livestockTC_calc_milk_yield","livestockTC_calc_electricity_cost","livestockTC_calc_water_usage","livestockTC_calc_feed_cost","livestockTC_calc_fuel_cost","livestockTC_calc_mortality_cost"],
    TC30:   ["livestockTC_calc_meat","livestockTC_calc_honey","livestockTC_calc_milk_yield","livestockTC_calc_labor_cost","livestockTC_calc_electricity_cost","livestockTC_calc_water_usage","livestockTC_calc_feed_cost","livestockTC_calc_antibiotics_cost"],
};

let indexTrees = [];
let currentFarmType = "";
let dataTree = {
    crop: {},
    livestock: {},
    cropTC: {},
    livestockTC: {}
};
let dataUserData = {
    crop: {},
    livestock: {},
    cropTC: {},
    livestockTC: {}
};
let currentType = {
    crop: "",
    livestock: "",
    cropTC: "",
    livestockTC: ""
};
let currentTC = {
    crop: 0,
    livestock: 0,
    cropTC: 0,
    livestockTC: 0
};
let currentDAT = {
    crop: "",
    livestock: "",
    cropTC: "",
    livestockTC: ""
};

document.addEventListener("DOMContentLoaded", setSidebar(tool_key));


SetLoggedUser(SetUI);

function SetUI() {
    user = JSON.parse(localStorage.getItem(key_usr));

    if (!user.loggedin) {
        document.getElementById('lnkLogin').hidden = !true;

        document.getElementById('lockTabcrop').hidden = !true;
        document.getElementById('btnTabcrop').disabled = !false;
        document.getElementById('lockTablivestock').hidden = !true;
        document.getElementById('btnTablivestock').disabled = !false;
        document.getElementById('lockTabcropTC').hidden = !true;
        document.getElementById('btnTabcropTC').disabled = !false;
        document.getElementById('lockTablivestockTC').hidden = !true;
        document.getElementById('btnTablivestockTC').disabled = !false;

        document.getElementById('lnkSearch').hidden = !false;

    } else
        LoadData();
}

function LoadData() {
    let par;
    const div1 = "divDAT" + live;
    const div2 = "divDAT" + crop;
    const div3 = "divDAT" + cropTC;
    const div4 = "divDAT" + liveTC;

    showSpinner(div1);
    showSpinner(div2);
    showSpinner(div3);
    showSpinner(div4);

    par = {
        "path": "/dat_tree",
        "data": { "myDatType": crop },
        "version": 1
    };

    CallAPI(apiURL, par, (data) => { dataTree[crop] = data; IndexTree(data, crop); }, div1, "");

    par = {
        "path": "/dat_tree",
        "data": { "myDatType": live },
        "version": 1
    };

    CallAPI(apiURL, par, (data) => { dataTree[live] = data; IndexTree(data, live); }, div2, "");

    par = {
        "path": "/dat_tree",
        "data": { "myDatType": crop },
        "version": 2
    };

    CallAPI(apiURL, par, (data) => { dataTree[cropTC] = data; IndexTree(data, cropTC); ClearTotalResult(cropTC); SetResultDisabled(cropTC, true); PopulateTreeTC(cropTC); }, div3, "");

    par = {
        "path": "/dat_tree",
        "data": { "myDatType": live },
        "version": 2
    };

    CallAPI(apiURL, par, (data) => { dataTree[liveTC] = data; IndexTree(data, liveTC); ClearTotalResult(liveTC); SetResultDisabled(liveTC, true); PopulateTreeTC(liveTC); }, div4, "");

    par = {
        "path": "/user_data_get",
        "type": crop,
        "data": { user_id: "" },
        "version": 1
    };

    CallAPI(apiURL, par, (data) => { dataUserData[crop] = FlatObject(data); PopulateUserData(crop); }, "", "");

    par = {
        "path": "/user_data_get",
        "type": live,
        "data": { user_id: "" },
        "version": 1
    };

    CallAPI(apiURL, par, (data) => { dataUserData[live] = FlatObject(data); PopulateUserData(live); }, "", "");
    
    par = {
        "path": "/user_data_get",
        "type": crop,  
        "data": { user_id: "" },
        "version": 2
    };

    CallAPI(apiURL, par, (data) => { dataUserData[cropTC] = FlatObject(data); PopulateUserData(cropTC); }, "", "");

    par = {
        "path": "/user_data_get",
        "type": live,
        "data": { user_id: "" },
        "version": 2
    };

    CallAPI(apiURL, par, (data) => { dataUserData[liveTC] = FlatObject(data); PopulateUserData(liveTC); }, "", "");

    //search
    const searchParams = new URLSearchParams(window.location.search);
    const stxt = searchParams.get('s');

    if (stxt) ShowSearch(stxt);
}

function PopulateTree() {
    if (Object.keys(dataTree[currentFarmType]).length === 0) return;

    const tree = dataTree[currentFarmType][currentType[currentFarmType]];
    const div = document.getElementById("divDAT" + currentFarmType);
    let o1, o2;
    let i = 0;
    const pref = "tree" + currentFarmType;
    let html = `<ul id="${pref}">`;

    //hard-coded 2 levels tree
    for (let l1 in tree) {
        o1 = tree[l1];
        html += `<li id="${pref + i++}"><a>${l1}</a><ul>`;

        for (let l2 in o1) {
            o2 = o1[l2];

            for (let l3 in o2) {
                html += `<li id="${pref + i++}"><a href="#" onclick="OnClickDAT('${o2[l3]}'); return false;">${o2[l3]}</a>
                <span><a href="#" onclick="ShowDetails('${o2[l3]}'); return false;" title="DAT info">
                <i class="bi bi-info-circle fa-lg"></i></a></span></li>`;
            }
        }
        html += `</ul></li>`;
    }
    html += `</ul>`;

    NavTree.remove(document.querySelector("#" + pref));

    div.innerHTML = html;

    new NavTree(document.querySelector("#" + pref), {
        searchable: false,
        showEmptyGroups: true,

        groupOpenIconClass: "fa-regular",
        groupOpenIcon: "fa-folder-open",

        groupCloseIconClass: "fa-solid",
        groupCloseIcon: "fa-folder",

        linkIconClass: "bi",
        linkIcon: "bi-gear"
    });

    // Category folder labels ("Farm Management Information Systems (FMIS)" etc.)
    // come straight from the DB in English - translate via costBenefitStrings.
    translateCostBenefit(localStorage.getItem(qf_lang_storage_key) || 'EN');
}

function PopulateTreeTC(ft) {
    if (Object.keys(dataTree[ft]).length === 0) return;

    const tree = dataTree[ft][ft.replace("TC", "")];
    const div = document.getElementById("divDAT" + ft);
    let o1;
    let i = 0;
    const pref = "tree" + ft;
    let html = `<ul id="${pref}">`;

    //hard-coded 2 levels tree
    for (let l1 in tree) {
        o1 = tree[l1];
        html += `<li id="${pref + i++}"><a>${l1}</a><ul>`;

        for (let l2 in o1) {
            let tcN = GetObjectFirstKeyName(o1[l2], 0).trim().slice(2);
            let dat = GetObjectFirstKeyName(o1[l2], 3);
            let cfilter = GetObjectFirstKeyName(o1[l2], 2);
            let cnt = GetObjectFirstKeyName(o1[l2], 1).trim();

            html += `<li id="${pref + i++}"><a href="#" onclick="OnClickDATTC('${dat}', '${cfilter}', ${tcN}); return false;">TC${tcN} in ${cnt}: ${l2}</a>
<span><a href="tcreport.html?n=${tcN}" target="_blank" title="Test Case ${tcN} info">
<i class="bi bi-info-circle fa-lg"></i></a></span></li>`;
        }
        html += `</ul></li>`;
    }
    html += `</ul>`;

    NavTree.remove(document.querySelector("#" + pref));

    div.innerHTML = html;

    new NavTree(document.querySelector("#" + pref), {
        searchable: false,
        showEmptyGroups: true,

        groupOpenIconClass: "fa-regular",
        groupOpenIcon: "fa-folder-open",

        groupCloseIconClass: "fa-solid",
        groupCloseIcon: "fa-folder",

        linkIconClass: "bi",
        linkIcon: "bi-gear"
    });

    // Category folder labels come straight from the DB in English - translate via
    // costBenefitStrings.
    translateCostBenefit(localStorage.getItem(qf_lang_storage_key) || 'EN');
}

function PopulateUserData(t) {
    Object.keys(dataUserData[t]).forEach((k) => {
        setUIValue(t + "_" + k, Number(dataUserData[t][k] || 0));
    });
}

function PopulateTotalResult(data) {
    ClearTotalResult();

    console.log(data);

    const lng = localStorage.getItem(qf_lang_storage_key);
    const strings = (typeof costBenefitStrings !== 'undefined' && lng) ? costBenefitStrings[lng] : null;
    const t = (s) => (strings && strings[s]) ? strings[s] : s;

    Object.keys(data).forEach((k) => {
        let v = Number(data[k]);
        let n = currentFarmType + "_" + k;

        if (isNaN(v)) v = 0;

        if (k.includes("is_the_dat_beneficial")) 
            setUIValue(n, v > 0 ? t("YES") : t("NO"));
        else if (k.includes("_roi") && v == 0)
            setUIValue(n, t("DATS is free"));
        else if (k.includes("payback_") && v < 0)
            setUIValue(n, t("N/A"));
        else
            setUIValue(n, v.toFixed(2));
    });
}

function ClearTotalResult(t) {
    const ft = t ? t : currentFarmType;

    Array.from(document.getElementById("divCalcs" + ft).getElementsByTagName('td')).forEach((n) => {
        if (n.id.startsWith(ft))
            n.innerHTML = "---";
    });
}

function OnClickTab(t) {
    if (Object.keys(dataTree[t]).length === 0) return;

    currentFarmType = t;

    if (t == crop || t == live) 
         OnChangeType();
    else
       ;
}

function OnClickDAT(dat) {
    currentDAT[currentFarmType] = dat;
    SetResultDisabled(currentFarmType, false);
    PopulateUserData(currentFarmType);
    GetTotalResult();
}

function OnClickDATTC(dat, cfilter, tc) {
    currentDAT[currentFarmType] = dat;
    currentType[currentFarmType] = cfilter;
    currentTC[currentFarmType] = tc;
    SetCalcsVisibility("TC"+tc);
    SetResultDisabled(currentFarmType, false);
    GetTotalResult();
}

function OnChangeType() {
    const t = getUIValue("cboType" + currentFarmType);

    if (t == currentType[currentFarmType]) return;

    currentType[currentFarmType] = t;
    currentDAT[currentFarmType] = "";

    PopulateTree();
    ClearTotalResult();
    SetCalcsVisibility(t);
    SetResultDisabled(currentFarmType, true);
}

function Recalculate() {
    const newData = { user_id: "" };
    
    Array.from(document.getElementById("divCalcs" + currentFarmType).getElementsByTagName('input')).forEach((n) => {
        if (n.id.startsWith(currentFarmType))
            newData[n.id.slice(currentFarmType.length + 1)] = Number(n.value);
    });

    const par = {
        "path": "/user_data_post",
        "type": currentFarmType.replace("TC", ""),
        "data": [newData],
        "version": (currentFarmType == crop || currentFarmType == live) ? 1 : 2
    };

    console.log(par);

    CallAPI(apiURL, par, (data) => { dataUserData[currentFarmType] = newData; GetTotalResult(); }, "", "btnCalc" + currentFarmType);
}

function GetTotalResult() {
    if (Object.keys(dataUserData[currentFarmType]).length === 0) return;

    const par = {
        "path": "/totals/",
        "data": {
            "user_id": "",
            "dat_name": currentDAT[currentFarmType],
            "myCultivationType": currentType[currentFarmType],
            "cfilter": currentType[currentFarmType],
            "tcnumber": currentTC[currentFarmType],
            "type": currentFarmType.replace("TC", "")
        },
        "version": (currentFarmType == crop || currentFarmType == live) ? 1 : 2
    };

    console.log(par);

    CallAPI(apiURL, par, (data) => {const res = data.result; PreProcessResult(res); PopulateTotalResult(FlatObject(res)) }, "", "btnCalc" + currentFarmType);
}

function ShowDetails(name) {

    LoadDATDetals(name, false, false);

}

function SetResultDisabled(ft, v) {
    setDisabled('divCalcList' + ft, v);
    document.getElementById('btnCalc' + ft).disabled = v;
}

function SetCalcsVisibility(k) {
    const arr = modulesMap[k];
    const el = document.getElementById("divCalcList" + currentFarmType);

    Array.from(el.children).forEach((n) => {
        n.hidden = arr.includes(n.id);
    });
}

function FlatObject(o) {
    const f = {};

    Object.keys(o).forEach((k) => {
        if (o[k] instanceof Object)
            Object.keys(o[k]).forEach((k1) => { f[k1] = o[k][k1] });
        else
            f[k] = o[k];
    });

    return f;
}

function PreProcessResult(data) {
    if (currentFarmType != liveTC) return;

    data.meat_current_revenue = data.meat_productivity.current_revenue_without_dats;
    data.meat_revenue_impact = data.meat_productivity.revenue_impact_with_dats;
    data.oyster_current_revenue = data.oyster.current_revenue_without_dats;
    data.oyster_revenue_impact = data.oyster.revenue_impact_with_dats;
    data.honey_current_revenue = data.honey.current_revenue_without_dat;
    data.honey_revenue_impact = data.livestock_revenue_impact.revenue_impact_with_dats;
    data.milk_current_revenue = data.milk.current_revenue_without_dats;
    data.milk_revenue_impact = data.revenue_impact.revenue_impact_with_dats;

}

function IndexTree(tree, ft) {
    let o0, o1, o2;
    let i, j;
    const pref = "tree" + ft;

    if (ft == crop || ft == live) {
        for(let l0 in tree) {
            o0 = tree[l0];
            i = 0;

            for (let l1 in o0) {
                o1 = o0[l1];
                j = i++;

                for (let l2 in o1) {
                    o2 = o1[l2];

                    for (let l3 in o2) {
                        indexTrees.push({"farmType": ft, "type": l0, "parentNodeID": pref + j, "nodeID": pref + i++, "dats": [o2[l3]]});
                    }
                }
            } 
        }
    }
    else {
        for(let l0 in tree) {
            o0 = tree[l0];
            i = 0;

            for (let l1 in o0) {
                o1 = o0[l1];
                j = i++;

                for (let l2 in o1) {
                    o2 = o1[l2];
                    let dat = GetObjectFirstKeyName(o1[l2], 3);
                    let cfilter = GetObjectFirstKeyName(o1[l2], 2).toLowerCase();

                    indexTrees.push({"farmType": ft, "type": cfilter, "parentNodeID": pref + j, "nodeID": pref + i++, "dats": dat.split('|')});
                }
            } 
        }
    }

}

function OnSearch() {
    let txt = getUIValue("txtSearchText").toLowerCase();

    if (txt.length < 3) return;

    let html = "";
    let n = 0;

    for (let i=0; i<indexTrees.length; i++) {
        for (let j=0; j<indexTrees[i].dats.length; j++) {
            if (indexTrees[i].dats[j].toLowerCase().includes(txt)) {
                let dats = indexTrees[i].dats[j];

                html += `<li><a href="#" onclick="OnSearchItem('${i}'); return false;">DATS "${dats}" for ${indexTrees[i].type.replace("_", " ")}</a></li>`;
                n++;
            }
        }
    }

    if(html)
        html = `<p>Click on the DATS to navigate to it:</p><ul>${html}</ul>`;
    else
        html = "<p class='fst-italic'>No DATSs found</p>";
    
    document.getElementById("divSearchResults").innerHTML = html;

}

function OnSearchItem(i) {
    const item = indexTrees[i];

    (new bootstrap.Tab(document.getElementById('btnTab'+item.farmType))).show();
    OnClickTab(item.farmType);

    if(item.farmType == crop || item.farmType == live) {
        setUIValue("cboType" + item.farmType, item.type);
        OnChangeType();
    }

    expandTreeNode(item.parentNodeID);
    scrollToTreeNode(item.nodeID);   
    clickAndActivateTreeNode(item.nodeID);

    CloseModal('modalSearch');
}

function ShowSearch(txt) {
    if (txt) {
        setUIValue("txtSearchText", txt);
        document.getElementById("divSearchResults").innerHTML = "";
    }

    ShowModal('modalSearch'); 

    return false;
}

// treeview functions
// Function to expand a tree node by its ID
function expandTreeNode(nodeId) {
    const collapseElement = document.getElementById('ntc-' + nodeId);

    console.log(collapseElement);

    if (collapseElement) {
        const collapseInstance = bootstrap.Collapse.getInstance(collapseElement);

        console.log(collapseInstance);

        if (collapseInstance) {
            collapseInstance.show();
        } else {
            new bootstrap.Collapse(collapseElement, {
                toggle: false
            }).show();
        }
    }
}

// Function to click on a tree node and make it active
function clickAndActivateTreeNode(nodeId) {
    const liElement = document.getElementById(nodeId);
    if (liElement) {
        // Remove active class from all tree items
        const allTreeItems = document.querySelectorAll('.nt-li');
        allTreeItems.forEach(item => item.classList.remove('active'));
        
        // Add active class to the target item
        liElement.classList.add('active');
        
        // Find and click the nav-link
        const navLink = liElement.querySelector('.nav-link');
        if (navLink) {
            navLink.click();
        }
    }
}

// Basic function to scroll to a tree node
function scrollToTreeNode(nodeId) {
    const targetNode = document.getElementById(nodeId);
    if (targetNode) {
        targetNode.scrollIntoView({
            behavior: 'smooth',
            block: 'center',
            inline: 'nearest'
        });
    }
}
