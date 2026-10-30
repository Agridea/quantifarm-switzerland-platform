# quantifarm-switzerland

**QuantiFarm Switzerland** brings the tools of the EU Horizon 2020 project QuantiFarm to Swiss agriculture. It is maintained by [AGRIDEA](https://www.agridea.ch).

The goal is to help farmers, advisors and policy makers find, assess and compare **Digital Agriculture Technologies (DATs)**, such as precision spraying, yield sensors, automated milking or farm management software, and to quantify what they bring in terms of costs, revenue and sustainability.

This repository is a monorepo: it bundles the original QuantiFarm components (mirrored from upstream) together with Swiss-specific adaptations, e.g. Swiss data, German/French/Italian translations and a unified web interface.

## What can the platform do?

| Question | Answered by |
|---|---|
| Which DATs fit my farm and needs? | Recommendation Tool |
| What does a DAT cost, what does it save, does it pay off? | Cost-Benefit Calculator |
| What measurable impact did a DAT have in real trials? | Assessment Tool *(deactivated)*, test cases |
| How does my farm compare to others? | Benchmarking Tool *(deactivated)* |

## How it fits together

```text
 Data sources              Data Platform                       Tools                      Users
 ------------              -------------                       -----                      -----
 FairShare / Excel  -->  Loaders (ETL)  -->  Triple Store  -->  Recommendation Tool   --\
 Test case JSON     -->                      (Apache Jena       Cost-Benefit Calculator --+--> Toolkit Dashboard
 DeepL translations -->                       Fuseki, RDF)      Assessment / Benchmark  --/     (web UI)
                                                  ^
                                       QCSM ontology (shared vocabulary)
```

> **Note:** The Assessment Tool, Benchmarking Tool and Advanced Decision Support Tool are currently **deactivated**. Their code remains in the repository but they are not deployed or maintained.

1. **Data is collected** from several sources (technology catalogues, Excel sheets, test-case reports from pilot farms).
2. **Loaders** convert it into a common semantic model (QCSM) and store it in a central knowledge graph (triple store).
3. **Tools** query this knowledge graph or their own databases and provide recommendations, calculations and benchmarks.
4. The **Toolkit Dashboard** is the single web entry point for users and links to all tools.

## Modules

### User-facing tools

- **[Toolkit Dashboard](packages/toolkit-dashboard/)** – Web front end with registration/login and a unified UI that gives access to all tools. Administrators can maintain DATs here.
- **[Recommendation Tool](packages/recommendation-tool/)** – Interactive selection of suitable DATs based on a farmer's needs. Content is available in German, French, Italian and English.
- **[Cost-Benefit Calculator V1](packages/cost-benefit-calculator-v1/) / [V2](packages/cost-benefit-calculator-v2/)** – Calculates savings (labour, fuel, fertiliser, water, pesticides), additional revenue, ROI and net benefit of adopting a DAT, for crop and livestock farming. V2 offers a refined API with separate crop and livestock inputs.
- **[Assessment Tool (deactivated)](packages/assessment-tool/)** – Calculation engine that evaluates revenue benefits and sustainability KPIs of DAT use. The calculation logic originates from Excel models and is converted to Python.
- **[Benchmarking Tool (deactivated)](packages/benchmarking-tool/)** – Aggregated datasets and comparisons based on parcel data and farm events (e.g. harvest, irrigation).
- **[Advanced Decision Support Tool (deactivated)](packages/advanced-decision-support-tool/)** – Extended decision support for DAT selection.

### Data and semantic layer

- **[Data Platform](packages/data-platform/)** – Central knowledge graph (Apache Jena Fuseki triple store) holding all DAT and test-case data, plus the loaders that fill it:
  - *DATs Loader* – merges DAT descriptions from several sources into one unified graph.
  - *Testcase Loader* – imports test-case results (JSON) as RDF, one graph per test case.
  - *Translation Loader* – pre-translates DAT texts and vocabulary into Swiss German, French and Italian using DeepL, so tools do not have to translate on the fly.
- **[QCSM](packages/qcsm/)** – QuantiFarm Common Semantic Model: the shared ontology that defines the terms and relations used by all tools, so that their data is interoperable.
- **[SAREF4AGRI](packages/saref4agri/)** – ETSI ontology for smart agriculture, on which parts of the semantic model build.

## Repository Structure

- `packages/` – the vendored QuantiFarm tools and semantic models described above
- `docs/` – data-flow descriptions, flowcharts and technical summaries



## Swiss Customisation

- Swiss German (`DE-CH`), French and Italian translations of DAT content
- Unified dashboard as a single entry point for all tools
- Admin interface for maintaining DATs directly in the knowledge graph

## Automation

- CODEOWNERS for Swiss-specific folders

## Running the Tools

Most packages are containerised.

1. Start the **data platform** first, see [packages/data-platform](packages/data-platform/README.md).
2. In each tool's folder `packages/<tool-name>`, create the `.env` file from `.env.example` and run `docker compose up`.

Mind the port mappings in the individual `docker-compose.yml` files if you run several tools at the same time.

## License

Unless stated otherwise, the code in this repository is licensed under the [EUPL v1.2](LICENSE). Packages and third-party components that ship their own `LICENSE` file (see `packages/<tool-name>`) keep that licence.

## AI Context

To assist AI coding agents, we maintain specialized technical summaries in `docs/ai-context/`.
These files provide high-density architecture and workflow details for each package, referenced by `.github/copilot-instructions.md`.
