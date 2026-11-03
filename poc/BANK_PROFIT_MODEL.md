# Bankgewinn und Gewinnverwendung · v19

Stand: 3. November 2026. Begrenzte Korrektur nach der [Diagnose des Zinsschocks](../qa/rate-transmission-v18-diagnosis.md). Alle Quoten und Beträge sind illustrative Modellannahmen. Die übrigen Wirtschafts- und Investitionsregeln bleiben erhalten. [Versuchsplan](../qa/bank-profit-v19-plan.md).

## Gewinn und zwei getrennte Steuern

Tatsächlich erhaltene Firmen-, Maschinen- und Staatskreditzinsen bilden den zahlungsbezogenen Modellgewinn. Nicht bezahlte Zinsen bleiben Vertragsrückstände. Kreditgutschrift und Tilgung verändern Forderungen und Einlagen, gehen aber nicht in den Gewinn ein. Bankbetriebskosten, Einlagenzinsen, Refinanzierung und Wertberichtigungen werden weiterhin nicht modelliert; der ausgewiesene Gewinn ist daher keine vollständige reale Bank-Gewinn-und-Verlustrechnung.

Auf den positiven Modellgewinn fallen wie bei den Firmen 20 % Gewinnsteuer an. Die Bank zahlt diese an das Staatskonto; die Steuer wird nicht von einer Haushaltsdividende ersetzt. Bei späterer tatsächlicher Auszahlung an die Haushalte werden wie bisher 25 % Ausschüttungssteuer einbehalten. Beispiel: 40 € bezahlte Zinsen ergeben 8 € Gewinnsteuer und 32 € Nachsteuergewinn. Werden davon 16 € ausgeschüttet, bleiben den Empfängern zusammen nach Quellensteuer 12 €, vorbehaltlich der bestehenden centweisen Rundung je Haushalt und Monat.

## Gewinnrücklagen und Auszahlung

- Pro Monat höchstens 50 % des aktuellen Nachsteuergewinns als reguläre Dividende.
- Am Quartalsende zusätzliche Ausschüttung bisheriger Gewinnrücklagen, soweit das Kapital oberhalb des geschützten Anfangseigenkapitals ausreicht.
- Gewinnvortrag am Ende = Gewinnvortrag am Anfang + aktueller Nachsteuergewinn − tatsächlich ausgezahlte Bruttodividenden.
- Die anfänglichen 10.000 € Bankeigenkapital dürfen nicht an Eigentümer ausgeschüttet werden. Diese feste Modellgrenze ist keine regulatorische risikogewichtete Kapitalquote.
- Wie bei den Firmen erhalten alle sechs Haushalte gleiche Anteile, verbleibende Cent werden der Reihe nach zugeteilt. Die Eigentümerstruktur wird in diesem Schritt nicht erweitert.

Bei unveränderten 40 € monatlichen Zinseingängen ohne Staats- oder Maschinenzinsen: Monatsdividenden 16 €, 16 €, 64 €; Gewinnrücklagen nach Abschluss 16 €, 32 €, 0 €. Im dritten Monat entfallen 16 € auf die reguläre und 48 € auf die zusätzliche Ausschüttung. Über das Quartal werden 96 € Nachsteuergewinn verteilt. Eine Monatsdividende kann somit höher als der aktuelle Monatsgewinn sein, aber nur durch zuvor einbehaltene Gewinne.

Die Regel ist der bestehenden Firmengewinnverwendung nachgebildet. Sie ist nicht anhand einer historischen Bankausschüttungsquote kalibriert. Die Bank benötigt im gegenwärtigen begrenzten Modell keinen laufenden Lohn-/Energiepuffer; geschützt wird stattdessen ihr Anfangseigenkapital. Wiederkehrende Quartalsausschüttungen verhindern, dass eine neue dauerhafte Geldsenke ohne ökonomischen Verwendungszweck eingeführt wird.

## Buchungsidentitäten

Zinseingang senkt Kundeneinlagen und erhöht Bankeigenkapital. Bankgewinnsteuer und Bankdividende senken Bankeigenkapital und erhöhen die Einlage des Staats beziehungsweise der Haushalte. Die Quellensteuer überträgt anschliessend Kundeneinlagen vom Haushalt zum Staat. Keine dieser Steuer- oder Dividendenzahlungen erzeugt einen Kredit.

`Kundeneinlagen = Anfangseinlagen + Kreditgutschriften − Tilgungen − gezahlte Bankzinsen + Bankgewinnsteuerzahlungen + Bruttobankausschüttungen`

Die Bankbilanz bleibt `Reserveposition + Kreditforderungen = Kundeneinlagen + Eigenkapital`. Bei regulärem Verlauf gilt nach Monatsabschluss `Eigenkapital = Anfangseigenkapital + noch nicht ausgeschüttete Bankgewinne`.

Steuern und Dividenden können dem Staat erlauben, fällige überfällige Zinsen nachzuzahlen. Diese tatsächlich bezahlten Zinsen erhöhen den Bankgewinn desselben Monats. Der Abschluss berechnet deshalb die kumulierte Gewinnsteuer und den gesamten Dividendenanspruch erneut und zahlt jeweils nur die Differenz. Er endet, sobald keine weitere finanzierte Zahlung entsteht. Die Quellensteuer bleibt je Haushalt auf kumulierte Monatsdividenden gerundet. Ein abgeschlossener Monat wird beim erneuten Aufruf nicht erneut besteuert oder ausgeschüttet.

## Schnittstelle und Oberfläche

Aktueller Modellvertrag: `illustrative_circular_flow_v19`. `banking.profit` enthält Regel, Steuersatz, letzten Abschluss und die letzten 36 Abschlüsse. Jeder Abschluss zeigt Zinseingänge, ausdrücklich nicht modellierte Betriebskosten als null, Vor-/Nachsteuergewinn, fällige/bezahlte Gewinnsteuer, reguläre/zusätzliche Dividende, Gewinnvortrag und Kapitaluntergrenze. `banking.profit_tax_paid_cents` trennt kumulierte Gewinnsteuer der Bank von Bruttodividenden in `banking.distributed_cents`. Die Einlagenbrücke zählt beide Bankauszahlungen getrennt.

Die Bankansicht zeigt Gewinnrechnung und Verwendung neben der bestehenden Bilanz. Beträge beziehen sich ausdrücklich auf den letzten abgeschlossenen Monat; zwischen den Phasen können aktuelle Bankkapitalbestände bereits weiterlaufen. Ein Rechenkernwechsel erfordert neu geladene Oberfläche und neuen Lauf. Vollständige Zahlungen bleiben im Laufjournal exportierbar.

`bank_profit_policy='legacy'` erhält die frühere steuerfreie sofortige Vollauszahlung nur für explizite Gegenläufe. Neue Oberflächenläufe verwenden `consistent`. Frühere Archive werden nicht überschrieben. Die alten Bankregeln sind nicht mit der neuen Standardvariante gleichzusetzen.

## Nachweise

[Bankgewinnprüfungen](test_bank_profit.py) decken Steuer, Monats-/Quartalsauszahlung, Tilgung, Einlagenbilanz, Kapitaluntergrenze, centweise Rundung, Rückkopplung über unbezahlte Staatszinsen und Wiederholschutz ab. Die bestehenden Finanzierungsprüfungen berücksichtigen zusätzliche reale Bankgewinnsteuerzahlungen und vorübergehend zurückgehaltene Gewinne. [Vergleichsskript](scripts/compare_bank_profit.py) trennt die reine Regeländerung vom Zinseffekt gegenüber der jeweiligen Kontrolle. Der Investitionskanal bleibt ausdrücklich unverändert.

[Ergebnisvergleich mit dem bisherigen Zinsschock](../qa/bank-profit-v19-report.md).
