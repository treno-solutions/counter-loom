# Counterloom

**Gesellschaftliche Perspektiven verstehen. Simulationen kritisch prüfen.**

Counterloom ist ein Forschungsprojekt von [Treno Solutions](https://github.com/treno-solutions). Wir untersuchen bestehende Modelle und offene Agenten-Frameworks darauf, ob sie nachvollziehbare Modellgesellschaften für Finanzbildungs-Workshops ermöglichen.

Menschen interpretieren dieselbe Nachricht unterschiedlich: Lebenslage, Erfahrungen, Sicherheitsbedürfnis und Vertrauen prägen ihre Sicht. Unser aktueller Forschungsfokus ist eine kleine soziale Finanzwelt, in der solche Unterschiede und gegenseitiger Einfluss sichtbar werden. Teilnehmer sollen fremde Perspektiven verstehen und die eigenen Reaktionen reflektieren können.

Der [Bauplan](BUILD_PLAN.md) konsolidiert das Ziel als reduziertes Lernmodell: verbundene Systeme von der schematischen Weltwirtschaft bis zur persönlichen Investmententscheidung, bevorzugt mit System Dynamics, algorithmischen Routinen und gezielten LLM-Entscheidungen. Die Umsetzung beginnt mit einem kleinen überprüfbaren Zusammenhang; Darstellung und Framework sind noch offen.

## Was wir untersuchen

- Eine abgegrenzte Investorengruppe einschließlich Nichtanlegern mit unterschiedlichen Lebenslagen.
- Über Zeit fortgeschriebene finanzielle Zustände und eigenständige Entscheidungen unter realistischen Möglichkeiten.
- Äußere Schocks wie Zinsänderungen oder geopolitische Ereignisse mit dokumentierten Übertragungskanälen.
- Individuelle Personas mit Hintergrund und veränderlichen Überzeugungen.
- Nachrichten und Informationen, die unterschiedliche Menschen unterschiedlich wahrnehmen.
- Austausch in plausiblen sozialen Gruppen und über einzelne Brückenkontakte.
- Nachvollziehbare Veränderungen von Einschätzung, Unsicherheit und Handlungsabsicht.
- Den tatsächlichen Mehrwert von Agentensimulationen gegenüber einfacheren Methoden.

Die [makroökonomische Zielarchitektur](research/decisions/0003-macroeconomic-world.md) umfasst eine laufende Wirtschaft mit Haushalten, Unternehmen, Banken, Staat und Zentralbank. Geld, Schulden, Investitionen und Auswirkungen von Ereignissen sollen rechnerisch nachvollziehbar und im Workshop sichtbar werden. Bestehende Makromodelle sind die nächste Prüfgrundlage; eine Darstellungsform ist noch nicht festgelegt.

Das [präzisierte Ziel](research/decisions/0002-world-state-and-shocks.md) ist eine Modellwelt, in der Belastung, Anpassung und veränderte Beteiligung nachvollziehbar werden. Diese Welt ist noch nicht implementiert oder validiert. Der Schwerpunkt liegt auf Perspektivübernahme und Selbstreflexion. Eine Assetklasse kann als gemeinsamer Gegenstand dienen. Preisprognosen, automatischer Handel und die Optimierung von Renditen sind für das gegenwärtige Lernziel nicht erforderlich.

## Ausgangspunkt: aus einem gescheiterten Versuch lernen

MiroFish war unser erster praktischer Ausgangspunkt. Der ausgewertete Versuch lieferte einen ausführlichen Bericht, aber keine zugänglichen Belege für individuelle Reaktionen oder sozialen Einfluss. Nachträgliche Gespräche waren nicht nutzbar. Für das beabsichtigte Erkenntnisziel bewerten wir diesen Methodenversuch als gescheitert und MiroFish in der getesteten Konfiguration als ungeeignet.

Diese Bewertung ist auf den dokumentierten Anwendungsfall begrenzt. Sie ersetzt kein allgemeines Urteil über alle Versionen des Projekts. Befunde, mögliche Ursachen und daraus abgeleitete Anforderungen stehen in der [MiroFish-Auswertung](research/frameworks/mirofish.md).

## Recherche vor Plattformwahl

Wir erfinden keine eigene Simulationsplattform, bevor vorhandene Ansätze geprüft sind. Der nächste Schritt ist ein nachvollziehbarer Marktvergleich auf Basis gemeinsamer Anforderungen. Die recherchierten Frameworks bleiben Kandidaten. TinyTroupe und Concordia wurden inzwischen am Quellcode und an technischen Bausteinen geprüft; ein erster [Concordia-Personenversuch](runs/004-concordia-group-influence/README.md) ist abgeschlossen. Auch ein [TinyTroupe-Vergleich mit direkten Persona-Prompts](runs/005-tinytroupe-group-influence/analysis/evaluation.md) liegt vor: geringer zusätzlicher Lernstoff bei erheblichem Tokenaufwand. Eine endgültige Auswahl steht aus.

| Einstieg | Inhalt |
|---|---|
| [Begrenzter POC](POC.md) | Ein sichtbarer algorithmischer Durchstich und klare Erfolgskriterien |
| [Bauplan](BUILD_PLAN.md) | Architektur, Etappen, Prüfungen und nächste konkrete Arbeit |
| [Forschungsprogramm](research/README.md) | Ziel, Abgrenzung und Reihenfolge der Arbeit |
| [Anforderungen](research/requirements.md) | Benötigte Fähigkeiten mit Herkunft und prüfbaren Nachweisen |
| [Prüfprotokoll](research/assessment-protocol.md) | Vergleichbare kleine Tests vor weiteren großen Läufen |
| [Frameworkübersicht](research/frameworks/README.md) | Eigene Tests, Dokumentationsprüfung und offene Fragen |
| [Literatur](notes/social-financial-world/literature.md) | Persönlichkeit, Erfahrung, Peer-Effekte und soziale Modelle |
| [Recherchebestand](RESEARCH.md) | Quellen, frühere Untersuchungen und archivierte Entwürfe |
| [Laufarchiv](runs/README.md) | Ausgeführte Versuche und noch nicht gestartete Vorbereitungen |

## Nachvollziehbarkeit und Grenzen

Externe Daten, Studienbefunde, Modellannahmen, simulierte Aussagen und eigene Interpretationen bleiben getrennt. Ein Gespräch ist noch kein Einflussnachweis. Eine plausible Modellgesellschaft ist noch keine repräsentative Bevölkerung; ein überzeugender Bericht ist noch kein belegter Lernerfolg.

Veröffentlichte Arbeiten sollen Forschungsfrage, tatsächliche Eingaben, bekannte Ausführungsparameter, Belegstellen und Grenzen erkennen lassen. Beim Zitieren bitte Dateipfad, Version oder Commit sowie gegebenenfalls Laufkennung angeben; externe Originalquellen zusätzlich direkt zitieren.

## Bestand und Arbeitsstand

Die Forschungsrichtung, der erste Methodenversuch und die Prüfanforderungen sind dokumentiert. Erste technische Prüfungen zu TinyTroupe und Concordia liegen vor. Begrenzte generative Vergleiche mit Concordia und TinyTroupe sind abgeschlossen; pädagogische Validierung und kausaler Einflussnachweis stehen aus. Bestehende Seeds und thematische Recherchen werden erhalten; sie gelten nicht automatisch als Eingaben einer neuen Simulation.

`research/` enthält Forschungsentscheidungen und Frameworkbewertungen; `sources/` die Quellenregister; `notes/` Literatur und methodische Ausarbeitungen; `runs/` Eingaben und verfügbare Ergebnisartefakte. `processed/`, `qa/`, `tools/` und `mirofish/` erhalten den bisherigen Forschungsbestand.

Originalberichte und vollständige Reproduktionen externer Quellen bleiben im ergänzenden Archiv, sofern ihre Weiterveröffentlichung nicht geklärt ist. Einzelheiten: [Daten und Quellenrechte](DATA_POLICY.md). Der [Seed- und Recherchestandard](SIMULATION_TEMPLATE.md) ergänzt das Prüfprotokoll für konkrete Läufe.
