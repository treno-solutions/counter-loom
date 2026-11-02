# 0002 · Zustandsbasierte Investorengesellschaft unter äußeren Schocks

Datum: 2. November 2026 · Status: Zieldefinition für die nächste Forschungsphase. Ergänzt Entscheidung 0001; keine implementierte oder validierte Simulation.

## Forschungsziel

Eine abgegrenzte Gruppe von Menschen wird als kleine Modellwelt über mehrere Zeitschritte fortgeführt. Dazu gehören aktive Anleger, ehemalige Anleger und Nichtanleger, die eine betrachtete Anlageklasse bisher ablehnen, nicht kennen oder sich nicht leisten können. Äußere Ereignisse verändern Informationen und gegebenenfalls wirtschaftliche Bedingungen. Untersucht wird, welche Personen belastet werden, ihre Einschätzung oder ihr Verhalten ändern, ausweichen, erstmals teilnehmen oder unverändert bleiben.

Neuartige Gedanken außerhalb der Fähigkeiten eines kontextreichen Sprachmodells sind keine Erfolgserwartung. Der Nutzen liegt in konsistent fortgeschriebenen Lebenslagen, begrenztem Handlungsspielraum, unterschiedlichen Informationswegen und nachvollziehbaren Folgewirkungen. Ein interessanter Dialog allein erfüllt das Ziel nicht.

## Population und Typen

Zuerst Bezugsraum und Grundgesamtheit bestimmen: beispielsweise Haushalte einer Region mit Zugang zu einer bestimmten Anlageklasse. Eine Stichprobe bestehender Depotkunden bildet Nichtanleger nicht automatisch ab. Personen sind aus gemeinsam beobachteten Merkmalen zu konstruieren; unabhängig gewürfelte Merkmale können unplausible Kombinationen erzeugen.

Typen sollen empirisch begründete Merkmalskonstellationen zusammenfassen, keine starren Schicksale vorgeben. Drei Ebenen getrennt halten:

1. **Ökonomische Möglichkeiten:** Einnahmen, Ausgaben, liquide Rücklagen, Besitz, Schulden, Zinsbindung, Anlagezugang und Verpflichtungen.
2. **Eher beständige Dispositionen und Erfahrungen:** Risikobereitschaft, Verlustempfindlichkeit, Vertrauen, Kontrollbedürfnis und prägende Erlebnisse; Messgrundlage und Unsicherheit angeben.
3. **Veränderliche Zustände:** Erwartungen, wahrgenommene Bedrohung, Aufmerksamkeit, Wissen, Vertrauen in konkrete Informationen und aktuelle Absichten.

Nichtanlegen ist ein zulässiger Ausgangszustand und kann dauerhaft bestehen bleiben. Neue Anlagebeteiligung oder Rückzug dürfen entstehen, werden aber nicht als gewünschte Ergebnisse vorgegeben. Gruppengewichte und Übergangswahrscheinlichkeiten bleiben offen, bis Erhebungen sie stützen. Vorläufige Typbezeichnungen sind illustrative Fälle und keine validierte psychologische Taxonomie.

## Architekturhypothese

Eine Kombination bestehender agentenbasierter Modellierung mit generativen Entscheidungen wird geprüft. Diese Kombination ist eine eigene Designhypothese, keine bereits nachgewiesene Empfehlung.

- Ein **Zustands- und Regelkern** verwaltet Zeit, Besitz, Zahlungsströme und Verpflichtungen. Er prüft, welche Aktionen möglich sind, und verbucht ihre Folgen. Ausgaben können Rücklagen tatsächlich mindern. Ein Akteur darf keine zusätzlichen Mittel oder bereits ausgeführten Transaktionen erfinden.
- Ein **Entscheidungsmodell** erhält ausschließlich die verfügbaren Informationen, den persönlichen Zustand und tatsächlich erhaltene Kontakte. Ein vorhandenes LLM kann Interpretationen, Ziele und strukturierte Handlungsanträge erzeugen. Bestehende regelbasierte Verhaltensmodelle dienen als Vergleich. Neue neuronale Netze zu trainieren ist keine Voraussetzung der Prüfung.
- **Soziale Kontakte und Informationskanäle** können Erwartungen verändern. Gespräche sind eine mögliche Informationsquelle; Entscheidungen und Zustandsübergänge müssen auch ohne Gespräch funktionieren.
- Ein **Prüf- und Protokollschritt** nimmt zulässige Aktionen an, dokumentiert Ablehnungen und berechnet den nächsten Zustand. Absicht, Antrag und tatsächlich realisierte Aktion bleiben unterscheidbar.

Ein LLM ist bereits ein neuronales Netz. Neuronale Architektur allein macht Agenten weder eigenständig noch empirisch realistisch. Hier bedeutet Eigenständigkeit: Innerhalb dokumentierter Ziele und Möglichkeiten Handlungen wählen, unter anderem abwarten, Informationen suchen, Pläne ändern oder mit anderen sprechen. Die konkrete Reaktion wird nicht vorgegeben. Verbindliche Bilanzregeln legen keine Meinung fest.

## Ereignisse und Schockkanäle

Eine Kriegsmeldung verändert zunächst verfügbare Information. Energiepreisänderungen, Einkommensausfälle oder Wechselkursbewegungen werden als gesonderte beobachtete oder hypothetische Pfade zugeführt. Ein Krieg erzwingt nicht per Definition steigende Goldpreise oder Panik. Wirkung und Dauer sind Szenarioparameter, keine vom LLM erfindbaren Weltfakten.

Eine Zentralbankentscheidung wird mit expliziter Übertragung modelliert: etwa auf Einlagenrendite, variable Kreditzinsen oder auslaufende Zinsbindungen. Nicht jeder Haushalt wird sofort gleich belastet. Reine Nachrichtenwirkung und veränderte finanzielle Möglichkeiten können getrennte Vergleichsbedingungen bilden.

Für den ersten Prüfgegenstand reichen exogene Preis- und Zinspfade. Endogene Preisbildung, vollständige Börsenmechanik und echte Finanztransaktionen sind zusätzliche, derzeit nicht erforderliche Aufgaben. Vereinfachte simulierte Bestandsänderungen können Verhalten abbilden, ohne einen Handelsoptimierer zu bauen.

## Was „kippen“ und „adaptieren“ bedeuten soll

Vor dem Lauf operationalisieren; keine nachträgliche Definition anhand interessanter Texte:

| Beobachtung | Möglicher prüfbarer Nachweis | Grenze |
|---|---|---|
| Finanzielle Überlastung | Unvermeidbare Zahlungen übersteigen verfügbare Mittel; Deckungslücke entsteht | Notwendige Ausgaben und Kreditregeln benötigen Quellen oder offen gelegte Annahmen. |
| Erzwungene Anpassung | Mittel müssen zur Erfüllung von Verpflichtungen beschafft werden | Überzeugung kann trotz veränderter Handlung gleich bleiben. |
| Freiwillige Anpassung | Veränderte Entscheidung bei weiterhin vorhandenen Alternativen | Agentenbegründung allein beweist keine menschliche Ursache. |
| Überzeugungsänderung | Vergleichbare Abfragen zeigen veränderte Erwartung oder Vertrauen | Sprachliche Variation nicht automatisch als Wechsel zählen. |
| Eintritt oder Rückzug | Änderung der simulierten Beteiligung an der Anlageklasse | Aufmerksamkeit, Kaufabsicht, Antrag und Besitz unterscheiden. |
| Widerstandsfähigkeit | Verpflichtungen bleiben erfüllbar und dokumentierte Ziele erreichbar | Stabilität ist kein Beweis einer optimalen Strategie. |

Keine dieser Größen wird ausschließlich aus einem emotional klingenden Text abgeleitet. Psychische Diagnosen sind kein Modellziel.

## Einordnung der bisherigen Versuche

Concordia 004 und TinyTroupe 005 prüften kurze Reaktionen, Gedächtnis, Zustellung und Gesprächsbedingungen. Es gab keine über mehrere Perioden fortgeschriebenen Haushaltsbudgets oder wirtschaftlichen Verpflichtungen. Der geringe Zusatznutzen dieser Gesprächspiloten widerlegt deshalb die hier definierte Modellwelt nicht. Die bisherigen Belege und Einschränkungen bleiben unverändert erhalten.

Auch ein direkter Persona-Prompt ist künftig als alleinige Vergleichsmethode unzureichend: Zusätzlich eine einfache zustandsbasierte regelgesteuerte Variante vergleichen. Nur so lässt sich der Nutzen generativer Entscheidungen von dem Nutzen der Zeit- und Budgetführung unterscheiden.

## Nächster Prüfauftrag

Vorhandene Systeme gezielt auf persistente Zustände, Ressourcenregeln, Zeitschritte, Schockinjektion, individuelle Sichtbarkeit, strukturierte Handlungen und Wiederherstellung prüfen. Kein weiterer großer Dialoglauf. Zunächst Datenquellen für eine abgegrenzte Population und gemeinsam gemessene Merkmale suchen. Danach einen kleinen Mehrperiodenversuch mit dokumentierten Ausgangszuständen, einer Bedingung ohne Schock und getrennten Schockvarianten planen. Die Ergebnisse müssen Zustandsübergänge und belastete beziehungsweise anpassungsfähige Fälle zeigen, nicht bloß längere Berichte.

## Quellen und Evidenzgrenzen

- [OFR: An Agent-based Model for Financial Vulnerability](https://www.financialresearch.gov/working-papers/2014/07/29/an-agent-based-model-for-financial-vulnerability/), 2014: institutionelles Modell für Finanzierungs-/Sicherheitenflüsse und Schockverstärkung. Autorenabstract gelesen; kein validiertes Modell unserer Haushalts- oder Nichtanlegerpopulation und kein eigener Test.
- [Horton: Large Language Models as Simulated Economic Agents](https://www.nber.org/papers/w31122), 2023: Untersuchung generativer ökonomischer Agenten mit vorgegebenen Ressourcen und Präferenzen. Metadaten/Abstract über Suchauszug geprüft; Direktzugriff gescheitert. Kein Beleg, dass ein LLM unsere Population repräsentiert.
- [Simulated responses from large language models are weak proxies for human economic preferences across 74 countries](https://www.nature.com/articles/s41562-026-02611-4), 2026: empirischer Vergleich synthetischer und menschlicher Präferenzen. Nur Verlags-Suchauszug geprüft; Volltextzugriff gescheitert. Als Validierungsfrage aufgenommen, keine Kalibrierungswerte extrahiert.

Abrufprüfung: 2. November 2026. Die Architektur und die Operationalisierung oben sind eigene Vorschläge. Sie folgen nicht als fertige Implementierung aus diesen Quellen.
