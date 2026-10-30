const searchParams = new URLSearchParams(window.location.search);
const tcNum = Math.max(Math.min(parseInt(searchParams.get('n')) || 1, 30), 1);
const tcNN = tcNum.toString().padStart(2, '0');
const tcObject = testCaseData[tcNum - 1];

document.getElementById('tcNumSpan').textContent = tcNum;
document.getElementById('tcSector').innerHTML = translateSector(tcObject.sector);
document.getElementById('tcCrop').innerHTML = translateCrop(tcObject.crop);
document.getElementById('tcCountry').innerHTML = translateCountry(tcObject.country);
document.getElementById('tcDAT').innerHTML = `<a href="#" onclick="LoadDATDetals('${tcObject.dats[0].id}');return false;">${tcObject.dats[0].name}</a>`;
    
const t = document.getElementById('tcTable');
for (let i = 1; i < tcObject.dats.length; i++) {
    t.innerHTML += `<tr><td class="text-nowrap pe-2 text-end w-50"></td><td class="text-start fw-bold w-50"><a href="#" onclick="LoadDATDetals('${tcObject.dats[i].id}');return false;">${tcObject.dats[i].name}</a></td></tr>`;
}

document.getElementById('a2023').href = `downloads/TC${tcNN}-2023-Assessment-report.pdf`;
document.getElementById('a2024').href = `downloads/TC${tcNN}-2024-Assessment-report.pdf`;
document.getElementById('a2025').href = `downloads/TC${tcNN}-2025-Assessment-report.pdf`;
document.getElementById('a2026').href = `downloads/TC${tcNN}-Aggregated-Assessment-report.pdf`;

const apiURL = baseURL + "sparql.php";
let dataMainImpact, dataMonetaryImpact, dataAggregatedImpact;
let chartAggregatedImpact2024, chartAggregatedImpact2025, chartAggregatedImpact2026;

// Translated labels for the aggregated-impact bar chart (x-axis categories and
// y-axis title).  Keys match tcreportStrings in uistrings.js; English is the
// source / fallback.
const chartLabelTranslations = {
    'DE': {
        yTitle: 'Prozent (%)',
        categories: [
            [['Kosten-'], ['effizienz']],
            ['Produktivität'],
            [['Wassermanagement-'], ['effizienz']],
            [['Betriebsmittel-'], ['manag.-'], ['Effizienz']],
            [['Energie-'], ['effizienz']],
            [['CO2-Emissions-'], ['reduktion']],
            [['Arbeits-'], ['effizienz']]
        ]
    },
    'FR': {
        yTitle: 'Pourcentage (%)',
        categories: [
            [['Efficacité'], ['des coûts']],
            ['Productivité'],
            [['Efficacité de la'], ['gestion de l\'eau']],
            [['Efficacité de la'], ['gestion des'], ['intrants']],
            [['Efficacité'], ['énergétique']],
            [['Réduction des'], ['émissions de CO2']],
            [['Efficacité du'], ['travail']]
        ]
    },
    'IT': {
        yTitle: 'Percentuale (%)',
        categories: [
            [['Efficienza'], ['dei costi']],
            ['Produttività'],
            [['Efficienza'], ['gestione idrica']],
            [['Efficienza'], ['gestione input']],
            [['Efficienza'], ['energetica']],
            [['Riduzione'], ['emissioni CO2']],
            [['Efficienza del'], ['lavoro']]
        ]
    }
};

function getChartLabels(lng) {
    const t = chartLabelTranslations[lng];
    if (!t) return { yTitle: 'Percentage (%)', categories: [[['Costs'], ['efficiency']], ['Productivity'], [['Water'], ['management'], ['efficiency']], [['Inputs'], ['management'], ['efficiency']], [['Energy'], ['efficiency']], [['CO2'], ['emissions'], ['reduction']], [['Labor'], ['efficiency']]] };
    return t;
}

// Build chart options with translated axis labels for the current language.
function getAggregatedImpactOptions() {
    const labels = getChartLabels(localStorage.getItem('qf-lang') || 'EN');
    return {
        series: [{
            name: 'with DATSs',
            data: [],
        }],
        chart: {
            height: 500,
            type: 'bar',
            background: '#fff',
            dropShadow: {
                enabled: true,
                left: 0,
                top: 0,
                blur: 3,
                opacity: 0.65,
            }
        },
        plotOptions: {
            bar: {
                horizontal: false,
                columnWidth: '50%',
                colors: {
                    ranges: [{
                        from: -100,
                        to: 0,
                        color: '#EA6E1A'
                    }, {
                        from: 0,
                        to: 100,
                        color: '#87BE62'
                    }]
                },
            },
        },
        fill: {
            opacity: 0.85,
            type: 'solid',
        },
        yaxis: {
            show: true,
            showAlways: true,
            min: -100,
            max: 100,
            forceNiceScale: true,
            title: {
                text: labels.yTitle,
                style: {
                    fontSize: '11pt',
                    fontWeight: 'normal'
                }
            },
            labels: {
                show: true,
                style: {
                    fontSize: '10pt',
                }
            }
        },
        xaxis: {
            categories: labels.categories,
            labels: {
                show: true,
                style: {
                    fontSize: '11pt',
                    fontWeight: 'normal'
                }
            }
        },
        legend: {
            show: false
        },
        dataLabels: {
            enabled: true
        }
    };
}
const titlesAggregatedImpact = {"total COSTS":1, "total PRODUCTIVITY":2, "total WATER":3, "total INPUTS":4, "total ENERGY":5, "total GHG EMISSIONS":6, "total LABOUR":7};
const titlesMonetaryImpact = {"DATSs COSTS":1, "COSTS":2, "OUTPUT":3, "CBA":4};

const iconsMainImpact = {"Cost of DATSs":"bi bi-currency-euro", "Initial investment":"bi bi-currency-euro", "Labour for":"bi bi-people-fill", "PAYBACK PERIOD":"fa-solid fa-money-bill-transfer", "BENEFIT":"fa-solid fa-coins", "Sum of costs":"fa-solid fa-coins" ,"productivity":"fa-solid fa-arrow-up-right-dots", "ROI":"bi bi-currency-euro", "NPV":"bi bi-currency-euro", "revenue":"fa-solid fa-money-bill-trend-up", "water":"ri-contrast-drop-2-fill", "fuel":"ri-gas-station-fill", "electricity":"bi bi-lightning-fill", "pesticide":"ri-bug-fill", "fertiliser":"ri-ink-bottle-fill", "nitrogen":"ri-ink-bottle-fill", "feed":"fa-solid fa-plate-wheat fa-fw", "drugs":"fa-solid fa-syringe fa-fw"};

const valueColorMap1 = ["table-danger", "table-success", "table-secondary", "table-primary"];
const valueColorMap2 = ["#FFBFBF", "#A3CCB8", "#CECECE", "#AACCFF"];

//stupid exception KPIs: use percDiff instead of absDiff 
let percKPIs = ["Land Productivity", "Meat productivity", "Mortality rate (aquaculture)", "Cows with high SCC", "Working time", "Nitrogen applied", "GHG emissions", "Irrigation water productivity", "Rate of time for quality analysis", "MILK PRODUCTIVITY"];
percKPIs = percKPIs.map(item => item.toUpperCase().trim());

// Swiss localisation: replace Euro with CHF
function ConvertUnit(unit) {
    return (unit || '').replace(/€/g, 'CHF').replace(/\bEUR\b/g, 'CHF');
}

//2023
Show2023();

//2024 and 2025 and 2026(three-year aggregation)
LoadData();



function LoadData() {
    // Destroy old charts and recreate with current language labels immediately
    [chartAggregatedImpact2024, chartAggregatedImpact2025, chartAggregatedImpact2026].forEach(c => {
        if (c) { try { c.destroy(); } catch(e) {} }
    });
    const opts = getAggregatedImpactOptions();
    chartAggregatedImpact2024 = new ApexCharts(document.querySelector("#divc32024"), opts);
    chartAggregatedImpact2024.render();
    chartAggregatedImpact2025 = new ApexCharts(document.querySelector("#divc32025"), opts);
    chartAggregatedImpact2025.render();
    chartAggregatedImpact2026 = new ApexCharts(document.querySelector("#divc32026"), opts);
    chartAggregatedImpact2026.render();

    const lng = localStorage.getItem('qf-lang') || 'en';
    const par = {
        "path": "/tcdata",
        "data": tcNum,
        "language": lng
    };

    CallAPI(apiURL, par, (data) => {

        dataMainImpact = data.q1;
        dataMonetaryImpact = data.q2;
        dataAggregatedImpact = data.q3;

        console.log('Query MainImpact:', dataMainImpact);
        console.log('Query MonetaryImpact:', dataMonetaryImpact);
        console.log('Query AggregatedImpact:', dataAggregatedImpact);

        // Extract unique products from dataMainImpact
        let products = [...new Set(dataMainImpact.filter(item => item.year.value === "2024").map(item => item.product.value))];
        if (products.length > 0) YesData(2024); 
        ShowProducts(products, 2024);

        products = [...new Set(dataMainImpact.filter(item => item.year.value === "2025").map(item => item.product.value))];
        if (products.length > 0) YesData(2025);
        ShowProducts(products, 2025);

        products = [...new Set(dataMainImpact.filter(item => item.year.value === "2026").map(item => item.product.value))];
        if (products.length > 0) YesData(2026);
        ShowProducts(products, 2026);

    }, "", "");
}

function NoData(y) {
    document.getElementById('divNoData' + y).hidden = false;
    document.getElementById('divData' + y).hidden = true;
}
function YesData(y) {
    document.getElementById('divNoData' + y).hidden = true;
    document.getElementById('divData' + y).hidden = false;
}

function SetRowspan(arr) {
    // sort the array by order
    const sortedArr = [...arr].sort((a, b) => a.order - b.order);
    
    for (let i = sortedArr.length - 1; i >= 0; i--) {
        if (i > 0 && sortedArr[i].title === sortedArr[i - 1].title) {
            sortedArr[i - 1].rowspan += sortedArr[i].rowspan;
            sortedArr[i].rowspan = 0;
        }
    }
   
    return sortedArr;
}

function GetIcon(name) {

    // Check each key in iconsMainImpact for substring match with name
    for (const [key, value] of Object.entries(iconsMainImpact)) {
        if (name.toLowerCase().includes(key.toLowerCase())) {
            return value;
        }
    }
    
    return "fa-solid fa-chart-line"; // Return it if no match found
}

function ShowProducts(data, year) {
    const n = document.getElementById("divProducts" + year);
    let html = "";

    if (!data || data.length === 0) return;

    for (let i = 0; i < data.length; i++) {
        html += `<input type="radio" class="btn-check" name="btnradio${year}" id="btnradio${year}${i}" autocomplete="off" data-product="${data[i].replace(/"/g, '&quot;')}">
        <label class="btn btn-outline-primary my-1" for="btnradio${year}${i}" data-product="${data[i].replace(/"/g, '&quot;')}">${data[i]}</label>`;
    }

    n.innerHTML = html;

    // Remove old listener if any (LoadData may be called again on language change)
    if (n._productClickHandler) n.removeEventListener('click', n._productClickHandler);

    // Event delegation on the container
    n._productClickHandler = function(e) {
        const el = e.target.closest('[data-product]');
        if (el) OnProduct(year, el.dataset.product);
    };
    n.addEventListener('click', n._productClickHandler);

    //select the first product
    OnProduct(year, data[0]);
}

function OnProduct(year, product) {
    let data;

    data = dataMainImpact
        .filter(item => item.year.value === year.toString() && item.product.value === product && item.title.value)   //filter out the items with title = ""
        .map(item => { 
            let c = parseInt(item.impactLevel.value);
            c = (c <= 3 && c >= 0) ? c : 2;
            const isPerc = percKPIs.includes(item.name.value.toUpperCase().trim());

            return {
            title: item.title.value,
            subtitle: item.subtitle.value, 
            unit: isPerc ? "%" : ConvertUnit(item.unit.value), 
            value: isPerc ? RoundValue(item.percDiff.value) : RoundValue(item.absDiff.value), 
            isgood: item.higherIsBetter.value, 
            icon: GetIcon(item.name.value),
            color1: valueColorMap1[c],
            color2: valueColorMap2[c]
        }});
 
    //order?
    ShowMainImpact(data, year);

    data = dataMonetaryImpact
        .filter(item => item.year.value === year.toString() && item.product.value === product)
        .map(item => { 
            let c = parseInt(item.impactLevel.value);
            c = (c <= 3 && c >= 0) ? c : 2;
            const isPerc = percKPIs.includes(item.name.value.toUpperCase().trim());

            return {
            title: item.category.value,
            subtitle: item.description.value, 
            unit: isPerc ? "%" : ConvertUnit(item.unit.value),  
            value: isPerc ? RoundValue(item.percDiff.value) : RoundValue(item.absDiff.value),
            isgood: item.higherIsBetter.value,    
            color1: valueColorMap1[c],
            rowspan: 1,
            order: titlesMonetaryImpact[item.category.value.trim()]
        }});

    data = SetRowspan(data);
    ShowMonetaryImpact(data, year);
    
    data = dataAggregatedImpact
        .filter(item => item.year.value === year.toString() && item.product.value === product)
        .map(item => ({
            title: item.name.value,
            value: Math.round(item.maxRangePercDiff.value), 
            order: titlesAggregatedImpact[item.name.value.trim()]
        }));

    data.sort((a, b) => a.order - b.order);
    ShowAggregatedImpact(data, year);
    
    // Auto-expand the first accordion section so the user sees the results
    const firstCollapse = document.querySelector('#accordion' + year + ' .accordion-collapse');
    if (firstCollapse && !firstCollapse.classList.contains('show')) {
        new bootstrap.Collapse(firstCollapse, { toggle: true });
    }
 }

function ShowMainImpact(data, year) {
    const n = document.getElementById("divc1" + year);
    let html = "";

    if (data && data.length > 0) {
 
        for (let i = 0; i < data.length; i++) {
            let fs = data[i].subtitle.length >= 200 ? "small" : "";

            html += `<div class="m-1" style="width: 500px; height:220px; border-radius: 15px;">
            <table class="table table-borderless w-100 h-100 ${data[i].color1}">
                <tbody>
                    <tr>
                        <td class="text-center align-middle" style="width: 100px; border-radius: 15px 0px 0px 15px; background-color:${data[i].color2} ">
                            <span class="h1"><i class="${data[i].icon}"></i></span>
                        </td>
                        <td class="text-center" style="border-radius: 0px 15px 15px 0px;">
                            <div class="row g-0">
                                <h2>${FormatNumber2String(data[i].value)}<span class="h5 ms-2">${data[i].unit}</span></h2>
                            </div>
                            <div class="row g-0">
                                <h5 class="fw-bold text-info">${data[i].title}</h5>
                            </div>
                            <div class="row g-0">
                                <p class="card-text ${fs}">${data[i].subtitle}</p>
                            </div>
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>`;
        }
    }

    n.innerHTML = html;
}

function ShowMonetaryImpact(data, year) {
    const n = document.getElementById("divc2" + year);
    let html = "";

    if (data && data.length > 0) {
        html = '<table class="table w-100"><tbody>';

        for (let i = 0; i < data.length; i++) {
            html += "<tr>";

            if (data[i].rowspan > 0)
                html += `<td rowspan="${data[i].rowspan}" class="align-middle fw-bold text-info table-secondary" style="border-radius: 15px 0px 0px 15px;">${data[i].title}</td>`;

            html += `
            <td class="text-end text-nowrap fw-bold ${data[i].color1}">${FormatNumber2String(data[i].value)}</td>
            <td class="${data[i].color1}">${data[i].unit}</td>
            <td class="${data[i].color1}">${data[i].subtitle}</td>`;

            html += "</tr>";
        }

        html += '</tbody></table>';
    }

    n.innerHTML = html;
}

function ShowAggregatedImpact(data, year) {
    //https://apexcharts.com/docs/methods/#updateSeries

    if (!data || data.length === 0) return;

    const options = getAggregatedImpactOptions();
    options.series[0].data = data.map(item => item.value);

    const chart = year==2024 ? chartAggregatedImpact2024 : year==2025 ? chartAggregatedImpact2025 : chartAggregatedImpact2026;

    if (chart) chart.updateSeries(options.series);
    
}

function Show2023() {
    document.getElementById('div2023-1').innerHTML = `<img src="assets/img/TC${tcNN}-2023-1.png" class="img-fluid" onerror="NoData(2023)"/>`;
    document.getElementById('div2023-2').innerHTML = `<img src="assets/img/TC${tcNN}-2023-2.png" class="img-fluid" onerror="NoData(2023)"/>`;
    document.getElementById('div2023-3').innerHTML = `<img src="assets/img/TC${tcNN}-2023-3.png" class="img-fluid" onerror="NoData(2023)"/>`;

    //exeption for TC12, TC29: no impacts were recorded. Only the Reports were shared.
    if (tcNum == 12 || tcNum == 29) {
        document.getElementById('tabTab1').innerHTML = `<div class="row text-center mt-3"><h5 class="card-title lh-lg"><a href="downloads/TC${tcNN}-2023-Assessment-report.pdf"><i class="bi bi-download me-2"></i>Download the full assessment report</a></h5></div>`;
    }
}

function RoundValue(v) {
    const vv = Number(v);
    if(Number.isNaN(vv))  return 0;
 
    if(Math.abs(vv) < 0.001) 
        return parseFloat(vv.toFixed(5));
    else if(Math.abs(vv) < 1) 
        return parseFloat(vv.toFixed(3));
    else if(Math.abs(vv) < 10)
        return parseFloat(vv.toFixed(2));
    else
        return Math.round(vv);
}



