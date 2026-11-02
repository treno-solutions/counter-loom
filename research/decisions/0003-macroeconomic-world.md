# 0003 · Makroökonomische Welt als Grundlage des Workshop-Simulators

Datum: 2. November 2026 · Status: präzisierte Zielarchitektur, keine Implementierung oder validierte Modellwahl. Ergänzt 0001/0002. Die frühere Annahme, dass exogene Wirtschaftsverläufe für das Gesamtziel ausreichen, gilt nur noch für vorbereitende Teiltests.

## Ziel

Eine über Zeit laufende Volkswirtschaft mit Haushalten einschließlich Nichtanlegern, Unternehmen, Geschäftsbanken, Staat und Zentralbank. Wirtschaftliche Entscheidungen verändern Ausgaben, Einnahmen, Beschäftigung, Investitionen, finanzielle Bestände und Verpflichtungen. Ein Außenwirtschafts-/Energiesektor ist je nach Szenario explizit oder mit dokumentierten Randbedingungen einzubeziehen.

Die Workshop-Oberfläche soll tatsächliche Modellzustände und Vorgänge sichtbar machen. Eine schematische Schaltzentrale mit verbundenen Sektorboxen ist ebenso offen wie eine räumlichere Darstellung. Eine bestimmte Darstellung ist nicht beschlossen. Aktivierte Verbindungen dürfen nicht bloß eine festgelegte Geschichte abspielen; sie müssen sich auf die protokollierten Vorgänge des laufenden Modells beziehen.

## Passende Modellklasse

Zu prüfen sind agentenbasierte makroökonomische Modelle, insbesondere die Verbindung mit Stock-Flow Consistency (SFC). SFC bedeutet konsistente Beziehungen zwischen Beständen, Transaktionen und Gegenpositionen. Es bedeutet keine konstante Geldmenge und beweist allein keine realistische Verhaltensdynamik.

- Haushalte erhalten Einkommen und Transfers, konsumieren, sparen, halten Vermögen, bedienen Verpflichtungen und können investieren.
- Unternehmen beschäftigen Menschen, produzieren, setzen Preise, zahlen Löhne, finanzieren sich und investieren.
- Geschäftsbanken führen Einlagen und Kredite, beurteilen Finanzierung und verbuchen Zinsen, Tilgungen, Ausfälle sowie die nötigen Gegenpositionen.
- Der Staat erhebt Steuern, gibt Mittel aus, leistet Transfers und trägt explizit modellierte Schulden und Zinslasten.
- Die Zentralbank beeinflusst dokumentierte monetäre Bedingungen. Geschäftsbankeinlagen und Zentralbankgeld bleiben unterscheidbar.
- Der Außenbereich erfasst gegebenenfalls Importe, Exporte und finanzielle Gegenpositionen; insbesondere importierte Energie ist nicht automatisch ein rein inländischer Geldfluss.

Die konkrete institutionelle Ordnung ist festzulegen. Ein einzelner Staat im Euroraum und ein Staat mit eigener Währung haben unterschiedliche Handlungsmöglichkeiten. Keine allgemeine Staatshaushaltsregel aus den Regeln eines Privathaushalts ableiten.

## Geld, Zins und Schulden

Geldschöpfung und Tilgung müssen als zulässige Bilanzvorgänge abbildbar sein. Bei einer Bankkreditvergabe können gleichzeitig eine Einlage und eine Kreditforderung entstehen; das ist keine unbelegte Erfindung von Mitteln. Die entsprechenden Verbindlichkeiten und späteren Tilgungen müssen mitgeführt werden. Ein LLM darf solche Buchungen nicht frei behaupten.

Staatsschulden benötigen modellierte Gläubiger, Instrumente, Laufzeiten und Zinsbedingungen. Eine Leitzinsänderung verändert nicht automatisch die Verzinsung sämtlicher alter Verträge. Einlagenzinsen, Kreditzinsen, Refinanzierung und Anleiherenditen sind unterschiedliche Größen. Ihre Übertragung, Verzögerungen und Verhaltensreaktionen müssen dokumentiert sein.

Geldmenge, Staatsverschuldung und Investitionen sind eigenständige Beobachtungsgrößen. Sinkende Zinsen schreiben keine feste Geldmengenausweitung oder Investitionsreaktion vor. Welches Ergebnis entsteht, hängt im Modell unter anderem von Kreditnachfrage, Vergaberegeln, Erwartungen und Finanzierungsbedingungen ab. Die Definition des gemessenen Geldaggregats ist vor dem Lauf festzuhalten.

## Rollen von Wirtschaftsmodell und generativen Agenten

Der ökonomische Kern führt Zeit, Bestände und Buchungen sowie die implementierten Märkte und institutionellen Regeln. Entscheidungskomponenten bestimmen Verhaltensweisen innerhalb dieses Rahmens. Vorhandene regelbasierte und lernende Komponenten sind als Ausgangspunkt zu prüfen.

LLMs können später ausgewählte Haushalts- oder Unternehmensentscheidungen, Informationsverarbeitung und Kommunikation ergänzen. Die gesamte Volkswirtschaft durch freie Texte berechnen zu lassen, ist nicht die Zielarchitektur. Zunächst muss eine bestehende makroökonomische Grundlage ohne LLM-Erzählung laufen und prüfbar sein. Danach den zusätzlichen Nutzen einer begrenzten generativen Anbindung untersuchen; keine eigene umfassende Plattform vor diesem Vergleich entwickeln.

## Sichtbare Wirkungsketten

Eine mögliche Kette Energiepreise → Betriebskosten → Preise oder Beschäftigung → Haushaltseinkommen/-ausgaben → Konsum → andere Unternehmensumsätze ist ein Untersuchungsgegenstand. Die Kette ist nicht als zwangsläufiges Ergebnis festgeschrieben. Eigenkapitalpuffer, Preisüberwälzung, Nachfrage, Transfers und andere Modellentscheidungen können Wege verändern oder unterbrechen.

Die Darstellung muss deshalb pro Verbindung Ursprung, Ziel, Ereignistyp, Periode und tatsächlich berechnete Größe anzeigen können. Ausgewählte Akteure öffnen ihren Zustand und die zeitgleich protokollierte Entscheidungsgrundlage. Annahmen, Buchungsregeln, simulierte Ergebnisse und Agentenbegründungen bleiben unterscheidbar. Grafische Bewegung allein ist kein Kausalnachweis.

## Konsequenz für die bisherige Forschung

Die Gesprächspiloten 004/005 sind Teilprüfungen von Personen, Gedächtnis und Zustellung. Sie haben weder einen makroökonomischen Kreislauf noch Staatsverschuldung oder Geldschöpfung geprüft. Die spätere Zielpräzisierung verändert ihre archivierten Ergebnisse nicht.

Die nächste Vorauswahl richtet sich vorrangig auf ökonomische Modellkerne und ihre Erweiterbarkeit. Ein reines Persona-Framework oder eine ansprechende Oberfläche reicht nicht. Ebenfalls offen bleibt, ob eine vorhandene regelbasierte Makrosimulation den Workshopzweck bereits erfüllt; LLMs sind kein Selbstzweck.

## Primärquellen und erster Suchstand

- [Caiani et al., Agent based-stock flow consistent macroeconomics: Towards a benchmark model](https://business.columbia.edu/sites/default/files-efs/imce-uploads/Joseph_Stiglitz/Agent%20based-stock%20flow.pdf), 2016: sektorübergreifender AB-SFC-Ansatz. Ausgewählter Textauszug und Sektorschaubild geprüft, kein vollständiger Replikationslauf.
- [JMAB](https://github.com/S120/jmab) und [Benchmarkmodell](https://github.com/S120/benchmark): Autorendokumentation beschreibt einen makroökonomischen SFC-ABM-Kern. Nur Dokumentationssichtung; Wartung, Lizenzen, Installation und heutige Eignung noch zu prüfen.
- [BeforeIT.jl](https://github.com/bancaditalia/BeforeIT.jl): Makro-ABM-Software im Repository der Banca d'Italia, als weiterer Kandidat gefunden. README/Repository-Metadaten geprüft, keine eigene Installation, keine bestätigte Abdeckung sämtlicher Anforderungen. Paper- und aktuelle Repository-Lizenzangaben sind bei einer konkreten Version gesondert abzugleichen.
- [Bank of England, Money creation in the modern economy](https://www.bankofengland.co.uk/quarterly-bulletin/2014/q1/money-creation-in-the-modern-economy), 2014: Erklärung der Bankgeldschöpfung und geldpolitischen Begrenzung. Institutioneller Hintergrund, keine fertige Kalibrierung unserer Modellwelt.

Stand der Prüfung: 2. November 2026. Noch kein neuer Modelllauf, keine Implementierung und keine abschließende Empfehlung.
