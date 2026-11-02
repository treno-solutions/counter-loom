# Modellplan: vorhandene soziale Simulationen erweitern

Status: Entwurf, 2. November 2026. Dieser Plan ist kein ausgeführtes oder validiertes Modell.

Die [Zielpräzisierung 0002](../../research/decisions/0002-world-state-and-shocks.md) ergänzt diesen ursprünglichen Gesprächsplan um Nichtanleger, persistente finanzielle Zustände, Mehrperiodenabläufe und äußere Schocks. Die unten beschriebene Dialogprüfung ist ein Teiltest, kein vollständiger Test der gewünschten Modellwelt.

Der aktuelle übergreifende [Bauplan](../../BUILD_PLAN.md) und [Entscheidung 0004](../../research/decisions/0004-reduced-hybrid-learning-model.md) ersetzen diesen ursprünglichen Gesprächsplan als Umsetzungsreihenfolge. Die folgenden Abschnitte bleiben als dokumentierter früherer Entwurf erhalten.

## Bestehende Ansätze statt einer neuen Plattform

| Grundlage | Dokumentierter Ansatz | Eignung und offene Frage |
|---|---|---|
| [TinyTroupe](https://github.com/microsoft/TinyTroupe) | Generative Personas, gemeinsame Umgebungen, demografische Erzeugung und Werkzeuge zum Abgleich mit Erhebungen | Erster Kandidat für Workshop-Gruppen. Prüfen, ob Überzeugungen sich über Kontakte verändern und gespeicherte Zustände wieder abrufbar sind. |
| [Concordia](https://github.com/google-deepmind/concordia) | Komponenten für Gedächtnis und Entscheidungen; eine Umgebung verarbeitet natürlichsprachliche Handlungen | Kandidat für explizite Lebensumstände und kontrollierte Begegnungen. Feed und Workshop-Oberfläche wären zusätzliche Arbeit. |
| [AgentSociety](https://github.com/tsinghua-fib-lab/AgentSociety) | Forschungsumgebung für soziale Agenten; aktuelle Version 2 und ursprünglicher Simulator sind zu unterscheiden | Umfangreichere Alternative. Nicht allein wegen der möglichen Größe auswählen. Passende Version und benötigte Module prüfen. |
| [OASIS](https://github.com/camel-ai/oasis) / MiroFish | Simulierte soziale Plattformen mit Agentenaktionen | Vorhandene Interaktion wiederverwenden, falls Zustandsänderungen und Gedächtnis nachweisbar sind. Kein weiterer langer Lauf nur für einen Bericht. |

TinyTroupe verwendet MIT, Concordia Apache-2.0. AgentSociety nennt Apache-2.0 mit Ausnahme des Ordners `packages/agentsociety/commercial`. Die Ausnahmen, Abhängigkeiten und Modellanbieter sind vor einer tatsächlichen Integration gesondert zu prüfen. Die ursprüngliche Einordnung beruhte auf Dokumentation und Lizenzdateien. Die spätere [vertiefte Prüfung](../../research/frameworks/README.md) enthält auch eine lokale Concordia-Installation und technische Tests. Ein Einflussnachweis mit generativen Personen steht aus.

## Modellgerüst

1. **Population:** Einen Bezugsraum festlegen. Erhebungen für Lebenslagen verwenden; soziale Gruppen nicht automatisch mit Vermögensklassen gleichsetzen. Zunächst eine transparente Fallauswahl statt behaupteter Repräsentativität.
2. **Personas:** Ein vorhandener Generator erstellt Personen aus dokumentierten Ausgangsdimensionen. Die Prüfung sucht fehlende Perspektiven und stereotype Kopplungen. Keine zukünftigen Reaktionen oder Positionswechsel vorgeben.
3. **Netzwerk:** Überwiegend Kontakte in ähnlichen Umfeldern, einige Brücken und gemeinsame öffentliche Informationen. Nähe kann auf Familie, Arbeitsplatz, Interesse oder Erfahrung beruhen. Sie ist nicht allein Einkommensähnlichkeit.
4. **Dynamische Akteure:** Bestehende Gedächtnis-, Reflexions- und Dialogmechanismen verwenden. Relativ beständige Bedürfnisse, aktuelle Emotionen, Überzeugungen und Absichten getrennt speichern. Ohne Beleg erzeugte Skalen bleiben Modellannahmen.
5. **Einflussmodelle:** Begrenzte Offenheit, soziale Informationsübernahme und Zugehörigkeitsmotiv als begründete alternative Erklärungen nutzen. Nicht sämtliche Mechanismen gleichzeitig fest verdrahten. Formale Modelle dienen als Vergleich oder begrenzender Rahmen; ein LLM ersetzt keine empirische Kalibrierung.
6. **Nachrichten:** Herkunft und Zeitstand erhalten. Fakten, Interpretationen, Gerüchte und hypothetische Szenarien unterscheiden. Nur tatsächlich zugestellte Informationen dürfen in die jeweilige Erinnerung eingehen.

## Wie Einfluss geprüft wird

Ein Beitrag oder eine Antwort ist zunächst eine Interaktion. Ein späterer ähnlicher Satz ist noch kein kausaler Einflussnachweis.

Für einen kleinen Test zunächst dieselben Ausgangspersonen und dieselbe Nachricht verwenden, mit getrennten Bedingungen:

- A: private Reaktion ohne Austausch;
- B: Austausch innerhalb der jeweiligen Gruppe;
- C: dieselbe Gruppenumgebung mit wenigen zusätzlichen Brückenkontakten.

Neuigkeiten, Sichtbarkeit und Systemanweisungen zwischen den Bedingungen kontrollieren. Die Gesprächsinhalte selbst dürfen sich entwickeln. Ausgangspersonen und Erinnerungen vor dem Abzweigen sichern; Bedingungen nicht nacheinander auf dieselben bereits veränderten Personen anwenden. Bei stochastischen LLMs reichen ein fixer Zufallsseed und ein einzelner Vergleich nicht aus; mehrere begrenzte Wiederholungen und tatsächliche Modellversionen dokumentieren.

Vor und nach der Interaktion dieselben neutralen Fragen stellen: Was ist geschehen? Welche Unsicherheit besteht? Was bedeutet Sicherheit in der eigenen Lage? Welche Handlungsabsicht besteht? Welches Argument könnte diese ändern? Nicht nach einem erwarteten Meinungswechsel fragen.

Für jede mögliche Änderung speichern: vorheriger Zustand, empfangener Beitrag, Absender, Nachricht oder Argument, anschließender Zustand und Entscheidung. Selbst zugeschriebene Überzeugung durch einen anderen ist ein Modellbericht, kein psychologischer Beweis. Unveränderte Haltung, gestiegene Unsicherheit und begründete Ablehnung sind ebenso Ergebnisse wie Annäherung. Ein Unterschied zwischen Bedingungen zeigt zunächst nur einen Effekt innerhalb des konkreten Modells.

## Minimaler Pilot

Vorgeschlagen: acht bis zwölf Personen in zwei bis drei Gruppen, eine Nachricht, wenige Gesprächsschritte. Noch keine gewählten numerischen Bevölkerungsgewichte oder Einflusskoeffizienten. Zuerst prüfen, ob die gewählte Bibliothek:

- Erinnerungen vor und nach dem Kontakt zugänglich hält;
- Nachrichten gezielt nur an bestimmte Personen zustellt;
- Kontakte begrenzt und dieselben Ausgangszustände für Vergleiche wiederherstellt;
- autonome Antworten statt vorgegebener Reaktionen erzeugt;
- Kosten, Aktionen und Fehler nachvollziehbar protokolliert.

Wenn die Basis diese Anforderungen erfüllt, eine Workshop-Oberfläche ergänzen. Die Darstellung eines sozialen Netzwerks ist eine Präsentationsentscheidung und kein Grund, eine ansonsten ungeeignete Engine zu wählen.

## Workshop-Erfolg

Teilnehmer sagen vor einer Nachricht mögliche Reaktionen voraus, beobachten unterschiedliche Reaktionen und reflektieren Bedürfnisse und Lebenslagen. Eine Gegenvariante ändert eine Lebensbedingung, ohne der Person eine andere Persönlichkeit zuzuschreiben. Reflexion bleibt freiwillig; keine automatische Diagnose oder Anlageempfehlung.

Pädagogisch prüfen: Können Teilnehmer danach mehr unterschiedliche Reaktionen nachvollziehbar erklären? Erkennen sie den Unterschied zwischen eigener Präferenz, finanzieller Möglichkeit und kurzfristiger Emotion? Kleine Vorher-/Nachher-Aufgaben können das untersuchen. Der Lerneffekt wird nicht aus der Länge des Simulationsberichts abgeleitet.
