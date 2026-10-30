# AI Context: Assessment Tool

## 🎯 Purpose
Calculates Revenue Benefits and Sustainability KPIs from DATs (Digital Agriculture Technologies) usage. It acts as a calculation engine that translates Excel-based logic into Python execution.

## 🏗️ Architecture & Stack
- **Language**: Python 3.6+
- **Framework**: FastAPI (for the web service wrapper, though core logic is script-based)
- **Core Pattern**: "Excel-to-Python"
  1.  **Source**: Logic defined in Excel formulas (Polimi Excel file).
  2.  **Extraction**: VBScript extracts formulas.
  3.  **Conversion**: Python script converts Excel formulas to JSON logic.
  4.  **Execution**: Python engine evaluates the JSON logic.

## 📂 Key Files & Structure
- `packages/assessment-tool/`
  - `main.py`: Entry point for the calculation engine.
  - `extract_formulas.vbs`: Script to extract formulas from the source Excel file.
  - `convert_formulas_to_json.py`: Converts extracted formulas into a JSON logic format.
  - `classes/`
    - `customFunctions.py`: Python implementations of specific Excel functions used in the formulas.
  - `InputTCs/`: JSON files containing input Test Cases (TC).
  - `ConvertedFormulas/`: JSON files containing the converted logic.

## 🔌 APIs & Interfaces
- **Input**: JSON object representing a Test Case (e.g., `InputTCs/tc06.json`).
  - Fields: `testcaseNumber`, `cultivationType`, `datsInformation`, etc.
- **Output**: JSON object with calculated KPIs.
  - Fields: `sust_kpis_dats`, `economic_productivity`, etc.

## 🛠️ Developer Workflow
- **Logic Updates**:
  - Do NOT edit `main.py` for logic changes.
  - Update the mapping or `customFunctions.py` if new Excel functions are needed.
  - Re-run conversion scripts if the source Excel changes.
- **Run Calculation**:
  ```bash
  python main.py
  ```
- **Dependencies**: Standard Python requirements (see `requirements.txt` if available, otherwise standard libs + `fastapi` for the service wrapper).
