# AI Context: Policy Monitoring Tool

## 🎯 Purpose
A visual dashboard for policy makers to monitor agricultural indicators and DATs uptake, using aggregated data from test cases and external sources.

## 🏗️ Architecture & Stack
- **Frontend**: React (Create React App).
- **Backend**: Node.js with Express.
- **Database**: MongoDB (Primary storage), Redis (Caching).
- **Deployment**: Docker Compose (Production) or npm scripts (Local).

## 📂 Key Files & Structure
- `packages/policymonitoring-tool/`
  - `policy-monitoring-tool/`: **Frontend** source code (React).
  - `express-api-mongo/`: **Backend** source code (Express API).
  - `docker-compose.prod.yml`: Production orchestration.
  - `docker-compose.dev.yml`: Development orchestration.

## 🔌 APIs & Interfaces
- **Backend API**: Port 3001 (Local)
  - Endpoints for fetching indicators, map data, and user authentication.
- **Frontend**: Port 3000 (Local)
  - Consumes the Backend API.

## 🛠️ Developer Workflow
- **Local Development (No Docker)**:
  1.  **Frontend**: `cd policy-monitoring-tool && npm run start`
  2.  **Backend**: `cd express-api-mongo && npm run dev`
  3.  **Config**: Switch `.env` variables to point to localhost DBs.
- **Docker Run**:
  ```bash
  docker compose -f docker-compose.prod.yml up
  ```
- **Data Seeding**:
  - The database is initially empty.
  - Must be populated via API calls (Postman collection referenced in README).
