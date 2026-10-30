# AI Context: DAT Management (Toolkit Dashboard)

## 🎯 Purpose
Admin-only web page in the Toolkit Dashboard to create, edit, delete and audit Digital Agricultural Technologies (DATs) directly in the Triple Store, without re-running the dats-loader.

## 🏗️ Architecture & Stack
- **Language/Framework**: Vanilla JavaScript + Bootstrap 5 (frontend), PHP 8.2 (backend)
- **Database**: Triple Store (Fuseki, graph `https://quantifarm.eu/graphs/dats`) for DAT data; MySQL (`dat_change_log`) for audit/ownership
- **Key Components**:
  - **Page** `datsmanagement.html`: DAT dropdown, New/Delete buttons, tabs "Edit" and "Change History"
  - **Frontend logic** `js/datsmanagement.js`: form handling, grouped multi-select dropdowns, API calls
  - **Backend API** `php/DatsManagement.php`: SPARQL read/write, validation, locking, change log
  - **Option lists**: loaded from the recommendation tool via `php/tool1.php` (`/profile_entries/`)
  - **Translations**: UI strings in `js/uistrings.js` (`translateDatsManagement()`); DAT field translations read from `dats-translations` graph

## 📂 Key Files & Structure
- `packages/toolkit-dashboard/datsmanagement.html`: Page markup
- `packages/toolkit-dashboard/js/datsmanagement.js`: Client logic (`InitDatsPage`, `LoadDatList`, `LoadDat`, `SaveDat`, `DeleteDat`, `LoadHistory`, `CallDatsAPI`)
- `packages/toolkit-dashboard/php/DatsManagement.php`: Server API (`DatList`, `DatGet`, `DatSave`, `DatDelete`, `DatHistory`, `BuildTriples`)
- `packages/toolkit-dashboard/php/app.php`: Graph URIs, `CheckAdmin()`, `CallSPARQLUpdate()`, `SparqlAsk()`
- `packages/toolkit-dashboard/setup-db.sql`: `dat_change_log` table

## 🔌 APIs & Interfaces
- **Endpoint**: `php/DatsManagement.php?a=<action>` (admin session required)
  - `list` (POST) — all DATs: `uri`, `label`, `lastModified`
  - `get` (GET, `uri`, `lang`) — all mapped fields; `lang` ≠ `en` reads translated values from the translations graph; adds `editable`
  - `save` (POST JSON) — create or update; returns the stored DAT
  - `delete` (POST JSON: `uri`, `lastModified`, `uiLanguage`)
  - `history` (GET, `uri`) — change log rows
- **Access control**:
  - Page visible only for logged-in users with `isadmin`; backend calls `CheckAdmin()`
  - Only the creator (matching `create` entry in `dat_change_log`) can update/delete a DAT
  - Only English (`sourceLanguage` and UI language = `en`) can be saved/deleted
- **Concurrency**: optimistic lock via `qcsm:lastModified`; mismatch returns HTTP 409
- **Errors**: 400 validation, 403 permission, 404 not found, 409 conflict/duplicate, 502 triple store failure
- **Side effect**: after save/delete, `RefreshRecommendationTool()` calls `{tool1URL}/admin/refresh` with `X-Refresh-Token` (env `REFRESH_TOKEN`, best effort)

## 💾 Data Models
- **DAT URI**: `https://quantifarm.eu/data/dats/<slug>` (slug = name lowercased, spaces to `_`, only `a-z0-9_-`; same as dats-loader)
- **Class**: `qcsm:DigitalAgriculturalTechnology`, label via `rdfs:label`
- **Form field to predicate** (`$fieldMap`, whitelist; no free-form SPARQL from client):

| Field | Predicate | Notes |
|---|---|---|
| title | `qcsm:hasTitle` | |
| description | `rdfs:comment` | |
| website | `qcsm:hasWebPage` | IRI, http(s) only |
| keywords | `qcsm:hasKeyword` | multi |
| sector | `qcsm:isTargetedTowardsAgriculturalSector` | multi |
| functionality | `qcsm:hasFunctionality` | multi |
| benefits | `qcsm:hasBenefits` | multi |
| delivery | `qcsm:hasDigitalForm` | multi |
| languages | `qcsm:hasSupportedLanguage` | multi |
| cost | `qcsm:hasCostStructure` | single |
| country | `qcsm:isTargetedTowardsCountry` | multi, IRI `https://quantifarm.eu/data/countries/<Name>` |
| launchYear / lastUpdateYear | `qcsm:hasLaunchYear` / `qcsm:lastUpdateYear` | `xsd:gYear`, >= 1980 |

- **Meta triples**: `qcsm:lastModified` (xsd:dateTime), `qcsm:hasSourceLanguage`, `qcsm:translationStatus` (set to `pending` on save so the translation-loader re-translates)
- **Save strategy**: `DELETE WHERE` all triples of the DAT, then `INSERT DATA` the rebuilt set (single update)
- **MySQL `dat_change_log`**: `id`, `user_email`, `dat_uri`, `action` (`create`/`update`/`delete`), `old_value`/`new_value` (JSON), `undone_log_id`, `createdon`

## 🛠️ Developer Workflow
- **Run**: via toolkit-dashboard `docker compose up` (port 8080); open `datsmanagement.html` as admin user
- **Prerequisites**: Triple Store, recommendation tool (option lists), MySQL with `dat_change_log` table
- **Config**: `REFRESH_TOKEN` env var (shared with recommendation tool), DB env vars (`DB_HOST`, `DB_USER`, `DB_PASSWORD`, `DB_NAME`)
- **Adding a field**: add input in HTML, id in `datFormFieldIds`, entry in `$fieldMap`, and (for dropdowns) Update/Set functions plus option source in `LoadBenefitOptions()`
- **Caution**: DATs also exist in the dats-loader source; a loader re-run may overwrite manual edits in the `dats` graph
- **Test**: Manual browser testing; no automated test suite

## 📖 Related
- [Toolkit Dashboard](toolkit-dashboard.md)
- [DATs Loader](dats-loader.md)
- [Translation Loader](translation-loader.md)
- [Triple Store Graphs](triple-store-graphs.md)
