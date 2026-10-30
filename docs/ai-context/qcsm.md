# AI Context: QCSM (QuantiFarm Common Semantic Model)

## 🎯 Purpose
The shared ontology that defines the vocabulary and relationships for all QuantiFarm tools. It ensures semantic interoperability between the Assessment, Benchmarking, and Policy Monitoring tools.

## 🏗️ Architecture
- **Format**: Turtle (`.ttl`) and JSON-LD.
- **Base**: Extends SAREF4AGRI and other standard ontologies.
- **Role**: Defines the schema for data stored in the Data Platform (Triple Store).

## 📂 Key Files & Structure
- `packages/qcsm/`
  - `qcsm.ttl`: The core ontology definition file.
  - `Instantiations/`: Example data or instances using the ontology.
  - `tests/`: Validation tests for the ontology.

## 💾 Key Concepts & Classes
*Refer to `qcsm.ttl` for the authoritative definitions.*
- **DAT (Digital Agriculture Technology)**: Core entity representing the tools being assessed.
- **TestCase**: Represents a specific deployment or trial of a DAT.
- **Indicator/KPI**: Metrics used for assessment and benchmarking.

## 🛠️ Developer Workflow
- **Modification**:
  - Edit `qcsm.ttl` to add new classes or properties.
  - Ensure changes are backward compatible if possible.
- **Validation**:
  - Use SHACL or other RDF validation tools (often found in `tests/`) to verify consistency.
- **Deployment**:
  - The `qcsm.ttl` file is loaded into the Data Platform's Triple Store (often by the loaders or during initialization).
