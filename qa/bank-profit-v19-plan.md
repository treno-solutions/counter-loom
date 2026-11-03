# Bankgewinn v19: abgegrenzte Änderung und Zinsvergleich

Stand: 3. November 2026. Umsetzung nach der [Ursachendiagnose](rate-transmission-v18-diagnosis.md). Alle Zahlen und Quoten sind Modellannahmen. Der Investitionskanal und die übrigen Verhaltensregeln werden nicht erweitert.

## Neue Regel

- Zahlungsbezogener Modellgewinn entspricht tatsächlich erhaltenen Kredit- und Staatszinsen. Kreditgutschrift und Tilgung sind kein Gewinn. Betriebskosten, Einlagen-/Refinanzierungszinsen und Wertberichtigungen bleiben ausserhalb dieses Schritts; das wird in der Oberfläche sichtbar.
- 20 % Gewinnsteuer, analog zu den beiden Firmen. Die Bank zahlt an das Staatskonto. Die Steuer ist von der bestehenden 25-%-Quellensteuer auf tatsächlich gezahlte Eigentümerdividenden getrennt.
- Reguläre Monatsdividende höchstens die Hälfte des aktuellen Nachsteuergewinns. Am Quartalsende zusätzliche Ausschüttung vorhandener Gewinnrücklagen. Das entspricht der bestehenden Firmenlogik, ersetzt aber deren Betriebspuffer durch den Schutz des Bank-Anfangseigenkapitals von 10.000 €.
- Kein Zugriff auf die 10.000 € für Eigentümerausschüttungen; nur tatsächlich vorhandenes Kapital oberhalb dieses Betrags kann ausgezahlt werden. Die Grenze ist kein bankaufsichtlicher Kapitalquotient und nicht empirisch kalibriert.
- Rundung der Gewinnsteuer auf die kumulierten Monatszinsen; Nachzahlungen erhöhen nur die noch nicht besteuerte Bemessungsgrundlage. Staatszinsen, die aus neuen Steuerzahlungen bedient werden können, werden vor Abschluss bis zum Ende der tatsächlich finanzierten Zahlungskette verarbeitet. Wiederholter Monatsabschluss erzeugt keine weitere Steuer oder Dividende.
- Bankgewinn, Gewinnsteuer, reguläre/zusätzliche Dividende und verbleibende Gewinnrücklagen erscheinen zusammen mit der vorhandenen Bankbilanz in der Bankansicht. Steuerzahlungen der Bank werden in die Einlagenbrücke aufgenommen.

## Vergleich vorab

Der archivierte Zustand nach M1440 wird mit der alten Bankregel exakt reproduziert. Aus demselben Zustand starten vier unabhängige 60-Monats-Zweige: alte/neue Bankregel jeweils ohne und mit Zinsschock. Beim Regelwechsel werden die bis dahin vollständig ausgeschütteten Bankerträge nicht rückwirkend besteuert; neue Rücklagen beginnen bei null. Der Zinsschock bleibt 2 auf 5 % für zwölf Monate; der variable Kredit folgt mit einem Monat Verzögerung. Alte Kontrolle und alter Schock müssen alle gespeicherten Monatsbeobachtungen des v18-Archivs reproduzieren.

Eine zweite Prüfung beginnt v19 bereits ab Welteröffnung, läuft ohne Schock bis M1440 und verzweigt dann in Kontrolle/Zinsschock mit weiteren 60 Monaten. Dieser zusätzliche Vergleich prüft, ob das Ergebnis nur von der Umstellung im ersten Monat stammt. Unterschiedliche Ausgangszustände dieser beiden Versuchsgruppen werden nicht als identische Referenz bezeichnet.

Auswertung: Schock minus eigene Kontrolle für die ersten zwölf Monate, bis Monat 13 und über 60 Monate; Haushaltskäufe und erhaltenes Nettoeinkommen, Firmengewinne, Bankgewinn und Ausschüttungen, Staatsfinanzposition Kasse minus Schuld. Die reine Regeländerung ohne Schock wird getrennt ausgewiesen. Das Quartalsmuster ist eine Folge der Annahmen und kein empirischer Konjunkturzyklus. Eine erwartete negative Konsumwirkung wird nicht durch Nachjustieren erzwungen.

Jede Phase behält die Modellprüfungen. Alle neuen Buchungen der sechs Zweige werden unabhängig anhand der Anfangs-/Endkonten rekonstruiert. Prüfungen decken Monatssteuer, Einlagen-/Kapitalbrücke, Quellensteuer, Ausschüttungsgrenze, Quartalsfreigabe, Tilgung, unbezahlte Staatszinsen und Wiederholschutz ab. Die neue Referenz läuft insgesamt 1500 Monate; die Konten- und Beschäftigungsbereiche ihrer letzten 60 Monate werden dokumentiert. Neue und alte Archive bleiben getrennt.
