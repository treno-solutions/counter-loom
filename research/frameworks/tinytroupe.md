# TinyTroupe · vertiefte Vorauswahl

Stand: 2. November 2026 · Prüfprotokoll 1.0 · Status: `documentation_reviewed` mit technischen Quellcode-Prüfungen · Eignung: `conditional`.

## Gegenstand und Umfang

[Microsoft/TinyTroupe](https://github.com/microsoft/TinyTroupe), Quellstand `7ce8be378a37ee73f9745d6781452712318afa04`, Paketversion laut `pyproject.toml`: 0.8.1, Python ab 3.10, MIT-Lizenz. Der README-Änderungsverlauf allein nennt einen älteren Release-Stand; diese Prüfung bindet Aussagen deshalb an den Commit.

Quellcode lokal gelesen, nicht das vollständige Framework installiert. Fünf isolierte Prüfungen verwenden echte, aus dem Quellbaum geladene Methoden, aber Testdoubles statt realer Personas; Dekoratoren sind für diese Prüfungen entfernt. Es wurden keine Modellaufrufe, keine Gespräche und keine pädagogischen Tests ausgeführt. Diese Grenze gilt besonders für die Interpretation der folgenden Fehlerbefunde.

## Was gut passt

Einzelne `TinyPerson`s erhalten Profile und Informationen, speichern episodische und semantische Erinnerungen und können mit anderen interagieren. `TinyPersonFactory` unterstützt die Erzeugung anhand demografischer Vorgaben. Das ist eine vorhandene Grundlage; wir müssten weder eine Agentenplattform noch sämtliche Personen von Hand schreiben. Eine demografische Vorgabe macht die erzeugte Population allerdings nicht automatisch repräsentativ.

`TinyWorld` kann getrennte Gesprächsräume bilden. `TinySocialNetwork` beschreibt zusätzlich Beziehungen. Methoden zum Kodieren von Personen- und Weltzuständen sind vorhanden; ihre Existenz ist noch kein eigener erfolgreicher Wiederherstellungstest des ganzen Frameworks.

Primärquellen: [Personas](https://github.com/microsoft/TinyTroupe/blob/7ce8be378a37ee73f9745d6781452712318afa04/tinytroupe/agent/tiny_person.py), [Welt](https://github.com/microsoft/TinyTroupe/blob/7ce8be378a37ee73f9745d6781452712318afa04/tinytroupe/environment/tiny_world.py), [Netzwerk](https://github.com/microsoft/TinyTroupe/blob/7ce8be378a37ee73f9745d6781452712318afa04/tinytroupe/environment/tiny_social_network.py).

## Kritische Befunde für unser Ziel

| Befund | Beobachtung in isolierter Quellprüfung | Konsequenz |
|---|---|---|
| T01 | Beziehungen steuern die als erreichbar markierten Personen. | Das Netzwerk ist mehr als eine bloße Darstellung. |
| T02 | Die geerbte TALK-Zustellung akzeptiert ein benanntes Ziel außerhalb der deklarierten Kontakte. | Erreichbarkeit in der Persona ist keine durchgängig erzwungene Zustellgrenze. |
| T03 | TALK ohne erkanntes Ziel sendet standardmäßig an die ganze Welt. | Getrennte soziale Gruppen in einer Welt sind so nicht zuverlässig isoliert. |
| T04 | Ein zulässiges REACH_OUT ruft die Basismethode auf und sendet anschließend trotzdem eine Ablehnung. | Inkonsistente Rückmeldung kann die Agenten verwirren. |
| T05 | `TinySocialNetwork._step` nimmt die von `TinyWorld.run` übergebenen Argumente nicht an. | Der naheliegende Netzwerkpfad ist am geprüften Quellstand nicht unmittelbar als Pilotgrundlage geeignet. |

[Maschinenlesbare Befunde](evidence/boundary-checks-2026-11-02.json), [reproduzierbares Prüfskript](../../tools/probe_framework_boundaries.py). Das sind technische Grenzprüfungen, kein vollständiger Lauf mit echten TinyPerson-Instanzen. Ob beziehungsweise wie oft ein LLM diese Pfade auslöst, wurde nicht gemessen.

Die Persona-Prompts verlangen zudem starke Treue zu vorgegebenen Überzeugungen. Das kann Konsistenz unterstützen, steht aber möglicherweise einer offenen Meinungsänderung entgegen. Es ist ein zu testender Zielkonflikt und kein bereits nachgewiesener Ausschluss von Lernen. Verhaltenkorrekturen dürfen für uns nicht einfach jede Abweichung von der Ausgangsmeinung zurückdrängen.

## Anforderungen R01–R10

| ID | Stand | Grenze / benötigter Nachweis |
|---|---|---|
| R01 | Dokumentiert | Erzeugte Personen und Unterschiede innerhalb der Gruppen noch nicht beurteilt. |
| R02 | Teilweise dokumentiert | Lebenslage/Emotionen vorhanden; stabile Bedürfnisse gegenüber revidierbaren Überzeugungen im Pilot unterscheiden. |
| R03 | Im Netzwerkpfad problematisch | T02/T03; zuerst getrennte TinyWorlds oder begrenzte, überprüfte Anpassung. |
| R04 | Quellcode vorhanden | Zustandsexport einschließlich Erinnerungen im vollständigen Framework noch nicht praktisch geprüft. |
| R05 | Offen | Keinerlei Meinungsänderung durch Gespräche nachgewiesen. |
| R06 | Teilweise vorhanden | Kodierung und globale Persona-Registrierung bei unabhängigen Vergleichszweigen prüfen. |
| R07 | Teilweise vorhanden | Kostenstatistik/Parallelisierung dokumentiert; umfangreiche Standardabhängigkeiten, mögliche Korrekturwiederholungen. Eigene Kosten noch nicht gemessen. |
| R08 | Problemstelle gefunden | T04; Fehler- und Aktionsbehandlung im Pilot nicht durch Reportertext ersetzen. |
| R09 | Durch Prüfdesign zu ergänzen | Quellenstatus und Beobachtungsfragen werden nicht automatisch wissenschaftlich korrekt. |
| R10 | Noch nicht getestet | Bibliothek und Notebooks statt fertiger Counterloom-Workshop-Oberfläche. |

## Entscheidung

Weiterhin interessanter Kandidat für kleine Gruppengespräche, aber nicht unverändert mit `TinySocialNetwork` starten. Ein erster Pilot wäre am ehesten mit **einer getrennten TinyWorld je Gruppe** sinnvoll. Brückenkontakte und Zustellung wären danach ausdrücklich zu prüfen. Vor zusätzlichen Anpassungen prüfen, ob Concordia die Anforderungen bereits besser erfüllt. Keine Fehlerkorrektur am Fremdprojekt und kein externer Issue wurden ausgeführt.
