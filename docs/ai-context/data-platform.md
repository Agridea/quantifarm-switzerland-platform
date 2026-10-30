# AI Context: Data Platform

## 🎯 Purpose
The central knowledge graph infrastructure for QuantiFarm. It stores all data about Digital Agriculture Technologies (DATs) and Test Cases using Semantic Web technologies.

## 🏗️ Architecture & Stack
- **Core**: Apache Jena Fuseki (Triple Store).
- **ETL**: Custom Python/Script loaders.
- **Containerization**: Docker Compose.

## 📂 Key Files & Structure
- `packages/data-platform/`
  - `docker-compose.yml`: Orchestrates the Triple Store and Loaders.
  - `triple-store/`: Configuration for the Jena Fuseki server.
  - `dats-loader/`: Service that loads DAT definitions from external sources (JSON/Excel) into the graph.
  - `testcase-loader/`: Service that loads Test Case data into the graph.
  - `translation-loader/`: Service that pre-translates DAT free-text fields and testcase vocabulary into German (Swiss), French, and Italian using the DeepL API. Incremental by design — only new/changed literals are translated.
  - `common/`: Shared modules (`qcsm_namespaces`, `qcsm_utils`) used across loaders.

## 🔌 APIs & Interfaces
- **SPARQL Endpoint**: `http://localhost:3030/quantifarm/query`
  - Used by all other tools to fetch data.
- **SPARQL Update**: `http://localhost:3030/quantifarm/update`
  - Used by loaders to write data.
- **Graph Store Protocol**: `http://localhost:3030/quantifarm/data`

## 💾 Data Models
- **Named Graphs**: Data is segregated by source.
  - `https://quantifarm.eu/graphs/dats`: Contains DAT definitions.
  - `https://quantifarm.eu/graphs/testcases`: Contains Test Case data.
  - `https://quantifarm.eu/graphs/dats-translations`: Pre-computed language-tagged literals (`@de`, `@fr`, `@it`) for DAT free-text fields (title, description, keywords, benefits, etc.).
  - `https://quantifarm.eu/graphs/testcase-translations`: Pre-computed language-tagged literals for testcase controlled vocabulary (indicator names, product types, impact titles, etc.).
- **Ontology**: Conforms to QCSM (QuantiFarm Common Semantic Model) and SAREF4AGRI.

## 🛠️ Developer Workflow
- **Start Platform**:
  ```bash
  cd packages/data-platform
  docker compose up