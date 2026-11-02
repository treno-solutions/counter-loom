# Staatsfinanzierung · begrenztes Modell v6

Stand: 2. November 2026. Eigene illustrative Annahmen; keine Kalibrierung, Rechtsbeschreibung oder Prognose realer Staatsfinanzierung. Ergänzt [Unternehmen](COMPANY_MODEL.md), [Bankbilanz](BANKING_MODEL.md) und [Außenhandel](FOREIGN_MODEL.md). Dieselben elf Akteure, feste Preise/Löhne und 24 Monate.

## Instrument und Gegenpartei

Ein verzinster **Staatskredit bei der vorhandenen Geschäftsbank**. Keine Zentralbankfinanzierung und kein Anleihemarkt. Anfangsschuld 0 €, Kreditobergrenze 50.000 €, fester Jahreszins 3 %. Diese Werte sind Parameter des Lernfalls, keine empirisch bestimmten Kredit- oder Schuldengrenzen. Anfangskasse 80.000 € bleibt die bisherige Startannahme.

Kreditaufnahme schafft gleichzeitig Staatsguthaben, eine gleich hohe Staatsschuld und eine Kreditforderung der Bank. Bankeigenkapital wird nicht ausgezahlt. Die Bankbilanz enthält getrennt bestehende Unternehmenskredite, Maschinenkredit und Staatskredit. Die vorhandene generelle Einlagenbrücke zählt alle Kreditgutschriften und Tilgungen; sie darf nicht nur den Maschinenfall zählen.

## Finanzierungsregel

Der tatsächliche monatliche Kassenfehlbetrag ist `bezahlte öffentliche Löhne + Transfers + Beschaffung + bezahlte Staatszinsen − tatsächlich erhaltene Steuern`. Kreditgutschriften sind Finanzierung, keine Steuereinnahmen. Tilgung ist Finanzierung, kein laufender Staatsverbrauch. Unbezahlte Ansprüche werden getrennt gezeigt und nicht als bereits bezahlte Ausgaben behandelt.

Die Politik dieses Lernfalls finanziert positive Fehlbeträge vorrangig mit Kredit und bewahrt damit die vorhandene Kasse als Reserve, solange die Kreditgrenze reicht. Kredit wird also auch vor vollständigem Verbrauch des Anfangspuffers aufgenommen. Laufende Ausgaben können bei untermonatlicher Geldlücke vorfinanziert werden; am Abschluss nach den Unternehmenssteuern wird nur noch der verbleibende Finanzierungsbedarf aufgenommen. Bereits gebuchte Zwischenkredite werden abgezogen. Zusätzliche Steuereingänge können Zwischenfinanzierung zurückführen. Dadurch wird derselbe Fehlbetrag nicht doppelt finanziert.

Ein tatsächlicher Kassenüberschuss dient zur Tilgung vorhandener Schuld, begrenzt durch verfügbares Geld. Ist die Schuld null, bleibt der Überschuss auf dem Staatskonto. Kredite dürfen nicht über die feste Obergrenze wachsen. Bei ausgeschöpfter Grenze wird die Kassenreserve verwendet; fehlen beide Finanzierungsmöglichkeiten, bleiben Zahlungen begrenzt und fällige Löhne/Zinsen als Rückstände sichtbar. Fehlende Ware löst keinen Beschaffungskredit aus. Es gibt keine automatische allgemeine Rückstandsabwicklung.

## Zinsen und Fälligkeit

Am Monatsbeginn werden bestehende Staatsschuld und Zinsrückstand eingefroren. Monatliche neue Zinsen sind `Anfangsschuld × 300 Basispunkte / 120.000`, auf ganze Cents abgerundet. Neue Kredite dieses Monats tragen erst im Folgemonat Zinsen. Neue Zinsen werden höchstens einmal pro Monat in der Produktions-/Lohnphase vor den öffentlichen Löhnen gebucht und soweit finanzierbar bezahlt. Spätere Steuereinnahmen können beim Abschluss zur Nachzahlung bestehender Zinsrückstände verwendet werden, ohne erneut Zinsen zu berechnen. Ein Zinsrückstand bleibt als eigener Anspruch bestehen und wird nicht bei jedem Aufruf neu angelegt. Auf Rückstände selbst fallen keine gesonderten Straf-/Zinseszinsen an; ein tatsächlich neu finanzierter Zinsbetrag erhöht hingegen den Kredit und damit die Zinsbasis des nächsten Monats.

Zinsen sind Bankertrag, keine Tilgung. Sie senken Staatsguthaben und erhöhen Bankkapital; die Bank schüttet wie bisher tatsächlich erhaltene Monatszinsen an die Haushaltseigentümer aus. Staatliche Zinszahlungen werden dabei mitgezählt. Tilgung senkt Staatsguthaben, Staatsschuld und Bankforderung um denselben Betrag, ohne Bankertrag. Keine feste Laufzeit, keine erzwungene Gesamttilgung am Ende des Lernlaufs. Restschuld und Zinsrückstände bleiben beim Ende nach 24 Monaten im Export sichtbar.

## Sichtbarkeit und Abgleich

Unter **Staat → In das System hineingehen**: tatsächliche Steuern, Primärausgaben, Zinsen, Kassenfehlbetrag/Überschuss, Kreditaufnahme und Tilgung; Staatskasse und Schuld als getrennte Bestände. Pfeile zeigen Kreditgutschrift Bank→Staat sowie Zins-/Tilgungsrichtung Staat→Bank. Bei Kreditgutschrift werden Staatsguthaben und Bankforderung/Staatsschuld gemeinsam sichtbar. Verlauf zeigt Schuld und gezahlte Zinsen nach abgeschlossenen Monaten. Die Bankansicht führt den Staatskredit als eigenen Vertrag/Bestand. Es gibt keinen zusätzlichen Banner außerhalb der Systemhierarchie.

Kontrollen: jede Konten-/Bankgegenbuchung; Staatsschuld=Bankforderung; alte Schuld+Kredite−Tilgung=neue Schuld; alte Kasse+Steuern+Kredite−Primärausgaben−Zinsen−Tilgung=neue Kasse; neue Einlagen aus allen Krediten; Zinsbasis aus Monatsanfang; keine Doppelberechnung, Überfinanzierung oder unbezahlte Ausschüttung; Finanzierungsgrenze und sichtbare Rückstände; Export vollständiger Ereignisse und Monatsgeschichte. Vergleichsläufe ohne Kredit, mit Standardkredit, Energie-/Nachfrageschocks, Erholung und Maschinenkredit sowie isolierte Zins-, Zwischenkredit-, Überschuss- und Grenzfälle.

Stabilität, fiskalische Tragfähigkeit, Inflation, Marktzinsen, Bonitätsaufschläge und reale Staatsschuldenpolitik sind hier nicht validiert. Ein korrekter Kreditpfad garantiert kein dauerhaftes wirtschaftliches Gleichgewicht.
