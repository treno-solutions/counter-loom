# 0004 · Reduziertes Lernmodell mit System Dynamics und gezielten Agentenentscheidungen

Datum: 2. November 2026 · Status: System Dynamics als bevorzugter Ansatz festgehalten; konkrete technische Auswahl und Lernmodule offen. Vollständiger Arbeitsplan: [BUILD_PLAN.md](../../BUILD_PLAN.md).

## Präzisierung gegenüber 0002/0003

Das Ziel bleibt eine verbundene Welt über mehrere Ebenen bis zur individuellen Investmententscheidung. Die Weltwirtschaft ist zunächst ein schematischer äußerer Rahmen. Volkswirtschaft, Unternehmen, Familie/Haushalt und Person werden nur so fein modelliert, wie die jeweilige Lernfrage es benötigt. Eine umfassende Reproduktion der realen Volkswirtschaft ist keine Voraussetzung für den ersten nutzbaren Ausschnitt.

Die zuletzt genannten Ereigniswege waren Beispiele. Sie legen weder das erste Lernmodul noch eine zwingende Kausalkette fest. Die in Entscheidung 0003 beschriebene makroökonomische Architektur bleibt ein fachlicher Erweiterungsrahmen. Die Prüfung einer vollständigen Makroplattform ist nicht länger zwingend der erste Umsetzungsschritt.

## Entscheidung

- System Dynamics für Bestände, Flüsse, Rückkopplungen und Verzögerungen als bevorzugten Ansatz prüfen.
- Ereignisse und Zustandsmodelle für diskrete Vorgänge und aktive Pläne ergänzen.
- Regelmäßige Abläufe und wirtschaftliche Folgen algorithmisch berechnen. Bekannte Identitäten, vertragliche Regeln, empirische Reaktionsbeziehungen und eigene Annahmen getrennt halten.
- LLMs später gezielt für ausgewählte persönliche, familiäre oder betriebliche Abwägungen einsetzen. Keine generative Ausführung jeder Operation und kein pauschaler Aufruf für jeden Akteur in jeder Periode.
- Bei der groben Darstellung anfangen und fachlich nur dort verfeinern, wo zusätzliche Details eine Lernfrage beantworten. Aggregat und Details dürfen Bestände nicht doppelt zählen.
- Eine Darstellung ist noch nicht beschlossen. Eine laufende Grafik muss gespeicherte Vorgänge zeigen; die Auswahl einer Ansicht löst keine neuen Modellentscheidungen aus.
- Zuerst einen vollständigen, begrenzten Pfad vom Ereignis über veränderte wirtschaftliche Möglichkeiten bis zur Entscheidung und ihren Folgen bauen. Dann vergleichend prüfen und erweitern.

## Werkzeuge und Grenzen

BPTK-Py ist aufgrund dokumentierter System-Dynamics-, Ereignis- und Agentenmechanismen der erste Kandidat für eine technische Vorauswahl. Das ist noch keine Installation oder Wahl als Produktgrundlage. Minsky ist ein Vorbild für sichtbare Bestände und Finanzflüsse; BeforeIT/JMAB bleiben makroökonomische Referenzen. Keine dieser Quellen liefert bereits die benötigte validierte Persona-Population oder eine fertige Workshop-Anwendung.

Die fachliche Verbindung zwischen Ebenen wird versioniert und geprüft. Deterministisch ausführbar bedeutet nicht empirisch wahr. Eine Regel für eine wirtschaftliche Reaktion benötigt weiterhin eine Quelle, Kalibrierung oder sichtbare Annahmenkennzeichnung.

## Ergebnis dieser Planungsphase

Ziel, Architektur, Arbeitsphasen, Prüfergebnisse als Übergangskriterien, offene Entscheidungen und nächster technischer Prüfauftrag sind in BUILD_PLAN.md konsolidiert. Bestehende Forschungsdaten und archivierte Simulationseingaben bleiben unverändert. Keine neue Simulation gestartet.
