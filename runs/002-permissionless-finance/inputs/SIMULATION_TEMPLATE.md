# Vorlage und Regeln für Seeds, Recherche und Simulationsläufe

Version: **1.0** · Stand: **1. November 2026**

Arbeitsstandard für neue und weiterentwickelte Läufe in diesem Repository. Ziel sind nachvollziehbare Eingaben, vielfältige Perspektiven und eine iterative Erweiterung des Wissensstands. Bereits archivierte Eingaben bleiben unverändert. Änderungen an dieser Vorlage werden mit neuer Versionsnummer und kurzer Änderungsnotiz festgehalten.

Die Mindestanforderungen unten gelten für die jeweils beanspruchte Auswertung. Ein ausdrücklich dokumentierter Funktionstest darf offene Punkte haben; seine Ergebnisse werden entsprechend begrenzt eingeordnet. Diese Vorlage ist eine Arbeitsanleitung. Sie wird derzeit nicht automatisch durch MiroFish geprüft.

## 1. Vier unterschiedliche Eingaben

| Begriff | Inhalt und Aufgabe |
|---|---|
| **Research Seed** | Forschungsfrage, belegte Ausgangswelt, Akteure, Mechanismen, Szenarien und Untersuchungsgrenzen |
| **Recherchepaket** | Quellen, Fakten, Datenreihen, Tabellen und überprüfte Berechnungen, auf die sich der Seed stützt |
| **Simulationsprompt** | Separater Arbeitsauftrag: Was soll mit diesen Informationen untersucht und ausgegeben werden? |
| **Zufallsseed** | Technischer Parameter zur Zufallsvariation, sofern die Software ihn unterstützt; kein Forschungsdokument |

Research Seed und Recherchepaket dürfen inhaltlich verbunden sein. Der Aufgabenprompt wird separat abgelegt. Ein reiner Arbeitsauftrag ersetzt kein Forschungsdokument mit konkreten Entitäten und Beziehungen.

## 2. Regeln für alle Läufe

### 2.1 Herkunft und Informationsklassen

Jede wesentliche Aussage erhält eine Herkunft und eine der folgenden Einordnungen:

| Klasse | Beispiel für die Einordnung, ohne einen konkreten Wert vorzugeben |
|---|---|
| Beobachtung | Datierte Preisnotierung oder veröffentlichter historischer Messwert |
| Historische Schätzung | Geschätzte Förderung oder Nachfrage eines vergangenen Jahres |
| Externe Prognose | Projektion eines Herausgebers unter bestimmten Annahmen |
| Autorenmeinung | Interpretation oder Investmentthese einer Studie |
| Eigene Berechnung | Aus benannten Daten und dokumentierter Formel berechnete Kennzahl |
| Szenarioannahme | Hypothetischer Schock, Verhaltensparameter oder repräsentativer Akteur |
| Simulierter Befund | Aktion, Interview oder Reportaussage aus einem bestimmten Vorgängerlauf |

- Quellen-ID, Belegstelle und Datenzeitraum mitführen. Veröffentlichungsdatum, Abrufdatum und Beobachtungszeitraum unterscheiden.
- Unbekannte Werte bleiben offen oder `null`. Fehlwerte sind keine Nullen.
- Eine externe Prognose wird nach Ablauf ihres Horizonts nicht automatisch zum Istwert.
- Wiederholungen eines Simulationsbefunds machen daraus keine empirische Beobachtung. Spätere externe Bestätigungen zusätzlich verknüpfen, statt die Herkunft umzubenennen.
- Widersprüche, Revisionen und verschiedene Definitionen sichtbar erhalten. Keine unbemerkten Mittelwerte aus inkompatiblen Quellen bilden.

### 2.2 Ergebnisoffenheit und Diversität

- Forschungsfragen ohne gewünschte Kursrichtung oder vorgegebenen Sieger formulieren.
- Mindestens zwei unterschiedliche Interessenlagen und zwei konkurrierende Wirkungswege beschreiben. Für jeden zentralen Mechanismus einen Gegenmechanismus oder einen begründeten offenen Gegenbefund nennen.
- Für jede wichtige Belastung auch Entspannung, Anpassung oder eine begründete Gegenvariante berücksichtigen.
- Unterschiedliche Ziele, regionale Betroffenheit, Informationen, Reaktionsgeschwindigkeiten und Ressourcen zulassen. Quelleninstitutionen ersetzen keine Minen, Hersteller oder Anleger.
- Reale Personen und Organisationen nur mit belegten Eigenschaften beschreiben. Repräsentative Modellakteure und zugeschriebene Präferenzen ausdrücklich als Annahmen kennzeichnen.
- Abweichende und erfolglose Positionen aus Vorgängerläufen erhalten. Auswahlkriterien für die Übergabe dokumentieren; Originalexporte vollständig archivieren.
- Weder Konsens noch Häufigkeit simulierter Ausgänge sind ohne zusätzliche Validierung reale Eintrittswahrscheinlichkeiten.

### 2.3 Zahlen und Wirkungsmodelle

- Einheiten, Währung, Preisart, Frequenz, Datenstand und geografischen Bezug angeben. Bestände, Flüsse, Brutto-/Nettogrößen und Teilmengen unterscheiden.
- Berechnungen außerhalb des Sprachmodells nachvollziehbar durchführen und Eingabedaten sowie Methode sichern. Das Hochladen von Zahlen belegt weder ihre Verwendung noch eine Kalibrierung.
- Wesentliche Zahlen gegen Originaltabellen prüfen. Summen, Einheitenumrechnung und Rundungstoleranzen dokumentieren.
- Wirkungsrichtungen nicht als zwangsläufig behandeln: Materialknappheit, hohe Schulden oder Inflation legen für sich keinen bestimmten Metallpreis fest.
- Angeben, welche Entscheidungen tatsächlich modelliert werden und welche Zusammenhänge Agenten lediglich diskutieren. Ein Diskussionsmodell wird durch zusätzliche Dokumente nicht automatisch zu einem numerischen Marktmodell.
- Diskussionsrunden sind keine Kalenderjahre. Eine Zuordnung zu realen Perioden muss ausdrücklich definiert und als Modellannahme ausgewiesen werden.
- Bei numerischen Materialflüssen Bilanzgrenzen und Teilmengen beachten. Für numerische Preisprognosen zusätzlich Modellgleichungen bzw. Entscheidungsregeln, Kalibrierungsdaten und unabhängige Validierung belegen.

## 3. Mindestaufbau eines Research Seeds

| Bestandteil | Mindestinhalt |
|---|---|
| Identifikation | Titel, Version, Laufkennung, Sprache, Informationsstichtag und geplanter Forschungszeitraum |
| Forschungsfrage | Konkrete Frage, zu untersuchende Größen und ausdrücklich offene Ergebnisse |
| Ausgangswelt | Belegte Zustände mit Fakten-/Quellen-IDs; bestehende Belastungen von zusätzlichen Schocks unterscheiden |
| Akteure | Relevante Entscheidungsträger mit Zielen, verfügbaren Informationen, Entscheidungen und Beschränkungen |
| Beziehungen | Gerichtete Verbindung zwischen identifizierten Akteuren/Objekten; Beleg oder ausdrückliche Modellannahme |
| Mechanismen | Mögliche Wirkung, Gegenwirkung, Verzögerung und verbleibende Unsicherheit |
| Szenarien | Ausgangsstand, veränderte Annahmen, Beginn/Dauer und konkurrierende Reaktionen; keine unbelegten Wahrscheinlichkeiten |
| Zeit und Modellgrenzen | Untersuchungszeitraum gegenüber tatsächlichen Simulationsschritten; technische und ökonomische Grenzen |
| Vorgängerausgänge | Herkunftsläufe, übernommene Befunde, Minderheitspositionen und Änderungen seit der letzten Iteration |
| Auswertung | Erwartete Exporte und Kriterien für Datenverwendung, neue Mechanismen, Gegenbefunde und technische Vollständigkeit |

Konkrete Eigennamen und belegte Beziehungen aufnehmen, soweit sie für die Frage relevant und recherchierbar sind. Generische Rollen bei fehlenden Belegen als Modellrollen kennzeichnen. Die Zahl der Quellen oder Entitäten allein ist kein Qualitätsnachweis.

## 4. Mindestanforderungen an die Recherche

### Quellen und Fakten

- Für zentrale quantitative Ausgangswerte mindestens eine identifizierte Originalquelle oder einen ausdrücklich gekennzeichneten Ersatzbeleg sichern. Unbestätigte Schlüsselwerte dürfen nicht als Tatsachen in den Lauf eingehen.
- Bevorzugt Primärquellen und Originaldatensätze verwenden. Bei Sekundärquellen den Vermittlungsschritt sowie mögliche Interessen nennen. Zwei Berichte mit derselben Ursprungsquelle sind keine zwei unabhängigen Bestätigungen.
- Für zeitkritische Angaben einen Aktualisierungsbedarf festlegen und vor dem tatsächlichen Start nochmals prüfen. Ältere Studien bleiben mit ihrem damaligen Datenstand nutzbar.
- Wesentliche Argumente gegen die Ausgangsthese aktiv recherchieren. Nicht jede Perspektive benötigt dieselbe Zahl von Quellen, aber einseitige Abdeckung ist zu dokumentieren.
- Pro wesentlichem Fakt: Fakten-ID, Aussage/Wert, Informationsklasse, Einheit/Zeitraum, Quellen-ID und Fundstelle.
- Pro Beziehung: Subjekt-ID, Beziehungstyp, Objekt-ID, Quelle/Fundstelle und Evidenzklasse. Namensvarianten auf kanonische Akteur-IDs zurückführen.

### Datenreihen und Kennzahlen

- Originaldatei, Tabellenblatt/Spalten, Einheiten und Zeitachse sichern. Dubletten, fehlende Monate und unterschiedliche Abdeckung prüfen.
- Transformationen, Filter, Aggregation und Umrechnung dokumentieren. Rohdaten unverändert aufbewahren.
- Kennzahlen mit Formel, Stichprobe und Grenzen ablegen. Beispielsweise Monatsmittel nicht als Tageshochs oder tatsächliche Barrenpreise bezeichnen.
- Metallpreise in unterschiedlichen Währungen nur mit dokumentierten Wechselkursen vergleichen. Nominale und reale Renditen bzw. Zinsen getrennt führen.

### PDFs und Konvertierung

- Original in `raw/`, vollständige Extraktion und bereinigte Fassung separat in `processed/` speichern.
- Quellenangaben, Einheiten, Fußnoten und Zuordnung zur physischen PDF-Seite erhalten. Gedruckte Seitenzahlen zusätzlich angeben, wenn sie abweichen.
- Dekorationen und wiederkehrende Seitenelemente dürfen entfallen. Datenhaltige Abbildungen entweder kontrolliert auswerten oder ausdrücklich als noch nicht digitalisiert kennzeichnen.
- Tabellen und für die Untersuchung wesentliche Diagrammwerte am Original prüfen. Umfang der Sichtprüfung und unlesbare Seiten dokumentieren; eine vollständige Konvertierung ist keine vollständige Inhaltsprüfung.
- Für den Upload ein kuratiertes Recherchepaket verwenden. Keine bloße Aneinanderreihung von Aufgaben, Navigation, Werbung oder Bildbeschriftungen als Forschungsgrundlage ausgeben.

## 5. Iteration: Jeder Lauf informiert den nächsten

Der nächste Lauf übernimmt die ausgewerteten Ausgänge seiner Vorgänger zusammen mit neuer Evidenz. Der bisherige Konsens ist dabei eine mögliche Position unter mehreren.

1. Originalexporte sichern und zu den tatsächlich verwendeten Eingaben zuordnen.
2. Anfangsbeiträge, autonome Agentenaktionen, Interviews und Reportinterpretation unterscheiden.
3. Relevante Befunde samt abweichenden Positionen mit Lauf-ID und Exportbeleg in `inputs/prior-run-findings.json` und `.md` übertragen. Kürzungen und Auswahlkriterien nachvollziehbar machen.
4. Neue externe Daten, Gegenbelege und neue Annahmen separat ergänzen.
5. Veränderte Akteursmischung, Szenarien und Parameter dokumentieren. Bei Bedarf zusätzliche Vergleichsvarianten mit nur einer geänderten Annahme abzweigen.

Aus einer Iteration mit mehreren Änderungen lassen sich keine eindeutigen Einzeleffekte ableiten. Unterschiedliche Zufallsseeds oder Wiederholungen ergänzen das Vorgehen, soweit technisch unterstützt.

## 6. Kopierbare Aufbauvorlage je Lauf

Die folgenden Überschriften in eine neue Datei unter `runs/<lauf-id>/inputs/` kopieren und ausfüllen. Leere Tabellen sind Platzhalter, keine Datensätze. Der genaue Simulationsprompt kommt in eine separate Datei.

```markdown
# Research Seed: <Titel>

Version: <Version>
Laufkennung: <ID>
Sprache: <Sprache>
Informationsstichtag: <Datum und bei Bedarf Uhrzeit/Zeitzone>
Forschungszeitraum: <Zeitraum>
Regionen/Währungen: <Abgrenzung>
Zentrale Regelvorlage: SIMULATION_TEMPLATE.md, Version <Version>
Vorgängerlauf-IDs: <IDs oder keine>

## Forschungsfrage und untersuchte Größen
<Frage, Größen, offene Ergebnisse und Grenzen>

## Quellenregister
| Quellen-ID | Herausgeber/Titel | URL/Originaldatei | Publikation/Abruf | Datenzeitraum | Interessen/Zugriffsgrenzen |
|---|---|---|---|---|---|

## Belegte Ausgangswelt
| Fakten-ID | Aussage/Wert | Informationsklasse | Einheit/Währung/Zeitraum | Quelle/Fundstelle | Unsicherheit/Revision |
|---|---|---|---|---|---|

## Datenreihen und eigene Berechnungen
<Dateien, Spalten, Einheiten, Abdeckung, Fehlwerte, Transformationen und Methoden>

## Akteure und unterschiedliche Interessen
| Akteur-ID | Kanonischer Name/Aliase | Rolle und Ziel | Informationen/Entscheidungen | Ressourcen/Beschränkungen | Beleg oder Modellannahme |
|---|---|---|---|---|---|

## Beziehungen
| Beziehungs-ID | Subjekt-ID | Beziehung | Objekt-ID | Quelle/Fundstelle oder Modellannahme | Gültigkeitszeitraum |
|---|---|---|---|---|---|

## Konkurrierende Mechanismen
<Wirkung, Gegenwirkung, Verzögerung, Interessenkonflikt und offene Evidenz>

## Szenarien
| Szenario-ID | Ausgangsstand | Geänderte Annahme | Beginn/Dauer | Erwartete konkurrierende Reaktionen | Offene Größen |
|---|---|---|---|---|---|
<Bestehende Belastungen nicht unbemerkt nochmals als neue Schocks anrechnen.>

## Übernommene Ausgänge früherer Läufe
<Verweise auf prior-run-findings.json/.md; Herkunft, Auswahlkriterien,
abweichende Positionen, neue Gegenbelege und ungeklärte Widersprüche>

## Tatsächliche Simulation und Zeitzuordnung
<Was wird entschieden, was nur diskutiert? Runden, Plattformen und bekannte
Parameter; Kalenderzuordnung nur mit ausdrücklich dokumentierter Annahme.>

## Erwartete Exporte und Auswertung
<Bericht, Aktionen, Graph, Konfiguration, Status und Logs; Prüfkriterien für
Informationsverwendung, autonome Entwicklungen, Widersprüche und Diversität>

## Offene Punkte und Änderungen seit dem Vorgänger
<Fehlende Daten, nicht unterstützte Funktionen, Annahmen und Änderungen>
```

## 7. Startprüfung und Mindeststatus

Die Startprüfung im Laufordner unter `inputs/start-check.md` dokumentieren. Sie hält offene Punkte und den vorgesehenen Aussageumfang fest.

### Vor dem technischen Test

- [ ] Forschungsfrage, Informationsstichtag und Quellenstände sind angegeben.
- [ ] Tatsächliche Upload-Dateien und separater Prompt sind bestimmt.
- [ ] Zentrale Aussagen, Einheiten und Informationsklassen sind nachvollziehbar.
- [ ] Akteure, Interessen und Beziehungen sind belegt oder als Modellannahmen gekennzeichnet.
- [ ] Gegenmechanismen und unterschiedliche Perspektiven sind enthalten.
- [ ] Vorgängerbefunde sind mit Herkunft übernommen oder es ist dokumentiert, warum noch keine vorliegen.
- [ ] Fehlende Daten und technische Unbekannte sind aufgeführt.

### Nach Import, vor einer inhaltlichen Auswertung

- [ ] Wichtige Fakten sind mit den korrekten Werten/Einheiten im Graphen, in Textpassagen oder im Agentenkontext tatsächlich wiederzufinden; Fundstelle dokumentiert.
- [ ] Relevante Akteure und Beziehungen wurden übernommen; Namensduplikate und falsche Rollen wurden geprüft.
- [ ] Fehlende Importinhalte sind dokumentiert. Bei fehlendem Markt-/Beziehungsmodell ist der Lauf entsprechend als Erkundungs- oder Funktionstest eingeordnet.
- [ ] Modell, Version, Parameter, Rundenzahl und Zufallsseed sind soweit verfügbar erfasst; nicht verfügbare Angaben bleiben offen.
- [ ] Die tatsächlich gestarteten Eingaben einschließlich Vorgängerübergabe sind kopiert und mit Prüfsummen gesichert.

### Nach Ausführung

- [ ] Tatsächlicher Abschluss-/Abbruchstatus und abgeschlossene Runden je Plattform sind geprüft.
- [ ] Anfangsbeiträge sind von autonomen Aktionen und Reportaussagen getrennt.
- [ ] Kernaussagen des Berichts besitzen Exportbelege; verwendete externe Fakten sind zugeordnet.
- [ ] Mehrheits-, Minderheits- und Gegenbefunde sowie Fehler sind für die nächste Iteration erhalten.

| Status | Bedeutung |
|---|---|
| `draft` | Vorbereitung; Mindestangaben oder Belege noch offen |
| `technical_test` | Funktionsprüfung mit ausdrücklich dokumentierten Daten-/Modellgrenzen; keine daraus abgeleitete Marktvalidierung |
| `prepared_for_import` | Inhaltliche Mindestangaben vorliegend, technische Übernahme noch zu prüfen |
| `import_checked` | Relevante Informationsübernahme geprüft; Ausführung noch nicht dadurch bestätigt |
| `results_reviewed` | Ausgänge und Grenzen ausgewertet; Übergabe an nächste Iteration möglich |

Diese Statuswerte beschreiben die Vorbereitung/Auswertung. In `run.json` bleibt der tatsächliche Ausführungsstatus separat. `results_reviewed` bedeutet keine empirische Kalibrierung oder bewiesene Prognosequalität.

## 8. Ablage und bestehende Dokumente

- [Repository-Übersicht](README.md)
- [Recherchebestand](RESEARCH.md) und [Quellenregister](sources/README.md)
- [Laufablage und Ergebnisimport](runs/README.md)
- [Vorlage für neue Läufe](runs/_template/README.md)
- [Iteration und Diversität](notes/iterative-run-design.md)
- [Iran-/Energie-Szenarien](notes/iran-energy-scenarios.md)
- [Ursprünglicher thematischer Seed](precious-metals-research-seed.md)

Die tatsächlich verwendete Version dieser Regelvorlage beim Start im Lauf dokumentieren, bei Bedarf als Kopie in `inputs/`. Archivierte Eingaben und Vorgängerergebnisse werden durch eine spätere Aktualisierung dieser Regeln nicht überschrieben.

## Änderungsverlauf

- **1.0, 2026-11-01:** Erste zentrale Fassung. Bestehende Vorgaben zu Quellen, Seed-Aufbau, Aufbereitung, Mindestprüfung, iterativer Übergabe und Diversität zusammengeführt.
