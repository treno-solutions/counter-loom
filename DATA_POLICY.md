# Daten und Quellenrechte

Counterloom unterscheidet den öffentlichen Forschungsbestand vom lokalen Originalarchiv.

## Im Repository

- Eigene Seeds, Simulationsprompts, Vorlagen und Recherchevermerke.
- Kuratierte Evidenz und ausgewählte strukturierte Forschungsdaten mit Quellenangaben.
- Verarbeitungsskripte, Prüfberichte und Quellenregister.
- Ablagevorlagen und verfügbare Artefakte des ersten Methodenversuchs: eine gerenderte Berichtsaufnahme und ein als Zusammenfassung gekennzeichneter Prüfvermerk. Vollständige Serverexporte liegen nicht vor.

Die enthaltenen Quellenangaben sind bei Weiterverwendung beizubehalten. Rechte an externen Inhalten verbleiben bei den jeweiligen Rechteinhabern; eine pauschale Lizenz für alle Forschungsdaten wird hier nicht erteilt.

## Nur lokal

Die folgenden Bestände sind über `.gitignore` von der Veröffentlichung ausgeschlossen:

- `raw/`: heruntergeladene Berichte, Originaldaten und archivierte Webkapitel.
- `processed/*.fulltext.txt`, `processed/*.pages.json` und `processed/*.clean.md`: vollständige Reproduktionen der Originaltexte.
- `sources/*.md` außer `sources/README.md` und Webseitenkopien in `sources/macro-2026-11-01/`.
- `qa/*.png`: Abbildungen aus Originalberichten.

Diese Dateien bleiben auf dem bestehenden Rechner erhalten. Kostenloser Download wird nicht als allgemeine Erlaubnis zur Weiterveröffentlichung behandelt. Eine spätere Aufnahme einzelner Originale setzt die Prüfung der jeweiligen Nutzungsbedingungen voraus.

## Nach einem frischen Clone

1. Quellen in `sources/README.md`, `sources/source-register.json` und `sources/macro-2026-11-01/source-register.json` nachschlagen.
2. Benötigte Originale beim Herausgeber beziehen und unter den dort dokumentierten lokalen Dateinamen ablegen.
3. Prüfsummen mit dem Quellenregister vergleichen. Geänderte Ausgaben gesondert dokumentieren.
4. Vollständige Konvertierungen bei Bedarf mit den Skripten unter `tools/` wiederholen; Abhängigkeiten stehen in `RESEARCH.md`.

`file-manifest.json` beschreibt das lokale Recherchearchiv einschließlich der nicht veröffentlichten Dateien. Es ist kein Verzeichnis ausschließlich eingecheckter Dateien. Kuratierte Evidenz und Ergebnisvorlagen sind bereits ohne Originalarchiv lesbar.

Vor dem Einchecken von Simulationsexporten Zugangsdaten, Sitzungsinformationen und personenbezogene Inhalte prüfen und gegebenenfalls entfernen.
