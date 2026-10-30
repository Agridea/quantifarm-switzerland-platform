
const testCaseData = [
    {
        id: 1,
        sector: "Arable",
        crop: "Potatoes",
        dats: [{ name: "gaiasense", id: "https://quantifarm.eu/data/dats/gaiasense"}],
        country: "Greece",
        partner: "NP",
        cultivation_type: "Arable",
        comparisons: 4,
        latlng: [35.17562187,25.4711726],
        icon: "Arable.png"
    },
    {
        id: 2,
        sector: "Arable",
        crop: "Corn",
        dats: [{ name: "Irristrat", id: "https://quantifarm.eu/data/dats/irristrat" }],
        country: "Portugal",
        partner: "Agromais",
        cultivation_type: "Arable",
        comparisons: 2,
        latlng: [39.3999,-8.2245],
        icon: "Arable.png"
    },
    {
        id: 3,
        sector: "Arable",
        crop: "Barley, Wheat",
        dats: [{ name: "SATIVUM", id: "https://quantifarm.eu/data/dats/sativum" }],
        country: "Spain",
        partner: "ITACyL",
        cultivation_type: "Arable",
        comparisons: 13,
        latlng: [41.81747734,-4.028318222],
        icon: "Arable.png"
    },
    {
        id: 4,
        sector: "Arable",
        crop: "Cotton",
        dats: [{ name: "Augmenta VRA", id: "https://quantifarm.eu/data/dats/augmenta_vra" }],
        country: "Greece",
        partner: "Augmenta",
        cultivation_type: "Arable",
        comparisons: 6,
        latlng: [40.60348533,22.28418609],
        icon: "Arable.png"
    },
    {
        id: 5,
        sector: "Arable",
        crop: "Wheat",
        dats: [{ name: "granoduro.net", id: "https://quantifarm.eu/data/dats/granoduro.net" }],
        country: "Turkiye",
        partner: "HORTA",
        cultivation_type: "Arable",
        comparisons: 10,
        latlng: [37.2137,40.3931],
        icon: "Arable.png"
    },
    {
        id: 6,
        sector: "Arable",
        crop: "Onion, Potatoes",
        dats: [{ name: "Delphy QMS system", id: "https://quantifarm.eu/data/dats/delphy_qms_system" }, { name: "Agro exact sencrop", id: "https://quantifarm.eu/data/dats/agro_exact_sencrop" }],
        country: "Netherlands",
        partner: "Delphy",
        cultivation_type: "Arable",
        comparisons: 1,
        latlng: [52.1226,5.2813],
        icon: "Arable.png"
    },
    {
        id: 7,
        sector: "Arable",
        crop: "Potatoes",
        dats: [{ name: "gaiasense", id: "https://quantifarm.eu/data/dats/gaiasense" }],
        country: "Poland",
        partner: "FFP2",
        cultivation_type: "Arable",
        comparisons: 3,
        latlng: [54.51806808,17.28648359],
        icon: "Arable.png"
    },
    {
        id: 8,
        sector: "Arable",
        crop: "Wheat",
        dats: [{ name: "AgroSmart for Silos", id: "https://quantifarm.eu/data/dats/agrosmart_for_silos" }],
        country: "Latvia",
        partner: "AgroSmart",
        cultivation_type: "Silos",
        comparisons: 1,
        latlng: [56.8796,24.6032],
        icon: "Arable.png"
    },
    {
        id: 9,
        sector: "Arable",
        crop: "Corn, Wheat",
        dats: [{ name: "Farm manager", id: "https://quantifarm.eu/data/dats/farm_manager" }],
        country: "Slovenia",
        partner: "KGZS",
        cultivation_type: "Arable",
        comparisons: 4,
        latlng: [46.38559403,15.07474589],
        icon: "Arable.png"
    },
    {
        id: 10,
        sector: "Arable",
        crop: "Wheat",
        dats: [{ name: "fms.agricloud.ro", id: "https://quantifarm.eu/data/dats/fms.agricloud.ro" }],
        country: "Romania",
        partner: "ANAMOB",
        cultivation_type: "Arable",
        comparisons: 1,
        latlng: [44.27919609,27.49014411],
        icon: "Arable.png"
    },
    {
        id: 11,
        sector: "Fruit",
        crop: "Olives",
        dats: [{ name: "gaiasense", id: "https://quantifarm.eu/data/dats/gaiasense" }],
        country: "Greece",
        partner: "NP",
        cultivation_type: "Horticulture",
        comparisons: 1,
        latlng: [37.14807847,21.82700563],
        icon: "Fruits.png"
    },
    {
        id: 12,
        sector: "Fruit",
        crop: "Apples",
        dats: [{ name: "QMS Root pruning", id: "https://quantifarm.eu/data/dats/qms_root_pruning" }, { name: "Digital vigour map", id: "https://quantifarm.eu/data/dats/digital_vigour_map" }, { name: "Digital blossom map", id: "https://quantifarm.eu/data/dats/digital_blossom_map" }, { name: "Estede", id: "https://quantifarm.eu/data/dats/estede" }, { name: "Trapview", id: "https://quantifarm.eu/data/dats/trapview" }],
        country: "Poland",
        partner: "Delphy",
        cultivation_type: "Horticulture",
        comparisons: 1,
        latlng: [52.16747392,20.15756646],
        icon: "Fruits.png"
    },
    {
        id: 13,
        sector: "Fruit",
        crop: "Grapes",
        dats: [{ name: "Vite-net", id: "https://quantifarm.eu/data/dats/vite-net" }],
        country: "Italy",
        partner: "HORTA",
        cultivation_type: "Horticulture",
        comparisons: 1,
        latlng: [44.8758,9.8577],
        icon: "Fruits.png"
    },
    {
        id: 14,
        sector: "Fruit",
        crop: "Strawberries, Blueberries",
        dats: [{ name: "NETAJET", id: "https://quantifarm.eu/data/dats/netajet" }, { name: "NMC pro system", id: "https://quantifarm.eu/data/dats/nmc_pro_system" }],
        country: "Serbia",
        partner: "Terra",
        cultivation_type: "Greenhouse", //Horticulture
        comparisons: 1,
        latlng: [45.274139,19.363813],
        icon: "Fruits.png"
    },
    {
        id: 15,
        sector: "Fruit",
        crop: "Olives",
        dats: [{ name: "gaiasense", id: "https://quantifarm.eu/data/dats/gaiasense" }],
        country: "Cyprus",
        partner: "Filagro",
        cultivation_type: "Horticulture",
        comparisons: 1,
        latlng: [34.95107237,33.27383455],
        icon: "Fruits.png"
    },
    {
        id: 16,
        sector: "Fruit",
        crop: "Apples",
        dats: [{ name: "Digital vigour map", id: "https://quantifarm.eu/data/dats/digital_vigour_map" }, { name: "Digital blossom map", id: "https://quantifarm.eu/data/dats/digital_blossom_map" }, { name: "Estede", id: "https://quantifarm.eu/data/dats/estede" }, { name: "Trapview", id: "https://quantifarm.eu/data/dats/trapview" }],
        country: "Netherlands",
        partner: "Delphy",
        cultivation_type: "Horticulture",
        comparisons: 1,
        latlng: [51.83865033,5.263890776],
        icon: "Fruits.png"
    },
    {
        id: 17,
        sector: "Fruit",
        crop: "Grapes",
        dats: [{ name: "fms.agricloud.ro", id: "https://quantifarm.eu/data/dats/fms.agricloud.ro" }],
        country: "Romania",
        partner: "ANAMOB",
        cultivation_type: "Horticulture",
        comparisons: 1,
        latlng: [45.9432,24.9668],
        icon: "Fruits.png"
    },
    {
        id: 18,
        sector: "Vegetables",
        crop: "Tomatoes",
        dats: [{ name: "pomodoro.net", id: "https://quantifarm.eu/data/dats/pomodoro.net" }],
        country: "Italy",
        partner: "HORTA",
        cultivation_type: "Horticulture",
        comparisons: 1,
        latlng: [45.1008,10.3025],
        icon: "Vegetables.png"
    },
    {
        id: 19,
        sector: "Vegetables",
        crop: "Tomatoes",
        dats: [{ name: "QMS Tomato", id: "https://quantifarm.eu/data/dats/qms_tomato" }],
        country: "Netherlands",
        partner: "Delphy",
        cultivation_type: "Greenhouse", //Horticulture
        comparisons: 1,
        latlng: [52.012804,4.513671],
        icon: "Vegetables.png"
    },
    {
        id: 20,
        sector: "Fruit",
        crop: "Bananas",
        dats: [{ name: "NADIA", id: "https://quantifarm.eu/data/dats/nadia" }],
        country: "Canary Islands",
        partner: "Anysol",
        cultivation_type: "Horticulture",
        comparisons: 1,
        latlng: [28.13896558,-15.52368183],
        icon: "Fruits.png"
    },
    {
        id: 21,
        sector: "Vegetables",
        crop: "Tomatoes",
        dats: [{ name: "Signify with GrowWise control system", id: "https://quantifarm.eu/data/dats/signify_with_growwise_control_system" }, { name: "Kathari UF1", id: "https://quantifarm.eu/data/dats/kathari_uf1" }],
        country: "Finland",
        partner: "LUKE",
        cultivation_type: "Greenhouse", //Horticulture
        comparisons: 1,
        latlng: [62.3971,21.3756],
        icon: "Vegetables.png"
    },
    {
        id: 22,
        sector: "Meat",
        crop: "Poultry",
        dats: [{ name: "NetFLOX", id: "https://quantifarm.eu/data/dats/netflox" }],
        country: "UK",
        partner: "FLOX",
        cultivation_type: "Meat-poultry",
        comparisons: 1,
        latlng: [50.9025623,-3.4875797],
        icon: "Meat.png"
    },
    {
        id: 23,
        sector: "Meat",
        crop: "Cows",
        dats: [{ name: "Lely", id: "https://quantifarm.eu/data/dats/lely" }, { name: "MSD & Lely", id: "https://quantifarm.eu/data/dats/msd_&_lely" }, { name: "Innoval", id: "https://quantifarm.eu/data/dats/innoval" }],
        country: "France",
        partner: "IDELE",
        cultivation_type: "Meat-cow",
        comparisons: 1,
        latlng: [46.2276,2.2137],
        icon: "Meat.png"
    },
    {
        id: 24,
        sector: "Meat",
        crop: "Pigs",
        dats: [{ name: "PigUp", id: "https://quantifarm.eu/data/dats/pigup" }, { name: "Acerva", id: "https://quantifarm.eu/data/dats/acerva" }, { name: "smaRt Counting", id: "https://quantifarm.eu/data/dats/smart_counting" }, { name: "Slimme stal", id: "https://quantifarm.eu/data/dats/slimme_stal" }],
        country: "Belgium",
        partner: "Leuven",
        cultivation_type: "Meat-pig",
        comparisons: 1,
        latlng: [51.2144,3.0719],
        icon: "Meat.png"
    },
    {
        id: 25,
        sector: "Dairy",
        crop: "Cows",
        dats: [{ name: "Lely", id: "https://quantifarm.eu/data/dats/lely" }],
        country: "France",
        partner: "IDELE",
        cultivation_type: "Milk",
        comparisons: 1,
        latlng: [46.2276,2.2137],
        icon: "Dairy.png"
    },
    {
        id: 26,
        sector: "Dairy",
        crop: "Cows",
        dats: [{ name: "DeLaval VMS V300 series", id: "https://quantifarm.eu/data/dats/delaval_vms_v300_series" }],
        country: "Ireland",
        partner: "Teagasc",
        cultivation_type: "Milk",
        comparisons: 1,
        latlng: [53.4,-8],
        icon: "Dairy.png"
    },
    {
        id: 27,
        sector: "Dairy",
        crop: "Cows",
        dats: [{ name: "SmaXtech", id: "https://quantifarm.eu/data/dats/smaxtech" }],
        country: "Germany",
        partner: "Leuven",
        cultivation_type: "Milk",
        comparisons: 1,
        latlng: [53.7919,10.5336],
        icon: "Dairy.png"
    },
    {
        id: 28,
        sector: "Dairy",
        crop: "Cows",
        dats: [{ name: "Boumatic milking", id: "https://quantifarm.eu/data/dats/boumatic_milking" }],
        country: "Romania",
        partner: "ANAMOB",
        cultivation_type: "Milk",
        comparisons: 1,
        latlng: [45.9432,24.9668],
        icon: "Dairy.png"
    },
    {
        id: 29,
        sector: "Apiculture",
        crop: "Bees",
        dats: [{ name: "ART 21", id: "https://quantifarm.eu/data/dats/art_21" }],
        country: "Lithuania",
        partner: "ART21",
        cultivation_type: "Bees",
        comparisons: 1,
        latlng: [55.1694,23.8813],
        icon: "Apiculture.png"
    },
    {
        id: 30,
        sector: "Aquaculture",
        crop: "Oysters",
        dats: [{ name: "BENCO", id: "https://quantifarm.eu/data/dats/benco" }],
        country: "Croatia",
        partner: "Benco",
        cultivation_type: "Oyster",
        comparisons: 1,
        latlng: [45.1,15.2],
        icon: "Aquaculture.png"
    }
];

const countryData = [
    {
        id: "Belgium",
        icon: "belgium.png",
        latlng: [50.72254683363231, 4.257202148437501]
    },
    {
        id: "Canary Islands",
        icon: "canary.png",
        latlng: [30.315987718557867, -17.369384765625004]
    },
    {
        id: "Croatia",
        icon: "croatia.png",
        latlng: [44.15068115978094, 15.172119140625002]
    },
    {
        id: "Cyprus",
        icon: "cyprus.png",
        latlng: [35.191766965947394, 32.66510009765626]
    },
    {
        id: "Finland",
        icon: "finland.png",
        latlng: [62.71446210149774, 23.181152343750004]
    },
    {
        id: "France",
        icon: "france.png",
        latlng: [45.98169518512228, 1.4282226562500002]
    },
    {
        id: "Germany",
        icon: "germany.png",
        latlng: [52.03897658307622, 11.019287109375]
    },
    {
        id: "Greece",
        icon: "greece.png",
        latlng: [37.20120736474139, 21.829833984375004]
    },
    {
        id: "Ireland",
        icon: "ireland.png",
        latlng: [52.8823912222619, -9.503173828125]
    },
    {
        id: "Italy",
        icon: "italy.png",
        latlng: [42.032974332441405, 12.008056640625]
    },
    {
        id: "Latvia",
        icon: "latvia.png",
        latlng: [57.58655886615978, 24.664306640625]
    },
    {
        id: "Lithuania",
        icon: "lithuania.png",
        latlng: [55.751849391735284, 22.818603515625]
    },
    {
        id: "Netherlands",
        icon: "netherlands.png",
        latlng: [53.199451902831555, 5.350341796875001]
    },
    {
        id: "Poland",
        icon: "poland.png",
        latlng: [53.067626642387374, 18.522949218750004]
    },
    {
        id: "Portugal",
        icon: "portugal.png",
        latlng: [40.730608477796636, -8.865966796875002]
    },
    {
        id: "Romania",
        icon: "romania.png",
        latlng: [46.89023157359399, 24.411621093750004]
    },
    {
        id: "Serbia",
        icon: "serbia.png",
        latlng: [44.18220395771566, 20.511474609375004]
    },
    {
        id: "Slovenia",
        icon: "slovenia.png",
        latlng: [46.255846818480315, 14.683227539062502]
    },
    {
        id: "Spain",
        icon: "spain.png",
        latlng: [40.413496049701955, -2.5158691406250004]
    },
    {
        id: "Turkiye",
        icon: null,
        latlng: [40.54720023441049, 32.71179199218751]
    },
    {
        id: "UK",
        icon: "uk.png",
        latlng: [55.33539361201609, -3.4881591796875004]
    }
];

const fieldsData = [
    { field: "testcaseNumber", disable: [] },
    { field: "testcaseLeader", disable: [] },
    { field: "cultivationType", disable: [] },
    { field: "datsInformation", disable: [] },
    { field: "farmNumber", disable: [] },
    { field: "biogeographicalRegion", disable: ["Silos"] },
    { field: "totalFarmSize", disable: ["Silos"] },
    { field: "parcelName", disable: [] },
    { field: "parcelDimension", disable: [] },
    { field: "soilFractionSand", disable: ["Meat-poultry", "Meat-cow", "Meat-pig", "Milk", "Oyster", "Bees", "Silos"] },
    { field: "soilFractionClay", disable: ["Meat-poultry", "Meat-cow", "Meat-pig", "Milk", "Oyster", "Bees", "Silos"] },
    { field: "soilFractionSilt", disable: ["Meat-poultry", "Meat-cow", "Meat-pig", "Milk", "Oyster", "Bees", "Silos"] },
    { field: "bulkDensity", disable: ["Meat-poultry", "Meat-cow", "Meat-pig", "Milk", "Oyster", "Bees", "Silos"] },
    { field: "soilOrganicCarbon", disable: ["Meat-poultry", "Meat-cow", "Meat-pig", "Milk", "Oyster", "Bees", "Silos"] },
    { field: "numberOfAnimals", disable: ["Arable", "Horticulture", "Greenhouse", "Oyster", "Bees", "Silos"] },
    { field: "numberOfPlants", disable: ["Arable", "Horticulture", "Meat-poultry", "Meat-cow", "Meat-pig", "Milk", "Oyster", "Bees", "Silos"] },
    { field: "livestockUnits", disable: ["Arable", "Horticulture", "Greenhouse", "Oyster", "Bees", "Silos"] },
    { field: "numberOfBeehives", disable: ["Arable", "Horticulture", "Greenhouse", "Meat-poultry", "Meat-cow", "Meat-pig", "Milk", "Oyster", "Silos"] },
    { field: "aquacultureArea", disable: ["Arable", "Horticulture", "Greenhouse", "Meat-poultry", "Meat-cow", "Meat-pig", "Milk", "Bees", "Silos"] },
    { field: "datsUsed", disable: [] },
    { field: "cultivationYear", disable: [] },
    { field: "startMonth", disable: ["Silos"] },
    { field: "endMonth", disable: ["Silos"] },
    { field: "productType", disable: [] },
    { field: "numberOfEmployees", disable: [] },
    { field: "numberOfFulltimeEmployees", disable: [] },
    { field: "numberOfSeasonalEmployees", disable: [] },
    { field: "waterPrice", disable: ["Oyster", "Bees", "Silos"] },
    { field: "fuelPrice", disable: [] },
    { field: "electricityPrice", disable: ["Oyster", "Bees"] },
    { field: "averageSalary", disable: [] },
    { field: "averageProfessionalSalary", disable: [] },
    { field: "productMarketPrice", disable: ["Arable", "Horticulture", "Greenhouse", "Meat-poultry", "Meat-cow", "Meat-pig", "Milk", "Bees", "Oyster"] },
    { field: "cropMarketPrice", disable: ["Meat-poultry", "Meat-cow", "Meat-pig", "Milk", "Bees", "Oyster", "Silos"] },
    { field: "meatMarketPrice", disable: ["Arable", "Horticulture", "Greenhouse", "Milk", "Bees", "Oyster", "Silos"] },
    { field: "milkMarketPrice", disable: ["Arable", "Horticulture", "Greenhouse", "Meat-poultry", "Meat-cow", "Meat-pig", "Bees", "Oyster", "Silos"] },
    { field: "oysterMarketPrice", disable: ["Arable", "Horticulture", "Greenhouse", "Meat-poultry", "Meat-cow", "Meat-pig", "Milk", "Bees", "Silos"] },
    { field: "honeyMarketPrice", disable: ["Arable", "Horticulture", "Greenhouse", "Meat-poultry", "Meat-cow", "Meat-pig", "Milk", "Oyster", "Silos"] },
    { field: "totalWaterUsage", disable: ["Oyster", "Bees", "Silos"] },
    { field: "waterUsageForIrrigation", disable: ["Meat-poultry", "Meat-cow", "Meat-pig", "Milk", "Oyster", "Bees", "Silos"] },
    { field: "waterUsageForFertigation", disable: ["Meat-poultry", "Meat-cow", "Meat-pig", "Milk", "Oyster", "Bees", "Silos"] },
    { field: "waterUsageForPestDilution", disable: ["Meat-poultry", "Meat-cow", "Meat-pig", "Milk", "Oyster", "Bees", "Silos"] },
    { field: "waterUsageForCleaning", disable: ["Arable", "Horticulture", "Greenhouse", "Oyster", "Bees", "Silos"] },
    { field: "waterUsageForDrinking", disable: ["Arable", "Horticulture", "Greenhouse", "Oyster", "Bees", "Silos"] },
    { field: "totalFuelUsage", disable: [] },
    { field: "fuelUsageForFertilisation", disable: ["Meat-poultry", "Meat-cow", "Meat-pig", "Milk", "Oyster", "Bees", "Silos"] },
    { field: "fuelUsageForPesticides", disable: ["Meat-poultry", "Meat-cow", "Meat-pig", "Milk", "Oyster", "Bees", "Silos"] },
    { field: "fuelUsageForIrrigation", disable: ["Meat-poultry", "Meat-cow", "Meat-pig", "Milk", "Oyster", "Bees", "Silos"] },
    { field: "fuelUsageForSowing", disable: ["Meat-poultry", "Meat-cow", "Meat-pig", "Milk", "Oyster", "Bees", "Silos"] },
    { field: "fuelUsageForPruning", disable: ["Meat-poultry", "Meat-cow", "Meat-pig", "Milk", "Oyster", "Bees", "Silos"] },
    { field: "fuelUsageForTemperatureHumidityControl", disable: ["Arable", "Horticulture", "Meat-poultry", "Meat-cow", "Meat-pig", "Milk", "Oyster", "Bees", "Silos"] },
    { field: "fuelUsageForBeehivesVisits", disable: ["Arable", "Horticulture", "Greenhouse", "Meat-poultry", "Meat-cow", "Meat-pig", "Milk", "Oyster", "Silos"] },
    { field: "fuelUsageForTransportingOysters", disable: ["Arable", "Horticulture", "Greenhouse", "Meat-poultry", "Meat-cow", "Meat-pig", "Milk", "Bees", "Silos"] },
    { field: "fuelUsageForMilking", disable: ["Arable", "Horticulture", "Greenhouse", "Meat-poultry", "Meat-pig", "Oyster", "Bees", "Silos"] },
    { field: "fuelUsageForFeeding", disable: ["Arable", "Horticulture", "Greenhouse", "Bees", "Silos"] },
    { field: "totalElectricityUsage", disable: ["Oyster", "Bees"] },
    { field: "electricityUsageForTemperatureHumidityControl", disable: ["Arable", "Horticulture", "Meat-poultry", "Meat-cow", "Meat-pig", "Milk", "Oyster", "Bees", "Silos"] },
    { field: "electricityUsageForIrrigation", disable: ["Meat-poultry", "Meat-cow", "Meat-pig", "Milk", "Oyster", "Bees", "Silos"] },
    { field: "electricityUsageForMilking", disable: ["Arable", "Horticulture", "Greenhouse", "Meat-poultry", "Meat-pig", "Oyster", "Bees", "Silos"] },
    { field: "electricityUsageForHeatDetection", disable: ["Arable", "Horticulture", "Greenhouse", "Oyster", "Bees", "Silos"] },
    { field: "electricityUsageForCalvingDetection", disable: ["Arable", "Horticulture", "Greenhouse", "Meat-poultry", "Oyster", "Bees", "Silos"] },
    { field: "electricityUsageForFeeding", disable: ["Arable", "Horticulture", "Greenhouse", "Oyster", "Bees", "Silos"] },
    { field: "fuelForTemperatureControlInformation", disable: ["Arable", "Horticulture", "Meat-poultry", "Meat-cow", "Meat-pig", "Milk", "Oyster", "Bees", "Silos"] },
    { field: "pesticidesUsageInformation", disable: ["Meat-poultry", "Meat-cow", "Meat-pig", "Milk", "Oyster", "Bees", "Silos"] },
    { field: "fertilizersUsageInformation", disable: ["Meat-poultry", "Meat-cow", "Meat-pig", "Milk", "Oyster", "Bees", "Silos"] },
    { field: "feedUsageInformation", disable: ["Arable", "Horticulture", "Greenhouse", "Silos"] },
    { field: "drugsUsageInformation", disable: ["Arable", "Horticulture", "Greenhouse", "Silos"] },
    { field: "labourForIrrigation", disable: ["Meat-poultry", "Meat-cow", "Meat-pig", "Milk", "Oyster", "Bees", "Silos"] },
    { field: "labourForPesticides", disable: ["Meat-poultry", "Meat-cow", "Meat-pig", "Milk", "Oyster", "Bees", "Silos"] },
    { field: "labourForFertilisation", disable: ["Meat-poultry", "Meat-cow", "Meat-pig", "Milk", "Oyster", "Bees", "Silos"] },
    { field: "labourForSowingOrPlanting", disable: ["Meat-poultry", "Meat-cow", "Meat-pig", "Milk", "Oyster", "Bees", "Silos"] },
    { field: "labourForPruning", disable: ["Meat-poultry", "Meat-cow", "Meat-pig", "Milk", "Oyster", "Bees", "Silos"] },
    { field: "labourForFieldVisits", disable: ["Meat-poultry", "Meat-cow", "Meat-pig", "Milk", "Bees", "Silos"] },
    { field: "labourForGreenhouseManagement", disable: ["Arable", "Horticulture", "Meat-poultry", "Meat-cow", "Meat-pig", "Milk", "Oyster", "Bees", "Silos"] },
    { field: "labourForQuantityTracking", disable: ["Arable", "Horticulture", "Greenhouse", "Meat-poultry", "Meat-cow", "Meat-pig", "Milk", "Oyster", "Bees"] },
    { field: "labourForGrainQualityAssessment", disable: ["Arable", "Horticulture", "Greenhouse", "Meat-poultry", "Meat-cow", "Meat-pig", "Milk", "Oyster", "Bees"] },
    { field: "labourForControllingPricesAndQuantities", disable: ["Arable", "Horticulture", "Greenhouse", "Meat-poultry", "Meat-cow", "Meat-pig", "Milk", "Oyster", "Bees"] },
    { field: "labourForOrganisingLogistics", disable: ["Arable", "Horticulture", "Greenhouse", "Meat-poultry", "Meat-cow", "Meat-pig", "Milk", "Oyster", "Bees"] },
    { field: "labourForCleaning", disable: ["Arable", "Horticulture", "Greenhouse", "Oyster", "Bees", "Silos"] },
    { field: "labourForStableVisits", disable: ["Arable", "Horticulture", "Greenhouse", "Oyster", "Bees", "Silos"] },
    { field: "labourForHeatDetection", disable: ["Arable", "Horticulture", "Greenhouse", "Oyster", "Bees", "Silos"] },
    { field: "labourForCalvingDetection", disable: ["Arable", "Horticulture", "Greenhouse", "Meat-poultry", "Oyster", "Bees", "Silos"] },
    { field: "labourForPigstyManagement", disable: ["Arable", "Horticulture", "Greenhouse", "Meat-poultry", "Meat-cow", "Milk", "Oyster", "Bees", "Silos"] },
    { field: "labourForMilking", disable: ["Arable", "Horticulture", "Greenhouse", "Meat-poultry", "Meat-cow", "Meat-pig", "Oyster", "Bees", "Silos"] },
    { field: "labourForMilkQualityAssessment", disable: ["Arable", "Horticulture", "Greenhouse", "Meat-poultry", "Meat-cow", "Meat-pig", "Oyster", "Bees", "Silos"] },
    { field: "labourForFeeding", disable: ["Arable", "Horticulture", "Greenhouse", "Oyster", "Bees", "Silos"] },
    { field: "labourForBeehiveVisits", disable: ["Arable", "Horticulture", "Greenhouse", "Meat-poultry", "Meat-cow", "Meat-pig", "Milk", "Oyster", "Silos"] },
    { field: "labourForOysterSampling", disable: ["Arable", "Horticulture", "Greenhouse", "Meat-poultry", "Meat-cow", "Meat-pig", "Milk", "Bees", "Silos"] },
    { field: "labourForOysterTransportation", disable: ["Arable", "Horticulture", "Greenhouse", "Meat-poultry", "Meat-cow", "Meat-pig", "Milk", "Bees", "Silos"] },
    { field: "labourForHarvesting", disable: ["Meat-poultry", "Meat-cow", "Meat-pig", "Milk", "Bees", "Silos"] },
    { field: "labourForStorage", disable: ["Arable", "Horticulture", "Greenhouse", "Meat-poultry", "Meat-cow", "Meat-pig", "Milk", "Bees"] },
    { field: "labourForAdministration", disable: [] },
    { field: "numberOfFulfilledOrders", disable: ["Arable", "Horticulture", "Greenhouse", "Meat-poultry", "Meat-cow", "Meat-pig", "Milk", "Oyster", "Bees"] },
    { field: "numberOfOrdersReceived", disable: ["Arable", "Horticulture", "Greenhouse", "Meat-poultry", "Meat-cow", "Meat-pig", "Milk", "Oyster", "Bees"] },
    { field: "numberOfWrongOrders", disable: ["Arable", "Horticulture", "Greenhouse", "Meat-poultry", "Meat-cow", "Meat-pig", "Milk", "Oyster", "Bees"] },
    { field: "additionalRevenues", disable: ["Arable", "Horticulture", "Greenhouse", "Meat-poultry", "Meat-cow", "Meat-pig", "Milk", "Oyster", "Bees", "Silos"] },
    { field: "percentageProteinInDryMatter", disable: ["Meat-poultry", "Meat-cow", "Meat-pig", "Milk", "Oyster", "Bees", "Silos"] },
    { field: "humidity", disable: ["Meat-poultry", "Meat-cow", "Meat-pig", "Milk", "Oyster", "Bees", "Silos"] },
    { field: "testWeight", disable: ["Meat-poultry", "Meat-cow", "Meat-pig", "Milk", "Oyster", "Bees", "Silos"] },
    { field: "cropProduction", disable: ["Meat-poultry", "Meat-cow", "Meat-pig", "Milk", "Oyster", "Bees", "Silos"] },
    { field: "milkProduction", disable: ["Arable", "Horticulture", "Greenhouse", "Meat-poultry", "Meat-cow", "Meat-pig", "Oyster", "Bees", "Silos"] },
    { field: "meatProduction", disable: ["Arable", "Horticulture", "Greenhouse", "Milk", "Oyster", "Bees", "Silos"] },
    { field: "oysterProduction", disable: ["Arable", "Horticulture", "Greenhouse", "Meat-poultry", "Meat-cow", "Meat-pig", "Milk", "Bees", "Silos"] },
    { field: "honeyProduction", disable: ["Arable", "Horticulture", "Greenhouse", "Meat-poultry", "Meat-cow", "Meat-pig", "Milk", "Oyster", "Silos"] },
    { field: "silosProduction", disable: ["Arable", "Horticulture", "Greenhouse", "Meat-poultry", "Meat-cow", "Meat-pig", "Milk", "Oyster", "Bees"] },
    { field: "numberOfDeathAnimals", disable: ["Arable", "Horticulture", "Greenhouse", "Silos"] },
    { field: "calvesDiedInFirst24Hours", disable: ["Arable", "Horticulture", "Greenhouse", "Meat-poultry", "Oyster", "Bees", "Silos"] },
    { field: "totalNumberOfCalvesBorn", disable: ["Arable", "Horticulture", "Greenhouse", "Meat-poultry", "Oyster", "Bees", "Silos"] },
    { field: "numberOfDaysWithPastureAccess", disable: ["Arable", "Horticulture", "Greenhouse", "Meat-poultry", "Meat-pig", "Oyster", "Bees", "Silos"] },
    { field: "outdoorLoafingArea", disable: ["Arable", "Horticulture", "Greenhouse", "Meat-poultry", "Meat-pig", "Oyster", "Bees", "Silos"] },
    { field: "herdSize", disable: ["Arable", "Horticulture", "Greenhouse", "Meat-poultry", "Meat-cow", "Meat-pig", "Milk", "Oyster", "Bees", "Silos"] },
    { field: "numberOfCowsWithHighSCCMilk", disable: ["Arable", "Horticulture", "Greenhouse", "Meat-poultry", "Meat-pig", "Oyster", "Bees", "Silos"] },
    { field: "numberOfNewInjuryCases", disable: [] },
    { field: "totalNumberOfLostWorkingHours", disable: [] },
    { field: "totalNumberOfWorkingHours", disable: [] },
    { field: "numberOfWorkingWeeks", disable: [] },
    { field: "numberOfNewLocalEmployeesHired", disable: [] },
    { field: "numberOfNewEmployeesHired", disable: [] },
    { field: "additionalFieldsInformation", disable: [] },

    //ui fields
    { field: "_ui.waterTitle", disable: ["Oyster", "Bees", "Silos"] },
    { field: "_ui.waterTotal", disable: ["Oyster", "Bees", "Silos"] },
    { field: "_ui.waterActivity", disable: ["Oyster", "Bees", "Silos"] },
    { field: "_ui.electricityTitle", disable: ["Oyster", "Bees"] },
    { field: "_ui.electricityTotal", disable: ["Oyster", "Bees"] },
    { field: "_ui.electricityActivity", disable: ["Oyster", "Bees", "Silos"] },
    { field: "_ui.fuelActivity", disable: ["Silos"] },
    { field: "_ui.performanceTitle", disable: ["Meat-poultry", "Meat-cow", "Meat-pig", "Milk", "Oyster", "Bees"] },
    { field: "_ui.animalTitle", disable: ["Arable", "Horticulture", "Greenhouse", "Silos"] },

];

const defObj = {
    testcaseNumber: 0, testcaseLeader: "", cultivationType: "", datsInformation: [],
    yearlyAssessmentInformation: [
        {
            cultivationYear: 2023,
            parcelComparison: [{
                parcelAssessmentWithDATS: {},
                parcelAssessmentWithoutDATS: {}
            }]
        },
        {
            cultivationYear: 2024,
            parcelComparison: []
        },
        {
            cultivationYear: 2025,
            parcelComparison: []
        }
    ]
}; // default empty object

const emptyPC = { parcelAssessmentWithDATS: {}, parcelAssessmentWithoutDATS: {} };


