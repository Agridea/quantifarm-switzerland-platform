# AI Context: DATs Loader

## 🎯 Purpose
Loads Digital Agricultural Technology (DAT) metadata from multiple heterogeneous sources (FairShare JSON, testcase Excel, website Excel, cost-benefit Excel) into a single unified RDF graph in the Fuseki triple store, normalizing all DATs under the QCSM ontology.

## 🏗️ Architecture & Stack
- **Language/Framework**: Python 3.11 (CLI module, no web framework)
- **Database**: Apache Jena Fuseki (Triple Store) — writes DATs graph
- **Key Dependencies**: `rdflib==7.0.0`, `requests==2.31.0`, `xlrd==2.0.1`, `qcsm_namespaces`, `qcsm_utils`
- **Key Components**:
  - **Multi-Source Ingestion**: Four sequential ingestion passes (FairShare → Testcase → Website → Cost-Benefit), each parsing a different file format
  - **Deduplication**: DATs are identified by normalized name (`name.replace(" ","_").lower()`); duplicates across sources are merged (additional properties added to existing URI)
  - **Graph Builder**: Accumulates all DATs into a single in-memory `rdflib.Graph`, then PUTs to Fuseki
- **Write Semantics**: The loader uses HTTP `PUT` to write the graph, which **fully replaces** the previous content of `https://quantifarm.eu/graphs/dats`. The loader does not fetch data from the running triple store — it reads only from local source files and overwrites the graph on each run.

## 📂 Key Files & Structure
```
packages/data-platform/dats-loader/
├── Dockerfile                          # Python 3.11-alpine, copies data files to /data/
├── README.md                           # Usage docs
├── setup.py                            # Package config (deps: rdflib, requests, xlrd)
├── dats_generator.py                   # Utility: generates random test DATs for testing
├── fairshare-dats-06-2024.json         # Source 1: FairShare API export (JSON array)
├── fairshare-dats-07-2023.json         # Older FairShare snapshot (not used by default)
├── testcase-dats.xls                   # Source 2: Testcase-associated DATs (Excel, sheet index 5)
├── cost-benefit-arable-dats.xls        # Source 3a: Arable cost-benefit DATs (Excel, sheet 0)
├── cost-benefit-lifestock-dats.xls     # Source 3b: Livestock cost-benefit DATs (Excel, sheet 0)
├── website-registered-dats.xls         # Source 4: Website-registered DATs (Excel, sheet 0)
├── ISO3166-country-code-name.json      # Country name → ISO 3166 code mapping
├── generated_dats.json                 # Output of dats_generator.py (test data)
└── dats_loader/
    ├── __init__.py
    └── __main__.py                     # All loading logic (4 passes + graph upload)
```

### Related Shared Modules
- `packages/data-platform/common/qcsm_namespaces/` — QCSM, S4AGRI, GS1 namespace definitions
- `packages/data-platform/common/qcsm_utils/` — `sparql_select()` utility (used in verification)

## 🔌 APIs & Interfaces

### Input: Data Sources (4 passes)
| # | Source | Format | Key Columns / Fields |
|---|--------|--------|---------------------|
| 1 | FairShare (`fairshare-dats-06-2024.json`) | JSON array | `name`, `title`, `desc`, `keywords`, `sector`, `challenges`, `benefits`, `languages`, `delivery`, `website`, `providerName`, `countries`, `cost`, `launchYear`, `updateYear` |
| 2 | Testcase (`testcase-dats.xls`) | Excel, sheet 5 | Col 0: TC number, Col 2: name, Col 3: provider, Col 4: desc, Col 5: web, Col 6: cost, Col 7: sectors, Col 8: functions, Col 9: countries, Col 10: languages, Col 11: delivery, Col 12: benefits |
| 3 | Website (`website-registered-dats.xls`) | Excel, sheet 0 | Col 1: name, Col 4: provider, Col 6: functions, Col 10: web, Col 12: desc, Col 14: sectors, Col 17: cost |
| 4 | Cost-Benefit (arable + livestock `.xls`) | Excel, sheet 0 | Col 3: name, Col 4: provider, Col 5: desc, Col 6: web, Col 8: crop/livestock type, Col 9-13: costs, Col 18: functions, Col 21: delivery, Col 22: benefits |

### Output: Named Graph (written to Fuseki)
| Graph | Content |
|-------|---------|
| `https://quantifarm.eu/graphs/dats` | All DATs from all sources, merged into one graph |

### Fuseki Endpoints Used
- `GET /$/ping` — Health check (wait for connection on startup)
- `PUT /quantifarm/data?graph=...` — Write DATs graph
- `GET /quantifarm/query` — SPARQL SELECT (used in verification functions)

### Namespace Bindings
- `qcsm` → `https://w3id.org/i40/qcsm#`
- `s4agri` → `https://w3id.org/def/saref4agri#`
- `gs1` → `https://gs1.org/voc/`
- `qcsmdata` → `https://quantifarm.eu/data/`

## 💾 Data Models

### Loading Flow
```
FairShare JSON ──┐
Testcase XLS   ──┤
Website XLS    ──┼──▶  map_to_graph()  ──▶  Single rdflib.Graph
Cost-Benefit   ──┘        │
                          │  Dedup by normalized name
                          │  Merge properties for same DAT
                          ▼
                   put_graph() to Fuseki (HTTP PUT = full replace)
                   Graph: https://quantifarm.eu/graphs/dats
```

### Key QCSM Ontology Classes & Properties
| Class | Description |
|-------|-------------|
| `qcsm:DigitalAgriculturalTechnology` | Root class for every DAT |
| `qcsm:TechnologyProvider` | Provider/manufacturer, linked via `qcsm:hasProvider` |
| `gs1:Country` | Target country, linked via `qcsm:isTargetedTowardsCountry` |

| Property | Type | Description |
|----------|------|-------------|
| `rdfs:label` | Literal | Display name |
| `qcsm:hasTitle` | Literal | Title |
| `rdfs:comment` / `qcsm:hasDescription` | Literal | Description |
| `qcsm:hasKeyword` | Literal | Comma-separated keywords (split into individual triples) |
| `qcsm:isTargetedTowardsAgriculturalSector` | Literal | Sector(s) |
| `qcsm:hasFunctionality` | Literal | Functionality/challenge |
| `qcsm:hasBenefits` | Literal | Benefit(s) |
| `qcsm:hasDigitalForm` | Literal | Delivery form (Web app, Mobile app, etc.) |
| `qcsm:hasSupportedLanguage` | Literal | Language(s) |
| `qcsm:hasCostStructure` | Literal | Cost description |
| `qcsm:hasWebPage` | URIRef | Website URL |
| `qcsm:hasSource` | Literal | Origin: `"fairshare"`, `"testcase"`, `"website"`, `"costbenefit"` |
| `qcsm:hasLaunchYear` / `qcsm:lastUpdateYear` | Literal (xsd:gYear) | Year metadata (FairShare only) |
| `qcsm:isUsedInTestcase` | URIRef | Link to testcase (Testcase source only) |
| `qcsm:hasMinimumInitialCosts` / `qcsm:hasMaximumInitialCosts` | Literal (xsd:decimal) | Numeric costs (Cost-Benefit only) |
| `qcsm:canBeUsedToCultivateCropType` / `qcsm:canBeUsedToCultivateLifestockType` | Literal | Cultivation type (Cost-Benefit only) |

### Deduplication Strategy
- DAT URI = `qcsmdata:dats/{name.replace(" ","_").lower()}`
- If a DAT URI already exists from a previous pass, new properties are **added** to the existing resource (no overwrite)
- Each DAT gets a `qcsm:hasSource` triple indicating its origin pass

## 🛠️ Developer Workflow
- **Run (all sources)**:
  ```bash
  cd packages/data-platform/dats-loader
  python -m dats_loader
  ```
- **Run (Docker Compose)**:
  ```bash
  cd packages/data-platform
  docker compose --profile loaders up dats-loader
  ```
- **Generate test data**: `python dats_generator.py` → writes `generated_dats.json`
- **Config**: Environment variables (see table below)

### Environment Variables
| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `TRIPLE_STORE_ENDPOINT` | no | `http://triple-store:3030` | Fuseki base URL |
| `FAIRSHARE_FILE_PATH` | no | `./fairshare-dats-06-2024.json` | Path to FairShare JSON export |
| `TESTCASE_FILE_PATH` | no | `./testcase-dats.xls` | Path to testcase DATs Excel |
| `WEBSITE_FILE_PATH` | no | `./website-registered-dats.xls` | Path to website DATs Excel |
| `COSTBENEFITARABLEDATS_FILE_PATH` | no | `./cost-benefit-arable-dats.xls` | Path to arable cost-benefit Excel |
| `COSTBENEFITLIFESTOCKDATS_FILE_PATH` | no | `./cost-benefit-lifestock-dats.xls` | Path to livestock cost-benefit Excel |
| `ISO3166_PATH` | no | `./ISO3166-country-code-name.json` | Path to country code mapping |

## 🔗 Integration Points
- **Downstream**: `translation-loader` reads the `dats` graph to translate free-text fields into `@de`/`@fr`/`@it`; `recommendation-tool` and other tools query DATs via SPARQL
- **Downstream Impact**: The `recommendation-tool` loads the DAT graph into memory at startup. After a successful DAT-Loader run, the recommendation tool must be **restarted** to pick up the updated graph.
- **Testcase Relationship**: `testcase-dats.xls` belongs to the DAT-Loader and describes general DAT metadata plus the linkage to testcase numbers. The actual testcase measurement data lives in separate `TC*.json` files and is loaded by the `testcase-loader` into its own named graph (e.g. `https://quantifarm.eu/graphs/testcase14`). The testcase number and DAT names must be consistent across both sources.
- **Shared**: Uses `qcsm_namespaces` and `qcsm_utils` from `packages/data-platform/common/`
- **Verification**: `check_triplestore()` / `check_triplestore1()` helper functions for post-load SPARQL validation

## 🔄 Updating DATs (Operational Workflow)

### Prerequisites
Before loading, ensure all source files in `packages/data-platform/dats-loader/` are up to date:

| Source | File | Content |
|--------|------|---------|
| FAIRshare | `fairshare-dats-06-2024.json` (or newer) | General FAIRshare DAT catalogue |
| QuantiFarm Website | `website-registered-dats.xls` | DATs registered on the QuantiFarm website |
| Testcases | `testcase-dats.xls` | DAT metadata + testcase number mapping |
| Cost-Benefit Arable | `cost-benefit-arable-dats.xls` | DATs + cost data for arable farming |
| Cost-Benefit Livestock | `cost-benefit-lifestock-dats.xls` | DATs + cost data for livestock |
| Countries | `ISO3166-country-code-name.json` | Country name → ISO code mapping |

### Generating a Fresh FairShare Export
The loader contains a helper function that queries the FAIRshare API. It is **not** part of the normal loader run and must be invoked manually:

```powershell
cd packages/data-platform/dats-loader
py -c "from dats_loader.__main__ import check_fairshare; check_fairshare()"
```

This writes `data.json` in the current directory without modifying the triple store. Review and rename the file before use:

```powershell
Rename-Item data.json fairshare-dats-2026-09-03.json
```

The loader expects `fairshare-dats-06-2024.json` by default. Either rename the new export to this name, or set `FAIRSHARE_FILE_PATH` to the new filename.

> **Validation**: Before loading a new FairShare export, verify the API still returns the expected fields: `name`, `title`, `desc`, `launchYear`, `updateYear`, `keywords`, `sector`, `benefits`, `languages`, `countries`, `providerName`.

### Rebuilding & Running After Source Changes
Because the Dockerfile copies source files into the image at build time, the Docker image must be **rebuilt** after any change to JSON or Excel files:

1. Ensure `packages/data-platform/.env` is configured:
   ```
   TRIPLE_STORE_ENDPOINT=http://triple-store:3030
   ```
2. Start the triple store (if not already running):
   ```powershell
   cd packages/data-platform
   docker compose up -d triple-store
   ```
3. Rebuild and run the loader:
   ```powershell
   docker compose build dats-loader
   docker compose up dats-loader
   ```
4. Verify the output — the loader reports the number of processed DATs and writes the graph to `https://quantifarm.eu/graphs/dats`.
5. Restart the `recommendation-tool` so it loads the updated DAT graph.
