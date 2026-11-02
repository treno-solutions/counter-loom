# Außenwirtschaft · begrenztes Modell v5

Stand: 2. November 2026. Eigene illustrative Annahmen, keine Kalibrierung einer realen Außenwirtschaft. Baut auf dem [Unternehmenssystem](COMPANY_MODEL.md) und der [Einbankbuchhaltung](BANKING_MODEL.md) auf.

## Umfang und Gegenpartei

Die bisherigen elf Akteure, festen Preise/Löhne und 24 Monate bleiben bestehen. Das bestehende Auslandskonto fasst Energieanbieter und ausländische Warenkunden zu einem System zusammen. Es erhält tatsächliche Energiezahlungen und kauft tatsächliche inländische Güter. Keine zusätzlichen Staaten, Banken, Währungen, Handelsfinanzierung oder Wechselkurse. Alle Kundenkonten einschließlich Ausland liegen weiterhin in der illustrativen Einbankbilanz; das bildet keine reale grenzüberschreitende Zahlungsabwicklung ab.

Das Ausland beginnt wie bisher mit **0 €**. Sein Geld wird nicht aufgefüllt. Energieeingänge können Bestellungen ab dem folgenden Monat finanzieren. Der erste Monat hat deshalb Energieimporte, aber keine bezahlten Warenexporte. Diese Verzögerung ist eine explizite Modellannahme.

## Bestellung und Lieferung

Die ausländischen Kunden wünschen monatlich **sechs Alltagsgüter zu je 100 € und zwei Werkstattgüter zu je 150 €**. Das ergibt einen maximalen Kaufplan von 900 €. Dieser feste Plan ist von der Höhe der Energiezahlungen unabhängig. Es gibt keinen automatischen Ausgleich des Außenhandelssaldos.

Am Monatsbeginn wird ein Budget von `min(Anfangsguthaben Ausland, 900 €)` festgelegt. Es wird nach den gewünschten Warenwerten aufgeteilt: zwei Drittel Alltag, ein Drittel Werkstatt, Rest-Cents im zweiten Teilbudget. Ganze Einheiten begrenzen die finanzierbaren Bestellungen; ungenutzte Beträge werden nicht umverteilt oder zwangsausgegeben.

Phase 3 (Konsum & Aufträge) bedient zunächst die bisherigen öffentlichen Aufträge und rotierenden Haushaltskäufe, danach die Auslandsbestellungen. Diese Reihenfolge gibt der bisherigen Inlandsnachfrage Vorrang und ist keine Behauptung über reale Marktverteilung. Exporte sind durch das festgelegte Teilbudget, tatsächlich vorhandenes Geld und frei verfügbares Lager begrenzt. Für eine Maschine reservierte Ware ist geschützt. Energieeingänge desselben Monats erhöhen das bereits festgelegte Kaufbudget nicht.

Jeder Export ist derselbe Verkaufsvorgang wie ein inländischer Kauf: Konto Ausland wird belastet, Firmenkonto begünstigt, konkrete Stückzahl aus dem Lager entnommen, anteiliger Lagerkostenwert als Warenkosten ausgebucht und Umsatz gebucht. Der Liefernachweis verknüpft Stückzahl, Preis, Lager vorher/nachher, Kosten und ID der tatsächlichen Zahlung. Die gekauften Güter gelten wie bei den Haushaltskäufen als verwendet; ausländische Lager/Weiterverarbeitung werden nicht modelliert. Keine Lieferung ohne Bezahlung, kein Umsatz ohne Ware, keine neue Geldschöpfung durch den Export. Fehlende Ware ist eine nicht erfüllte Bestellung, keine Forderung oder spätere Lieferverpflichtung.

Finanzierbare Auslandswünsche fließen wie andere finanzierbare Bestellungen in die geglättete Absatzplanung ein. Bloße Wünsche ohne gedecktes Teilbudget treiben Produktion und Personal nicht an. Die vorhandene Steuer-, Gewinn- und Personalplanung bleibt erhalten.

## Geldbestände und Saldo

- Auslandskonto: Anfangsbestand + Energieeinnahmen − bezahlte Warenkäufe = Endbestand.
- Außenhandel aus Inlandssicht: Warenexporterlöse − Energieimportzahlungen. Positiv bedeutet Nettozufluss ins Inland, negativ Nettoabfluss. Dieser vereinfachte Waren-/Energiesaldo ist keine vollständige Leistungsbilanz.
- Inlandsguthaben: Anfangsguthaben + Exporte − Energieimporte + Kreditgutschriften − Tilgung − Bankerträge + Bankausschüttungen. Bankkapital wird getrennt geführt.
- Exporte und Energieimporte verschieben vorhandene Einlagen. Sie ändern die Summe aller Kundenkonten einschließlich Ausland nicht.

## Sichtbarkeit und Fertigkriterien

Die Übersicht zeigt die tatsächlichen Energiezahlungen und Exporterlöse als getrennte Zahlungswege. Unter **Ausland → Details öffnen** stehen Energie-/Warenlieferungen und Zahlungen mit entgegengesetzten Pfeilen, der beschränkte Kaufplan pro Betrieb, konkrete Liefernachweise und der Saldo. Inland- und Auslandsguthaben bleiben getrennt; Änderungen eines noch offenen Monats sind als solche gekennzeichnet.

Fertigkriterien: vollständige Zahlungs- und Warengegenbuchung; Budgetgrenze vor aktuellem Energieeingang; keine Exporte bei fehlendem Geld oder frei verfügbarer Ware; Schutz reservierter Maschinen; Exportabsatz in der Firmenplanung; sichtbarer Geldrückfluss und Liefermenge; Vergleichsläufe ohne Auslandsbestellungen, mit Standardbestellungen und mit Energie-/Nachfrageschock sowie Maschinenkredit. Alte V3-/V4-Prüfbelege bleiben unverändert und beziehen sich auf ihre alten Kernhashes.

Ein dauerhafter Gleichgewichtssaldo wird nicht zugesichert. Ein durchgängig schwacher oder starker Außenhandel ist ein möglicher Modellbefund. Staatsfinanzierung, Kapitalverschleiß, Preisbildung und unterschiedlich verteilte Haushaltseigentumsanteile bleiben außerhalb dieser Erweiterung.
