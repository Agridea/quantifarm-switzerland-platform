# AI Context: Cost Benefit Calculator V2

## 🎯 Purpose
An improved version of the Cost Benefit Calculator that assesses the financial impact of adopting Digital Agriculture Technologies (DATs). Calculates operational savings, revenue increases, ROI, and Net Benefit for crop and livestock systems. V2 introduces a refined API with separate crop/livestock user data endpoints and an enhanced totals endpoint with crop/animal filtering.

## 🏗️ Architecture & Stack
- **Language/Framework**: Python (FastAPI)
- **Database**: PostgreSQL (containerized, port 5559 → 5432 internally)
- **Key Components**:
  - **FastAPI Web Service**: REST API with Swagger UI at `/documentation` (port 8687 → 8686 internally)
  - **PostgreSQL**: Stores DAT definitions, user input data, and calculation schemas
  - **Calculator Models**: Domain-specific modules for yield, investment, fertilizer, water, pesticide, labor, and fuel savings
  - **Formula Engine** (`amFormulas.py`): Evaluates cost-benefit calculations
  - **Model Manager** (`amModel.py`): Handles database CRUD operations and model initialization
  - **Utility Layer** (`amTools.py`): Common helper functions and config loading

## 📂 Key Files & Structure
```
packages/cost-benefit-calculator-v2/
├── docker-compose.yml              # Service orchestration (db + api)
├── openapi_schema.json             # Full OpenAPI 3.0 specification
├── build/
│   ├── fastapi/                    # Dockerfile for API service
│   └── postgresql/                 # Dockerfile + init scripts for DB
├── volume/fastapi-app/app/source/
│   ├── main.py                     # FastAPI entry point with all route definitions
│   ├── cfg/
│   │   ├── config.json             # Service config (DB connection, paths, service metadata)
│   │   ├── tags.py                 # API endpoint tag definitions for Swagger grouping
│   │   └── ivaylo_mapping.json     # DAT-to-model mapping configuration
│   ├── classes/
│   │   ├── amModel.py              # Database model operations (CRUD, table creation)
│   │   ├── amFormulas.py           # Cost-benefit calculation formulas
│   │   └── amTools.py              # Utility functions (config loading, type checks)
│   ├── models/
│   │   ├── inputs.py               # Pydantic input models for API request validation
│   │   └── template.py             # Template/model initialization logic
│   ├── schema.json                 # Database schema definition
│   ├── calculator_schema_v2.json       # V2 crop calculator model definitions
│   ├── calculator_schema_livestock_v2.json  # V2 livestock calculator model definitions
│   └── tree.json                   # DAT tree structure (hierarchy of available DATs)
└── test_data/                      # CSV/Excel files with DAT data and test scenarios
    └── NewData/                    # V2-specific test data
```

## 🔌 APIs & Interfaces
- **Port**: 8687 (external, bound to `127.0.0.1`) → 8686 (internal container)
- **Swagger UI**: `http://localhost:8687/documentation`

### Administration Endpoints
Protected with HTTP Basic auth via `API_ADMIN_USERNAME` / `API_ADMIN_PASSWORD` env vars; disabled (403) if unset.

| Method | Path | Description |
|--------|------|-------------|
| GET | `/administration/create_db_tables` | Initialize database tables (run once on first install) |
| GET | `/administration/create_input_models` | Initialize calculator input models (run once on first install) |

### User Data Endpoints (separate crops/livestock)
| Method | Path | Description |
|--------|------|-------------|
| POST | `/user_data/crops` | Add user input data for crop calculations |
| POST | `/user_data/livestock` | Add user input data for livestock calculations |
| GET | `/user_data` | Retrieve stored user data by `user_id` |

### Data Input Endpoints (under "Add Data" tag)
| Method | Path | Description |
|--------|------|-------------|
| POST | `/generic` | Add generic user input data |
| POST | `/yield` | Add yield-specific user data |
| POST | `/fertilizer` | Add fertilizer usage data |
| POST | `/water` | Add water usage data |
| POST | `/pestcide` | Add pesticide usage data |
| POST | `/labor` | Add labor cost data |
| POST | `/fuel` | Add fuel cost data |

### Result Endpoints (per cultivation type)
| Method | Path | Tags | Description |
|--------|------|------|-------------|
| POST | `/results/arable/investment` | arable_results | Investment calculation for arable crops |
| POST | `/results/arable/yield` | arable_results | Yield savings for arable crops |
| POST | `/results/arable/fertilizer_reduction` | arable_results | Fertilizer savings |
| POST | `/results/arable/water_reduction` | arable_results | Water savings |
| POST | `/results/arable/pesticide_reduction` | arable_results | Pesticide savings |
| POST | `/results/arable/labor_reduction` | arable_results | Labor savings |
| POST | `/results/arable/fuel_reduction` | arable_results | Fuel savings |
| POST | `/results/fruits/...` | fruits_results | Same model set for fruits |
| POST | `/results/vegetables/...` | vegetables_results | Same model set for vegetables |
| POST | `/results/vineyards/...` | vineyards_results | Same model set for vineyards |
| POST | `/results/livestock/...` | livestock_results | Same model set for livestock |

### Summary & Utility Endpoints
| Method | Path | Description |
|--------|------|-------------|
| GET | `/totals/` | Get aggregated results. Params: `user_id`, `dat_name`, `myCultivationType`, `cfilter` (crop/animal name, e.g. "Vegetables (Potato)") |
| GET | `/dat_tree` | Retrieve all available DATs in a tree structure |

### DAT Management (CRUD)
| Method | Path | Description |
|--------|------|-------------|
| GET | `/dat` | List/retrieve DATs (with filters: `dat_category`, `platform`, `purpose_for`, `dat_name`) |
| PUT | `/dat` | Add new DAT entries |
| POST | `/dat` | Update existing DAT entries |
| DELETE | `/dat` | Delete DAT entries |

### CSV Import/Export
| Method | Path | Description |
|--------|------|-------------|
| POST | `/csv/import/dat` | Bulk import DATs from CSV |
| GET | `/csv/export/dat` | Export DATs to CSV |
| GET | `/csv/clear/dat` | Clear export files |

## 💾 Data Models

### User Input Data (POST `/user_data/crops`)
```json
{
  "user_id": "string",
  "years_of_usage": 8.0,
  "number_of_units_sensors_etc": 2.0,
  "total_area_ha": 10.0,
  "current_yield_tonsha": 10000.0,
  "market_price1ton": 1.0,
  "current_fertilizer_usage_kg_ha": 10.0,
  "current_fertilizer_cost1_kg": 1.0,
  "current_water_usage_m3ha": 100.0,
  "current_water_costm3": 2.0,
  "current_pestcide_usage_kg_or_lt_ha": 10.0,
  "current_pesticide_costkg_or_lt": 1.0,
  "current_labor_costin_1_year": 1000.0,
  "current_fuel_costin_1_year": 1.0
}
```

### Totals Response (GET `/totals/`)
Returns aggregated economic outputs:
- **Total Cost Savings** (combined labor, fuel, fertilizer, water, pesticide savings)
- **Return on Investment (ROI)**
- **Net Benefit**

### Cultivation Types
Enum: `arable`, `fruits`, `vegetables`, `vineyards`, `livestock`

### Key V2 Difference: `cfilter` Parameter
The `/totals/` endpoint in V2 accepts an additional `cfilter` parameter to specify the exact crop or animal name (e.g., `"Vegetables (Potato)"`, `"Cattle"`), enabling more granular result filtering.

## 🔄 V1 vs V2 Differences
| Aspect | V1 | V2 |
|--------|----|----|
| API Port | 8688 | 8687 |
| DB Port | 5558 | 5559 |
| User Data Input | Single `/generic` endpoint | Separate `/user_data/crops` and `/user_data/livestock` |
| Totals Endpoint | Basic (`user_id`, `dat_name`, `myCultivationType`) | Enhanced with `cfilter` for crop/animal name |
| Calculator Schemas | `calculator_schema.json` | `calculator_schema_v2.json` |
| Test Data | Standard CSV/Excel | Includes `NewData/` directory with V2-specific data |

## 🛠️ Developer Workflow
- **Run**: `cd packages/cost-benefit-calculator-v2 && docker compose up`
- **API Docs**: `http://localhost:8687/documentation`
- **DB Port**: `localhost:5559` (PostgreSQL, password: value of `POSTGRES_PASSWORD` in `.env`)
- **Schema**: `ws_cost_benefit_calculator`
- **Init Sequence**:
  1. `GET /administration/create_db_tables` — create DB tables
  2. `GET /administration/create_input_models` — load calculator models
  3. `POST /user_data/crops` or `POST /user_data/livestock` — add user data
  4. `GET /totals/?user_id=...&dat_name=...&myCultivationType=...&cfilter=...` — get results
- **Config**: `volume/fastapi-app/app/source/cfg/config.json` — DB connection, service metadata
- **Network**: Uses shared Docker network `quantifarm-network`
