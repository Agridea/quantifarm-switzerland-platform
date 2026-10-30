# AI Context: TCreport Data Flow

## 🎯 Purpose
Documents how the test case report page (`tcreport.html`) loads and displays assessment data for each of the 30 QuantiFarm test cases. Covers the three data sources (static JS, static images, SPARQL/Triple Store), the full request chain, and common failure modes in production.

## 🏗️ Architecture Overview

`tcreport.html` renders a per-test-case dashboard with four tabs (2023, 2024, 2025, Three-year analysis). Data comes from **three independent sources**:

```
┌─────────────────────────────────────────────────────────────┐
│                     tcreport.html                           │
│                                                             │
│  ┌──────────────┐  ┌──────────────┐  ┌───────────────────┐  │
│  │ 2023 Tab     │  │ 2024 Tab     │  │ 2025/2026 Tabs    │  │
│  │ (Images)     │  │ (SPARQL)     │  │ (SPARQL)          │  │
│  └──────┬───────┘  └──────┬───────┘  └────────┬──────────┘  │
│         │                 │                    │             │
└─────────┼─────────────────┼────────────────────┼─────────────┘
          │                 │                    │
          ▼                 ▼                    ▼
   assets/img/        php/sparql.php        php/sparql.php
   TC{NN}-2023-*.png       │                     │
                           ▼                     ▼
                    http://triple-store:3030/quantifarm/query
                    (Apache Jena Fuseki SPARQL Endpoint)
```

## 📂 Key Files

| File | Role |
|------|------|
| `tcreport.html` | HTML structure: 4 tabs, accordion panels, chart containers |
| `js/tcreport.js` | **Main orchestrator**: reads URL param `?n=`, loads metadata from `testcasedata.js`, calls `LoadData()` for SPARQL queries |
| `js/testcasedata.js` | Hardcoded JS array of 30 test case definitions (sector, crop, country, DATs, coordinates) |
| `js/datinfo.js` | DAT detail modal: loads DAT metadata via `php/tool1.php` → Recommendation Tool |
| `js/app.js` | Shared utilities: `CallAPI()`, `baseURL` construction, language switching, `translateTcreport()` |
| `js/uistrings.js` | UI translation strings for DE/FR/IT |
| `php/sparql.php` | **SPARQL proxy**: receives `{path, data, language}`, builds 3 SPARQL queries, calls Fuseki |
| `php/app.php` | Config & helpers: `CallSPARQL()`, `sparqlURL = "http://triple-store:3030/quantifarm/query"` |

## 🔄 Data Sources & Loading

### Source 1: Static Metadata (`testcasedata.js`)

- **Loaded**: Automatically via `<script src="js/testcasedata.js">` in HTML `<head>`
- **Data**: `testCaseData` array with 30 objects, each containing:
  ```json
  { "id": 1, "sector": "Arable", "crop": "Potatoes",
    "dats": [{"name": "gaiasense", "id": "https://quantifarm.eu/data/dats/gaiasense"}],
    "country": "Greece", "partner": "NP" }
  ```
- **Used for**: Header fields (sector, crop/livestock, country, DAT names), download links for PDF reports
- **Always works** — no network dependency

### Source 2: 2023 Assessment Images

- **Loaded**: `Show2023()` in `tcreport.js` sets `innerHTML` to `<img>` tags pointing to:
  ```
  assets/img/TC{NN}-2023-1.png
  assets/img/TC{NN}-2023-2.png
  assets/img/TC{NN}-2023-3.png
  ```
  where `{NN}` = zero-padded test case number (e.g., `01`, `02`, ..., `30`)
- **Error handling**: `onerror="NoData(2023)"` hides the data div and shows "Data is expected"
- **Special cases**: TC12 and TC29 show only a download link for the PDF report (no impact images)

### Source 3: 2024/2025/2026 Data via SPARQL (Triple Store)

This is the **critical data path** that typically fails in production.

#### Request Chain

```
1. Browser (tcreport.js)
   └─ LoadData() called on page load
   └─ Constructs params: { path: "/tcdata", data: tcNum, language: lng }
   └─ POST to: {currentDir}/php/sparql.php  (via CallAPI in app.js)

2. PHP Proxy (sparql.php)
   └─ Receives: { path: "/tcdata", data: <1-30>, language: "de"|"fr"|"it"|"en" }
   └─ Maps language to SPARQL lang tag
   └─ Builds 3 SPARQL queries (q1, q2, q3) with placeholders:
      - {{NN}} → test case number (e.g., "7" → graph testcase7)
      - {{LANG}} → language tag (e.g., "de")
   └─ Calls CallSPARQL() for each query

3. CallSPARQL() (app.php)
   └─ cURL POST to: http://triple-store:3030/quantifarm/query
   └─ Content-Type: application/sparql-query
   └─ Body: raw SPARQL query string

4. Apache Jena Fuseki (triple-store:3030)
   └─ Executes SPARQL against named graphs
   └─ Returns JSON results

5. Response flows back:
   Fuseki → sparql.php (combines q1+q2+q3 into {q1, q2, q3}) → Browser
   └─ tcreport.js parses results and renders charts/tables
```

#### SPARQL Queries

All three queries follow the same pattern: query a per-testcase named graph, with optional translations from the translations graph.

**q1 — Main Impact Information** (KPI cards: costs, productivity, water, energy, etc.)
```sparql
SELECT DISTINCT ?year ?product ?name ?unit ?absDiff ?percDiff
                ?title ?subtitle ?higherIsBetter ?impactLevel
WHERE {
    GRAPH <https://quantifarm.eu/graphs/testcase{{NN}}> {
        ?uri rdf:type qcsm:Testcase .
        ?uri qcsm:hasYearlyAssessmentInformation ?info .
        ?info qcsm:hasCultivationYear ?year .
        ?info qcsm:hasParcelComparison ?comparison .
        ?comparison qcsm:hasMainImpactInformation ?indicatorInfo .
        # ... binds for name, unit, absDiff, percDiff, title, subtitle, etc.
    }
    OPTIONAL {
        GRAPH <https://quantifarm.eu/graphs/testcase-translations> {
            ?parcel qcsm:hasProductType ?productTr .
        }
        FILTER(lang(?productTr) = "{{LANG}}")
    }
    BIND(COALESCE(?productTr, ?productEn) as ?product)
}
```

**q2 — Cost & Revenue Impact** (monetary table)
- Same structure, queries `qcsm:hasCostRevenueImpactInformation`

**q3 — Aggregated Sustainability Impact** (bar chart)
- Same structure, queries `qcsm:hasAggregatedImpactInformation`
- 7 dimensions: cost efficiency, productivity, water, inputs, energy, CO2, labour

#### Named Graphs Used

| Graph URI | Content | Loader |
|-----------|---------|--------|
| `https://quantifarm.eu/graphs/testcase{N}` | Test case assessment data (N = 0–30) | `testcase-loader` |
| `https://quantifarm.eu/graphs/testcase-translations` | Translated vocabulary (@de/@fr/@it) | `translation-loader` |

**Note**: Graph names use **no zero-padding** (`testcase1`, not `testcase01`). The SPARQL template uses `{{NN}}` but the replacement value `$data` is the raw integer from the URL (1–30), so the graph name resolves correctly.

## ⚠️ Known Issue: URI vs Literal in Export/Import

### Problem (fixed)

The testcase export/import process (`testcase_loader/exporter.py` + `importer.py`) previously lost URI type information during round-tripping:

- **Exporter** saved all RDF objects as plain strings (`str(obj)`) without recording whether they were URIs or Literals
- **Importer** treated every object as `Literal()`, never as `URIRef()`

This caused connections between entities (e.g. `testcase → YearlyAssessmentInformation`) to be stored as literal strings instead of RDF URIs, breaking SPARQL queries that traverse the graph.

### Fix

Both `exporter.py` and `importer.py` now preserve the RDF node type:

- **Exporter** writes a `"type": "uri"` or `"type": "literal"` field for each triple
- **Importer** reads the `type` field and reconstructs `URIRef` vs `Literal` nodes faithfully
- **Legacy fallback**: Importer treats strings starting with `http://` or `https://` as URIs when no `type` field is present

### After fixing: Re-export and re-import

```bash
# 1. Export from local Fuseki (correct URIs)
cd packages/data-platform/testcase-loader
python -m testcase_loader.exporter

# 2. Import into production
TRIPLE_STORE_ENDPOINT=<prod-url> python -m testcase_loader.importer
```