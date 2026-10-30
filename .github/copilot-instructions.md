# QuantiFarm Switzerland - AI Coding Instructions

You are working on the **Quantifarm Switzerland** project, a monorepo that localizes QuantiFarm digital agriculture tools for the Swiss market. The codebase mirrors upstream components via `git subtree` and layers Swiss-specific customizations.

## 🏗️ Architecture & Big Picture

- **Monorepo Structure**: All tools reside in `packages/`. Each package is effectively an independent service or tool.
- **Central Data Platform**: `packages/data-platform` is the core.
  - **Triple Store**: Apache Jena Fuseki stores all data (DATs, test cases).
  - **Loaders**: `dats-loader`, `testcase-loader`, and `translation-loader` ETL data into the Triple Store.
  - **Pattern**: Loaders write to specific named graphs; Tools query the Triple Store via SPARQL.
- **Tool Ecosystem**:
  - **Assessment Tool** *(deactivated)*: Python-based engine that converts Excel formulas to Python for evaluation.
  - **Benchmarking** *(deactivated)* **& Cost-Benefit**: Python (FastAPI) services containerized with Docker.
  - **Advanced Decision Support Tool** *(deactivated)*: Extended decision support for DAT selection.
  - **QCSM**: Shared Semantic Model (Ontology).
- **Deactivated Packages**: `assessment-tool`, `benchmarking-tool`, and `advanced-decision-support-tool` are **not active** — their code stays in the repo for reference but they are not deployed or maintained. Do not invest work there unless explicitly asked.

## 🚀 Development Workflows

### Running Services
- **Docker Compose** is the standard runtime.
- Most packages have their own `docker-compose.yml`.
- **Data Platform**:
  ```bash
  cd packages/data-platform
  # Create .env first (see README)
  docker compose up
  ```
- **Tools**: Navigate to `packages/<tool-name>` and run `docker compose up`.

### Configuration
- **Environment Variables**: heavily used. Always check for `.env.example` or README instructions to create `.env` files before running services.
- **Ports**: Be aware of port conflicts if running multiple tools simultaneously (check `docker-compose.yml` port mappings).

### Upstream Sync
- This repo uses `git subtree` to vendor upstream code.
- **Caution**: When modifying files in `packages/`, determine if the change is a **Swiss customization** or a **fix for upstream**.
- Swiss customizations should ideally be isolated or clearly marked to facilitate future syncs.

## 🧠 Project-Specific Patterns

### Assessment Tool (`packages/assessment-tool`) — *deactivated*
- **Status**: Not active; kept for reference only.
- **Excel-to-Python**: Logic is defined in Excel, extracted via VBScript (`extract_formulas.vbs`), converted to JSON (`convert_formulas_to_json.py`), and evaluated in Python (`main.py`).
- **Modification**: Changes to calculation logic often start with the Excel definitions or the conversion scripts, not just the Python code.

### Data Platform (`packages/data-platform`)
- **Graph Isolation**: Loaders should write to their own specific graphs in the Triple Store to allow easy replacement/updates.
- **SPARQL**: Tools interact with data primarily through SPARQL queries to the Fuseki endpoint.
- **Translation Loader**: Pre-translates DAT free-text fields and testcase vocabulary into `@de`/`@fr`/`@it` via DeepL, storing results in dedicated translation graphs. Incremental by design — only new/changed literals are translated. Uses Swiss German (`DE-CH`) orthography. The recommendation-tool consumes these pre-computed translations instead of translating on the fly.

### Policy Monitoring Tool — *removed*
- The `policymonitoring-tool` package no longer exists in this repository. Legacy documentation remains in `docs/ai-context/policymonitoring-tool.md` for reference only.

## 🧪 Testing & Quality
- **Python**: Look for `test.py` or `tests/` directories. Common frameworks: `unittest` or `pytest`.
- **Node/JS**: Check `package.json` for `scripts.test`.
- **Integration**: Testing often requires the Data Platform (Triple Store) to be running.

## 📂 Key Directories
- `packages/data-platform`: Core data infrastructure.
- `packages/qcsm`: Shared ontology definitions.

## 📦 Package-Specific Context
For detailed architecture, API definitions, and workflows for specific tools, refer to the **AI Context** documentation:

- **Assessment Tool** *(deactivated)*: [../docs/ai-context/assessment-tool.md](../docs/ai-context/assessment-tool.md)
- **Benchmarking Tool** *(deactivated)*: [../docs/ai-context/benchmarking-tool.md](../docs/ai-context/benchmarking-tool.md)
- **Cost Benefit Calculator V1**: [../docs/ai-context/cost-benefit-calculator-v1.md](../docs/ai-context/cost-benefit-calculator-v1.md)
- **Cost Benefit Calculator V2**: [../docs/ai-context/cost-benefit-calculator-v2.md](../docs/ai-context/cost-benefit-calculator-v2.md)
- **Data Platform**: [../docs/ai-context/data-platform.md](../docs/ai-context/data-platform.md)
- **DATs Loader**: [../docs/ai-context/dats-loader.md](../docs/ai-context/dats-loader.md)
- **DAT Management (Toolkit Dashboard)**: [../docs/ai-context/dats-management.md](../docs/ai-context/dats-management.md)
- **Testcase Loader**: [../docs/ai-context/testcase-loader.md](../docs/ai-context/testcase-loader.md)
- **Translation Loader**: [../docs/ai-context/translation-loader.md](../docs/ai-context/translation-loader.md)
- **Policy Monitoring** *(removed, legacy docs)*: [../docs/ai-context/policymonitoring-tool.md](../docs/ai-context/policymonitoring-tool.md)
- **Recommendation Tool**: [../docs/ai-context/recommendation-tool.md](../docs/ai-context/recommendation-tool.md)
- **QCSM (Ontology)**: [../docs/ai-context/qcsm.md](../docs/ai-context/qcsm.md)
- **Toolkit Dashboard**: [../docs/ai-context/toolkit-dashboard.md](../docs/ai-context/toolkit-dashboard.md)
- **Triple Store Graphs**: [../docs/ai-context/triple-store-graphs.md](../docs/ai-context/triple-store-graphs.md)
