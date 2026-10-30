const datsApiURL = baseURL + "datsmanagement.php";
const datFormFieldIds = ['fName', 'fTitle', 'fWebsite', 'fDescription', 'fKeywords', 'fSector', 'fFunctionality', 'fBenefits', 'fDelivery', 'fLanguages', 'fCost', 'fCountry', 'fLaunchYear', 'fLastUpdateYear'];

let datEditable = false;

document.addEventListener("DOMContentLoaded", setSidebar(null));
SetLoggedUser(InitDatsPage);

function InitDatsPage() {
    const user = JSON.parse(localStorage.getItem(key_usr));

    if (typeof translateDatsManagement === 'function') {
        translateDatsManagement(localStorage.getItem('qf-lang') || 'EN');
    }

    if (!user.loggedin || !user.isadmin) {
        document.getElementById('divNotAdmin').hidden = false;
        document.getElementById('divAdmin').hidden = true;
        return;
    }

    document.getElementById('divNotAdmin').hidden = true;
    document.getElementById('divAdmin').hidden = false;
    LoadBenefitOptions();
    UpdateFormLanguageMode();
    LoadDatList();
}

function PopulateGroupedMultiSelect(el, groups) {
    setUIValue(el, "");
    const e = document.querySelector(`#${el} ~ ul`);
    e.innerHTML = '';

    const groupedEntries = Array.isArray(groups)
        ? [['', groups]]
        : Object.entries(groups || {});

    groupedEntries.forEach(function (entry) {
        const group = entry[0];
        const groupItems = entry[1];
        const items = Array.isArray(groupItems) ? groupItems : Object.values(groupItems || {});
        if (group) {
            const header = document.createElement('li');
            header.innerHTML = '<span class="dropdown-header qf-benefit-group-header"></span>';
            header.querySelector('span').textContent = group;
            e.appendChild(header);
        }

        items.forEach(function (item) {
            const value = String(item);
            const row = document.createElement('li');
            const label = document.createElement('label');
            const checkbox = document.createElement('input');
            checkbox.type = 'checkbox';
            checkbox.className = 'me-2 qf-scale-14';
            checkbox.value = value;
            checkbox.addEventListener('click', function (event) {
                event.stopPropagation();
            });
            label.className = 'dropdown-item ps-4';
            label.style.display = 'block';
            label.appendChild(checkbox);
            label.appendChild(document.createTextNode(value.substring(0, 100).trim()));
            row.appendChild(label);
            e.appendChild(row);
        });
    });
}

function LoadBenefitOptions() {
    fetch(baseURL + 'tool1.php', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ path: '/profile_entries/', data: {} })
    })
        .then(function (r) { return r.json(); })
        .then(function (data) {
            PopulateGroupedMultiSelect('fBenefitsSelect', data.benefit_groups || {});
            document.querySelectorAll('#fBenefitsOptions input').forEach(function (input) {
                input.addEventListener('change', handleMultiSelectDropdownCB);
                input.addEventListener('change', UpdateBenefitsValue);
            });
            SetBenefitsValue(document.getElementById('fBenefits').value);

            PopulateGroupedMultiSelect('fSectorSelect', data.farm_type_groups || {});
            document.querySelectorAll('#fSectorOptions input').forEach(function (input) {
                input.addEventListener('change', handleMultiSelectDropdownCB);
                input.addEventListener('change', UpdateSectorValue);
            });
            SetSectorValue(document.getElementById('fSector').value);

            PopulateGroupedMultiSelect('fFunctionalitySelect', data.functionality_groups || {});
            document.querySelectorAll('#fFunctionalityOptions input').forEach(function (input) {
                input.addEventListener('change', handleMultiSelectDropdownCB);
                input.addEventListener('change', UpdateFunctionalityValue);
            });
            SetFunctionalityValue(document.getElementById('fFunctionality').value);

            PopulateGroupedMultiSelect('fCountrySelect', data.country || []);
            document.querySelectorAll('#fCountryOptions input').forEach(function (input) {
                input.addEventListener('change', handleMultiSelectDropdownCB);
                input.addEventListener('change', UpdateCountryValue);
            });
            SetCountryValue(document.getElementById('fCountry').value);

            PopulateGroupedMultiSelect('fLanguagesSelect', data.language || []);
            document.querySelectorAll('#fLanguagesOptions input').forEach(function (input) {
                input.addEventListener('change', handleMultiSelectDropdownCB);
                input.addEventListener('change', UpdateLanguagesValue);
            });
            SetLanguagesValue(document.getElementById('fLanguages').value);

            PopulateGroupedMultiSelect('fCostSelect', data.cost_structures || []);
            document.querySelectorAll('#fCostOptions input').forEach(function (input) {
                input.addEventListener('change', handleMultiSelectDropdownCB);
                input.addEventListener('change', UpdateCostValue);
            });
            SetCostValue(document.getElementById('fCost').value);

            PopulateGroupedMultiSelect('fDeliverySelect', data.digital_forms_groups || {});
            document.querySelectorAll('#fDeliveryOptions input').forEach(function (input) {
                input.addEventListener('change', handleMultiSelectDropdownCB);
                input.addEventListener('change', UpdateDeliveryValue);
            });
            SetDeliveryValue(document.getElementById('fDelivery').value);
        })
        .catch(function (e) { ShowErr(e); });
}

function UpdateBenefitsValue() {
    var values = Array.from(document.querySelectorAll('#fBenefitsOptions input:checked')).map(function (input) {
        return input.value;
    });
    document.getElementById('fBenefits').value = values.join(', ');
    setUIValue('fBenefitsSelect', values.join(sep_MultiSelect));
}

function SetBenefitsValue(value) {
    var values = (value || '').split(',').map(function (item) { return item.trim(); }).filter(Boolean);
    var select = document.getElementById('fBenefitsSelect');
    var selectedValues = [];
    var selectedItems = [];

    document.getElementById('fBenefits').value = values.join(', ');
    setUIValue('fBenefitsSelect', values.join(sep_MultiSelect));

    document.querySelectorAll('#fBenefitsOptions input').forEach(function (input) {
        input.checked = values.includes(input.value);
        input.parentElement.style.fontWeight = input.checked ? 'bold' : 'normal';
        if (input.checked) {
            selectedValues.push(input.value);
            selectedItems.push(input.parentElement.innerText);
        }
    });

    select.qfSelectedValuesAsArray = selectedValues;
    select.qfSelectedItemsAsArray = selectedItems;
    if (selectedValues.length > 0 || values.length === 0) UpdateBenefitsValue();
}

function UpdateSectorValue() {
    var values = Array.from(document.querySelectorAll('#fSectorOptions input:checked')).map(function (input) {
        return input.value;
    });
    var select = document.getElementById('fSectorSelect');
    select.qfSelectedValuesAsArray = values;
    select.qfSelectedItemsAsArray = values.slice();
    document.getElementById('fSector').value = values.join(', ');
    select.value = values.join(sep_MultiSelect);
}

function SetSectorValue(value) {
    var values = (value || '').split(',').map(function (item) { return item.trim(); }).filter(Boolean);
    var select = document.getElementById('fSectorSelect');
    var selectedValues = [];
    var selectedItems = [];

    document.querySelectorAll('#fSectorOptions input').forEach(function (input) {
        input.checked = values.includes(input.value);
        input.parentElement.style.fontWeight = input.checked ? 'bold' : 'normal';
        if (input.checked) {
            selectedValues.push(input.value);
            selectedItems.push(input.parentElement.innerText);
        }
    });

    select.qfSelectedValuesAsArray = selectedValues;
    select.qfSelectedItemsAsArray = selectedItems;
    document.getElementById('fSector').value = values.join(', ');
    select.value = selectedItems.join(sep_MultiSelect);
}

function UpdateFunctionalityValue() {
    var values = Array.from(document.querySelectorAll('#fFunctionalityOptions input:checked')).map(function (input) {
        return input.value;
    });
    var select = document.getElementById('fFunctionalitySelect');
    select.qfSelectedValuesAsArray = values;
    select.qfSelectedItemsAsArray = values.slice();
    document.getElementById('fFunctionality').value = values.join(', ');
    select.value = values.join(sep_MultiSelect);
}

function SetFunctionalityValue(value) {
    var values = (value || '').split(',').map(function (item) { return item.trim(); }).filter(Boolean);
    var select = document.getElementById('fFunctionalitySelect');
    var selectedValues = [];
    var selectedItems = [];

    document.querySelectorAll('#fFunctionalityOptions input').forEach(function (input) {
        input.checked = values.includes(input.value);
        input.parentElement.style.fontWeight = input.checked ? 'bold' : 'normal';
        if (input.checked) {
            selectedValues.push(input.value);
            selectedItems.push(input.parentElement.innerText);
        }
    });

    select.qfSelectedValuesAsArray = selectedValues;
    select.qfSelectedItemsAsArray = selectedItems;
    document.getElementById('fFunctionality').value = values.join(', ');
    select.value = selectedItems.join(sep_MultiSelect);
}

function UpdateCountryValue() {
    var values = Array.from(document.querySelectorAll('#fCountryOptions input:checked')).map(function (input) {
        return input.value;
    });
    var select = document.getElementById('fCountrySelect');
    select.qfSelectedValuesAsArray = values;
    select.qfSelectedItemsAsArray = values.slice();
    document.getElementById('fCountry').value = values.join(', ');
    select.value = values.join(sep_MultiSelect);
}

function SetCountryValue(value) {
    var values = (value || '').split(',').map(function (item) { return item.trim(); }).filter(Boolean);
    var select = document.getElementById('fCountrySelect');
    var selectedValues = [];
    var selectedItems = [];

    document.querySelectorAll('#fCountryOptions input').forEach(function (input) {
        input.checked = values.includes(input.value);
        input.parentElement.style.fontWeight = input.checked ? 'bold' : 'normal';
        if (input.checked) {
            selectedValues.push(input.value);
            selectedItems.push(input.parentElement.innerText);
        }
    });

    select.qfSelectedValuesAsArray = selectedValues;
    select.qfSelectedItemsAsArray = selectedItems;
    document.getElementById('fCountry').value = values.join(', ');
    select.value = selectedItems.join(sep_MultiSelect);
}

function UpdateLanguagesValue() {
    var values = Array.from(document.querySelectorAll('#fLanguagesOptions input:checked')).map(function (input) {
        return input.value;
    });
    var select = document.getElementById('fLanguagesSelect');
    select.qfSelectedValuesAsArray = values;
    select.qfSelectedItemsAsArray = values.slice();
    document.getElementById('fLanguages').value = values.join(', ');
    select.value = values.join(sep_MultiSelect);
}

function SetLanguagesValue(value) {
    var values = (value || '').split(',').map(function (item) { return item.trim(); }).filter(Boolean);
    var select = document.getElementById('fLanguagesSelect');
    var selectedValues = [];
    var selectedItems = [];

    document.querySelectorAll('#fLanguagesOptions input').forEach(function (input) {
        input.checked = values.includes(input.value);
        input.parentElement.style.fontWeight = input.checked ? 'bold' : 'normal';
        if (input.checked) {
            selectedValues.push(input.value);
            selectedItems.push(input.parentElement.innerText);
        }
    });

    select.qfSelectedValuesAsArray = selectedValues;
    select.qfSelectedItemsAsArray = selectedItems;
    document.getElementById('fLanguages').value = values.join(', ');
    select.value = selectedItems.join(sep_MultiSelect);
}

function UpdateCostValue() {
    var values = Array.from(document.querySelectorAll('#fCostOptions input:checked')).map(function (input) {
        return input.value;
    });
    var select = document.getElementById('fCostSelect');
    select.qfSelectedValuesAsArray = values;
    select.qfSelectedItemsAsArray = values.slice();
    document.getElementById('fCost').value = values.join(', ');
    select.value = values.join(sep_MultiSelect);
}

function SetCostValue(value) {
    var values = (value || '').split(',').map(function (item) { return item.trim(); }).filter(Boolean);
    var select = document.getElementById('fCostSelect');
    var selectedValues = [];
    var selectedItems = [];

    document.querySelectorAll('#fCostOptions input').forEach(function (input) {
        input.checked = values.includes(input.value);
        input.parentElement.style.fontWeight = input.checked ? 'bold' : 'normal';
        if (input.checked) {
            selectedValues.push(input.value);
            selectedItems.push(input.parentElement.innerText);
        }
    });

    select.qfSelectedValuesAsArray = selectedValues;
    select.qfSelectedItemsAsArray = selectedItems;
    document.getElementById('fCost').value = values.join(', ');
    select.value = selectedItems.join(sep_MultiSelect);
}

function UpdateDeliveryValue() {
    var values = Array.from(document.querySelectorAll('#fDeliveryOptions input:checked')).map(function (input) {
        return input.value;
    });
    var select = document.getElementById('fDeliverySelect');
    select.qfSelectedValuesAsArray = values;
    select.qfSelectedItemsAsArray = values.map(function (value) {
        return value;
    });
    document.getElementById('fDelivery').value = values.join(', ');
    select.value = values.join(sep_MultiSelect);
}

function SetDeliveryValue(value) {
    var values = (value || '').split(',').map(function (item) { return item.trim(); }).filter(Boolean);
    var select = document.getElementById('fDeliverySelect');
    var selectedValues = [];
    var selectedItems = [];

    document.querySelectorAll('#fDeliveryOptions input').forEach(function (input) {
        input.checked = values.includes(input.value);
        input.parentElement.style.fontWeight = input.checked ? 'bold' : 'normal';
        if (input.checked) {
            selectedValues.push(input.value);
            selectedItems.push(input.parentElement.innerText);
        }
    });

    select.qfSelectedValuesAsArray = selectedValues;
    select.qfSelectedItemsAsArray = selectedItems;
    document.getElementById('fDelivery').value = values.join(', ');
    select.value = selectedItems.join(sep_MultiSelect);
}

function CallDatsAPI(action, data) {
    return fetch(datsApiURL + "?a=" + action, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(Object.assign({ action: action }, data || {}))
    }).then(function (response) {
        return response.json().then(function (json) {
            if (!response.ok) throw new Error(json.error || ('HTTP ' + response.status));
            return json;
        });
    });
}

function LoadDatList() {
    fetch(datsApiURL + "?a=list", { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: '{}' })
        .then(function (r) { return r.json(); })
        .then(function (list) {
            const cbo = document.getElementById('cboDat');
            cbo.innerHTML = '<option value="">-- Create new DAT --</option>';
            list.forEach(function (d) {
                const o = document.createElement('option');
                o.value = d.uri;
                o.innerText = d.label;
                cbo.appendChild(o);
            });
            if (typeof translateDatsManagement === 'function') {
                translateDatsManagement(localStorage.getItem('qf-lang') || 'EN');
            }
        })
        .catch(function (e) { ShowErr(e); });
}

function NewDat() {
    document.getElementById('cboDat').value = '';
    ClearForm();
}

function LoadDat() {
    const uri = document.getElementById('cboDat').value;
    if (!uri) { ClearForm(); return; }

    const language = document.getElementById('fSourceLanguage').value;
    fetch(datsApiURL + "?a=get&lang=" + encodeURIComponent(language) + "&uri=" + encodeURIComponent(uri), { method: 'GET' })
        .then(function (r) { return r.json(); })
        .then(FillForm)
        .catch(function (e) { ShowErr(e); });
}

function SourceLanguageChanged() {
    UpdateFormLanguageMode();
    if (document.getElementById('cboDat').value) LoadDat();
    else ClearForm();
}

function UpdateFormLanguageMode() {
    const isEn = document.getElementById('fSourceLanguage').value === 'en';
    const isNew = !document.getElementById('datUri').value;
    const canEdit = isEn && (isNew || datEditable);
    datFormFieldIds.forEach(function (id) {
        document.getElementById(id).readOnly = !canEdit;
    });
    document.getElementById('btnNew').disabled = !isEn;
    document.getElementById('btnSave').disabled = !canEdit;
    document.getElementById('btnDelete').disabled = !(canEdit && !isNew);
}

function ClearForm() {
    datEditable = false;
    document.getElementById('datUri').value = '';
    document.getElementById('datLastModified').value = '';
    datFormFieldIds.forEach(function (id) {
        document.getElementById(id).value = '';
    });
    SetBenefitsValue('');
    SetSectorValue('');
    SetFunctionalityValue('');
    SetCountryValue('');
    SetLanguagesValue('');
    SetCostValue('');
    SetDeliveryValue('');
    document.getElementById('fTranslationStatus').value = '';
    UpdateFormLanguageMode();
}

function FillForm(d) {
    datEditable = !!d.editable;
    document.getElementById('datUri').value = d.uri;
    document.getElementById('datLastModified').value = d.lastModified || '';
    document.getElementById('fName').value = d.label || '';
    document.getElementById('fTitle').value = d.title || '';
    document.getElementById('fCountry').value = d.country || '';
    document.getElementById('fLaunchYear').value = d.launchYear || '';
    document.getElementById('fLastUpdateYear').value = d.lastUpdateYear || '';
    document.getElementById('fWebsite').value = d.website || '';
    document.getElementById('fDescription').value = d.description || '';
    document.getElementById('fKeywords').value = d.keywords || '';
    SetSectorValue(d.sector || '');
    document.getElementById('fFunctionality').value = d.functionality || '';
    SetBenefitsValue(d.benefits || '');
    SetFunctionalityValue(d.functionality || '');
    SetCountryValue(d.country || '');
    SetLanguagesValue(d.languages || '');
    SetCostValue(d.cost || '');
    SetDeliveryValue(d.delivery || '');
    document.getElementById('fLanguages').value = d.languages || '';
    document.getElementById('fCost').value = d.cost || '';
    document.getElementById('fTranslationStatus').value = d.translationStatus || '';
    UpdateFormLanguageMode();
}

function CollectForm() {
    UpdateBenefitsValue();
    UpdateSectorValue();
    UpdateFunctionalityValue();
    UpdateCountryValue();
    UpdateLanguagesValue();
    UpdateCostValue();
    UpdateDeliveryValue();
    return {
        uri: document.getElementById('datUri').value || null,
        lastModified: document.getElementById('datLastModified').value || null,
        uiLanguage: document.getElementById('fSourceLanguage').value,
        name: document.getElementById('fName').value.trim(),
        sourceLanguage: 'en',
        title: document.getElementById('fTitle').value,
        country: document.getElementById('fCountry').value,
        launchYear: document.getElementById('fLaunchYear').value,
        lastUpdateYear: document.getElementById('fLastUpdateYear').value,
        website: document.getElementById('fWebsite').value,
        description: document.getElementById('fDescription').value,
        keywords: document.getElementById('fKeywords').value,
        sector: document.getElementById('fSector').value,
        functionality: document.getElementById('fFunctionality').value,
        benefits: document.getElementById('fBenefits').value,
        delivery: document.getElementById('fDelivery').value,
        languages: document.getElementById('fLanguages').value,
        cost: document.getElementById('fCost').value
    };
}

function SaveDat() {
    if (document.getElementById('fSourceLanguage').value !== 'en') return;
    const form = document.getElementById('formDat');
    if (!form.reportValidity()) return;

    CallDatsAPI('save', CollectForm())
        .then(function (d) {
            ShowOk('Saved.');
            FillForm(d);
            LoadDatList();
        })
        .catch(function (e) { ShowErr(e); });
}

function DeleteDat() {
    return;
    const data = CollectForm();
    if (!data.uri || data.uiLanguage !== 'en') return;
    if (!confirm('Delete DAT "' + data.name + '"?')) return;

    CallDatsAPI('delete', { uri: data.uri, lastModified: data.lastModified, uiLanguage: data.uiLanguage })
        .then(function () {
            ShowOk('Deleted.');
            ClearForm();
            LoadDatList();
        })
        .catch(function (e) { ShowErr(e); });
}

function LoadHistory() {
    const uri = document.getElementById('datUri').value;
    const tbl = document.getElementById('tblHistory');
    tbl.innerHTML = '';
    if (!uri) return;

    fetch(datsApiURL + "?a=history&uri=" + encodeURIComponent(uri), { method: 'GET' })
        .then(function (r) { return r.json(); })
        .then(function (rows) {
            rows.forEach(function (row) {
                const tr = document.createElement('tr');
                tr.innerHTML = '<td>' + row.createdon + '</td><td>' + row.user_email + '</td><td>' + row.action + '</td>';
                tbl.appendChild(tr);
            });
        })
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
