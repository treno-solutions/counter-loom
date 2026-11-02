# Laufender Wirtschaftskreislauf · POC 02

Version 0.1 · 2. November 2026 · Technischer Lernversuch, keine kalibrierte Volkswirtschaft. Dieses Konzept begrenzt die folgende Implementierung. POC 01 bleibt als Haushaltsansicht erhalten.

## Frage und Abnahme

Kann eine kleine Modellwirtschaft ohne weitere Eingriffe Monat für Monat laufen, während Zahlungen und Güterlieferungen die Zustände ihrer tatsächlichen Gegenparteien verändern? Übersicht, Sektor und Einzelsystem zeigen denselben Zustand und dieselbe globale Zeit. Animationen werden ausschließlich aus verbuchten Vorgängen gespeist. Pausieren hält die Berechnung an; der nächste Schritt führt eine neue Buchungsphase im Python-Kern aus.

## Systeme und Grenze

Sechs fiktive Haushalte; zwei Unternehmen (Alltagsgüter und Werkstatt/Technik); Staat; Finanzsektor; explizites Auslandskonto für vereinfachte Energieimporte. Vier Haushalte arbeiten zunächst zu je zwei in den Unternehmen, zwei im öffentlichen Dienst. Alle Konten gehören genau einem System. Sektoren sind Aggregationen, keine zusätzlichen Konten. Die Energie-Gegenpartei bleibt eine sichtbar vereinfachte Außengrenze.

Jedes System besitzt Kennung, Bestände, Eingänge, Ausgänge, Regeln und ein Monatsprotokoll. Explizite Systemeingänge und Ausgänge in `systems.py` sowie getrennte Regeln für Haushalt, Unternehmen, Staat und Finanzsektor werden durch den geprüften BPTK-Agentenscheduler aufgerufen. Ein System kann mit belegten Testzahlungen von Außenanschlüssen geprüft werden. In der integrierten Welt ersetzen die verbundenen Systeme diese Anschlüsse vollständig; keine zusätzlichen fiktiven Löhne neben echten Unternehmenszahlungen.

## Anfangszustand und eigene Annahmen

Alle Zahlen und Verhaltensschwellen sind **eigene illustrative Testannahmen**, keine Forschungsergebnisse über Anleger oder reale Länder. Kein LLM und keine zufällige Psychologie.

- Je Haushalt 3.000 € verfügbare Zahlungsmittel; Bruttolohn 2.400 € pro Beschäftigtem, Einkommensteuer 30 %. Unbeschäftigte erhalten, soweit finanzierbar, 1.000 € Transfer.
- Unternehmen je 24.000 € Zahlungsmittel und 12.000 € bestehende Verbindlichkeit gegenüber dem Finanzsektor. Einfache jährliche Kreditzinsen 2 %, keine neuen Kredite oder Tilgung.
- Staat 80.000 €, Finanzsektor 10.000 €, Ausland 0 € Zahlungsmittel. Zahlungsmittel sind vereinfachte Abrechnungseinheiten, keine vollständige Bankeinlagen-/Zentralbankbilanz oder Geldmengenstatistik.
- Haushalt konsumiert 95 % seines tatsächlich verfügbaren laufenden Nettoeinkommens, begrenzt durch sein Konto. Kaufbudget 55 % Alltagsgüter, Rest Werkstattprodukte. Nicht konsumiertes Geld bleibt auf dem Konto; kein Wertpapiermarkt.
- Alltagsbetrieb: 36 Einheiten je Beschäftigtem und Monat, 100 € Stückpreis. Werkstatt: 20 Einheiten, 150 €. Energieimportkosten 180 € je aktivem Beschäftigtem/Monat. Produzierte, nicht verkaufte Einheiten bleiben als Lagerbestand erhalten. Fehlende Ware begrenzt tatsächliche Käufe. Käufe erfolgen in ganzen Gütereinheiten; bei Preisen von 100 € beziehungsweise 150 € bleibt auch durch Rundung ungenutztes Kaufbudget auf dem Haushaltskonto. Geplanter Konsumanteil und tatsächlich realisierte Ausgaben sind deshalb verschieden.
- Öffentliche Beschaffung bis zu 1.200 € je Unternehmen/Monat. Steuer auf positive operative Monatsüberschüsse 20 %. Investitionsausgaben sind ein Vermögenszugang und kein laufender Verbrauch; Güter werden geliefert und beim Lieferanten ausgebucht.
- Der Alltagsbetrieb kann für 1.200 € acht Werkstatteinheiten als Anlage kaufen, sofern Nachfrage nicht bedient werden konnte oder mindestens 80 % der Monatsproduktion verkauft wurden und nach dem Kauf zwei Monatslohnsummen verfügbar bleiben. Jede solche Anlage erhöht seine Kapazität ab nächstem Monat um vier Einheiten. Keine Abschreibung in diesem ersten Versuch.
- Liegen Umsätze zwei Monate unter 80 % der laufenden betrieblichen Kosten, wird zum Folgemonat eine Stelle abgebaut. Bei nicht bedienter Nachfrage und drei verfügbaren Monatslöhnen kann eine unbeschäftigte Person eingestellt werden. Diese Schwellen sind offen gelegte Modellregeln, keine empirischen Gesetze.
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

Centgenaue Transfers haben identische Belastung und Gutschrift. Summe aller Zahlungsmittel einschließlich Ausland bleibt konstant. Konten und Lagerbestände sind nicht negativ. Getrennte Prüfung der beiden Seiten von Kreditforderungen/-verbindlichkeiten; keine Addition zum Zahlungsmittelbestand. Einzelsystem mit Testanschluss, unabhängige Ledger-Rekonstruktion, echte Folgeschritte, Neustart, Eingriff ab Monatsgrenze und Auswirkungen auf beide Gegenparteien prüfen. Kein Nachweis empirischer Prognosegüte, realer Geldschöpfung oder pädagogischer Wirkung.

Technische Grundlage: geprüfter [BPTK-Screen](../research/frameworks/bptk-py.md), [Bestands-/Fluss-Architektur](../research/decisions/0004-reduced-hybrid-learning-model.md). Die konkrete kleine Wirtschaft und ihre Regeln sind eigene Szenarioannahmen; es wird keine Übernahme eines validierten Makromodells behauptet. Die übernommenen Framework-Fähigkeiten ersetzen keine fachliche Kalibrierung. Zunächst maximal 240 Monate pro Lauf im Arbeitsspeicher; kein Fortsetzen nach Serverneustart.
