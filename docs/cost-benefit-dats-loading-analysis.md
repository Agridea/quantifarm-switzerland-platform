# Cost-Benefit DATs Loading Analysis for tool2.html

## 🎯 Overview

> **⚠️ Correction (2026-09-11)**: An earlier version of this document incorrectly claimed that the **tool2.html** DAT tree (`/dat_tree` sidebar) is served from the Triple Store. Code review of `packages/cost-benefit-calculator-v1` and `-v2` shows this is **not** the case. There are actually **two independent pipelines** that both happen to involve "Cost-Benefit DATs", and they must not be confused:
>
> 1. **Excel → DATs Loader → Triple Store** (documented in sections 1-3 below): Reads `cost-benefit-arable-dats.xls` / `cost-benefit-lifestock-dats.xls`, tags matching DATs in the Triple Store with `qcsm:hasSource "costbenefit"` and adds cost metadata. This is consumed by the **Recommendation Tool (tool1.html)** to show the calculator icon (see [js/datinfo.js](../packages/toolkit-dashboard/js/datinfo.js) `GetCostBenefitData()`), which links out to `tool2.html`. It does **not** feed the tool2.html sidebar tree itself.
> 2. **Excel/CSV → PostgreSQL → Cost-Benefit Calculator API (v1 & v2)** (documented in the new section 4 below): The actual DAT tree shown in **tool2.html**'s sidebar (`/dat_tree` endpoint) is read directly from each calculator's own PostgreSQL database (`ws_cost_benefit_calculator` schema), which was seeded from separate Excel/CSV files. There is **no runtime connection to the Triple Store or quantifarm.eu** in this path.
>
> Sections 1-3 remain accurate for pipeline 1. Section 4 has been corrected to describe pipeline 2 accurately.

This document analyzes how Cost-Benefit DAT metadata is loaded from Excel files into the Triple Store (pipeline 1), and separately, how the **tool2.html** Cost & Benefit Calculator interface actually sources its DAT tree data from PostgreSQL (pipeline 2).

---

## 📊 Data Flow Architecture

**Pipeline 1 - DAT metadata tagging (feeds the tool1.html calculator icon/link only):**
```
Excel Files (dats-loader) → DATs Loader → Triple Store (hasSource="costbenefit") → Recommendation Tool API → tool1.html icon → link to tool2.html
```

**Pipeline 2 - Actual tool2.html DAT tree (sidebar content):**
```
Excel/CSV Files (test_data/) → manual import → PostgreSQL (per API version) → Cost-Benefit API (v1 & v2) /dat_tree → tool2.php → tool2.js → tool2.html
```

---

## 1️⃣ Source Data: Excel Files

### Input Files
Located in: `packages/data-platform/dats-loader/`

1. **`cost-benefit-arable-dats.xls`** - Crop/Arable farming DATs
2. **`cost-benefit-lifestock-dats.xls`** - Livestock farming DATs

### Excel Structure (Sheet 0)
The loader reads from **row 2 onwards** (row 0 = headers, row 1 = skipped):

| Col | Field | Description | Used For |
|-----|-------|-------------|----------|
| 0 | ID | Unique identifier | Reference |
| 3 | **DAT Name** | Technology name | URI generation, Label |
| 4 | **Provider Name** | Company/organization | Provider triples |
| 5 | **Description** | Detailed description | `rdfs:comment`, `qcsm:hasDescription` |
| 6 | **Web Page** | URL | `qcsm:hasWebPage` |
| 8 | **Cultivation Types** | Crop or livestock types | Sector targeting |
| 9 | **Min Initial Costs** | Minimum investment | `qcsm:hasMinimumInitialCosts` |
| 10 | **Max Initial Costs** | Maximum investment | `qcsm:hasMaximumInitialCosts` |
| 11 | **Initial Cost Item** | Cost unit (e.g., "ha", "farm") | `qcsm:hasInitialCostItem` |
| 12 | **Annual Fee** | Recurring cost | `qcsm:hasAnnualFeePerItem` |
| 13 | **Annual Fee Item** | Fee unit | `qcsm:hasAnnualFeeItem` |
| 18 | **Functionalities** | Comma-separated functions | `qcsm:hasFunctionality` |
| 21 | **Digital Forms** | Delivery methods | `qcsm:hasDigitalForm` |
| 22 | **Benefits** | Comma-separated benefits | `qcsm:hasBenefits` |

---

## 2️⃣ ETL Process: DATs Loader

### Code Location
`packages/data-platform/dats-loader/dats_loader/__main__.py` (lines 300-420)

### Processing Logic

```python
filenames = [COST_BENEFIT_ARABLE_FILE_PATH, COST_BENEFIT_LIFESTOCK_FILE_PATH]
for file in filenames:
    wb = open_workbook(file)
    sh = wb.sheet_by_index(0)  # Read first sheet
    for rx in range(sh.nrows):
        if rx > 1:  # Skip header rows
            # Process each row
```

### Key Processing Steps

#### Step 1: DAT URI Generation
```python
dat_name = sh.cell_value(rx,3).replace(" ","_").lower()
dat = data_namespace[f"dats/{dat_name}"]
```
- Converts DAT name to lowercase
- Replaces spaces with underscores
- Creates URI: `https://quantifarm.eu/data/dats/{dat_name}`

#### Step 2: Deduplication Check
```python
if dat not in dat_uris:
    # Create new DAT with full metadata
else:
    # Enrich existing DAT with additional metadata
```

**New DAT**: Add all RDF triples (name, provider, costs, sectors, etc.)

**Existing DAT** (from FAIRshare/Test Cases): Only add:
- Additional functionalities
- Additional digital forms
- Additional benefits

#### Step 3: Sector Differentiation

**For Arable/Crop DATs** (`cost-benefit-arable-dats.xls`):
```python
if cultivation_type == "All" or cultivation_type == "Arable":
    cultivation_type = "Arable farming"
g.add((dat, QCSM.canBeUsedToCultivateCropType, Literal(cultivation_type)))
g.add((dat, QCSM.isTargetedTowardsAgriculturalSector, Literal(cultivation_type)))
```

**For Livestock DATs** (`cost-benefit-lifestock-dats.xls`):
```python
if cultivation_type == "All":
    cultivation_type = "Livestock"
g.add((dat, QCSM.canBeUsedToCultivateLifestockType, Literal(cultivation_type)))
g.add((dat, QCSM.isTargetedTowardsAgriculturalSector, Literal(cultivation_type)))
```

#### Step 4: Cost Structure Generation

Dynamic cost structure description:
```python
if sh.cell_value(rx,10) > 0:  # Has max initial cost
    value = "Initial investment costs"
    if sh.cell_value(rx,11) != "none":
        value = value + " per " + sh.cell_value(rx,11)
    if sh.cell_value(rx,12) > 0:  # Has annual fee
        value = value + " and Annual fee"
        if sh.cell_value(rx,13) != "none":
            value = value + " per " + sh.cell_value(rx,13)
else:
    if sh.cell_value(rx,12) > 0:
        value = "Annual fee"
        if sh.cell_value(rx,13) != "none":
            value = value + " per " + sh.cell_value(rx,13)

g.add((dat, QCSM.hasCostStructure, Literal(value)))
```

**Example outputs**:
- `"Initial investment costs per ha"`
- `"Initial investment costs per ha and Annual fee per ha"`
- `"Annual fee per farm"`

#### Step 5: Metadata Parsing

**Functionalities** (Column 18):
```python
functionalities = [function.strip().capitalize() for function in sh.cell_value(rx,18).split(",")]
for function in functionalities:
    g.add((dat, QCSM.hasFunctionality, Literal(function)))
```

**Digital Forms** (Column 21):
```python
deliveries = [d.strip().capitalize() for d in sh.cell_value(rx,21).split(",")]
for delivery in deliveries:
    g.add((dat, QCSM.hasDigitalForm, Literal(delivery)))
```

**Benefits** (Column 22):
```python
benefits = [b.strip().capitalize() for b in sh.cell_value(rx,22).split(",")]
for benefit in benefits:
    g.add((dat, QCSM.hasBenefits, Literal(benefit)))
```

#### Step 6: RDF Triple Generation

All DATs receive:
```python
g.add((dat, QCSM.hasSource, Literal("costbenefit")))
g.add((dat, RDF.type, QCSM.DigitalAgriculturalTechnology))
g.add((dat, RDFS.label, Literal(sh.cell_value(rx,3))))
g.add((dat, QCSM.hasTitle, Literal(sh.cell_value(rx,3))))
g.add((dat, RDFS.comment, Literal(sh.cell_value(rx,5))))
g.add((dat, QCSM.hasDescription, Literal(sh.cell_value(rx,5))))
g.add((dat, QCSM.hasWebPage, URIRef(sh.cell_value(rx,6))))
g.add((dat, QCSM.hasMinimumInitialCosts, Literal(sh.cell_value(rx,9), datatype=XSD.decimal)))
g.add((dat, QCSM.hasMaximumInitialCosts, Literal(sh.cell_value(rx,10), datatype=XSD.decimal)))
g.add((dat, QCSM.hasInitialCostItem, Literal(sh.cell_value(rx,11))))
g.add((dat, QCSM.hasAnnualFeePerItem, Literal(sh.cell_value(rx,12), datatype=XSD.decimal)))
g.add((dat, QCSM.hasAnnualFeeItem, Literal(sh.cell_value(rx,13))))
```

Provider information:
```python
provider = data_namespace[f"providers/{provider_name}"]
g.add((provider, RDF.type, QCSM.TechnologyProvider))
g.add((provider, S4AGRI.hasName, Literal(provider_name)))
g.add((dat, QCSM.hasProvider, provider))
```

---

## 3️⃣ Triple Store Storage

### Graph Location
- **Graph URI**: `https://quantifarm.eu/graphs/dats`
- **Endpoint**: `http://triple-store:3030/quantifarm/data`

### Storage Method
**Destructive Loading** - The entire graph is replaced via HTTP PUT:
```python
requests.put(
    graph_store_endpoint,
    params={"graph": GRAPH_NAME},
    headers={"Content-Type": "application/n-triples"},
    data=g.serialize(format="nt", encoding="utf-8"),
)
```

---

## 4️⃣ Cost-Benefit Calculator APIs *(corrected)*

### API Versions
The toolkit uses **two versions** of the Cost-Benefit Calculator, each with its **own PostgreSQL database** (no shared Triple Store access):

#### Version 1
- **Purpose**: Original/commercial DAT calculations
- **Path**: `packages/cost-benefit-calculator-v1/`
- **Container/DB**: `quantifarm-cost-benefit-calculator-v1-tool-postgresql` (Postgres, port 5558 host / 5432 internal)
- **API container**: `quantifarm-cost-benefit-calculator-v1-tool-api` (port 8686 internal, 8688 host)
- **Used for**: Generic crop and livestock calculations

**Note**: Referenced from `tool2.php` as `version: 1`.

#### Version 2
- **Purpose**: Test Case specific calculations
- **Path**: `packages/cost-benefit-calculator-v2/`
- **Container/DB**: `quantifarm-cost-benefit-calculator-v2-tool-postgresql` (Postgres, port 5559 host / 5432 internal)
- **API container**: `quantifarm-cost-benefit-calculator-v2-tool-api` (port 8686 internal, 8687 host)
- **Used for**: TC-specific calculations (cropTC and livestockTC)

### Key API Endpoint: `/dat_tree` - implementation

Unlike originally documented, this endpoint does **not** query the Triple Store. It runs plain SQL against the API's own PostgreSQL schema `ws_cost_benefit_calculator`.

Implementation in `packages/cost-benefit-calculator-v2/volume/fastapi-app/app/source/classes/amModel.py` (identical logic in v1):

```python
async def getCultivationDATTree(self, cultivation_type):
    # 1. Get all distinct DAT names used for this cultivation type
    cultivationDataset = await self.getTableData(cultivation_type)  # SELECT * FROM crop|livestock
    myDATs = [row["datss_name"] for row in cultivationDataset if row["datss_name"] not in myDATs]

    # 2. Get full DAT rows for those names
    cultivationDataset = await self.getTableData("dat", {"column": "datss_name", "value": "'...'"}, operator="in")

    # 3. Build a nested tree: category -> tc_name_title -> test_case_number -> tc_country -> crop/animal type -> [dat names]
    myDATTree = self.get_tree_from_object(cultivationDataset, [
        "dats_category", "tc_name_title", "test_case_number", "tc_country", "crop_or_animal_type"
    ])
    return myDATTree
```

`getTableData()` executes a parameterized `SELECT * FROM ws_cost_benefit_calculator.<table>` via `psycopg2` against the local Postgres instance - **no HTTP/SPARQL call to the Triple Store or quantifarm.eu happens here**.

### How the PostgreSQL tables are populated

There is **no automated loader** for this data (unlike the `dats-loader` in `packages/data-platform`). The `dat`, `crop`, and `livestock` tables were seeded from Excel/CSV source files kept in each package's `test_data/` folder, e.g.:
- `test_data/C&B_tool_V1_Literature Review DATs - Crop DATS.xlsx`
- `test_data/C&B_tool_V1_Literature Review DATs - Livestock DATS.xlsx`
- `test_data/DATS_list_fixed.csv`, `test_data/DATS_livestock.csv`, various `Z_*.csv`

These were imported manually/one-off (e.g. via the API's generic `/administration` and add-data endpoints described in the package README), not via a scheduled or code-driven ETL job, and not from `quantifarm.eu`.

---

## 5️⃣ Backend Integration: tool2.php

### Location
`packages/toolkit-dashboard/php/tool2.php`

### Version Selection Logic
```php
$version = $req->version;
$baseURL = 'http://localhost:8688';  // Default: Version for comercial Dat's
if($version == 2) $baseURL = 'http://localhost:8687';  // Version 2 for TCs
```

### API Call Routing
```php
case '/dat_tree':
    $url = $baseURL . $path . '?' . http_build_query($data);
    $res = CallAPI('GET', $url, null);
    break;
```

**Parameters**:
- `myDatType`: Type of DATs to retrieve (`crop`, `livestock`, `cropTC`, `livestockTC`)
- `version`: API version (1 or 2)

---

## 6️⃣ Frontend Integration: tool2.js & tool2.html

### Location
- `packages/toolkit-dashboard/js/tool2.js`
- `packages/toolkit-dashboard/tool2.html`

### Data Types
```javascript
const crop = "crop";              // Arable/Crop DATs (v1)
const live = "livestock";         // Livestock DATs (v1)
const cropTC = "cropTC";          // Test Case Crop DATs (v2)
const liveTC = "livestockTC";     // Test Case Livestock DATs (v2)
```

### Data Loading Process

#### Initial Load (lines 99-130)
```javascript
function LoadData() {
    // Load Crop DATs (Version 1)
    par = {
        "path": "/dat_tree",
        "data": { "myDatType": crop },
        "version": 1
    };
    CallAPI(apiURL, par, (data) => { 
        dataTree[crop] = data; 
        IndexTree(data, crop); 
    }, div1, "");

    // Load Livestock DATs (Version 1)
    par = {
        "path": "/dat_tree",
        "data": { "myDatType": live },
        "version": 1
    };
    CallAPI(apiURL, par, (data) => { 
        dataTree[live] = data; 
        IndexTree(data, live); 
    }, div2, "");

    // Load Crop TC DATs (Version 2)
    par = {
        "path": "/dat_tree",
        "data": { "myDatType": crop },
        "version": 2
    };
    CallAPI(apiURL, par, (data) => { 
        dataTree[cropTC] = data; 
        IndexTree(data, cropTC); 
    }, div3, "");

    // Load Livestock TC DATs (Version 2)
    par = {
        "path": "/dat_tree",
        "data": { "myDatType": live },
        "version": 2
    };
    CallAPI(apiURL, par, (data) => { 
        dataTree[liveTC] = data; 
        IndexTree(data, liveTC); 
    }, div4, "");
}
```

### Calculation Modules Mapping

The system maps different cultivation types to specific calculation modules:

```javascript
const modulesMap = {
    // Crop types
    arable:     [],
    fruits:     [],
    vineyards:  [],
    vegetables: [],
    orchards:   [],
    
    // Livestock types
    cattle :        ["livestock_calc_water_usage", "livestock_calc_mortality_cost"],
    pigs:           ["livestock_calc_milk_yield", "livestock_calc_water_usage", ...],
    poultry:        ["livestock_calc_milk_yield", "livestock_calc_energy_cost", ...],
    small_ruminants:["livestock_calc_water_usage", "livestock_calc_profit_per_animal", ...],
    
    // Test Cases
    TC2:    ["cropTC_calc_fertilizer", "cropTC_calc_pesticide", "cropTC_calc_fuel"],
    TC3:    ["cropTC_calc_water", "cropTC_calc_electricity"],
    // ... more TCs
    TC22:   ["livestockTC_calc_oyster", "livestockTC_calc_honey", ...],
    TC23:   ["livestockTC_calc_oyster", "livestockTC_calc_honey", ...],
    // ... more TCs
};
```

---

## 7️⃣ Complete Data Flow Example

### Example: Loading "Precision Irrigation" DAT

1. **Excel File** (`cost-benefit-arable-dats.xls`):
   ```
   Row 5:
   [3] = "Precision Irrigation System"
   [4] = "IrrigationTech Ltd"
   [5] = "Automated irrigation system with soil moisture sensors"
   [8] = "Arable, Vegetables"
   [9] = 5000  (min cost)
   [10] = 15000 (max cost)
   [11] = "ha"
   [18] = "Water management, Precision irrigation"
   [21] = "Stand-alone software, Mobile app"
   [22] = "Water saving, Yield improvement"
   ```

2. **DATs Loader** processes row:
   ```python
   dat_name = "precision_irrigation_system"
   dat = <https://quantifarm.eu/data/dats/precision_irrigation_system>
   ```
   
   Creates RDF triples:
   ```turtle
   <dat> rdf:type qcsm:DigitalAgriculturalTechnology .
   <dat> rdfs:label "Precision Irrigation System" .
   <dat> qcsm:hasSource "costbenefit" .
   <dat> qcsm:hasMinimumInitialCosts "5000"^^xsd:decimal .
   <dat> qcsm:hasMaximumInitialCosts "15000"^^xsd:decimal .
   <dat> qcsm:hasInitialCostItem "ha" .
   <dat> qcsm:hasCostStructure "Initial investment costs per ha" .
   <dat> qcsm:canBeUsedToCultivateCropType "Arable" .
   <dat> qcsm:canBeUsedToCultivateCropType "Vegetables" .
   <dat> qcsm:hasFunctionality "Water management" .
   <dat> qcsm:hasFunctionality "Precision irrigation" .
   <dat> qcsm:hasDigitalForm "Stand-alone software" .
   <dat> qcsm:hasDigitalForm "Mobile app" .
   <dat> qcsm:hasBenefits "Water saving" .
   <dat> qcsm:hasBenefits "Yield improvement" .
   ```

3. **Triple Store** stores in graph `https://quantifarm.eu/graphs/dats`. This is used by the **Recommendation Tool (tool1.html)** to show the calculator icon/link for this DAT - it is **not** the source of the tool2.html sidebar tree.

> **Corrected step 4 onwards** (actual tool2.html data path, independent of the Triple Store):

4. **PostgreSQL** (`ws_cost_benefit_calculator.dat` / `.crop` / `.livestock` tables, seeded separately from `test_data/*.xlsx`/`*.csv`) holds the row for `precision_irrigation_system`.

5. **Cost-Benefit API (v1 or v2)** `/dat_tree` endpoint queries **PostgreSQL directly via SQL** (`amModel.getCultivationDATTree`) and returns a tree, e.g.:
   ```json
   {
     "Arable": {
       "Water management": {
         "Precision Irrigation System": {
           "id": "precision_irrigation_system",
           "name": "Precision Irrigation System",
           "provider": "IrrigationTech Ltd",
           "costs": {
             "min": 5000,
             "max": 15000,
             "item": "ha"
           }
         }
       }
     }
   }
   ```

6. **tool2.php** proxies the request from frontend to the correct API version container

7. **tool2.js** receives data and populates UI tree

8. **tool2.html** displays interactive tree where users can:
   - Browse by cultivation type
   - Filter by functionality
   - Select DATs for cost-benefit analysis
   - Input farm parameters (hectares, animal count, etc.)
   - Calculate cost savings and benefits

---

## 🔑 Key Design Decisions

### 1. **Source Attribution**
All Cost-Benefit DATs are tagged with:
```python
g.add((dat, QCSM.hasSource, Literal("costbenefit")))
```
This allows tracking which DATs come from the Cost-Benefit calculators vs. FAIRshare or Test Cases.

### 2. **Enrichment Strategy**
When a DAT already exists (from FAIRshare), the Cost-Benefit loader **enriches** it with:
- Additional functionalities
- Additional digital forms
- Additional benefits
- Cost information (which FAIRshare often lacks)

### 3. **Sector Specialization**
The loader creates **two distinct properties** for cultivation types:
- `qcsm:canBeUsedToCultivateCropType` - For crop DATs
- `qcsm:canBeUsedToCultivateLifestockType` - For livestock DATs

### 4. **Cost Structure Flexibility**
The dynamic cost structure string accommodates:
- DATs with only initial costs
- DATs with only annual fees
- DATs with both
- Different cost units (ha, farm, animal, etc.)

### 5. **Dual API Architecture**
Using two API versions allows:
- **v1**: Generic calculations based on cultivation type
- **v2**: Test Case specific calculations with predefined parameters

---

## 📋 Summary *(corrected)*

There are **two separate loading processes**, and only one of them powers tool2.html:

**Pipeline 1 - Triple Store metadata tagging** (sections 1-3):
1. **Extracts** DAT metadata from `dats-loader` Excel files with cost information
2. **Transforms** data into QCSM-compliant RDF triples
3. **Loads** into the central Triple Store's DATs graph, tagged `hasSource="costbenefit"`
4. **Enriches** existing DATs from other sources (FAIRshare, Test Cases)
5. **Powers** only the calculator icon/link shown in **tool1.html** (Recommendation Tool)

**Pipeline 2 - Cost-Benefit Calculator databases** (section 4, actually powers tool2.html):
1. Each API version (v1, v2) has its **own PostgreSQL database**, seeded once from Excel/CSV files in `test_data/`
2. The `/dat_tree` endpoint queries **PostgreSQL directly via SQL** - no Triple Store or quantifarm.eu involved at runtime
3. **Serves** data through two independently-databased Cost-Benefit Calculator APIs
4. **Powers** the tool2.html interface for farmers to calculate ROI and benefits

This means cost-benefit information for tool2.html is:
- ❌ **Not** centrally stored in the Triple Store
- ❌ **Not** queryable via SPARQL
- ❌ **Not** loaded from quantifarm.eu at runtime
- ✅ Stored in two separate, independently-seeded PostgreSQL databases (v1 and v2)
- ✅ Specific to agricultural contexts (crops vs. livestock) and, for v2, Test Cases
