//Common constants
const baseURL = (new RegExp(/^.*\//)).exec(window.location.href)[0] + "php/";

// Escapes a string for safe insertion into HTML (prevents XSS from data-derived values)
function escHtml(v) {
    if (v === null || v === undefined) return "";
    return String(v)
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#39;");
}

// Returns the URL if it is a safe http(s) link, otherwise an empty string
function safeUrl(v) {
    if (!v) return "";
    const s = String(v).trim();
    return /^https?:\/\//i.test(s) ? s : "";
}


const role_fa = "fa";
const role_ad = "ad";
const role_pm = "pm";
const role_xx = "xx";

const key_role = "role";
const key_usr = "usr";
const sep_MultiSelect = "; ";

const toolsMetaData = [
    {
        "key": "tool1",
        "icon": "bi bi-list-stars",
        "roles": [role_xx, role_fa, role_ad]
    },
    {
        "key": "tool2",
        "icon": "bi bi-calculator-fill",
        "roles": [role_xx, role_fa, role_ad]
    },
    // Benchmarking Tool (tool3) temporarily hidden - customer may reactivate
    // {
    //     "key": "tool3",
    //     "icon": "ri-bar-chart-horizontal-fill",
    //     "roles": [role_xx, role_fa, role_ad]
    // },
    // DATS Assessment Engine (tool4) temporarily hidden - customer may reactivate
    // {
    //    "key": "tool4",
    //    "icon": "bi bi-ui-checks",
    //    "roles": [role_xx, role_ad, role_pm]
    // },
    // Advanced Decision Support Tool (tool5) temporarily hidden - customer may reactivate
    // {
    //     "key": "tool5",
    //     "icon": "ri-flow-chart",
    //     "roles": [role_xx, role_ad]
    // },

]

//multilanguage functions
//
const do_lang_translation = false; 
const lang_key = "qf-lang-key";  
const qf_lang_storage_key = 'qf-lang';
 
if (do_lang_translation) {
    document.addEventListener("DOMContentLoaded", () => {
        document
            .querySelectorAll("[" + lang_key + "]")
            .forEach(translateElement);
    });
}

document.addEventListener("DOMContentLoaded", () => {
    let savedLng = localStorage.getItem(qf_lang_storage_key);
    if (!savedLng) {
        const browserLang = (navigator.language || navigator.userLanguage || '').substring(0, 2).toUpperCase();
        savedLng = ['DE', 'FR', 'IT'].includes(browserLang) ? browserLang : 'EN';
        localStorage.setItem(qf_lang_storage_key, savedLng);
    }
    if (savedLng !== 'EN') {
        setLanguage(savedLng);
    } else {
        // EN has no option in the Swiss dropdown – show DE as default
        const toggle = document.getElementById('lngDropdown');
        if (toggle) toggle.textContent = 'DE';
    }
});

function setLanguage(lng) {
    localStorage.setItem(qf_lang_storage_key, lng);
    const btn = document.getElementById('lngBtn' + lng);
    if (btn) btn.click();
    const toggle = document.getElementById('lngDropdown');
    if (toggle) toggle.textContent = lng;

    // Each step runs independently - one failing step (e.g. a page not having a
    // given element) must not stop the others (e.g. the tool1.html Recommend()
    // refresh below) from running.
    const steps = [
        () => triggerGoogleTranslate(lng),
        () => translateNavbar(lng),
        () => translateModalButtons(lng),
        () => translateSidebar(lng),
        () => translateCostBenefit(lng),
        () => translateRecommend(lng),
        () => translateProfileMultiSelect(lng),
        () => translateResults(lng),
        () => translateTcreport(lng),
        () => translateDatsManagement(lng),
        // tool1.html: DAT titles/descriptions/etc. come translated from the
        // backend, so already-shown results must be re-fetched (not just
        // re-rendered) to reflect the new language. Only re-fetch if a
        // recommendation has actually been made.
        () => {
            if (typeof Recommend === 'function' && typeof cardData !== 'undefined' && cardData && cardData.length > 0) {
                Recommend();
            }
        }
    ];
    steps.forEach(step => {
        try { step(); } catch (e) { console.error('setLanguage step failed:', e); }
    });
}

function translateNavbar(lng) {
    const strings = (typeof navbarStrings !== 'undefined') ? navbarStrings[lng] || navbarStrings['EN'] : null;
    if (!strings) return;
    Object.entries(strings).forEach(([id, text]) => {
        document.querySelectorAll('#' + id).forEach(el => el.textContent = text);
    });
}

// Translates the sidebar tool names (built by setSidebar() from `uistrings`, which
// only holds English text) and marks them notranslate/translate="no" so the Google
// Translate widget doesn't re-mangle them afterwards (e.g. it translated "Cost and
// Benefit Calculators" as "...d'avantages" instead of the correct "...bénéfices").
function translateSidebar(lng) {
    const strings = (typeof toolStrings !== 'undefined') ? toolStrings[lng] : null;
    if (!strings) return;
    Object.entries(strings).forEach(([key, text]) => {
        document.querySelectorAll(`#sidebar-nav a[href="${key}.html"] span`).forEach(el => {
            el.textContent = text;
            el.classList.add('notranslate');
            el.setAttribute('translate', 'no');
        });
    });
}

// Translates generic Bootstrap modal "Close" buttons (icon + text) and marks them
// notranslate/translate="no" so the Google Translate widget doesn't re-mangle them
// afterwards (known bug: mistranslates "Close" the verb as "Vicino"/"near" in Italian).
function translateModalButtons(lng) {
    const strings = (typeof commonStrings !== 'undefined') ? commonStrings[lng] || commonStrings['EN'] : null;
    if (!strings) return;
    document.querySelectorAll('button.btn-close[data-bs-dismiss="modal"]').forEach(el => {
        el.setAttribute('aria-label', strings.close);
        el.classList.add('notranslate');
        el.setAttribute('translate', 'no');
    });
    document.querySelectorAll('.modal-footer button[data-bs-dismiss="modal"]').forEach(el => {
        el.textContent = strings.close;
        el.classList.add('notranslate');
        el.setAttribute('translate', 'no');
    });
}

// Caches each text node's/element's ORIGINAL English content the first time it's
// seen, so repeated calls (DE->FR->IT etc.) always translate from the true source
// text instead of whatever language is currently displayed (which wouldn't match
// any dictionary key once already translated once).
const originalTextCache = new WeakMap();

function getOriginalText(node, currentText) {
    if (!originalTextCache.has(node)) originalTextCache.set(node, currentText);
    return originalTextCache.get(node);
}

// Replaces text nodes / placeholder attributes within `root` whose whitespace-
// normalized content exactly matches a key in `dict`. Preserves each text node's
// original leading/trailing whitespace so mixed icon+text markup stays intact, and
// works for wrapped/multi-line HTML source (indentation/newlines get normalized
// away before the lookup).
function applyStringDict(root, dict) {
    if (!root || !dict) return;
    const walker = document.createTreeWalker(root, NodeFilter.SHOW_TEXT);
    const textNodes = [];
    let node;
    while ((node = walker.nextNode())) textNodes.push(node);
    textNodes.forEach(n => {
        const raw = getOriginalText(n, n.textContent);
        const key = raw.replace(/\s+/g, ' ').trim();
        if (key && dict[key]) {
            const leading = raw.match(/^\s*/)[0];
            const trailing = raw.match(/\s*$/)[0];
            n.textContent = leading + dict[key] + trailing;
        }
    });
    root.querySelectorAll('[placeholder]').forEach(el => {
        const orig = getOriginalText(el, el.getAttribute('placeholder'));
        const key = orig.replace(/\s+/g, ' ').trim();
        if (dict[key]) el.setAttribute('placeholder', dict[key]);
    });
}

// Translates the Cost & Benefit Calculators page (tool2.html): headers, labels,
// placeholders, dropdown options, and result description cells (some contain
// literal <br> tags for multi-line text). Matched by exact original English text
// against `costBenefitStrings`, so a single dictionary entry covers a label wherever
// it repeats (button, header, placeholder, etc.) without needing per-element IDs.
// Scoped to #main and marked notranslate/translate="no" once translated so the
// Google Translate widget doesn't re-mangle the (already correct) DeepL output.
function translateCostBenefit(lng) {
    // #btnTabcrop only exists on tool2.html - guard so #main isn't marked
    // notranslate (blocking Google) on other pages that don't have this content
    // (note: #tab1Content id is reused by tool1.html, so it can't be used here).
    if (!document.getElementById('btnTabcrop')) return;
    const strings = (typeof costBenefitStrings !== 'undefined') ? costBenefitStrings[lng] : null;
    const root = document.getElementById('main');
    if (!strings || !root) return;

    applyStringDict(root, strings);

    // Result description cells: some contain literal <br> tags spanning multiple
    // text nodes, so they aren't matched by the text-node pass above. Some source
    // keys have a trailing space (e.g. "...equipment) "), which el.innerHTML.trim()
    // would strip - so look up against trimmed keys, not the raw dict.
    const trimmedStrings = {};
    Object.keys(strings).forEach(k => { trimmedStrings[k.trim()] = strings[k]; });
    root.querySelectorAll('td').forEach(el => {
        const orig = getOriginalText(el, el.innerHTML).trim();
        if (trimmedStrings[orig]) el.innerHTML = trimmedStrings[orig];
    });

    root.classList.add('notranslate');
    root.setAttribute('translate', 'no');
}

// Translates tool1.html: the page title, the "Recommendations"/"Description" nav-tab
// buttons, and the "Recommendations" tab's Farmer Profile Information accordion +
// left filter sidebar headers. See translateCostBenefit() above for the matching
// approach; gated on #tabResult, which only exists on tool1.html, but applied to
// #main so the page title/tab buttons (siblings of #tabResult) are covered too.
function translateRecommend(lng) {
    if (!document.getElementById('tabResult')) return;
    const strings = (typeof recommendStrings !== 'undefined') ? recommendStrings[lng] : null;
    const root = document.getElementById('main');
    if (!strings || !root) return;

    applyStringDict(root, strings);

    root.classList.add('notranslate');
    root.setAttribute('translate', 'no');
}

// Translates the visible text of <option> elements in a <select> by looking up each
// option's `value` (kept in English) via translateCountry() - used for results.html's
// dynamically-populated #cboCountry, whose options aren't in resultsStrings since
// they're built at runtime, not present in the static HTML.
function translateCountryOptions(elId) {
    document.querySelectorAll(`#${elId} option`).forEach(opt => {
        if (opt.value) opt.textContent = translateCountry(opt.value);
    });
}

// Translates results.html: the intro heading/paragraphs (paragraphs contain inline
// <a> links, so matched/replaced via innerHTML like costBenefitStrings' <td> cells),
// filter labels/options, table headers, and the dynamically-populated country filter.
// Gated on #cboSector, which only exists on results.html.
function translateResults(lng) {
    if (!document.getElementById('cboSector')) return;
    const strings = (typeof resultsStrings !== 'undefined') ? resultsStrings[lng] : null;
    const root = document.querySelector('main');
    if (!strings || !root) return;

    applyStringDict(root, strings);

    const trimmedStrings = {};
    Object.keys(strings).forEach(k => { trimmedStrings[k.trim()] = strings[k]; });
    root.querySelectorAll('p').forEach(el => {
        const orig = getOriginalText(el, el.innerHTML).trim();
        if (trimmedStrings[orig]) el.innerHTML = trimmedStrings[orig];
    });

    translateCountryOptions('cboCountry');

    // The results table's Sector/Country cells are translated at render time
    // (see PopulateTable() in results.js) - re-render so already-shown rows
    // reflect the new language instead of staying in whatever language they
    // were last built in.
    if (typeof LoadData === 'function') LoadData();

    root.classList.add('notranslate');
    root.setAttribute('translate', 'no');
}

// Translates datsmanagement.html: form labels, buttons, and history table headers.
// Gated on #fTranslationStatus, which only exists on datsmanagement.html.
function translateDatsManagement(lng) {
    if (!document.getElementById('fTranslationStatus')) return;
    const language = (lng || 'EN').toUpperCase();
    const strings = (typeof datsManagementStrings !== 'undefined') ? datsManagementStrings[language] : null;
    const root = document.getElementById('main');
    if (!strings || !root) return;

    applyStringDict(root, strings);

    root.classList.add('notranslate');
    root.setAttribute('translate', 'no');
}

// Translates tcreport.html: labels, tab names, and headings repeated across the
// 2023/2024/2025/3-year tabs (a single dictionary entry covers every occurrence).
// Gated on #tcTitle, which only exists on tcreport.html.
function translateTcreport(lng) {
    if (!document.getElementById('tcTitle')) return;
    const strings = (typeof tcreportStrings !== 'undefined') ? tcreportStrings[lng] : null;
    const root = document.querySelector('main');
    if (!strings || !root) return;

    applyStringDict(root, strings);

    // Re-translate dynamic header fields (crop/livestock) that are set once at
    // page load from testCaseData and not covered by tcreportStrings.
    if (typeof tcObject !== 'undefined' && typeof translateCrop === 'function') {
        const cropEl = document.getElementById('tcCrop');
        if (cropEl) cropEl.innerHTML = translateCrop(tcObject.crop);
    }

    root.classList.add('notranslate');
    root.setAttribute('translate', 'no');

    // Reload impact data with new language (LoadData destroys & recreates charts
    // with correct language labels before the API call)
    if (typeof LoadData !== 'undefined') {
        LoadData();
    }
}

// Translates the option labels of tool1.html's farmer-profile multiselect dropdowns
// (farmFarmType/farmFunctionality/farmBenefit/farmTechnology), populated by
// PopulateMultiSelect() from the /profile_entries/ endpoint. Only the visible label
// text is changed - the checkbox's `value` attribute stays the English category key
// used for filtering/backend calls.
const PROFILE_MULTISELECT_CATEGORIES = {
    farmFarmType: 'farm_type',
    farmFunctionality: 'functionalities',
    farmBenefit: 'benefits',
    farmTechnology: 'digital_forms'
};

function translateProfileMultiSelect(lng) {
    if (typeof profileEntryStrings === 'undefined') return;
    Object.entries(PROFILE_MULTISELECT_CATEGORIES).forEach(([elId, category]) => {
        const ul = document.querySelector(`#${elId} ~ ul`);
        if (!ul) return;
        ul.querySelectorAll('label.dropdown-item').forEach(label => {
            const input = label.querySelector('input[type="checkbox"]');
            if (!input) return;
            const dict = profileEntryStrings[category] && profileEntryStrings[category][lng];
            const textNode = Array.from(label.childNodes).find(n => n.nodeType === Node.TEXT_NODE);
            if (textNode) textNode.textContent = (dict && dict[input.value]) || input.value;
        });
    });
}

// Trigger the hidden Google Translate widget (present only on tool1 and tool2).
// Retries up to 20 times (every 500 ms) to wait for widget initialisation.
function triggerGoogleTranslate(lng, retryCount) {
    if (!document.getElementById('google_translate_element')) return;

    const langMap = { 'EN': '', 'DE': 'de', 'FR': 'fr', 'IT': 'it' };
    const gtLang = langMap[lng];
    if (gtLang === undefined) return;

    const selectEl = document.querySelector('.goog-te-combo');
    if (!selectEl) {
        const count = retryCount || 0;
        if (count < 20) setTimeout(() => triggerGoogleTranslate(lng, count + 1), 500);
        return;
    }

    if (gtLang === '') {
        // Restore to original English: try the "Show original" link in the GT banner iframe
        const iframes = document.querySelectorAll('.goog-te-banner-frame, .skiptranslate iframe');
        for (const iframe of iframes) {
            try {
                const inner = iframe.contentDocument || iframe.contentWindow.document;
                const anchors = inner.querySelectorAll('a');
                for (const a of anchors) {
                    if (/original/i.test(a.textContent)) { a.click(); return; }
                }
            } catch (e) { /* cross-origin guard */ }
        }
        // Fallback: clear combo selection (bubbles required for GT event delegation)
        selectEl.value = '';
        selectEl.dispatchEvent(new Event('change', { bubbles: true }));
    } else {
        selectEl.value = gtLang;
        selectEl.dispatchEvent(new Event('change', { bubbles: true }));
    }
}

SetLoggedUser();

function translateElement(element) {
    const key = element.getAttribute(lang_key);
    const str = uistrings[key];

    if (str != null) {
        if (element.nodeName.toLowerCase() == "input")
            element.setAttribute("placeholder", str);
        else if (element.nodeName.toLowerCase() == "label" && element.classList.contains("dropdown-item")) //<label class="dropdown-item"> �� multiple selection dropdown
            element.childNodes[1].nodeValue = str;
        else
            element.innerText = str;
    }
}

//UI navigation functions
//
function setSidebar(x) {

    let role = localStorage.getItem(key_role);
    if (role == null) role = role_fa;

    let s = ``;

    toolsMetaData.forEach((t) => {
        if (t.roles.includes(role))
            s += `            
<li class="nav-item">
    <a class="nav-link ${(x == t.key ? "" : "collapsed")}" href="${t.key}.html">
        <i class="${t.icon}" style="font-size: 32px; font-weight: normal"></i>
        <span>${uistrings[t.key]}</span>
    </a>
</li>
`;
    });

    document.getElementById("sidebar-nav").innerHTML = s;
}

// Data language for the backend; null = original (EN) data.
function getDataLanguage() {
    const lng = localStorage.getItem(qf_lang_storage_key);
    return lng && lng !== 'EN' ? lng.toLowerCase() : null;
}

// Appends "DAT Management" (admins) / "Admin Users" (super-admin only) links below the
// regular tool list. Not role-based like toolsMetaData - driven purely by the isadmin /
// issuperadmin flags returned by php/api.php?c=usr, which are never client-assignable.
function addAdminSidebarLinks(data) {
    const nav = document.getElementById("sidebar-nav");
    if (!nav || !data || !data.loggedin) return;

    // SetLoggedUser() can run more than once per page load; drop any links added earlier
    nav.querySelectorAll('[data-admin-link]').forEach((el) => el.remove());

    let s = ``;

    if (data.isadmin) {
        s += `
<li class="nav-item" data-admin-link>
    <a class="nav-link collapsed" href="datsmanagement.html">
        <i class="bi bi-database-fill-gear" style="font-size: 32px; font-weight: normal"></i>
        <span>DAT Management</span>
    </a>
</li>
`;
    }

    if (data.issuperadmin) {
        s += `
<li class="nav-item" data-admin-link>
    <a class="nav-link collapsed" href="admin-users.html">
        <i class="bi bi-person-fill-gear" style="font-size: 32px; font-weight: normal"></i>
        <span>Admin Users</span>
    </a>
</li>
`;
    }

    if (s !== ``) nav.insertAdjacentHTML('beforeend', s);
}

function gotoTool(role, tool) {
    localStorage.setItem(key_role, role);

    let url;
    if (tool === undefined)
        url = toolsMetaData.find(t => t.roles.includes(role)).key;
    else
        url = tool;

    url += ".html";

    window.location.href = url;
}

function SetLoggedUser(func) {
    const n1 = document.getElementById('mnuLogin');
    const n2 = document.getElementById('mnuUser');
    const n3 = document.getElementById('mnuUserName');
    const n4 = document.getElementById('mnuLogin2');
    const n5 = document.getElementById('mnuLogout2');
    const n6 = document.getElementById('mnuProfile2');

    if (!n1 || !n2 || !n3) return;

    fetch('php/api.php?c=usr', { method: 'GET', mode: 'cors'})
        .then(function (response) {
            if (response.ok)
                return response.json();
            else
                return response.text()
        })
        .then(function (data) {
            localStorage.setItem(key_usr, JSON.stringify(data));

            if (data.loggedin) {
                n1.hidden = true;
                n2.hidden = false;
                n3.innerHTML = data.user;
                if (n4) n4.hidden = true;
                if (n5) n5.hidden = false;
                if (n6) n6.hidden = false;
            }
            else {
                n1.hidden = false;
                n2.hidden = true;
                if (n4) n4.hidden = false;
                if (n5) n5.hidden = true;
                if (n6) n6.hidden = true;
            }

            addAdminSidebarLinks(data);

            if (func instanceof Function) func();
        })
        .catch(function (error) {
            console.log(error);
        })
        .finally(function () {
            ;
        });
}

//multiple selection dropdown
//
function handleMultiSelectDropdownCB(event) {
    const cb = event.target;
    const dd = cb.closest('div').querySelector('input');

    if (dd.qfSelectedItemsAsArray === undefined) dd.qfSelectedItemsAsArray = [];
    if (dd.qfSelectedValuesAsArray === undefined) dd.qfSelectedValuesAsArray = [];

    if (cb.checked) {
        dd.qfSelectedItemsAsArray.push(cb.parentElement.innerText);
        dd.qfSelectedValuesAsArray.push(cb.value);
        cb.parentElement.style.fontWeight = "bold";
    } else {
        dd.qfSelectedItemsAsArray = dd.qfSelectedItemsAsArray.filter((item) => item !== cb.parentElement.innerText);
        dd.qfSelectedValuesAsArray = dd.qfSelectedValuesAsArray.filter((item) => item !== cb.value);
        cb.parentElement.style.fontWeight = "normal";
    }

    dd.value = dd.qfSelectedItemsAsArray.length > 0 ? dd.qfSelectedItemsAsArray.join(sep_MultiSelect) : '';
}

//common functions
//
function showErr(node, err) {
    console.log('Error:', err.message);

    const n = document.getElementById(node);
    n.innerHTML = "";
    const e = document.createElement("div");
    n.appendChild(e);

    e.outerHTML = `<div class="alert alert-warning alert-dismissible fade show" role="alert">
<i class="bi bi-exclamation-octagon me-1"></i>
[${err.name}] ${err.message}
<button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button></div>`;

}

function showInfo(node, txt) {
    const n = document.getElementById(node);

    n.innerHTML = `<div class="alert alert-info alert-dismissible fade show" role="alert">
<i class="bi bi-info-square me-2"></i>${txt}
<button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button></div>`;
}

function showSpinner(node) {
    const n = document.getElementById(node);
    n.innerHTML = `<div class="d-flex justify-content-center">
    <div class="spinner-border text-primary me-3" role="status"></div>Loading...
</div>`;
}

function setButtonState(node, busy) {
    const n = document.getElementById(node);
    if (n == null) return;

    n.disabled = busy;

    if (busy) {
        const s = document.createElement("span");
        n.appendChild(s);
        s.outerHTML = `<span> ... </span><span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>`;
    }
    else {
        n.removeChild(n.lastElementChild);
        n.removeChild(n.lastElementChild);
    }
}

function getObjPropVal(obj, prop1, prop2 = "", maxElements = 0) {
    let v = "", s = "";
    const sep = "; ";

    if (Array.isArray(obj)) {
        v = [];
        obj.forEach((o) => { v.push(getObjPropVal(o, prop1, prop2)); });
    }
    else if (prop1 in obj) {
        if (prop2 != "" && prop2 in obj[prop1])
            v = obj[prop1][prop2];
        else
            v = obj[prop1];
    }

    if (Array.isArray(v)) {
        if (maxElements > 0 && v.length > maxElements) s = sep + `<span class="ms-1 text-black-50 fst-italicX">(+${v.length - maxElements})</span>`;
        if (maxElements > 0) v = v.slice(0, maxElements);
        v = v.join(sep) + s;    
    }

    return v;
}

function getSelectedText(selectID) {
    const el = document.getElementById(selectID);
    let t = "";

    if (el.selectedIndex >= 0)
        t = el.options[el.selectedIndex].text;

    return t;
}

function getSelectedItemsAsArray(selectID) {
    const el = document.getElementById(selectID);

    if (el.qfSelectedItemsAsArray === undefined)
        return [];
    else
        return el.qfSelectedItemsAsArray;
}

function getSelectedValuesAsArray(selectID) {
    const el = document.getElementById(selectID);

    if (el.qfSelectedValuesAsArray === undefined)
        return [];
    else
        return el.qfSelectedValuesAsArray;
}

function getUIValue(ctrl) {
//input type = "number" or "range"
//input type = "text"
//input type = "date"
//input type = "time"
//textarea
//select
//multi select: <input type="text" data-bs-toggle="dropdown"> ...

    const el = (ctrl instanceof Object) ? ctrl : document.getElementById(ctrl);
    const n = el.nodeName.toLowerCase(); 
    let v;

    if (n === "input") {
        if (el.getAttribute("data-bs-toggle") === "dropdown") {
            if (el.qfSelectedValuesAsArray)
                v = el.qfSelectedValuesAsArray.length > 0 ? el.qfSelectedValuesAsArray.join(',') : '';
        }
        else if (el.type === "number" || el.type === "range") {
            v = parseFloat(el.value);
            if (isNaN(v)) v = null;
        }
        else
            v = el.value;
    }
    else if (n === "textarea") {
        v = el.value;
    }
    else if (n === "select") {
        v = el.value;
    }
    else 
        ;

    return v;
}

function setUIValue(ctrl, v) {
    const el = (ctrl instanceof Object) ? ctrl : document.getElementById(ctrl);
    if (!el) return;

    const n = el.nodeName.toLowerCase(); 
    v = ifNull(v);

    if (n === "input") {
        if (el.getAttribute("data-bs-toggle") === "dropdown") {
            const values = v.split(sep_MultiSelect);
            const chk = Array.from(document.querySelector(`#${ctrl} ~ ul`).getElementsByTagName('input'));

            chk.forEach((item) => {
                const b = values.includes(item.value);
                const f = item.checked != b;
                item.checked = b;
                if (f) item.dispatchEvent(new Event('change', { bubbles: true }));
            });
        }
        else
            el.value = v;
    }
    else if (n === "textarea") {
        el.value = v;
    }
    else if (n === "select") {
        el.value = v;
    }
    else if (n === "td") {
        el.innerHTML = v;
    }
    else 
        ;

}

function getCheckListValues(ctrl) {
    const el = document.getElementById(ctrl);
    const chk = Array.from(el.getElementsByTagName('input'));
    const arr = [];

    chk.forEach((item) => {
        if (item.checked)
            arr.push(item.value); //arr.push(item.nextElementSibling.innerHTML);
        });

    return arr;
}

function setDisabled(el, v) {

    document.getElementById(el).querySelectorAll("input, button").forEach((e) => { e.disabled = v; });

}

function PostgisCoord(text) {
    // regular expression to match groups enclosed in parentheses
    const regex = /\(([^)]+)\)/g;

    const groups = [...text.matchAll(regex)];

    // extract pairs of numbers from each matched group
    const pairList = groups.map(group => {
        const groupText = group[1]; 
        const groupPairs = groupText.match(/[-+]?\d*\.?\d+(?:[eE][-+]?\d+)?/g);

        // extract pairs from the list (assuming even number of elements)
        const pairGroup = [];
        for (let i = 0; i < groupPairs.length; i += 2) {
            pairGroup.push([Number(groupPairs[i + 1]), Number(groupPairs[i])]);
        }
        return pairGroup;
    });

    return pairList;
}

function CoordPostgis(coord) {
    let s = "";

    coord.forEach((p) => { s += p.lng + " " + p.lat + "," });

    if (s) s = "POLYGON((" + s + coord[0].lng + " " + coord[0].lat + "))"; //add first point at the end

    return s;
}

function DateHM(d) {
    return ifNull(d).trim().substring(0, 16).replace("T", " ");
}

function FormatNumber2String(v) {
    //12 345.123
    return new Intl.NumberFormat('en-US', {
        minimumFractionDigits: 0,
        maximumFractionDigits: 5
      }).format(Number(v)).replace(/,/g, ' ');

    //depending on the locale
    //return Number(v).toLocaleString();
}

function ifNull(v, n = "") {
    if (v === 0)
        return 0;
    else
        return v || n;
}

function ifEmpty(v, n = null) {
    if (v === 0)
        return 0;
    else
        return v ? v : n;
}

function CloneObject(o) {
    return JSON.parse(JSON.stringify(o));
}

function IsObjectEmpty(o) {
    return !o || (Object.keys(o).length === 0)
}

function FindByProp(data, findName, findValue, returnName) {

    const n = data.findIndex((item) => {
        return item[findName] == findValue;
    });

    if (n >= 0)
        return data[n][returnName];
    else
        return "";
}

function FindIndexByProp(data, findName, findValue) {

    const n = data.findIndex((item) => {
        return item[findName] == findValue;
    });

    return n;
}

function JoinProp(data, propName, sep) {

    if (!sep) sep = ',';

    return data.map((item) => [item[propName]]).join(sep);
}

function GetObjectFirstKeyName(obj, l) {
    let o = obj;

    for (let i = 0; i < l; i++) {
        o = o[Object.keys(o)[0]];
    }

    if (Array.isArray(o))
        return o[0];
    else
        return Object.keys(o)[0];
}

function PopulateSelect(el, data, propText, propValue, emptyItem) {
    const e = document.getElementById(el);
    let html = "";

    if (emptyItem) html = "<option></option>";      //<option selected="" disabled="" value=""></option>
    data.forEach((item) => {
        if (propValue)
            html += `<option value="${item[propValue]}">${item[propText].substring(0, 100).trim()}</option>`;
        else if (propText)
            html += `<option>${item[propText]}</option>`;
        else
            html += `<option value="${item}">${item.substring(0, 100).trim()}</option>`;
            
    });

    e.innerHTML = html;
}

function PopulateMultiSelect(el, data, propText, propValue) {
    setUIValue(el, "");
    const e = document.querySelector(`#${el} ~ ul`);
    let html = "";

    data.forEach((item) => {
        let v, t;

        if (propValue) {
            v = item[propValue];
            t = item[propText];
        } else if (propText) {
            v = item[propText];
            t = item[propText];
        } else {
            v = item;
            t = item;
        }

        html += `<li><label class="dropdown-item"><input type="checkbox" class="me-2 qf-scale-14" value="${v}">${t.substring(0, 100).trim()}</label></li>`;
    });

    e.innerHTML = html;
}

function PopulateGroupedMultiSelect(el, groups) {
    setUIValue(el, "");
    const e = document.querySelector(`#${el} ~ ul`);
    let html = "";

    Object.entries(groups || {}).forEach(([group, items]) => {
        html += `<li><span class="dropdown-header text-start">${group}</span></li>`;
        items.forEach((item) => {
            html += `<li><label class="dropdown-item ps-4"><input type="checkbox" class="me-2 qf-scale-14" value="${item}">${item.substring(0, 100).trim()}</label></li>`;
        });
    });

    e.innerHTML = html;
}

function PopulateCheckList(el, data, propText, propAdd, maxFirst = 5, nonZero = true) {
    const e = document.getElementById(el);
    let html = "";
    let add = "";
    let chk = "";
    let i = 0;

    data.forEach((item) => {
        if (nonZero && !item.checked && propAdd && item[propAdd] == 0)
            return;

        if (i == maxFirst) {
            html += `<div class="text-primary mt-1" onclick="ToggleViewMore(event)" data-bs-toggle="collapse" href="#collapse${el}" aria-expanded="false" role="button" aria-controls="collapse${el}">
<i class="bi bi-caret-down-fill me-1"></i><span>View more</span>
<i class="bi bi-caret-up-fill me-1" hidden></i><span hidden>View less</span>
</div>`;
            html += `<div class="collapse mb-2 mt-1" id="collapse${el}">`;
        }

        chk = (item.checked) ? "checked" : "";

        if (propAdd)
            add = `<span class="ms-2 text-black-50">(${item[propAdd]})</span>`;

        html += `<label class="qf-cursor-pointer"><input type="checkbox" class="me-2 qf-cursor-pointer" ${chk} value="${item[propText]}"><span>${item[propText]}</span>${add}</label><br>`;
        i++;
    });

    if (i === 0)
        html = `<span class="fst-italic ms-3 text-black-50">(no items)</span>`;

    if (i >= maxFirst)
        html += `</div>`;

    e.innerHTML = html;
}

function ToggleViewMore(event) {
    const el = event.target.getAttribute("data-bs-toggle") === "collapse" ? event.target : event.target.parentElement;

    for (let i = 0; i < el.children.length; i++) {
        el.children[i].hidden = !el.children[i].hidden;
    }
}

function CloseModal(id) {
    const m = bootstrap.Modal.getInstance(document.getElementById(id));
    m.hide();
}

function ShowModal(id) {
    const m = bootstrap.Modal.getOrCreateInstance(document.getElementById(id));
    m.show();
}

function ShowModalInfo(v) {
    const div = document.getElementById("divModalInfo");
    div.innerHTML = v;

    ShowModal('modalInfo');
}

function GetQueryParams() {
    return new URLSearchParams(location.search);
}

function CallAPI(url, par, funcSuccess, errContainer, startButton) {

    if (startButton != "") setButtonState(startButton, true);

    fetch(url, { method: 'POST', mode: 'cors', headers: { 'Accept': 'application/json' }, body: JSON.stringify(par) })
        .then(function (response) {
            return response.text().then(function (text) {
                if (!response.ok)
                    throw new Error(text.substring(0, 200));
                try {
                    return JSON.parse(text);
                } catch (e) {
                    throw new Error(text.substring(0, 200));
                }
            });
        })
        .then(function (data) {
            if (funcSuccess instanceof Function) funcSuccess(data);
        })
        .catch(function (error) {
            if (errContainer != "") showErr(errContainer, error);
            console.log(error);
        })
        .finally(function () {
            if (startButton != "") setButtonState(startButton, false);
        });
}

function LoadLanguageContent(lng, funcPost) {
    localStorage.setItem(qf_lang_storage_key, lng);
    let name = window.location.pathname.split('/').pop().replace(".html", "");
    if (name == "") name = "index";

    const url = "assets/lng/" + name + "-" + lng + ".html";
    const container = "lngTab" + lng;

    if (document.getElementById(container).innerHTML.trim() != "") return;

    fetch(url, { method: 'GET', cache: 'no-store' })
        .then(function (response) {
            if (response.ok)
                return response.text();
            else
                return response.statusText;
        })
        .then(function (data) {
            document.getElementById(container).innerHTML = data;
            if (funcPost instanceof Function) funcPost(lng);
        })
        .catch(function (error) {
            showErr(container, error);
            console.log(error);
        })
}

//
// const do_lang_translation = false; 
// const lang_key = "qf-lang-key";  
 
// if (do_lang_translation) {
//     document.addEventListener("DOMContentLoaded", () => {
//         document
//             .querySelectorAll("[" + lang_key + "]")
//             .forEach(translateElement);
//     });
// }
