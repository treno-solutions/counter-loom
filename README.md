# Counterloom

Counterloom verbindet Recherche, unterschiedliche Perspektiven und iterative Simulationen, um mögliche Entwicklungen zu untersuchen. Der erste Forschungsstrang nutzt MiroFish für Gold, Silber und Kupfer.

Repository: [treno-solutions/counter-loom](https://github.com/treno-solutions/counter-loom).

## Öffentlicher Bestand und lokales Archiv

Dieses Repository enthält Seeds, Vorlagen, kuratierte Evidenz, strukturierte Daten und die Ablage für Simulationsergebnisse. Heruntergeladene Originalberichte, vollständige Textextraktionen, Webseitenkopien und Abbildungen bleiben im lokalen Recherchearchiv. Sie werden nicht mit Git veröffentlicht. Bezugsquellen und Prüfsummen bleiben dokumentiert. Details: [Daten und Quellenrechte](DATA_POLICY.md).

## Zentrale Arbeitsvorlage

[Regeln, Mindestanforderungen und kopierbare Vorlage für Seeds und Recherche](SIMULATION_TEMPLATE.md). Für neue Läufe und iterative Erweiterungen hier beginnen. Die Vorlage enthält auch die Startprüfung und Vorgaben zur Übernahme früherer Ergebnisse.

## Simulationsläufe und Ergebnisse

- [Erste Simulation: vorbereitete Ergebnisablage](runs/001-first-simulation/README.md)
- [Übersicht und Ablageanleitung](runs/README.md)
- [Vorlage für weitere Läufe](runs/_template/README.md)

Originalexporte des ersten Laufs nach `runs/001-first-simulation/exports/` kopieren. Auswertung und Quellenabgleich kommen nach `analysis/`. In `run.json` die tatsächlichen Kennungen, Eingaben und Parameter anhand des Exports ergänzen. Der vorbereitete Ordner enthält noch keine Simulationsergebnisse.

## Recherche für Folgeläufe

- [Iteratives Vorgehen und Diversität](notes/iterative-run-design.md)
- [Iran-Krieg und Energie-Szenarien](notes/iran-energy-scenarios.md)
- [Historische Energiepreise](notes/energy-data.md)

- [Rechercheübersicht mit Originalstudien und Datensätzen](RESEARCH.md)
- [Originaler englischer Research Seed, Kapitel 1–17](precious-metals-research-seed.md)
- [Kompaktes Recherchepaket für den nächsten Lauf](mirofish/precious-metals-evidence-pack.md)
- [Historische Preisauswertung](mirofish/historical-price-evidence.md)
- [Separater Prompt für den Folgelauf](mirofish/next-run-prompt.md)
- [Quellenverzeichnis](sources/README.md)

## Ordner

| Pfad | Inhalt |
|---|---|
| `runs/` | Eingaben, Originalexporte und eigene Auswertung je Lauf |
| `raw/` | Unveränderte heruntergeladene Studien und Rohdaten |
| `processed/` | Textextraktionen und strukturierte Forschungsdaten |
| `mirofish/` | Aufbereitete Recherche und Prompt für spätere Uploads |
| `sources/` | Quellen, Abrufstände und Dateinachweise |
| `notes/` | Recherchebefunde und Datenkonflikte |
| `qa/` | Extraktionsprüfungen und Zahlenabgleiche |
| `tools/` | Reproduzierbare Verarbeitung der Forschungsdaten |

`file-manifest.json` beschreibt nur den Recherchebestand. Je Lauf werden die Eingaben separat mit Prüfsummen dokumentiert; Ergebnisse werden dadurch nicht mit Forschungsquellen vermischt. Ein erneuter Rechercheaufbau aktualisiert RESEARCH.md und lässt diese Repository-Übersicht und die Laufablagen bestehen.
