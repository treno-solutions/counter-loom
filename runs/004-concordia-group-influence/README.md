# 004 · Erster Concordia-Gruppenversuch

Vorbereitung: 2. November 2026 · Status: **Modellanbindung ausstehend; keine generativen Ergebnisse**.

## Frage

Welche Unterschiede entstehen, wenn dieselben Personen dieselbe Nachricht zunächst allein und anschließend mit beziehungsweise ohne Austausch in ihrem eigenen Gesprächskreis betrachten? Eine Veränderung ist nicht vorgeschrieben. Angst, Unsicherheit, Absicht und Lebenslage werden sprachlich getrennt erfragt.

## Begrenzter Aufbau

Acht ausdrücklich fiktive Personen in zwei Gruppen. Eine hypothetische Nachricht, eine gemeinsame Ausgangsbefragung, gespeicherte Zustände, danach zwei unabhängige Bedingungen:

- A: dieselben Ausgangspersonen ohne neue Beiträge; abschließende neutrale Befragung.
- B: dieselben Ausgangspersonen mit zwei Gesprächsrunden nur innerhalb ihres jeweiligen Kreises; identische Schlussbefragung.

Das sind insgesamt höchstens 40 Textaufrufe mit je höchstens 400 Ausgabetokens, ohne automatische Wiederholungen. Ein Anbieterzugang und gegebenenfalls ein monetäres Budget müssen vor der Ausführung feststehen. Der bereits konfigurierte Ollama-Zugang war bei der Vorbereitung nicht funktionsfähig; es wurde kein Ersatzdienst mit unbekannten Kosten gestartet.

## Eingaben und Technik

- [Fiktive Fälle und Gruppen](inputs/people.json).
- [Nachricht und neutrale Fragen](inputs/scenario.json).
- [Design und Grenzen](inputs/design.json).
- [Auswertungsplan](analysis/evaluation.md).
- [Startprüfung](inputs/start-check.md).
- [Ablaufskript](../../tools/run_concordia_pilot.py), [technischer Workflowtest](../../tools/check_concordia_pilot_workflow.py) und [Prüfergebnis](../../qa/concordia-pilot-workflow-test.json).
- [Laufmetadaten](run.json).

Verwendet werden vorhandene Concordia-Agenten, Beobachtungs-/Gedächtniskomponenten und getrennte Foren. Ein dünner Ablauf koordiniert die Bedingungen; er modelliert keine eigenen psychologischen Einflusskoeffizienten. Der minimale Agentenbaustein reduziert Kosten, ist aber nicht mit der umfangreicheren Reflexionsarchitektur gleichzusetzen.

Ein einzelner Lauf kann interessante Fälle und technische Machbarkeit zeigen. Er ist kein kausaler Nachweis realer gesellschaftlicher Reaktionen und keine pädagogische Validierung. Die Reihenfolge der Beiträge ist dokumentiert und kann selbst Ergebnisse beeinflussen.

## Technischer Vorlauf

Der vollständige Ablauf wurde mit der echten Concordia-Bibliothek und einem lokalen Transport-Testdouble geprüft: 40 technische Antwortaufrufe, identische Ausgangszustände der beiden Bedingungen, 48 dokumentierte Zustellungen ausschließlich innerhalb der jeweiligen Gruppe und gespeicherte Endzustände. Das Testdouble erzeugt ausdrücklich keine Personenmeinungen. Diese Daten sind keine Simulationsergebnisse; die temporären Testantworten wurden nicht im Ergebnisarchiv abgelegt.

Der minimale Personenbaustein nutzt die jüngsten Beobachtungen. Der technische Speicher verwendet einen konstanten Vektor; semantische Ähnlichkeitssuche wird in diesem Pilot nicht beansprucht. Eine spätere Reflexions- oder semantische Gedächtnisvariante wäre ein eigener Vergleich.

Für den Modellzugang liest das Ablaufskript nur lokal konfigurierte Umgebungsvariablen `CONCORDIA_BASE_URL`, `CONCORDIA_MODEL` und gegebenenfalls `CONCORDIA_API_KEY`. Keine Zugangsdaten in Dokumente oder Commits übernehmen. Der Transport erwartet eine kompatible Chat-Completions-Schnittstelle. Provider, tatsächliche Modellkennung, unterstützte Tokenbegrenzung und bei kostenpflichtigen Diensten ein Preis-/Budgetabgleich bleiben vor dem Start zu klären.
