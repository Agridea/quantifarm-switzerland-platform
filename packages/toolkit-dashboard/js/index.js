let mapFlag = false;

document.addEventListener("DOMContentLoaded", () => {
    SetMap('');
});

function SetMap(lng) {
    // Check if map container exists before initializing
    const mapContainer = document.getElementById('map' + lng);
    if (!mapContainer) {
        return; // Map container not found, skip initialization
    }

    const map = L.map('map' + lng).setView([48, 15], 3);
    L.tileLayer('http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 18,
        attribution: 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a>',
        id: 'OSM'
    }).addTo(map);

    map.on('click', function (e) { console.log(e.latlng); });

    const cIcon = L.Icon.extend({
        options: {
            iconSize: [33, 48],
            iconAnchor: [16, 48]
        }
    });

    testCaseData.forEach((t) => {
        let xIcon = new cIcon({ iconUrl: `assets/img/${t.icon}` });
        let info = GetTCinfo(t);

        L.marker(t.latlng, { icon: xIcon }).addTo(map).bindPopup(`${info}`, {offset: [0, -35]});
    });

}

function GetTCinfo(item) {
    const datsStr = item.dats.map(d => d.name).join(", ");
    return `Test Case: <b>${item.id}</b>
    <br>Agriculture Sector: <b>${translateSector(item.sector)}</b>
    <br>Crop/Livestock: <b>${translateCrop(item.crop)}</b>
    <br>Country: <b>${translateCountry(item.country)}</b>
    <br>Digital Solutions: <b>${datsStr}</b>
    <div class="mt-1"><a href='tcreport.html?n=${item.id}' target='_blank'><b>Read more</b><i class="bi bi-caret-right-fill ms-1"></i></a></div>`;
}

