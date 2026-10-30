# V1 vs V2 im Toolkit Dashboard (tool2.html)

## Tab-Struktur

Die Cost & Benefit Calculator-Seite im Toolkit Dashboard hat **4 Tabs**, die auf die beiden Versionen verteilt sind:

| Tab | Variable (JS) | Version | Zweck |
|-----|---------------|---------|-------|
| DATSs for Crop Farming | `crop` | **V1** | Allgemeine kommerzielle DATs (Pflanzenbau) |
| DATSs for Livestock Farming | `livestock` | **V1** | Allgemeine kommerzielle DATs (Tierhaltung) |
| Test Cases' DATSs for Crop Farming | `cropTC` | **V2** | Testfall-DATs (Pflanzenbau) |
| Test Cases' DATSs for Livestock Farming | `livestockTC` | **V2** | Testfall-DATs (Tierhaltung) |

## Routing-Logik in `js/tool2.js`

Die Versionierung wird über eine einfache Bedingung gesteuert:

```js
"version": (currentFarmType == crop || currentFarmType == live) ? 1 : 2
```

- `crop` / `livestock` → **Version 1** → wird an `cost-benefit-calculator-v1` (Port 8688) weitergeleitet
- `cropTC` / `livestockTC` → **Version 2** → wird an `cost-benefit-calculator-v2` (Port 8687) weitergeleitet

## Proxy-Routing in `php/tool2.php`

```php
$tool2URL1 = "http://quantifarm-cost-benefit-calculator-v1-tool-api:8686";  // V1
$tool2URL2 = "http://quantifarm-cost-benefit-calculator-v2-tool-api:8686";  // V2
if($version == 2) $baseURL = $tool2URL2;
```

## Zusammenfassung

| | V1 (allgemein) | V2 (Test Cases) |
|---|---|---|
| **Datenquelle** | Kommerzielle DATs (Literatur) | QuantiFarm-Projekt-Testfälle (TC1–TC29) |
| **Calculator Schemas** | `calculator_schema.json` | `calculator_schema_v2.json` |
| **`/totals/` Endpoint** | Basis-Filter | Erweiterter `cfilter` + `tcnumber` |
| **Tabs** | Crop + Livestock (allgemein) | Crop TC + Livestock TC |

> **Hinweis:** Die Test-Case-Tabs (V2) verwenden zudem spezifische **TC-Nummern** (TC1–TC29) mit eigenen Calculator-Modulen (z. B. `cropTC_calc_fertilizer`, `livestockTC_calc_milk_yield`), die in den allgemeinen Tabs (V1) nicht vorhanden sind.