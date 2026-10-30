# AI Context: Recommendation Tool

## 🎯 Purpose
Interactive tool for farmers and advisors to select Digital Agriculture Technologies (DATs) based on their needs. It queries the central Triple Store to find matching DATs.

## 🏗️ Architecture & Stack
- **Language**: Python 3.10+
- **Framework**: FastAPI
- **Server**: Uvicorn
- **Dependency**: Requires access to the Data Platform (Triple Store).

## 📂 Key Files & Structure
- `packages/recommendation-tool/`
  - `src/app.py`: Main FastAPI application entry point.
  - `src/`: Source code for logic and routes.
  - `common/`: Shared utilities.
  - `config/`: Configuration handling.
  - `requirements.txt`: Python dependencies.
  - `Dockerfile` & `docker-compose.yml`: Containerization.

## 🔌 APIs & Interfaces
- **Port**: 8000 (Local default)
- **Documentation**: `http://localhost:8000/docs` (Swagger UI)
- **Key Interactions**:
  - Queries the Triple Store (`SPARQL_QUERY_ENDPOINT`) to retrieve DATs.
  - Exposes endpoints to filter and recommend DATs.

## 🛠️ Developer Workflow
- **Configuration**:
  - Copy `.env-default` to `.env`.
  - Set `SPARQL_QUERY_ENDPOINT` (defaults to `http://localhost:3030/quantifarm/query`).
- **Run (Docker)**:
  ```bash
  docker compose up
  ```
- **Run (Python)**:
  ```bash
  pip install -r requirements.txt
  uvicorn src.app:app --reload
  ```
- **Testing**:
  - `test.py` or `tests/` directory.
