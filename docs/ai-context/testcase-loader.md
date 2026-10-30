# AI Context: Testcase Loader

## 🎯 Purpose
Loads testcase data from JSON files into the Fuseki triple store, converting structured JSON (based on JSON schemas) into RDF triples following the QCSM ontology. Each testcase gets its own named graph.

## 🏗️ Architecture & Stack
- **Language/Framework**: Python 3.11 (CLI module, no web framework)
- **Database**: Apache Jena Fuseki (Triple Store) — writes testcase graphs
- **Key Dependencies**: `rdflib==7.0.0`, `requests==2.31.0`, `pandas==2.0.3`, `openpyxl==3.1.2`, `qcsm_namespaces` (shared common module)
- **Key Components**:
  - **JSON-to-RDF Converter**: Recursively walks nested JSON structures guided by JSON schemas, mapping fields to QCSM ontology classes and properties
  - **Graph Uploader**: PUTs each testcase as a named graph to Fuseki
  - **Schema-Driven Parsing**: Uses JSON Schema `$ref` references to determine class types and nested structures

## 📂 Key Files & Structure
```
packages/data-platform/testcase-loader/
├── Dockerfile                              # Python image, installs common + this module
├── README.md                               # Usage docs
├── setup.py                                # Package config (deps: rdflib, requests, pandas, openpyxl)
├── TC0.json ... TC30.json                  # Testcase data files (JSON)
├── json-schemas/                           # JSON Schema definitions for all testcase entity types
│   ├── Testcase.schema.json                # Root schema
│   ├── FarmInformation.schema.json
│   ├── ParcelInformation.schema.json
│   ├── AssessmentInformation.schema.json
│   ├── EconomicInformation.schema.json
│   ├── MainImpactInformation.schema.json
│   ├── CostRevenueImpactInformation.schema.json
│   └── ... (27 schemas total)
├── testcase-classes                        # Generated: list of discovered QCSM classes
├── testcase-properties                     # Generated: list of discovered QCSM properties
└── testcase_loader/
    ├── __init__.py
    ├── __main__.py                         # Entry point: iterates TC*.json files, calls loader
    ├── testcase_data_json_loader.py        # Core: recursive JSON→RDF conversion via schema walking
    └── testcase_indicator_excel_to_json_converter.py  # Utility: Excel → JSON conversion
```

### Related Shared Modules
- `packages/data-platform/common/qcsm_namespaces/` — QCSM ontology namespace definitions (QCSM, S4AGRI, etc.)

## 🔌 APIs & Interfaces

### Input: JSON Testcase Files
- Pattern: `TC{N}.json` (e.g., `TC0.json`, `TC1.json`, ..., `TC30.json`)
- Root schema: `json-schemas/Testcase.schema.json`
- Each file represents one complete testcase with farm, parcel, assessment, and impact data

### Output: Named Graphs (written to Fuseki)
| Graph Pattern | Content |
|---------------|---------|
| `https://quantifarm.eu/graphs/testcase{N}` | All RDF triples for testcase N |

### Fuseki Endpoints Used
- `GET /$/ping` — Health check (wait for connection on startup)
- `PUT /quantifarm/data?graph=...` — Write testcase graph

### RDF Conversion Rules (Schema-Driven)
| JSON Schema Type | RDF Mapping |
|-----------------|-------------|
| `string`, `integer`, `number`, `boolean` | `qcsm:has{Property}` → `Literal` (DatatypeProperty) |
| `array` of primitives | Multiple `qcsm:has{Property}` → `Literal` triples |
| `array` of objects (`$ref`) | New class instance per element, linked via `qcsm:has{Property}` (ObjectProperty) |
| Single object (`$ref`) | New class instance, linked via `qcsm:has{Property}` (ObjectProperty) |

### Namespace Bindings
- `qcsm` → `https://w3id.org/i40/qcsm#`
- `s4agri` → `https://w3id.org/def/saref4agri#`
- `qcsmdata` → `https://quantifarm.eu/data/`

## 💾 Data Models

### Loading Flow
```
TC{N}.json  ──load()──▶  Recursive parse via JSON schemas
                              │
                              ▼ parse_json_based_on_schema()
                         For each property:
                           - primitive → Literal triple
                           - $ref → new QCSM class + recurse
                           - array of $ref → multiple classes + recurse
                              │
                              ▼ Graph built in memory
                         Each testcase URI: qcsmdata:testcases/testcase{N}
                         Type: qcsm:Testcase
                              │
                              ▼ put_graph()
                         PUT to Fuseki as named graph testcase{N}
```

### Key Ontology Classes (from JSON Schemas)
- `Testcase` (root), `FarmInformation`, `ParcelInformation`, `ParcelComparison`
- `AssessmentInformation`, `YearlyAssessmentInformation`, `CalculatedIndicatorInformation`
- `EconomicInformation`, `MarketInformation`, `OutputInformation`
- `MainImpactInformation`, `AggregatedImpactInformation`, `CostRevenueImpactInformation`
- Resource usage: `FertilizerUsageInformation`, `PesticideUsageInformation`, `FuelUsageInformation`, `ElectricityUsageInformation`, `WaterUsageInformation`, `DrugsUsageInformation`, `FeedUsageInformation`, `FuelForTempControlUsageInformation`
- `LabourInformation`, `AdditionalLabourInformation`, `AdditionalAnimalInformation`
- `ThreeYearAverages`, `AdditionalFieldsInformation`

### Generated Debug Files
- `testcase-classes` — all QCSM classes discovered during loading
- `testcase-properties` — all QCSM properties (with domain/range) discovered during loading

## 🛠️ Developer Workflow
- **Run (all testcases)**:
  ```bash
  cd packages/data-platform/testcase-loader
  python -m testcase_loader
  ```
- **Run (single testcase)**:
  ```bash
  TESTCASE_FILE=TC1 python -m testcase_loader
  ```
- **Run (Docker Compose)**:
  ```bash
  cd packages/data-platform
  docker compose --profile loaders up testcase-loader
  ```
- **Test**: `python -m pytest`
- **Config**: Environment variables (see table below)

### Environment Variables
| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `TRIPLE_STORE_ENDPOINT` | no | `http://triple-store:3030` | Fuseki base URL |
| `TESTCASE_DATA_DIR` | no | `.` (current dir) | Directory containing `TC*.json` files |
| `TESTCASE_FILE` | no | — | Load only one testcase (e.g., `TC1`); if unset, loads all `TC*.json` |

### Excel-to-JSON Utility
`testcase_indicator_excel_to_json_converter.py` converts testcase data from Excel format to JSON. Use separately before loading if source data is in Excel.

## 🔗 Integration Points
- **Upstream**: JSON testcase files (manually curated or converted from Excel)
- **Downstream**: `translation-loader` reads testcase graphs to translate controlled vocabulary; tools query testcase data via SPARQL
- **Shared**: Uses `qcsm_namespaces` from `packages/data-platform/common/`
