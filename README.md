# Counterloom

**Recherche. Simulation. Nachvollziehbare Erkenntnisse.**

Counterloom ist ein Forschungsprojekt von [Treno Solutions](https://github.com/treno-solutions). Wir bereiten recherchierte Grundlagen und Seeds für Simulationen vor, werten deren Ergebnisse aus und stellen die dokumentierten Arbeiten als Quellen für weitere Untersuchungen bereit.

Im Mittelpunkt steht ein nachvollziehbarer Forschungsprozess: von der ursprünglichen Frage über die verwendeten Daten und Annahmen bis zu den Befunden und ihren Grenzen. Counterloom ist themenübergreifend angelegt. Unterschiedliche Perspektiven, konkurrierende Erklärungen und alternative Szenarien sind Teil der Untersuchung.

## Unser Vorgehen

1. **Fragestellung entwickeln.** Untersuchungsziel, Ausgangslage, Zeithorizont und Grenzen festlegen.
2. **Recherche aufbereiten.** Quellen prüfen, konkrete Akteure und Beziehungen erfassen, Datenstände dokumentieren und Widersprüche sichtbar machen.
3. **Simulation vorbereiten.** Einen Research Seed erstellen, Szenarien und Annahmen benennen und den Simulationsauftrag separat formulieren.
4. **Ergebnisse auswerten.** Ausgaben mit den Eingaben und externen Quellen abgleichen, unterschiedliche Positionen untersuchen und Unsicherheiten festhalten.
5. **Erkenntnisse bereitstellen und weiterentwickeln.** Ausgewertete Arbeiten mit Quellen, Versionen und Belegstellen veröffentlichen. Befunde früherer Läufe können neue Fragen und Varianten begründen.

Jeder Durchlauf erhält eine eigene Dokumentation. So bleibt erkennbar, welche Eingaben tatsächlich verwendet wurden und wie sich die Untersuchung zwischen den Läufen verändert hat.

## Was eine Quelle hier nachvollziehbar macht

Beobachtete Daten, externe Prognosen, eigene Berechnungen, Szenarioannahmen und simulierte Befunde werden ausdrücklich gekennzeichnet. Zu einer veröffentlichten Auswertung gehören die Forschungsfrage, die verwendeten Eingaben, bekannte Ausführungsparameter, Belegstellen und eine Einordnung der Aussagekraft.

Simulationsergebnisse beschreiben Entwicklungen unter den jeweiligen Bedingungen. Sie werden als simulierte Befunde zitiert. Abweichende Ergebnisse und Minderheitspositionen bleiben erhalten; eine Wiederholung in späteren Läufen gilt nicht als unabhängige Bestätigung.

Beim Bezug auf eine Arbeit aus Counterloom bitte Dateipfad, Version oder Commit sowie gegebenenfalls Laufkennung und Belegstelle angeben. Externe Originalquellen zusätzlich direkt zitieren. Bedingungen zur Weiterverwendung stehen unter [Daten und Quellenrechte](DATA_POLICY.md).

## Einstieg in die Arbeit

| Dokument | Zweck |
|---|---|
| [Seed- und Recherchestandard](SIMULATION_TEMPLATE.md) | Regeln, Mindestanforderungen, kopierbare Vorlage und Startprüfung |
| [Simulationsläufe](runs/README.md) | Dokumentierte Läufe, jeweiliger Status und Ergebnisablage |
| [Vorlage für neue Läufe](runs/_template/README.md) | Eingaben, Konfiguration, Exporte und Auswertung vorbereiten |
| [Iteration und Diversität](notes/iterative-run-design.md) | Frühere Befunde übernehmen und unterschiedliche Perspektiven erhalten |
| [Recherchebestand](RESEARCH.md) | Übersicht über die bisher aufbereiteten Untersuchungsmaterialien |
| [Quellenverzeichnis](sources/README.md) | Herkunft, Datenstände und Nachweise der vorhandenen Recherche |

## Aufbau des Repositorys

| Pfad | Inhalt |
|---|---|
| `runs/` | Eingaben, Ausführungsnachweise, Originalexporte und Auswertungen je Lauf |
| `processed/` | Strukturierte Forschungsdaten und abgeleitete Kennzahlen |
| `sources/` | Quellenregister, Abrufstände und Dateinachweise |
| `notes/` | Methodische Überlegungen, Recherchebefunde und offene Fragen |
| `qa/` | Dokumentierte Daten- und Verarbeitungsprüfungen |
| `tools/` | Skripte zur Aufbereitung und Verarbeitung der Forschungsdaten |
| `mirofish/` | Für MiroFish vorbereitete Eingaben des bisherigen Untersuchungsbestands |

Die Arbeitsweise ist unabhängig vom Untersuchungsthema angelegt. Bei jedem Lauf wird dokumentiert, welches Simulationswerkzeug tatsächlich eingesetzt wurde.

## Veröffentlichungsstand

Das Repository enthält derzeit Arbeitsstandards, vorbereitete Seeds, Recherchematerial und Vorlagen für die Ergebnisauswertung. Ausgewertete Simulationsergebnisse wurden noch nicht veröffentlicht. Der jeweilige Bearbeitungsstand wird in den [Laufübersichten](runs/README.md) ausgewiesen.

Heruntergeladene Originalberichte, vollständige Textextraktionen, Webseitenkopien und Abbildungen gehören zum ergänzenden Recherchearchiv und werden nicht automatisch mitveröffentlicht. Quellenregister und Prüfsummen dokumentieren auch diese Bestände. `file-manifest.json` beschreibt das Recherchearchiv; die tatsächlich verwendeten Eingaben werden zusätzlich je Lauf nachgewiesen. Details: [Daten und Quellenrechte](DATA_POLICY.md).
