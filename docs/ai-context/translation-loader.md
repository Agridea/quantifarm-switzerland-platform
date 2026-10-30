# AI Context: Translation Loader

## 🎯 Purpose
Pre-translates free-text fields of DATs (title, description, keywords, sectors, benefits, etc.) and testcase controlled vocabulary (indicator names, product types) into German (Swiss), French, and Italian using the DeepL API, storing results as language-tagged RDF literals in dedicated named graphs in the Fuseki triple store.

## 🏗️ Architecture & Stack
- **Language/Framework**: Python 3.11 (CLI module, no web framework)
- **Database**: Apache Jena Fuseki (Triple Store) — reads source graphs, writes translation graphs
- **External API**: DeepL API for machine translation
- **Key Dependencies**: `rdflib==7.1.1`, `requests==2.31.0`, `deepl==1.18.0`, `qcsm_namespaces` (shared common module)
- **Key Components**:
  - **Translation Engine**: Reads translatable literals from source graphs, diffs against existing translations, calls DeepL for missing ones
  - **Incremental Checkpointing**: Writes translations to the triple store after each target language to avoid losing progress on failure
  - **Dual Job System**: Separate translation jobs for DAT free text and testcase vocabulary

## 📂 Key Files & Structure
```
packages/data-platform/translation-loader/
├── Dockerfile                          # Python 3.11-alpine, installs common + this module
├── README.md                           # Usage docs
├── setup.py                            # Package config (deps: rdflib, requests, deepl)
├── translate_ui_strings.py             # One-off utility for translating toolkit-dashboard UI strings
└── translation_loader/
    ├── __init__.py                     # Empty
    └── __main__.py                     # All translation logic (SPARQL queries, DeepL calls, graph I/O)
```

### Related Shared Modules
- `packages/data-platform/common/qcsm_namespaces/` — QCSM ontology namespace definitions
- `packages/data-platform/common/qcsm_utils/` — Shared utilities

## 🔌 APIs & Interfaces

### Input: Source Named Graphs (read from Fuseki)
| Graph | Content |
|-------|---------|
| `https://quantifarm.eu/graphs/dats` | DAT free-text fields (title, description, keywords, benefits, etc.) |
| Testcase graphs (all) | Controlled vocabulary (indicator names, product types, impact titles) |

### Output: Translation Named Graphs (written to Fuseki)
| Graph | Content |
|-------|---------|
| `https://quantifarm.eu/graphs/dats-translations` | Language-tagged literals for DAT fields (`@de`, `@fr`, `@it`) |
| `https://quantifarm.eu/graphs/testcase-translations` | Language-tagged literals for testcase vocabulary |

### Translatable DAT Predicates
- `qcsm:hasTitle`, `rdfs:comment`, `qcsm:hasKeyword`, `qcsm:isTargetedTowardsAgriculturalSector`
- `qcsm:hasBenefits`, `qcsm:hasCostStructure`, `qcsm:hasDigitalForm`, `qcsm:hasFunctionality`
- Excluded: `rdfs:label` (proper nouns/brand names), language/country names

### Translatable Testcase Predicates
- `qcsm:hasIndicatorName`, `qcsm:hasProductType`, `qcsm:hasMainImpactTitle`, `qcsm:hasMainImpactSubtitle`
- `qcsm:hasCostRevenueImpactCategory`, `qcsm:hasCostRevenueImpactName`, `qcsm:hasCostRevenueImpactShortDescription`
- `qcsm:hasAggregatedImpactName`
- Excluded: `qcsm:hasSustainabilityParameterName` (internal parsing only)

### Fuseki Endpoints Used
- `GET /quantifarm/query` — SPARQL CONSTRUCT to fetch translatable triples
- `GET /quantifarm/data?graph=...` — Read existing translation graph
- `PUT /quantifarm/data?graph=...` — Write back updated translation graph
- `GET /$/ping` — Health check (wait for connection on startup)

## 💾 Data Models

### Translation Flow
```
Source Graph (dats)  ──SPARQL CONSTRUCT──▶  Source triples (subject, predicate, literal)
                                              │
                                              ▼ collect_missing_texts()
                                         Diff against existing translations graph
                                              │
                                              ▼ translate_language()
                                         DeepL API (chunked, ≤50 texts/request)
                                              │
                                              ▼ put_graph()
                                         Write language-tagged literals back
```

### DeepL Language Mapping
| Target Code | DeepL Code | Notes |
|-------------|------------|-------|
| `de` | `DE-CH` | Swiss German orthography (no "ß", always "ss") |
| `fr` | `FR` | Standard French |
| `it` | `IT` | Standard Italian |

### Deduplication Strategy
- Identical source texts within a language batch are de-duped before calling DeepL (saves quota)
- Missing translations are detected by checking `(subject, predicate, language)` tuples already present in the translations graph

## 🛠️ Developer Workflow
- **Run (single DAT, dry run)**:
  ```bash
  cd packages/data-platform
  TRANSLATE_ONLY_DAT=gaiasense DRY_RUN=true python -m translation_loader
  ```
- **Run (single DAT, real)**:
  ```bash
  DEEPL_API_KEY=... TRANSLATE_ONLY_DAT=gaiasense python -m translation_loader
  ```
- **Run (all DATs)**:
  ```bash
  DEEPL_API_KEY=... python -m translation_loader
  ```
- **Run (Docker Compose)**:
  ```bash
  # Add DEEPL_API_KEY to packages/data-platform/.env
  docker compose --profile loaders up translation-loader
  ```
- **Config**: Environment variables (see table below)

### Environment Variables
| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `TRIPLE_STORE_ENDPOINT` | no | `http://localhost:3030` | Fuseki base URL |
| `DEEPL_API_KEY` | yes* | — | DeepL API key (*not required when `DRY_RUN=true`) |
| `TARGET_LANGUAGES` | no | `de,fr,it` | Comma-separated target languages |
| `TRANSLATE_ONLY_DAT` | no | — | Restrict to single DAT (slug or full URI); skips testcase job |
| `DRY_RUN` | no | `false` | If `true`: log counts only, no API calls, no writes |

### UI String Translation Utility
`translate_ui_strings.py` is a **one-off helper** (not part of the regular pipeline) that translates toolkit-dashboard UI strings via DeepL and prints a ready-to-paste JS dictionary. Use:
```bash
DEEPL_API_KEY=... python translate_ui_strings.py > output.js
```

## 🔗 Integration Points
- **Upstream**: Reads from graphs populated by `dats-loader` and `testcase-loader`
- **Downstream**: `recommendation-tool` looks up pre-computed `@de`/`@fr`/`@it` literals instead of translating on the fly
- **Toolkit Dashboard**: `translate_ui_strings.py` generates translations for the frontend UI strings
