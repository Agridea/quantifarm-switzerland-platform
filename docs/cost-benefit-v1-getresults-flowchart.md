# Cost-Benefit Calculator v1 - getResults Funktion Flowchart

## Übersicht
Die `getResults` Funktion ist ein FastAPI Endpoint, der die Gesamtberechnungen (Totals) für einen bestimmten DAT (Digital Agriculture Technology) durchführt.

```mermaid
flowchart TD
    Start([Start GET totals<br/>getResults]) --> InputParams[Parameter:<br/>user_id, dat_name,<br/>myCultivationType, type]
    
    InputParams --> CheckType{type livestock}
    
    CheckType -->|Ja| SetLivestock[Livestock Konfiguration:<br/>calculator_schema_livestock_v2<br/>userdata_generic_livestock]
    
    CheckType -->|Nein| SetCrop[Crop Konfiguration:<br/>calculator_schema_v2<br/>userdata_generic]
    
    SetLivestock --> CallGetTotals[Funktion getTotalsOptions]
    SetCrop --> CallGetTotals
    
    CallGetTotals --> GetWholeDataset[Funktion getWholeDataset]
    
    GetWholeDataset --> GetTableData[Funktion getTableData<br/>DAT Daten aus DB laden]
    
    GetTableData --> CheckDAT{DAT gefunden}
    
    CheckDAT -->|Nein| ErrorDAT[Error: Unknown DAT]
    ErrorDAT --> End([Ende])
    
    CheckDAT -->|Ja| GetEntityByUser[Funktion getEntityByUserId<br/>User Daten aus DB laden]
    
    GetEntityByUser --> CheckUser{User hat Daten}
    
    CheckUser -->|Nein| ErrorUser[Error: No User Records]
    ErrorUser --> End
    
    CheckUser -->|Ja| MergeData[User Daten mit<br/>DAT Defaults mergen]
    
    MergeData --> TurnZero[Funktion turnIneligiblePropertiesIntoZero<br/>Ungeeignete Properties auf Zero setzen]
    
    TurnZero --> CreateMemory[Funktion createMemoryObject<br/>Memory Object erstellen]
    
    CreateMemory --> CheckError{Fehler}
    
    CheckError -->|Ja| ThrowError[HTTPException 401]
    ThrowError --> End
    
    CheckError -->|Nein| InitResponse[Response initialisieren]
    
    InitResponse --> TryBlock[Try Block]
    
    TryBlock --> LoadJSON[amTool.load<br/>JSON Schema laden]
    
    LoadJSON --> BuildResponse[Response Struktur:<br/>4 Totals definieren]
    
    BuildResponse --> LoopModels[Loop Models]
    
    LoopModels --> LoopItems[Loop Items]
    
    LoopItems --> CheckFunction{Formel vorhanden}
    
    CheckFunction -->|Ja| EvalFormula[getResultFromFormula<br/>Formel auswerten]
    CheckFunction -->|Nein| NextItem{Weitere Items}
    
    EvalFormula --> SetGlobal[Globals setzen]
    
    SetGlobal --> AddToResponse[Zu Response hinzufügen]
    
    AddToResponse --> NextItem
    
    NextItem -->|Ja| LoopItems
    NextItem -->|Nein| NextModel{Weitere Models}
    
    NextModel -->|Ja| LoopModels
    NextModel -->|Nein| ExitTry[Try beenden]
    
    ExitTry --> ReturnResponse[Return Response]
    
    TryBlock --> CatchException[Exception Handler]
    CatchException --> ReturnResponse
    
    ReturnResponse --> End

    style Start fill:#90EE90
    style End fill:#FFB6C1
    style ErrorDAT fill:#FF6B6B
    style ErrorUser fill:#FF6B6B
    style ThrowError fill:#FF6B6B
    style CheckError fill:#FFD700
    style CheckType fill:#87CEEB
    style CheckDAT fill:#FFD700
    style CheckUser fill:#FFD700
    style CheckFunction fill:#FFD700
    style NextItem fill:#FFD700
    style NextModel fill:#FFD700
    style TryBlock fill:#DDA0DD
    style CatchException fill:#FFA07A
    style GetTableData fill:#B0E0E6
    style GetEntityByUser fill:#B0E0E6
    style MergeData fill:#98FB98
    style CreateMemory fill:#98FB98
```

## Beschreibung

### Eingabeparameter
- **user_id**: Benutzer-ID
- **dat_name**: Name der Digitalen Agrartechnologie
- **myCultivationType**: Typ der Kultivierung (z.B. arable, fruits, cattle, pigs)
- **type**: Haupttyp (crop oder livestock)

### Hauptschritte

1. **Typ-Erkennung**: Unterscheidet zwischen Crop und Livestock

2. **getTotalsOptions**: Zentrale Datenbeschaffungsfunktion
   - **getWholeDataset**: Kombiniert DAT-Daten und User-Daten
   - **getTableData**: Lädt DAT-Daten aus PostgreSQL (z.B. Investment, Yield, Fertilizer)
   - **getEntityByUserId**: Lädt User-spezifische Daten aus DB
   - **Merge**: User-Daten überschreiben DAT-Defaults
   - **turnIneligiblePropertiesIntoZero**: Setzt ungeeignete Properties auf 0
   - **createMemoryObject**: Erstellt Memory-Object für Berechnungen

3. **Response-Struktur**: 4 Haupttotals
   - annual_change_in_net_income
   - costs_saving
   - return_on_investment
   - net_benefit

4. **Formelauswertung**:
   - Iteriert durch Models (investment, yield, fertilizer_reduction, etc.)
   - Wertet Excel-Formeln aus
   - Speichert in Globals mit Suffix "3" (A3, B3, etc.)

5. **Rückgabe**: Vollständiges Response-Objekt mit allen berechneten Werten

### Wichtige Datenbankfunktionen

- `getTableData(cultivationType, filter)`: Lädt DAT-Daten für spezifischen Typ (z.B. arable, cattle)
- `getEntityByUserId(entity, user_id)`: Lädt User-spezifische Input-Daten
- Die User-Daten überschreiben die Default-Werte aus der DAT-Tabelle

### Unterschiede zu v2
- Feste Totals-Liste (v2 hat unterschiedliche für Crop/Livestock)
- Verwendet CultivationType Parameter statt cfilter und tcnumber
- Globals mit Suffix "3" (v2 ohne Suffix)

### Fehlerbehandlung
- Unknown DAT: Error 401 wenn DAT nicht in DB gefunden
- No User Records: Error 401 wenn User keine Daten hat
- Memory Object Error: Error 401 bei Problemen beim Erstellen
- Try-Catch für Formelauswertung
- Try-Catch Block für die gesamte Verarbeitung
- HTTPException 401 bei Fehlern in getTotalsOptions
- Fehlerausgabe in Console bei Exceptions während der Formelauswertung
