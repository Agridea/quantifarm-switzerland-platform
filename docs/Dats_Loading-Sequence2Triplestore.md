# 📊 DATs Loading Process

**QuantiFarm Switzerland - Digital Agriculture Technologies ETL Pipeline**

---

## Flowchart

```mermaid
flowchart TD
    Start([Start DATs Loader]) --> CheckTS{Triple Store<br/>Available?}
    CheckTS -->|No| Wait[Wait & Ping<br/>Triple Store]
    Wait --> CheckTS
    CheckTS -->|Yes| LoadCountries[Load ISO3166<br/>Country Codes]
    
    LoadCountries --> CreateGraph[Create RDF Graph]
    
    CreateGraph --> FS[Process FAIRshare DATs]
    
    FS --> ReadFS[Read fairshare-dats-06-2024.json]
    ReadFS --> LoopFS{For Each<br/>FAIRshare DAT}
    
    LoopFS -->|Next DAT| ParseFS[Parse DAT Data:<br/>- Name, Title, Description<br/>- Launch/Update Year<br/>- Keywords, Sectors<br/>- Benefits, Functionalities<br/>- Languages, Countries<br/>- Web Pages, Costs]
    
    ParseFS --> CheckExistFS{DAT URI<br/>Exists?}
    CheckExistFS -->|No| AddFS[Add to Graph:<br/>- RDF triples<br/>- Provider info<br/>- Country mappings<br/>- Source: 'fairshare']
    CheckExistFS -->|Yes| SkipFS[Skip: DAT Already Exists]
    
    AddFS --> LoopFS
    SkipFS --> LoopFS
    LoopFS -->|Done| TC[Process Test Case DATs]
    
    TC --> ReadTC[Read testcase-dats.xls<br/>Sheet 6]
    ReadTC --> LoopTC{For Each<br/>Row > 1}
    
    LoopTC -->|Next Row| ParseTC[Parse DAT Data:<br/>- Name, Title<br/>- Description<br/>- Provider<br/>- Test Case Link]
    
    ParseTC --> CheckExistTC{DAT URI<br/>Exists?}
    CheckExistTC -->|No| AddTC[Add to Graph:<br/>- Basic RDF triples<br/>- Test case reference<br/>- Source: 'testcase']
    CheckExistTC -->|Yes| LinkTC[Add Test Case Link Only]
    
    AddTC --> LoopTC
    LinkTC --> LoopTC
    LoopTC -->|Done| CB[Process Cost-Benefit DATs]
    
    CB --> ReadCB[Read Excel Files:<br/>- cost-benefit-arable-dats.xls<br/>- cost-benefit-lifestock-dats.xls]
    
    ReadCB --> LoopCB{For Each<br/>File & Row}
    
    LoopCB -->|Next Row| ParseCB[Parse DAT Data:<br/>- Name, Provider, Description<br/>- Web Page, Functionalities<br/>- Cultivation Types, Costs<br/>- Digital Forms, Benefits]
    
    ParseCB --> CheckExistCB{DAT URI<br/>Exists?}
    CheckExistCB -->|No| AddCB[Add to Graph:<br/>- Full RDF triples<br/>- Cost structure details<br/>- Source: 'costbenefit']
    CheckExistCB -->|Yes| EnrichCB[Enrich Existing DAT:<br/>- Add functionalities<br/>- Add digital forms<br/>- Add benefits]
    
    AddCB --> LoopCB
    EnrichCB --> LoopCB
    LoopCB -->|Done| Serialize[Serialize Graph<br/>to N-Triples]
    
    Serialize --> PUT[HTTP PUT to Triple Store<br/>Endpoint: /quantifarm/data<br/>Graph: https://quantifarm.eu/graphs/dats]
    
    PUT --> Replace[Replace Entire<br/>DATs Graph]
    
    Replace --> Verify[Run Verification<br/>SPARQL Query]
    
    Verify --> End([End])
    
    style Start fill:#90EE90
    style End fill:#FFB6C1
    style FS fill:#87CEEB
    style TC fill:#87CEEB
    style CB fill:#87CEEB
    style PUT fill:#FFD700
    style Replace fill:#FFD700
```

---

## Legende

| Farbe | Bedeutung |
|-------|-----------|
| 🟩 Grün | Start / Ende |
| 🟦 Blau | Datenquellen |
| 🟨 Gelb | Speicheroperationen |
| ⬜ Weiss | Verarbeitungsschritte |

---

## 📁 Data Sources

- FAIRshare Platform (JSON)
- Test Case Data (Excel)
- Cost-Benefit Arable (Excel)
- Cost-Benefit Livestock (Excel)

## 🎯 Key Features

- Deduplication across sources
- Enrichment strategy for existing DATs
- RDF/Semantic Web compliant
- Destructive loading (full replace)

## 🔧 Technical Stack

- Python 3.11+ (Loader)
- Apache Jena Fuseki (Triple Store)
- RDFLib (RDF Processing)
- QCSM Ontology (Data Model)

## 📊 Output

- **Graph**: `quantifarm.eu/graphs/dats`
- **Format**: N-Triples
- **Protocol**: SPARQL Graph Store
- **Method**: HTTP PUT (Replace)

---

*QuantiFarm Switzerland | Data Platform Documentation | Generated: January 2026*
