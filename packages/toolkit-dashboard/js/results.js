let mapFlag = false;

PopulateSelect("cboCountry", countryData, "id", "id", true);
translateCountryOptions('cboCountry');
LoadData();

function SetMap() {

    if (!mapFlag) {

        const map = L.map('map').setView([48, 15], 3);
        L.tileLayer('http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            maxZoom: 18,
            attribution: 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a>',
            id: 'OSM'
        }).addTo(map);

        map.on('click', function (e) { console.log(e.latlng); });

        const cIcon = L.Icon.extend({
            options: {
                //shadowUrl: 'assets/img/sha1.png',
                //shadowAnchor: [7, -1]
                //shadowSize: [32, 32],
                iconSize: [32, 32],
                iconAnchor: [16, 16]
            }
        });

        countryData.forEach((t) => {
            let xIcon = new cIcon({ iconUrl: `assets/img/${t.icon}`, iconID: `${t.id}` });

            L.marker(t.latlng, { icon: xIcon }).addTo(map)
                .bindTooltip(`${t.id}`,
                    {
                        permanent1: false,
                        direction1: 'right'
                    }
            ).on('click', OnIconClick);
        });

        mapFlag = true;
    }

}

function LoadData() {
    const country = getUIValue("cboCountry");
    const sector = getUIValue("cboSector");

    PopulateTable("table1", country, sector);
}

function OnIconClick(e) {
    const c = e.target.options.icon.options.iconID;
    PopulateTable("table2", c);
}

function PopulateTable(table, country, sector) {
    const e = document.getElementById(table);
    let html = "";
    let dats;

    testCaseData.forEach((item) => {
        if ((item.country == country || !country) && (item.sector == sector || !sector)) {

            dats = "";
            item.dats.forEach((d) => { dats += `<a href="#" onclick="LoadDATDetals('${d.id}');return false;">${d.name}</a><br>`; });
             
            html +=
                `<tr>
                <td>${item.id}</td>
                <td>${translateSector(item.sector)}</td>
                <td>${translateCrop(item.crop)}</td>
                <td>${dats}</td>
                <td>${translateCountry(item.country)}</td>
                <td>${item.partner}</td>
                <td class="text-end">
                    <a type="button" class="btn btn-primary qf-bnt-sm" href="tcreport.html?n=${item.id}" target="_blank"><i class="bi bi-search"></i></a></td>
                </td>
                </tr>`;
        }
    });

    if (html === "") html = "(no test cases found)";

    e.innerHTML = html;
}

