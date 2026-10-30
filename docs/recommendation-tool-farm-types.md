# Recommendation Tool – Herkunft der Farm-Types

## Übersicht

Die Farm-Types im Recommendation Tool kommen aus **zwei fest codierten Quellen** (nicht dynamisch aus dem Triple Store).

---

## 1. Anzeige-Liste (`src/app.py`)

Der `/profile_entries/` Endpoint gibt eine hardcodierte Liste zurück, die im Frontend zur Auswahl angezeigt wird:

- `Arable farm`
- `Dairy farm`
- `Fruit farm`
- `Egg farm`
- `Arboriculture farm`
- `Meat production`
- `Flower farm`
- `Other`

---

## 2. Synonym-Mapping (`data/literals-mapping.json`)

Dieses File mappt jeden Farm-Type auf eine Liste synonymer Begriffe, wie sie in den DAT-Daten im Triple Store vorkommen können. Beispiel:

```json
"farm_type": {
    "Dairy farm": ["All agricultural sectors", "all", "Dairy (cattle, sheep, goats)", "cattle", "dairy cow", "Dairy"],
    "Arable farm": ["All agricultural sectors", "all", "Vegetables", "Arable farming", "Arable", "arable", ...],
    ...
}
```

---

## Datenfluss

1. Nutzer wählt einen Farm-Type aus der Liste im Frontend.
2. Das Mapping in `literals-mapping.json` expandiert den gewählten Wert auf alle synonymen Begriffe.
3. `src/querybuilder.py` nutzt diese Synonyme, um passende DATs im Triple Store zu finden (Property: `saref4agri-new/hasFarmType`).

---

## Status (Stand: April 2026)

Die Farm-Types sind in `main` und `dev` **identisch**.
