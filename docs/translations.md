# Toolkit Dashboard — Übersetzungen

Dieses Dokument beschreibt die drei Übersetzungsmechanismen des Toolkit Dashboards sowie deren Fundstellen und Anpassungsmöglichkeiten.

## 1) Statische HTML-Fragmente pro Seite
- Speicherort: `assets/lng/` mit Dateinamen nach dem Muster `<page>-<LANG>.html` (z. B. `index-TR.html`).
- Ladevorgang: Die Funktion `LoadLanguageContent(lng)` in `packages/toolkit-dashboard/js/app.js` lädt `assets/lng/<page>-<LANG>.html` und fügt das zurückgegebene HTML in das Tab-Container-Element mit der ID `lngTab<LANG>` ein (zum Beispiel `lngTabTR`).
  - Implementierungsverweis: [packages/toolkit-dashboard/js/app.js](packages/toolkit-dashboard/js/app.js#L600-L664).
  - Fetch-Optionen: `{ method: 'GET', cache: 'no-store' }`.
  - Der Loader überspringt den Abruf, wenn der Ziel-Container bereits HTML enthält (`document.getElementById(container).innerHTML.trim() != ""`).
- Eine statische Sprache entfernen: den Navigations-Button auf der Seite (das Element `lngBtn<LANG>`) entfernen, den zugehörigen Container `lngTab<LANG>` entfernen, das Fragment in `assets/lng/` löschen und ein eventuelles Flaggenbild in `assets/img/` entfernen.

## 2) Maschinelle Übersetzung (Google-Translate-Widget)
- Einsatzort: `tool1.html` (und möglicherweise weitere Seiten, die das Widget einbinden).
  - Widget-Skript: `//translate.google.com/translate_a/element.js?cb=googleTranslateElementInit`.
  - Bei der Initialisierung werden `includedLanguages` (kommagetrennte Sprachcodes) und `pageLanguage` innerhalb von `googleTranslateElementInit()` gesetzt.
  - Beispielverweis: [packages/toolkit-dashboard/tool1.html](packages/toolkit-dashboard/tool1.html#L556).
- Hinweise: Dies stellt eine clientseitige maschinelle Übersetzung bereit. Um eine Sprache aus dem Widget zu entfernen, `includedLanguages` in der Widget-Initialisierung bearbeiten und den Sprachcode entfernen (z. B. `tr`).

## 3) Schlüsselbasiertes clientseitiges i18n (`uistrings`)
- Mechanismus: ein Wörterbuch-Objekt `uistrings` (Zeichenketten, referenziert über Schlüssel) sowie ein Laufzeitmodus, gesteuert über den booleschen Wert `do_lang_translation` in `packages/toolkit-dashboard/js/app.js`.
  - Ist `do_lang_translation` auf `true` gesetzt, sucht ein `DOMContentLoaded`-Handler alle Elemente mit dem Attribut `qf-lang-key` und ersetzt deren Text/Platzhalter über `translateElement()` anhand der Werte aus `uistrings`.
  - Implementierungsverweis: [packages/toolkit-dashboard/js/app.js](packages/toolkit-dashboard/js/app.js#L20-L30) sowie die nahegelegene Implementierung von `translateElement()`.
- Anwendungsfall: Kleine UI-Textschlüssel können ohne seitenspezifische HTML-Fragmente ausgetauscht werden; dazu `uistrings` mit den benötigten Übersetzungen befüllen und `do_lang_translation` aktivieren.

## Praktische Hinweise & Checkliste zum Entfernen
- Zu prüfende Dateien beim vollständigen Entfernen einer Sprache:
  - Navigations-Buttons der Seite: `lngBtn<LANG>` (in HTML-Seiten wie `index.html`, `tool1.html` usw.).
  - Tab-Container: `lngTab<LANG>`.
  - Statische Fragmente: `assets/lng/<page>-<LANG>.html`.
  - Flaggen-Icons: `assets/img/<flag>.png`.
  - Google-Translate-`includedLanguages` (falls das Widget verwendet wird).
  - Alle `uistrings`-Einträge (falls das schlüsselbasierte System aktiviert ist).
- Laufzeit: Wird die Website über die mitgelieferte `docker-compose.yml` betrieben, bindet der Dienst `web` das Projekt per Bind-Mount nach `/var/www/html` ein. Änderungen an Dateien sind dem Container sofort sichtbar (kein Image-Rebuild nötig), jedoch kann ein Leeren des Browser-Caches nötig sein.