const tool_key = "tool1";
const apiURL = baseURL + "tool1.php";

const pageSize = 15;
const maxItems = 3;
let currentN = 0;
let cardData;
let last_sidebar_filters = {};
const sustPref = {
    "1": { //Family First
        "ecological": 0.6,
        "economic": 0.3,
        "social": 1
    },
    "2": { //Digital Autonomy
        "ecological": 1,
        "economic": 0.3,
        "social": 0.6
    },
    "3": { //Cautiously Ardent
        "ecological": 0.6,
        "economic": 1,
        "social": 0.3
    },
    "4": { //Business Mentality
        "ecological": 0.3,
        "economic": 1,
        "social": 0.6
    },
    "5": { //Community Focused
        "ecological": 0.9,
        "economic": 0.2,
        "social": 1
    },
    "6": { //Other
        "ecological": 0.5,
        "economic": 0.5,
        "social": 0.5
    }
};


document.addEventListener("DOMContentLoaded", setSidebar(tool_key));

document.addEventListener("DOMContentLoaded", () => {
    document
        .querySelectorAll('[qf-multiselect]')
        .forEach((item) => item.addEventListener('change', handleMultiSelectDropdownCB));
});

// LoadFilterLists(); kein Befüllen der sidebar-Filters
LoadProfileLists();
OnProfile(6);


function DoTest() {
    const searchParams = new URLSearchParams(window.location.search);
    if (!searchParams.has('test')) return;

    setTimeout(() => {
        console.log("DoTest...");
        setUIValue("farmFarmType", "Arables");
        setUIValue("farmFunctionality", "Farm & Resource Management");
        OnProfile(2);
        Recommend();
    }, 1000);
}

/* function LoadFilterLists() {
    const par = {
        "path": "/filters",
        "data": {}
    };

    showSpinner("divResultInfo");

    CallAPI(apiURL, par, (data) => {
        UpdateAllCheckListData(data["filter_list"]);

        document.getElementById("divResultInfo").innerHTML = "";
    }, "divResultInfo", "");
} */

function LoadProfileLists() {
    const par = {
        "path": "/profile_entries/",
        "data": {}
    };

    showSpinner("divResultInfo");

    CallAPI(apiURL, par, (data) => {
        PopulateMultiSelect("farmFarmType", data.farm_type, "", "");
        // CH customization (disabled): was restricted to Switzerland only
        // PopulateSelect("farmCountry", data.country ? data.country.filter(c => c === "Switzerland") : [], "", "", true);
        // setUIValue("farmCountry", "Switzerland");
        PopulateSelect("farmCountry", data.country, "", "", true);
        PopulateMultiSelect("farmFunctionality", data.functionalities, "", "");
        PopulateMultiSelect("farmBenefit", data.benefits, "", "");
        PopulateMultiSelect("farmTechnology", data.digital_forms, "", "");
        // Populated after setLanguage() already ran once (async response), so
        // translate the newly-added option labels for the current language now.
        translateProfileMultiSelect(localStorage.getItem(qf_lang_storage_key) || 'EN');

        document.getElementById("divResultInfo").innerHTML = "";

        DoTest();

    }, "divResultInfo", "");
}

/* function UpdateAllCheckListData(data) {
    const v1 = "option";
    const v2 = "count";

    // CH customization: restrict Language filter to DE/FR/IT only
    // Commented-out entries can be re-enabled for future use
    const chLanguages = ["German", "French", "Italian"];
    // Excluded: "English", "Spanish", "Portuguese", "Dutch", "Polish",
    //           "Greek", "Romanian", "Hungarian", "Czech", "Bulgarian",
    //           "Croatian", "Slovak", "Danish", "Finnish", "Swedish",
    //           "Lithuanian", "Latvian", "Estonian", "Slovenian", "Maltese"
    const filteredLanguages = data.languages
        ? data.languages.filter(item => chLanguages.includes(item[v1]))
        : [];

    // CH customization: restrict Country filter to Switzerland only    
    const chCountries = ["Switzerland"];
    const filteredCountries = data.countries
         ? data.countries.filter(item => chCountries.includes(item[v1]))
         : [];

    PrepareCheckList(data.agricultural_sectors, last_sidebar_filters.agricultural_sectors);
    PrepareCheckList(data.functionalities, last_sidebar_filters.functionalities);
    PrepareCheckList(data.benefits, last_sidebar_filters.benefits);
    PrepareCheckList(data.digital_forms, last_sidebar_filters.digital_forms);
    PrepareCheckList(filteredCountries, last_sidebar_filters.countries);
    PrepareCheckList(filteredLanguages, last_sidebar_filters.languages);
    PrepareCheckList(data.cost_structures, last_sidebar_filters.cost_structures);

    PopulateCheckList("filterSector", data.agricultural_sectors, v1, v2);
    PopulateCheckList("filterFunctionality", data.functionalities, v1, v2);
    PopulateCheckList("filterBenefits", data.benefits, v1, v2);
    PopulateCheckList("filterDigitalform", data.digital_forms, v1, v2);
    PopulateCheckList("filterCountry", filteredCountries, v1, v2);
    PopulateCheckList("filterLanguage", filteredLanguages, v1, v2);
    PopulateCheckList("filterCost", data.cost_structures, v1, v2);

} */

function PrepareCheckList(data, filter) {
    if (!data) return;

    //set the last checked
    data.forEach((item) => {
        if (filter && filter.indexOf(item.option) >= 0) item.checked = true;
    });

    //move checked on top
    data.sort(function (a, b) { return (a.checked ? 0 : 1) - (b.checked ? 0 : 1) });
}

function Recommend() {
    const par = {
        "path": "/dats/recommend",
        "data": {},
        "q": {},
    };

    par.q = {};
    CollectProfileFilters(par.data);
    //CollectSidebarFilters(par.data); Sidebar-Filter ausgeschaltet, da nicht sichtbar
    CollectSearchbarFilters(par.data);

    const lng = getDataLanguage();
    if (lng) par.data.language = lng;

    last_sidebar_filters = par.data.selected_filters ? par.data.selected_filters : {};

    console.log("POST /dats/recommend body:", par.data);

    CallAPI(apiURL, par, (data) => {
        console.log("return:", data);

        cardData = data.recommendation_list;
        if (!cardData) cardData = [];

        currentN = 0;
        PopulateDATs();
        //UpdateAllCheckListData(data.filter_list); Checklist befüllt nur sidebar, daher hier ausgeschaltet

    }, "divResultInfo", "btnRecommend");

}

function CollectProfileFilters(obj) {
    let o = obj.farmer_profile = {};

    GetProfileItemArr("farmFarmType", o, "farm_type", false);
    GetProfileItemArr("farmCountry", o, "country", true);
    GetProfileItemArr("farmTechnology", o, "digital_forms", false);
    GetProfileItemArr("farmFunctionality", o, "functionalities", false);
    GetProfileItemArr("farmBenefit", o, "benefits", false);

    if (Object.keys(o).length == 0) delete obj.farmer_profile;
}

/* function CollectSidebarFilters(obj) {
    let arr;
    let o = obj.selected_filters = {};

    arr = getCheckListValues("filterSector");
    if (arr.length > 0) o.agricultural_sectors = arr;
    arr = getCheckListValues("filterFunctionality");
    if (arr.length > 0) o.functionalities = arr;
    arr = getCheckListValues("filterBenefits");
    if (arr.length > 0) o.benefits = arr;
    arr = getCheckListValues("filterDigitalform");
    if (arr.length > 0) o.digital_forms = arr;
    arr = getCheckListValues("filterLanguage");
    if (arr.length > 0) o.languages = arr;
    arr = getCheckListValues("filterCountry");
    if (arr.length > 0) o.countries = arr;
    arr = getCheckListValues("filterCost");
    if (arr.length > 0) o.cost_structures = arr;

    if (Object.keys(o).length == 0) delete obj.selected_filters;
} */

function CollectSearchbarFilters(obj) {
    // Search now matches the (pre-translated) title/description/keywords for the
    // selected language directly on the backend - no need to translate the query
    // itself into English anymore (previously done via the Google Translate widget).
    let v = getUIValue("txtSearchText");

    if (v) {
        let o = obj.searchbar_filter = {};
        o["query_string"] = v;
        o["search_description"] = true;
        o["search_title"] = true;
        o["search_keywords"] = true;
    }
}

function GetProfileItemArr(el, obj, name, singleChoise) {
    let val;
    const arr = [];

    if (singleChoise) {
        val = getUIValue(el);
        if (val) obj[name] = { "value": val, "requireExactMatch": true };

    } else {
        getSelectedValuesAsArray(el).forEach((v) => {
            arr.push({ "value": v, "requireExactMatch": true });
        });
        if (arr.length > 0) obj[name] = arr;
    }
}

function PopulateDATs() {
    const div = document.getElementById("divResult");
    const divInfo = document.getElementById("divResultInfo");
    const divMore = document.getElementById("divResultMore");

    if (currentN == 0) {
        div.innerHTML = "";
        divInfo.innerHTML = "";
        divMore.innerHTML = "";
        divInfo.appendChild(CreateTotal(cardData.length));
    }
    else
        divMore.innerHTML = "";

    let el, t, cb;
    let j = 0;
    for (let i = currentN; i < cardData.length; i++) {

        j++;
        if (j > pageSize) {
            el = CreateLoadMore();
            divMore.appendChild(el);
            break;
        }

        item = cardData[i];
        t = item.description.test_cases?.length > 0;
        cb = item.properties.source?.includes("costbenefit");
        el = CreateCard(item.description.ID, item.description.name, getObjPropVal(item.filterable_properties, "agricultural_sectors", "", maxItems), getObjPropVal(item.filterable_properties, "functionalities", "", maxItems), getObjPropVal(item.filterable_properties, "benefits", "", maxItems), item.explanation, t, cb);
        div.appendChild(el);

    }

    currentN += --j;
}

function CreateCard(id, label, sector, functionality, benefits, explanation, isTested, isCostBenefit) {
    const card = document.createElement("div");
    const isTestedIcon = isTested ? '<img src="assets/img/tested.png" style="position:absolute; right:0px; top:0px;" title="This DATS has been evaluated by the QuantiFarm assessment framework">' : '';
    const isCostBenefitIcon = isCostBenefit ? '<i class="bi bi-calculator-fill text-primary" style="font-size: 32px; font-weight: normal; position:absolute; right:3px; top:0px;" title="This DATS is available for further analysis by the Cost and Benefit Calculators"></i>' : '';
    const me = isCostBenefit || isTested ? 'me-4' : '';
    card.classList.add("col");

    if(isCostBenefit && isTested) console.log(id);

    card.innerHTML = `
<div class="card mb-0 h-100">
    <div class="card-body" style="position: relative;">
        ${isTestedIcon}
        ${isCostBenefitIcon}
        <h5 class="card-title ${me}"><a href="#" onclick="return LoadDATDetals('${escHtml(String(id).replace(/['\\]/g, ""))}');"><i class="bi bi-gear fa-lg me-2"></i>${escHtml(label)}</a></h5>
        <p>
            <i class="bi bi-caret-right-fill me-1"></i><b>Agricultural Sector</b><br>
            <small>${escHtml(sector)}</small>
        </p>
        <p>
            <i class="bi bi-caret-right-fill me-1"></i><b>Functionality</b><br>
            <small>${escHtml(functionality)}</small>
        </p>
        <p>
            <i class="bi bi-caret-right-fill me-1"></i><b>Benefits</b><br>
            <small>${escHtml(benefits)}</small>
        </p>
        ${explanation ? `
        <p>
            <i class="bi bi-info-circle fa-lg text-primary me-1"></i><b>This DATS is listed because:</b><br>
            <span class="fst-italic">${escHtml(explanation)}</span>
        </p>
        ` : ''}
    </div>
</div>
`;

    return card;
}

function CreateLoadMore() {
    const el = document.createElement("div");

    el.innerHTML = `<div class="d-flex justify-content-center" id="buttonLoadMore">
 <button type="button" class="btn btn-primary rounded-pill" onclick="PopulateDATs()">
 <i class="bi bi-arrow-down me-3"></i>Load more<i class="bi bi-arrow-down ms-3"></i></button>
 </div>`;

    return el;
}

function CreateTotal(n) {
    const el = document.createElement("div");

    el.innerHTML = `<div class="d-flex justify-content-left">${formatDatsFound(n)}
 </div>`;

    return el;
}

function OnKeyPressSearch(event) {
    if (event.key === "Enter") Recommend();
}

function OnProfile(profile) {
    const v = sustPref[profile];
    if (!v) return;
    
    setUIValue("rangeEconomic", v.economic);
    setUIValue("rangeSocial", v.social);
    setUIValue("rangeEcological", v.ecological);
}

function OnRangeChange(event) {
    console.log(event.target.value);
    document.getElementById("radioProfile6").checked = true;
}

function ClearFilters() {

    document.getElementById("divFilters").querySelectorAll("input[type='checkbox']").forEach((el) => {
        el.checked = false;
    });

    return false;
}

