# AI Context: Benchmarking Tool

## 🎯 Purpose
Provides aggregated datasets and benchmarking results derived from Parcel data and Calendar events (e.g., harvest, irrigation).

## 🏗️ Architecture & Stack
- **Language**: Python
- **Framework**: FastAPI
- **Containerization**: Docker

## 📂 Key Files & Structure
- `packages/benchmarking-tool/`
  - `docker-compose.yml`: Service definition.
  - `openapi_schema.json`: API definition.
  - `volume/`: Likely contains persistent data or source code mapped into the container.

## 🔌 APIs & Interfaces
- **Port**: 8686
- **Documentation**: `http://localhost:8686/documentation` (Swagger UI)
- **Key Endpoints**:
  - `PUT /parcel`: Add parcel data (supports Polygons).
  - `PUT /event`: Add calendar events (Harvest, Spray, Irrigation, Fertilization).
  - `GET /parcels/{parcelid}/aggregations`: Calculate aggregates (Sum, Avg, Min, Max) for a specific event type over a time range.

## 💾 Data Models
- **Parcel**: Geospatial entity (Polygon) with metadata.
- **Event**: Time-bound activity linked to a Parcel.
  - Types: `harvest`, `spray`, `irrigation`, `fertilization`.

## 🛠️ Developer Workflow
- **Run**:
  ```bash
  docker compose up
  ```
- **Usage**:
  1.  Add Parcel via API.
  2.  Add Events via API.
  3.  Request Aggregations via API.
