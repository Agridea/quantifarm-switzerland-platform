# AI Context: Toolkit Dashboard

## 🎯 Purpose
Web-based frontend dashboard for the QuantiFarm toolkit that provides user registration/authentication and a unified UI to access all backend tools (Recommendation, Cost-Benefit Calculator, Benchmarking, Assessment Engine, Advanced Decision Support).

## 🏗️ Architecture & Stack
- **Language/Framework**: PHP 8.2 (Apache), Vanilla JavaScript, HTML/CSS
- **Database**: MySQL 8.0 (user management only)
- **UI Framework**: Bootstrap 5, ApexCharts, Leaflet
- **Key Components**:
  - **Web Server**: PHP 8.2 Apache container serving static HTML/JS and PHP API endpoints
  - **MySQL Database**: Stores user accounts, profiles, and roles
  - **PHP Proxy Layer** (`php/app.php`, `php/tool1.php`–`php/tool3.php`): Proxies frontend API calls to backend microservices
  - **SPARQL Client** (`php/sparql.php`): Queries the Triple Store (Fuseki) for test case data with i18n translation support
  - **Multi-language System**: DE/FR/IT/EN via separate HTML partials in `assets/lng/`

## 📂 Key Files & Structure
- `index.html`: Landing page / home
- `toolkit.html`: Main toolkit page with tool cards
- `tool1.html`–`tool5.html`: Individual tool pages (Recommendation, Cost-Benefit, Benchmarking, Assessment, ADST)
- `results.html` / `tcreport.html`: Test case results and reporting views
- `login.html` / `register.html` / `profile.html`: User management pages
- `php/api.php`: Central API router (session, login, registration, logout)
- `php/app.php`: Config and utility functions (API URLs, `CallAPI()`, `CallSPARQL()`, `CheckLogin()`)
- `php/db.php`: MySQL database connection (env-var driven)
- `php/tool1.php`: Proxy to Recommendation Tool
- `php/tool2.php`: Proxy to Cost-Benefit Calculator (V1 & V2)
- `php/tool3.php`: Proxy to Benchmarking Tool
- `php/sparql.php`: SPARQL queries against the Triple Store for test case data
- `js/app.js`: Shared constants, tool metadata, language switching, utility functions
- `js/tool1.js`–`js/tool5.js`: Per-tool frontend logic
- `js/results.js` / `js/tcreport.js`: Test case results logic
- `setup-db.sql`: MySQL schema initialization (users table)
- `docker-compose.yml`: Full stack deployment (MySQL + PHP/Apache)
- `Dockerfile`: PHP 8.2 Apache image with mysqli/pdo extensions

## 🔌 APIs & Interfaces
- **Port**: 8080 (HTTP)
- **Internal API Endpoints** (via `php/api.php?c=`):
  - `usr` — Get current session user info
  - `log` — Login (POST email/password)
  - `reg` — Register new user (POST name/email/password/roles/age/gender/country)
  - `out` — Logout / destroy session
- **Tool Proxy Endpoints** (POST JSON to `php/tool{N}.php`):
  - `tool1.php` → forwards to Recommendation Tool (`http://recommendation-tool:8000`)
  - `tool2.php` → forwards to Cost-Benefit Calculator V1/V2 (`http://quantifarm-cost-benefit-calculator-v{1,2}-tool-api:8686`)
  - `tool3.php` → forwards to Benchmarking Tool
- **SPARQL Endpoint**: `php/sparql.php` → queries `http://triple-store:3030/quantifarm/query`
  - Supports i18n via `testcase-translations` graph (DE/FR/IT)
- **Inputs**: JSON body with `path`, `data`, optional `version`, `language`, `method`
- **Outputs**: JSON responses proxied from backend services

## 💾 Data Models
- **MySQL `users` table**: id, name, email, psw (hashed), createdon, roles, age, gender, country, isvalidated, isdel
- **User Roles**: `fa` (farmer), `ad` (advisor), `pm` (policy maker), `xx` (guest/demo)
- **Tool Metadata** (`js/app.js`): Each tool has a key, icon, and allowed roles
- **Sustainability Preferences** (`js/tool1.js`): 6 predefined profiles with ecological/economic/social weightings
- **QCSM Ontology**: SPARQL queries use `qcsm:` namespace for test case, assessment, and impact data

## 🛠️ Developer Workflow
- **Run**: `docker compose up` (starts MySQL + PHP/Apache on port 8080)
- **Prerequisites**: Create `.env` file or use default credentials; ensure `quantifarm-network` Docker network exists (`docker network create quantifarm-network`)
- **Database**: Auto-initialized via `setup-db.sql` on first MySQL container start
- **Config**: Environment variables `DB_HOST`, `DB_USER`, `DB_PASSWORD`, `DB_NAME`, `DB_PORT`, `DOCKER_ENV`
- **Backend Services**: Must be running on `quantifarm-network` — Recommendation Tool, Cost-Benefit Calculator(s), Triple Store
- **Test**: Manual browser testing; no automated test suite
- **i18n**: Language partials in `assets/lng/` (e.g., `index-DE.html`, `index-FR.html`, `index-IT.html`); selected via localStorage

## 📖 Related
- **[TCreport Data Flow](tcreport-data-flow.md)** — Detailed documentation of how `tcreport.html` loads data from the Triple Store via SPARQL, including production failure modes and debugging steps
