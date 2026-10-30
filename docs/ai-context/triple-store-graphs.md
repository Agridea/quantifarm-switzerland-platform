# Triple Store Named Graphs

Stand: *(Datum einfügen)*

Endpoint: `http://localhost:3030/quantifarm/query`

## Vorhandene Graphs

<!-- Ausfüllen mit dem Ergebnis des SPARQL-Queries -->

| Graph URI | Beschreibung |
|-----------|-------------|
| `https://quantifarm.eu/graphs/dats` | DAT free-text fields (geladen durch dats-loader) |
| `https://quantifarm.eu/graphs/dats-translations` | DAT Übersetzungen @de/@fr/@it (geladen durch translation-loader) |
  `https://quantifarm.eu/graphs/testcase2`
  `https://quantifarm.eu/graphs/testcase24`
  `https://quantifarm.eu/graphs/testcase20`
  `https://quantifarm.eu/graphs/testcase3`
  `https://quantifarm.eu/graphs/testcase12`
  `https://quantifarm.eu/graphs/testcase21`
  `https://quantifarm.eu/graphs/testcase28`
  `https://quantifarm.eu/graphs/testcase7`
  `https://quantifarm.eu/graphs/testcase25`
  `https://quantifarm.eu/graphs/testcase14`
  `https://quantifarm.eu/graphs/testcase13`
  `https://quantifarm.eu/graphs/testcase9`
  `https://quantifarm.eu/graphs/testcase4`
  `https://quantifarm.eu/graphs/testcase11`
  `https://quantifarm.eu/graphs/testcase30`
  `https://quantifarm.eu/graphs/testcase19`
  `https://quantifarm.eu/graphs/testcase23`
  `https://quantifarm.eu/graphs/testcase18`
  `https://quantifarm.eu/graphs/testcase27`
  `https://quantifarm.eu/graphs/testcase22`
  `https://quantifarm.eu/graphs/testcase8`
  `https://quantifarm.eu/graphs/testcase5`
  `https://quantifarm.eu/graphs/testcase6`
  `https://quantifarm.eu/graphs/testcase10`
  `https://quantifarm.eu/graphs/testcase16`
  `https://quantifarm.eu/graphs/testcase1`
  `https://quantifarm.eu/graphs/testcase29`
  `https://quantifarm.eu/graphs/testcase17`
  `https://quantifarm.eu/graphs/testcase15`
  `https://quantifarm.eu/graphs/testcase26`
  `https://quantifarm.eu/graphs/testcase0` | All 30 TestCases (geladen durch translation-loader) |

| `https://quantifarm.eu/graphs/testcase-translations` | Testfall-Vokabular Übersetzungen (geladen durch translation-loader) |

## Abfrage-Commands (PowerShell)

```powershell
# Alle Graphs auflisten
Invoke-RestMethod -Uri "http://localhost:3030/quantifarm/query?query=SELECT+DISTINCT+?g+WHERE+{+GRAPH+?g+{+?s+?p+?o+}+}" -Headers @{ Accept = "application/sparql-results+json" }

# Triples pro Graph zählen
Invoke-RestMethod -Uri "http://localhost:3030/quantifarm/query?query=SELECT+?g+(COUNT(*)+AS+?triples)+WHERE+{+GRAPH+?g+{+?s+?p+?o+}+}+GROUP+BY+?g+ORDER+BY+DESC(?triples)" -Headers @{ Accept = "application/sparql-results+json" }