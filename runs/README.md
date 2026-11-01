# Simulationsläufe

Jeder Lauf erhält einen eigenen Ordner. Ein Neustart mit geänderten Eingaben oder Parametern erhält eine neue Laufnummer. Die Kennung im Ordner ist unsere Ablagekennung; sie ist unabhängig von der MiroFish-ID.

Vorbereitung und Mindestanforderungen: [zentrale Seed- und Recherchevorlage](../SIMULATION_TEMPLATE.md). Die verwendete Vorlagenversion und den Prüfstatus im jeweiligen Lauf dokumentieren.

| Ablage | Inhalt | Status |
|---|---|---|
| [001-first-simulation](001-first-simulation/README.md) | Erste abzulegende Simulation; Seed-Kopie und aus dem Chat rekonstruierter Prompt vorbereitet | Ergebnisse noch nicht importiert |

## Ergebnisse ablegen

1. Originalexporte in `exports/` des passenden Laufs kopieren. Die erwarteten Dateitypen stehen dort in der README. Auch ein unvollständiger oder fehlgeschlagener Lauf kann archiviert werden.
2. In `run.json` die MiroFish-Projekt- und Simulations-ID anhand des Exports bestätigen sowie Zeitraum, Modell, Konfiguration und tatsächlichen Ausführungsstatus ergänzen. Fehlende Angaben bleiben `null`.
3. Eingaben unter `inputs/` mit dem Export abgleichen. Das spätere Recherchepaket wurde nicht automatisch im ersten Lauf verwendet.
4. Befunde und Belegstellen in `analysis/evaluation.md` eintragen. Originalexporte und eigene Interpretation bleiben getrennt.
5. Status in dieser Übersicht und in der Lauf-README aktualisieren. Ein vorhandener Bericht allein bedeutet nicht, dass die Simulation vollständig oder inhaltlich belastbar war.

## Weitere Läufe

Die Folge wird iterativ aufgebaut: Ausgewertete Ausgänge eines Vorgängers, einschließlich abweichender Positionen, werden als simulierte Befunde in den nächsten Lauf übernommen. Neue externe Daten und neue Annahmen getrennt hinzufügen. Ziel und Vorgehen: [Diversität und Iteration](../notes/iterative-run-design.md). Die Vorlage enthält dafür `inputs/prior-run-findings.json` und eine Textfassung; beide sind zunächst leer bzw. als Vorlage markiert.

`_template/` in einen neuen Ordner wie `002-expanded-evidence` kopieren, `run.json` ergänzen und die tatsächlich hochgeladenen Dateien nach `inputs/` kopieren. Den genauen Prompt und einen Konfigurationsexport mit ablegen. Zufallsseed und Modellversion nur eintragen, wenn bekannt.

Erst mit bestätigten Eingaben und Laufparametern lassen sich Durchläufe vergleichen. Für eine zusätzliche Variante immer eine neue Ablage verwenden, statt alte Ergebnisse zu überschreiben.
