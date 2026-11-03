# Laufende Modellwirtschaft · aktuelle Fassung v13

V13 ergänzt ein [anpassendes Staatsbudget](PUBLIC_BUDGET_MODEL.md). Anhaltende Defizite verändern Beschaffung und öffentliche Stellen; aktuelle öffentliche Arbeit wird nur nach bestätigter Finanzierung freigegeben. Alte Lohnansprüche, tatsächliche Nachzahlungen und ungedeckter Sozialbedarf bleiben sichtbar. Das ist eine illustrative ausgabenseitige Reaktion, keine Zusage eines ausgeglichenen Haushalts.

V12 ergänzt [Gewinnvortrag und zusätzliche Quartalsausschüttungen](PROFIT_POLICY.md). Erwirtschaftete, nach Verlustverrechnung verbleibende Gewinne können oberhalb des Betriebspuffers und gebundener Maschinenmittel an die Eigentümer zurückfliessen. Gewinnvortrag und Kontoguthaben bleiben getrennt. Der Referenzmodus erhält die frühere Auszahlungsregel für kontrollierte Vergleiche; Staats- und Steuerregeln bleiben unverändert.

V11 ergänzt [befristete Betriebsschliessungen und Kurzarbeitsleistung](CRISIS_MODEL.md). Eine angeordnete Produktions-/Verkaufssperre erhält Arbeitsverträge; die Ersatzquote ist in der Oberfläche zwischen 0 und 60 % des vorherigen Netto-Arbeitszeitlohns wählbar. Staatszahlungen sind kassen-/kreditbegrenzt. Erhaltungsenergie von 300 € pro geschlossenem Betrieb und Monat belastet das Firmenkonto. Zwei getrennte Fortsetzungen erlauben einen kontrollierten Vergleich mit sechs Monaten Nachbeobachtung. Keine gesetzliche oder empirische Corona-Nachbildung.

V10 ergänzt [proportionale Arbeitszeit und Betriebszustände](BUSINESS_MODEL.md). Der Vollzeitlohnsatz bleibt fest; private Lohnzahlung und Arbeits-/Anlagenkapazität folgen der geplanten, tatsächlich bezahlten Arbeitszeit. Eine begrenzte Verlustbrücke, Stilllegung und zweistufiger Wiederanlauf ersetzen die reine Vollzeitstellen-Schwelle. Zustände und Quoten werden historisch exportiert.

V9 ersetzt die Wiederauffüllung der Anfangskasse durch eine [begrenzte Staatsreserve](FISCAL_MODEL.md). Die Oberfläche zeigt Kasse, Haushaltssaldo, Staatsschuld, Zinszahlungen und tatsächliche öffentliche Lohnrückstände getrennt. Der normale Lauf ist offen; Energie- und Konsumeingriffe können zurückgenommen und später erneut angewandt werden. Diagramme zeigen die letzten 36 Monate, der Export behält den gesamten Lauf. Die früheren 24 Monate sind weiterhin mögliche feste Beobachtungsfenster für Vergleiche.

V8 ergänzt [begrenzte Preise und Kaufkraft](PRICES_MODEL.md): zusätzliche Energie-Stückkosten werden zu 50 % mit einem Monat Verzögerung und höchstens 1 % Preisänderung pro Monat weitergegeben. Nominale Löhne, Transfers und Budgets bleiben fest. Haushaltshistorien trennen Ausgaben, gelieferte Mengen und deren Wert zu Startpreisen. Maschinenpreise werden bei Kreditgutschrift fest gebunden. Die [V8-Prüfung](../qa/prices-v8-plausibility.md) ergänzt die älteren versionsgebundenen Belege.

V7 ergänzt die [Leitzins- und Vertragsregeln](RATES_MODEL.md). Eine vorgemerkte Leitzinsänderung wirkt am folgenden Monatsbeginn. Der variable Alltagskredit übernimmt den Vormonatsleitzins; der feste Werkstattkredit behält 2 %. Neue Maschinenkredite und Staatskreditbeträge binden bei Gutschrift den Leitzins plus ihren jeweiligen Modellaufschlag. Alte Festzinsen und Zinsrückstände werden nicht rückwirkend verändert. Die Staatszinsbasis wird pro festem Kreditbetrag dokumentiert.

Die [V7-Prüfung](../qa/rates-v7-plausibility.md) ergänzt die unveränderten älteren Belege. Der Modell-Leitzins ist eine externe Vorgabe, keine zusätzliche Zentralbankbilanz. Alle Anfangswerte und Übertragungsregeln sind eigene illustrative Annahmen.

## Staatsfinanzierung aus v6

V6 ergänzt die [Staatsfinanzierung](FISCAL_MODEL.md): monatliche Kassenfehlbeträge werden vorrangig durch einen Staatskredit der bestehenden Geschäftsbank finanziert. Obergrenze 50.000 €, anfänglicher Jahreszins 3 % bei 2 % Modell-Leitzins, Zinsbasis bestehende Schuld am Monatsbeginn. Überschüsse tilgen; untermonatliche Kredite werden beim Abschluss angerechnet. Kreditgutschriften sind Finanzierung und keine Steuereinnahme. Die Bankforderung und die Staatsschuld werden gemeinsam gebucht; Zinsen sind Bankertrag und fließen in die bestehenden tatsächlichen Ausschüttungen ein. Keine Zentralbankfinanzierung oder Anleihemärkte.

Die [V6-Prüfung](../qa/fiscal-v6-plausibility.md) ergänzt die unveränderten Belege älterer Fassungen. Elf Akteure bleiben erhalten; die damalige 24-Monats-Grenze ist seit V9 optional. Nominallöhne bleiben fest; seit V8 folgen Preise der begrenzten Energiekostenregel. Die aktuelle staatliche Finanzierung ersetzt den früheren ausschließlichen Verbrauch der Staatskasse.

## Außenhandelsgrundlage v5

Die aktuelle Unternehmenslogik steht im [Unternehmenskonzept](COMPANY_MODEL.md), die Geld-/Kreditbuchungen im [Bankkonzept](BANKING_MODEL.md). V5 ergänzt den [Außenhandelsanschluss](FOREIGN_MODEL.md): das vorhandene Auslandskonto kauft tatsächliche Waren und führt dadurch Geld ins Inland zurück. Die damalige Begrenzung auf 24 Monate und feste Preise ist durch die Erweiterungen V8/V9 ersetzt; dieselben elf Akteure bleiben erhalten.

Das Ausland beginnt mit 0 €. Es wünscht monatlich 6 Alltagsgüter / 2 Werkstattgüter im Wert von 900 €. Nur Anfangsguthaben des Monats finanziert den anteiligen Kaufplan. Öffentliche Aufträge und Haushalte kaufen zuerst; verbleibende freie Ware kann gegen tatsächliche Zahlung exportiert werden. Energieeingänge desselben Monats erhöhen das vorab festgelegte Kaufbudget nicht. Einzelne Exportlieferungen sind durch Zahlungsbeleg, Stückzahl, Lagerabgang und Warenkosten nachprüfbar. Diese Parameter und Reihenfolge sind illustrative Annahmen.

Die Reihenfolge bleibt Produktion/Löhne → Steuern/Transfers → Käufe einschließlich Exporten → Investitionen → Abschluss. Der erste Monat hat Energieimporte ohne finanzierbare Exportbestellung. Spätere Exporterlöse fließen in Unternehmensumsatz, Warenkosten und Absatzplanung ein. Der Außenhandelssaldo wird nicht vorgegeben. Inland und Ausland verschieben vorhandene Einlagen; nur die getrennten Bank-/Kreditvorgänge verändern die Summe aller Kundeneinlagen.

[Unabhängige V5-Prüfung](../qa/foreign-v5-plausibility.md). Rückstände, endlicher Staatskassenpuffer und Staatskreditrahmen, fehlende Abschreibung und begrenzte Preisbildung bleiben bekannte Grenzen. Kein langfristiger Gleichgewichts-, Prognose- oder Workshop-Wirksamkeitsnachweis.

## Unternehmensentwicklung v4

V4 ersetzte die früheren Produktions-, Personal- und Gewinnregeln: geglättete finanzierbare Nachfrage, Lagerpuffer, durch bezahlte Inputs begrenzte Produktion, gleitende Lagerkosten, verzögerte tragfähige Stellenplanung und tatsächliche begrenzte Eigentümerausschüttung. Energie kostet 5 € je Alltags- beziehungsweise 9 € je Werkstatteinheit, beim Energieschock doppelt so viel. Ein Lohn verursacht auch bei ungenutzter Kapazität Aufwand. Die sechs Haushalte sind zu gleichen Teilen Eigentümer. Ausschüttungen sind für den folgenden Kaufplan verfügbar und in diesem begrenzten Steuerrahmen nicht zusätzlich besteuert. Kreditlieferung erfolgt vor dem Unternehmensabschluss; Kreditgutschrift, Tilgung und Maschinenkauf bleiben getrennte Vorgänge.

## Historische Entwicklung bis v3

Die folgenden Abschnitte dokumentieren die früheren Fassungen. Insbesondere die dort genannte 240-Monats-Grenze sowie alte Energie-, Personal- und Produktionsregeln sind durch V4/V5 ersetzt. Aussagen über fehlende Auslandsrückflüsse beschreiben den Stand bis V4. Archivierte Prüfberichte bleiben unverändert.

### Laufender Wirtschaftskreislauf · POC 02

Version 0.3 · Modellklassifikation `illustrative_circular_flow_v3` · 2. November 2026 · Technischer Lernversuch, keine kalibrierte Volkswirtschaft. Dieses Konzept begrenzt die folgende Implementierung. POC 01 bleibt als Haushaltsansicht erhalten.

## Frage und Abnahme

Kann eine kleine Modellwirtschaft ohne weitere Eingriffe Monat für Monat laufen, während Zahlungen und Güterlieferungen die Zustände ihrer tatsächlichen Gegenparteien verändern? Übersicht, Sektor und Einzelsystem zeigen denselben Zustand und dieselbe globale Zeit. Animationen werden ausschließlich aus verbuchten Vorgängen gespeist. Pausieren hält die Berechnung an; der nächste Schritt führt eine neue Buchungsphase im Python-Kern aus.

## Systeme und Grenze

Sechs fiktive Haushalte; zwei Unternehmen (Alltagsgüter und Werkstatt/Technik); Staat; Finanzsektor; explizites Auslandskonto für vereinfachte Energieimporte. Vier Haushalte arbeiten zunächst zu je zwei in den Unternehmen, zwei im öffentlichen Dienst. Alle Konten gehören genau einem System. Sektoren sind Aggregationen, keine zusätzlichen Konten. Die Energie-Gegenpartei bleibt eine sichtbar vereinfachte Außengrenze.

Jedes System besitzt Kennung, Bestände, Eingänge, Ausgänge, Regeln und ein Monatsprotokoll. Explizite Systemeingänge und Ausgänge in `systems.py` sowie getrennte Regeln für Haushalt, Unternehmen, Staat und Finanzsektor werden durch den geprüften BPTK-Agentenscheduler aufgerufen. Ein System kann mit belegten Testzahlungen von Außenanschlüssen geprüft werden. In der integrierten Welt ersetzen die verbundenen Systeme diese Anschlüsse vollständig; keine zusätzlichen fiktiven Löhne neben echten Unternehmenszahlungen.

## Anfangszustand und eigene Annahmen

Alle Zahlen und Verhaltensschwellen sind **eigene illustrative Testannahmen**, keine Forschungsergebnisse über Anleger oder reale Länder. Kein LLM und keine zufällige Psychologie.

- Je Haushalt 3.000 € verfügbare Zahlungsmittel; Vollzeit-Bruttolohn 2.400 € pro Vertrag (betriebliche Auszahlung seit V10 proportional zur Arbeitszeit), Einkommensteuer 30 %. Unbeschäftigte erhalten, soweit finanzierbar, 1.000 € Transfer.
- Unternehmen je 24.000 € Zahlungsmittel und 12.000 € bestehende Verbindlichkeit gegenüber dem Finanzsektor. Einfache jährliche Kreditzinsen 2 %, keine Tilgung dieser Altbestände. Ein zusätzlicher, begrenzter Maschinenkredit mit eigenem Zinssatz und Tilgung ist im [Bankkonzept](BANKING_MODEL.md) definiert.
- Staat 80.000 € und Ausland 0 € Kundeneinlagen. Der Finanzsektor besitzt 10.000 € Eigenkapital, das nicht zum Kundengeld addiert wird. Anfangseinlagen aller Nichtbanken: 146.000 €. Die einfache Bankbilanz ergänzt 132.000 € feste Reserveposition und 24.000 € bestehende Kreditforderungen. Siehe [Bankgrenze und Buchungen](BANKING_MODEL.md); keine Behauptung einer realen Geldmengenstatistik.
- Haushalt plant den größeren Betrag aus 1.000 € Grundbedarfsbudget und 95 % seines laufenden Nettoeinkommens. Beim Konsumeingriff sinkt der einkommensabhängige Anteil auf 65 %; der Grundbedarfsplan bleibt bestehen. Das gesamte finanzierbare Kaufbudget ist durch den vorhandenen Kontostand begrenzt. Damit kann auch ohne neues Einkommen aus früher angespartem Geld gekauft werden. Die 1.000 € sind eine eigene illustrative Testannahme, keine empirische Bedarfsgrenze. Kaufbudget 55 % Alltagsgüter, Rest Werkstattprodukte. Nicht konsumiertes Geld bleibt auf dem Konto; kein Wertpapiermarkt.
- Alltagsbetrieb: 36 Einheiten je Beschäftigtem und Monat, anfangs 100 € Stückpreis. Werkstatt: 20 Einheiten, anfangs 150 €. Energie kostet je produzierter Einheit anfangs 5 € beziehungsweise 9 €, beim Energieschock das Doppelte. Produktionsmenge benötigt finanzierte Arbeit und Energie; zusätzliche Anlagen wirken nur bei aktivem Betrieb. Lagerware bleibt erhalten und wird zu Herstellungskosten geführt. Seit V8 gelten [verzögerte, teilweise Preisänderungen](PRICES_MODEL.md). Ganze Gütereinheiten und die feste Budgetaufteilung können ungenutzte Beträge auf dem Haushaltskonto lassen.
- Öffentliche Beschaffung bis zu 1.200 € je Unternehmen/Monat. Steuer auf positive operative Monatsüberschüsse 20 %. Investitionsausgaben sind ein Vermögenszugang und kein laufender Verbrauch; Güter werden geliefert und beim Lieferanten ausgebucht.
- Der Alltagsbetrieb kann nach zwei Monaten Warenengpass eine Anlage aus acht Werkstatteinheiten zum aktuellen Stückpreis kaufen, frühestens drei Monate nach der vorherigen Eigeninvestition. Freie Ware und ein finanzierter Betriebspuffer sind Voraussetzung. Ein gesonderter Maschinenkredit kann den dokumentierten Einmalvertrag finanzieren. Jede gelieferte Anlage erhöht die Kapazität ab Folgemonat um vier Einheiten; keine Abschreibung im Lernlauf.
- Liegen Umsätze zwei Monate unter 80 % der laufenden betrieblichen Kosten, wird zum Folgemonat eine Stelle abgebaut. Bei finanzierbarer, wegen fehlender Ware nicht bedienter Nachfrage und drei verfügbaren Monatslöhnen kann eine unbeschäftigte Person eingestellt werden. Diese Schwellen sind offen gelegte Modellregeln, keine empirischen Gesetze.
- Finanzsektor verteilt seine tatsächlich vereinnahmten Monatszinsen am Monatsende an die sechs Haushalte. Das Ausland führt erhaltene Energiezahlungen zunächst nicht zurück. Staat und Firmen haben endliche Anfangspuffer; keine dauerhafte Gleichgewichtslage wird zugesichert. Nicht finanzierbare Zahlungen und ausbleibende Käufe werden sichtbar protokolliert.

## Monat und Ausführungsreihenfolge

1. Unternehmen produzieren mit dem bestehenden Personal, zahlen Löhne, Kreditzinsen und Energie. Staat zahlt Löhne seiner zwei Beschäftigten.
2. Haushalte zahlen Einkommensteuer auf tatsächlich erhaltene Löhne; danach zahlt der Staat Transfers an Unbeschäftigte. Transfers sind in diesem Ausschnitt steuerfrei.
3. Der Staat beschafft Güter; danach kaufen die Haushalte gegen die verbleibenden Lagerbestände. Öffentliche Aufträge erhalten in dieser vereinfachten Ausführungsreihenfolge Vorrang. Unbediente Nachfrage wird gezählt, aber nicht als Umsatz verbucht.
4. Der Alltagsbetrieb kann eine finanzierbare Anlage von der Werkstatt kaufen. Lieferung, Zahlung und Kapitalzugang gehören zu demselben Vorgang.
5. Unternehmen zahlen Überschusssteuer und überprüfen Beschäftigung für den Folgemonat. Finanzsektor schüttet vereinnahmte Zinsen aus. Monatsgeschichte und Bilanzkontrolle werden gespeichert.

Die sichtbare Zeit schreitet in diesen fünf Phasen voran. Reihenfolge und Kaufreihenfolge sind Modellannahmen; die Reihenfolge der Haushaltskäufe rotiert monatlich, damit nicht immer derselbe Haushalt zuerst bedient wird. Geplante Zahlungen werden auf verfügbare Mittel begrenzt; unerfüllte Lohn-/Zins-/Steuerpflichten werden separat als offene Verpflichtungen festgehalten. Kein stiller Dispokredit. Abgaben werden nur auf tatsächlich gezahlte Einkommen erhoben.

## Eingriffe und Vergleiche

Ohne Eingriff läuft der Kreislauf weiter. Zwei klar bezeichnete optionale Annahmen gelten ab dem nächsten Monatsbeginn: Energieimportkosten verdoppeln; Haushalte reduzieren ihren Konsumanteil von 95 % auf 65 %. Keine vorgegebenen Entlassungstermine oder erzwungenen Ergebnistexte. Neustart stellt den identischen Anfangszustand her. Derselbe Eingriffszeitpunkt erzeugt dieselben numerischen Ergebnisse.

## Darstellung

Eine schematische Systemkarte mit Sektorknoten, tatsächlichen Zahlungswegen, Betrag pro Monat und bewegten Buchungsmarkern der aktuellen Phase. Kontostände sind Bestände; Verbindungssummen sind Flüsse. Klick öffnet Erklärung und Ledger, „Hineingehen“ zeigt Haushalte beziehungsweise Betriebe. Ein sichtbarer Navigationspfad führt zurück. Globale Zeit, laufende Berechnung und Eingriffe bleiben in allen Ebenen gleich. Der aktuelle Verlauf kann als JSON mit Zuständen, Regeln und Buchungen exportiert werden.

## Prüfungen und Grenzen

Normale Kundentransfers belasten und begünstigen Einlagen um denselben Betrag. Bankgutschrift und Tilgung verändern dagegen Kundeneinlagen und Kreditforderung; Zinszahlungen und Bankausschüttungen verändern Einlagen und Eigenkapital. Bankbilanz und Einlagenfortschreibung müssen nach jeder einzelnen Buchung stimmen. Konten und Lagerbestände sind nicht negativ. Getrennte Prüfung der beiden Seiten von Kreditforderungen/-verbindlichkeiten; keine Addition zum Zahlungsmittelbestand. Einzelsystem mit Testanschluss, unabhängige Ledger-Rekonstruktion, echte Folgeschritte, Neustart, Eingriff ab Monatsgrenze und Auswirkungen auf beide Gegenparteien prüfen. Kein Nachweis empirischer Prognosegüte, realer Geldschöpfung oder pädagogischer Wirkung.

Technische Grundlage: geprüfter [BPTK-Screen](../research/frameworks/bptk-py.md), [Bestands-/Fluss-Architektur](../research/decisions/0004-reduced-hybrid-learning-model.md). Die konkrete kleine Wirtschaft und ihre Regeln sind eigene Szenarioannahmen; es wird keine Übernahme eines validierten Makromodells behauptet. Die übernommenen Framework-Fähigkeiten ersetzen keine fachliche Kalibrierung. Der frühere maximale Zeitraum ist aufgehoben; der Zustand lebt weiterhin im Arbeitsspeicher. Kein Fortsetzen nach Serverneustart. Lange Läufe können durch Rechenzeit und Speicher praktisch begrenzt werden.


## Korrektur v2 und sichtbare Zahlungsrechnung

V1 koppelte Käufe allein an neues Einkommen. Ohne neues Einkommen blieb der Kaufplan bei null, selbst bei gefülltem Konto. Der [diagnostizierte Lauf](../qa/circular-flow-v1-limitations-2026-11-02.json) hält die Grenzen und die Verteilung nach 12 beziehungsweise 97 Monaten fest. V2 ergänzt den oben beschriebenen Grundbedarfsplan; fehlendes Geld, Warenmangel und Stückelung begrenzen weiterhin die tatsächlich gebuchten Käufe. Ein nicht erfüllter Kaufplan ist keine Verbindlichkeit.

Die Oberfläche weist je Haushalt Kaufplan, finanzierbares Budget, tatsächlich bezahlte Käufe und den daraus finanzierten Verbrauch älteren Kontoguthabens aus. Letzterer ist der positive Unterschied zwischen bezahlten Käufen und laufendem Einkommen nach Lohnsteuer. Die Bankausschüttung erfolgt erst in der späteren Abschlussphase; sie wird im Kontoauszug getrennt als Eingang sichtbar.

In der Übersicht stehen Anfangsbestand, aktuelle Verteilung und Änderungen der Sektoren. Seit V3 werden nur Kundeneinlagen verglichen; deren Veränderung wird mit Kreditvergabe, Tilgung, Bankertrag und Ausschüttung abgeglichen. Bankkapital steht separat. Bei Staat und Einzelsystem gilt: Monatsanfang + tatsächlich eingegangene Zahlungen − tatsächlich ausgegangene Zahlungen = aktuelles Konto. Während eines offenen Monats sind diese Zahlen ausdrücklich unvollständige Monatsflüsse.

Die Staatsansicht trennt Steuern, Ausgaben, Saldo, Rückgriff auf vorhandenes Geld und aktuellen Puffer. Eine konstante Fortschreibung des letzten abgeschlossenen Defizits ist nur eine gekennzeichnete Rechenhilfe, keine Prognose. Neue staatliche Anleihen oder Kredite sind weiterhin nicht implementiert. Ein begrenzter Unternehmenskredit ist in V3 integriert. Der vereinfachte Energie-Außenanschluss führt erhaltene Zahlungen weiterhin nicht zurück; die Welt ist kein dauerhaft geschlossener Güter-/Nachfragekreislauf und kein validiertes Gleichgewichtsmodell.


## V3 · Bank und unabhängiger Plausibilitätsaudit

[Bankkonzept](BANKING_MODEL.md) und [unabhängiger Audit](../qa/bank-plausibility-review-2026-11-02.md). Kreditgutschrift erfolgt in der Investitionsphase, Lieferung und Zahlung erst in der Abschlussphase. Jeder Vorgang besitzt Bankbilanz vor/nach, Einlagen-, Forderungs- und Eigenkapitaländerung. Die tatsächliche 12-monatige Rückzahlung wird separat vom weiterhin laufenden Altbestand gezeigt.

Zwei V2-Fehler sind behoben: nicht finanzierbare Kaufwünsche treiben die Einstellung nicht mehr an; unbezahlte Arbeits-/Energieinputs erzeugen keine Produktion. Arbeitsverhältnisse und tatsächlich erfolgte Lohnzahlungen werden in der Übersicht getrennt. Das stellt keine vollständige Absatz-/Personalplanung dar.

Der Audit bestätigt die Bankbuchungen, findet aber weiterhin einen langfristig unvollständigen Wirtschaftskreislauf: einbehaltene Firmenmittel, Lager- und Personalregeln, Rückstände, Staatsfinanzierung und Auslandsrückflüsse brauchen eigenständige Erweiterungen. Ein korrekter Bankpfad macht die Gesamtwirtschaft nicht automatisch plausibel oder empirisch gültig.

### Konsumhistorie je Haushalt

Am Kaufzeitpunkt werden pro Haushalt Konsumwunsch, durch Guthaben finanzierbares Budget, tatsächliche Käufe, Arbeitgeber, Einkommen, gezahlte Steuern, Transfers und seit der letzten Kaufrunde verfügbare Ausschüttungen festgehalten. Der Monatsabschluss übernimmt diese Werte unverändert in die Historie und den JSON-Export. Spätere Ausschüttungen und Personalentscheidungen überschreiben die damaligen Entscheidungsgrundlagen nicht.

Die Differenz zwischen Wunsch und Käufen wird centgenau zerlegt:

- Geldmangel: Wunsch minus finanziertes Budget.
- Warenmangel: Wert ganzer, aus dem zugeteilten Budget bezahlbarer Einheiten minus tatsächliche Käufe.
- Restbeträge: finanziertes Budget minus Wert dieser ganzen Einheiten, getrennt für die beiden Warenbudgets.

Alle sechs Haushaltsdiagramme haben dieselbe Euro-Skala ab null und denselben Zeitbereich der abgeschlossenen Monate. Eine gemeinsame Monatsauswahl zeigt historische Beträge, Vormonatsänderungen und Kaufplan-Eingaben. Szenario- und Leitzinsänderungen werden im Monat ihres Wirksamwerdens markiert; die spätere Anpassung des variablen Betriebskredits erhält eine eigene Markierung. Arbeitsplatzwechsel werden durch Vergleich der Arbeitgeber an aufeinanderfolgenden Kaufzeitpunkten erkannt. Eine Entlassungsentscheidung beim Abschluss erscheint damit erst in der nächsten Kaufrunde als wirksamer Wechsel. Die Ereigniszeile dokumentiert zeitliche Abfolgen; sie schreibt einem Ereignis keine isolierte Kausalwirkung zu.

Haushalte haben im aktuellen Modell keine eigenen Kredite. Zinsänderungen beeinflussen ihren Konsum gegebenenfalls über Betriebe, Staatsfinanzierung und Ausschüttungen. Ein unmittelbarer Konsumrückgang wird nicht erzwungen. Vor dieser Ergänzung begonnene Läufe enthalten keine Haushalts-Konsumhistorie und müssen neu gestartet werden.

## Einlaufphase und lange Beobachtung

Die Anfangswerte sind keine eingeregelte Gleichgewichtswirtschaft. Leere Lager, vorgegebene Absatzerwartungen und anfangs zwei Arbeitsverhältnisse je Betrieb können bereits ohne äußeren Eingriff einen Einschwingeffekt verursachen: Im V9-Basislauf reduzierte die Werkstatt nach zwei Abschlussprüfungen eine Stelle; danach entstanden zeitweise Warenengpässe. V10 kann stattdessen zunächst Arbeitszeit anpassen und hat dadurch einen anderen Basispfad. Alle Haushalte erhalten gleiche Unternehmens-/Bankgewinnanteile; deren Veränderung kann Kaufbudgets gleichzeitig bewegen. Die gleichzeitigen Knicke in frühen Haushaltsverläufen sind deshalb kein unabhängiger Nachweis einer Krise oder eines externen Schocks.

Der normale Lauf stoppt nicht automatisch nach Monat 24. Auch nach längerer Beobachtung sind Änderungen und Rücknahmen der Energie- und Konsumannahmen sowie Leitzinsänderungen möglich. Eine gegenläufige gleichzeitige Vormerkung desselben Bereichs wird abgewiesen. Die Anzeige rollt über 36 Abschlüsse; alle älteren Monate und Ereignisse bleiben exportierbar.

Lange Läufe dienen zum Prüfen von Regeln und Belastungsgrenzen. Sie sind keine kalibrierte Langfristprognose. Fehlende Abschreibung, fehlende Insolvenz-/Lohnrückstandsabwicklung, feste Nominallöhne, keine Demografie und keine veränderte Technologie bleiben relevant. Bei auffälligen Stillständen ist zwischen einer Liquiditäts-/Absatzgrenze und einem Widerspruch der Implementierung zu ihren eigenen Regeln zu unterscheiden. Ein positiver Kontostand, eine bestehende Stelle und eine tatsächliche Zahlung sind verschiedene Größen.

Seit V10 können Personal- und Anfangsverläufe von den beschriebenen V9-Knicken abweichen. Die Regeln und ursprünglichen Audits bleiben ihrer Version zugeordnet; ein veränderter Basispfad ist kein isolierter Effekt eines äußeren Ereignisses.
