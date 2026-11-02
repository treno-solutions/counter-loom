# Begrenzter Lernlauf und Unternehmenssystem · Grundlage v4, erweitert bis v9

Stand: 2. November 2026 · Die Unternehmensregeln aus v4 gelten mit den [Preis- und Kaufkraftergänzungen v8](PRICES_MODEL.md). Die [Leitzinsregeln](RATES_MODEL.md) ergänzen einen variablen und einen festen Betriebskredit. Der [begrenzte Staatskredit](FISCAL_MODEL.md) ergänzt die Finanzierungsseite. Der [Außenhandelsanschluss v5](FOREIGN_MODEL.md) ergänzt tatsächliche Auslandsbestellungen und Warenexporte. Alle Parameter sind eigene illustrative Annahmen; keine empirische Kalibrierung oder Prognose.

## Verbindliche Grenze dieser Version

- Sechs Haushalte, zwei Unternehmen, eine Bank, Staat und der bestehende vereinfachte Außenanschluss für Energieimporte und Warenexporte. Keine weiteren Akteure oder Systemarten.
- **Offener Beobachtungslauf.** Seit V9 gibt es in der normalen Oberfläche keinen automatischen Stopp nach 24 Monaten. Feste Horizonte bleiben für reproduzierbare Vergleiche optional; keine Zusicherung langfristiger Stabilität.
- Nominale Löhne, Technologien und Steuersätze bleiben fest; Preise folgen der begrenzten, verzögerten Energiekostenregel. Energiepreis und Konsumquote sind die vorhandenen äußeren Eingriffe; eine Rücknahme des Konsumschocks erlaubt einen gezielten Erholungsfall.
- Staat nutzt weiterhin seinen vorgegebenen Anfangspuffer und feste Regeln für Löhne, Transfers und Beschaffung. Ein begrenzter Staatskredit finanziert Kassenfehlbeträge und verursacht Zinsen; Anleihemärkte und Zentralbankfinanzierung bleiben außerhalb des Umfangs. Energiezahlungen senken das Inlandsguthaben, tatsächlich bezahlte Warenexporte erhöhen es. Das separate Auslandskonto bleibt in der Kontrollsumme aller Kundenkonten enthalten. Diese Kontrollsumme darf nicht als verfügbare inländische Geldmenge gelesen werden.
- Der bestehende einzelne Maschinenkredit bleibt enthalten. Kein Ausbau zu einem allgemeinen Kreditmarkt, weiteren Anlageklassen, allgemeiner Inflationsmodellierung, Steuersystem, LLM-Personas oder neuer Grafikplattform.
- Fertig, wenn Konten/Bankbilanz und Waren-/Kostenbestände stimmen, die dokumentierten Regeln in Baseline und ausgewählten Eingriffen nachvollziehbar reagieren und ein Lernender die Wirkung über die Systemansichten erklären kann. Die technische Prüfung ersetzt den noch ausstehenden Verständlichkeitstest nicht.

## Monatlicher Zusammenhang

**Erwarteter Absatz → Zielbestand → Produktionsbedarf → finanzierbare Produktion → Verkäufe → Kosten/Ergebnis → Personal und Gewinnverwendung für den nächsten Monat.** Monatsplanung, Entscheidungen und tatsächlich ausgeführte Vorgänge werden getrennt gezeigt. Der Navigationsweg bleibt Wirtschaft → Unternehmen → Betrieb; kein zusätzlicher Einstieg außerhalb dieser Hierarchie.

### Absatz und Lager

Jeder Betrieb beginnt mit einer ausdrücklich vorgegebenen Absatzerwartung (Alltag: 60, Werkstatt: 32 Einheiten). Am Monatsende wird sie als geglättete Erwartung fortgeschrieben: 75 % bisherige Erwartung, 25 % tatsächlich finanzierbare Kaufwünsche des Monats. Nicht finanzierbare Wünsche treiben keine Produktion oder Einstellung. Finanzierung von Nachfrage bedeutet vorhandenes Geld beim Käufer, nicht zwingend vorhandene Ware beim Verkäufer.

Zielbestand: aufgerundet 25 % des erwarteten Monatsabsatzes. Produktionsbedarf: `max(0, erwarteter Absatz + Zielbestand − frei verfügbarer Anfangsbestand)`. Bereits vorhandene Ware wird verwendet. Eine für die Maschine reservierte Menge bleibt geschützt. Produktion ist durch bestehende Arbeits-/Anlagenkapazität und bezahlbare Arbeits-/Energieinputs begrenzt. Bei vollem Lager kann Produktion null sein; bestehende Arbeitsverträge verursachen weiterhin Lohnkosten.

### Kosten und Ergebnis

Energie wird variabel je tatsächlich produzierter Einheit bezahlt: 5 € im Alltagsbetrieb und 9 € in der Werkstatt, beim Energieschock jeweils das Doppelte. Bruttolohn bleibt 2.400 € je bestehender Stelle. Bezahlter Lohn wird im Verhältnis tatsächlich produzierter zu durch bezahlte Arbeit/Anlagen möglicher Einheiten auf produktive Kosten und Leerlauf aufgeteilt. Dies ersetzt die frühere Pauschale je Beschäftigtem.

Das Lager führt Menge und einen centgenauen Kostenwert. Bezahlte produktive Arbeits-/Energiekosten erhöhen den Lagerkostenwert. Verkäufe entnehmen anteilige Kosten nach gleitendem Durchschnitt; Rest-Cents verbleiben bis zur letzten entnommenen Einheit im Lager. Bei Produktion null sind bezahlte Arbeitskosten laufender Aufwand. Nicht bezahlte fällige Löhne werden als Aufwand und offene Verpflichtung berücksichtigt. Zinsaufwand des aktuellen Monats bleibt getrennt von Tilgung und Investitionen; Kreditgutschriften sind kein Umsatz.

Vereinfachtes Ergebnis vor Steuer: `Umsatz − Kosten verkaufter Ware − Leerlauf-/unbezahlter Lohnaufwand − Zinsaufwand`. Dies ist eine explizit begrenzte Kostenrechnung, keine vollständige handelsrechtliche GuV. Der Staat erhält wie bisher 20 % des positiven Ergebnisses; Investitionszahlungen und Tilgung sind kein laufender Verbrauchsaufwand. Maschinen werden im begrenzten Lernlauf nicht abgeschrieben.

### Personal

Der nächste dauerhafte Personalbedarf richtet sich nach der geglätteten Absatzerwartung und Produktivität, mit Abzug vorhandener Anlagenkapazität. Ein zusätzlicher einmaliger Lageraufbau erzeugt keinen dauerhaften Personalbedarf. Für die folgende Personal-/Liquiditätsplanung wird der bereits bekannte Vertragszins des nächsten Monats verwendet; die aktuelle Produktionsrunde verwendet den aktuell wirksamen Satz.

Zusätzlich begrenzt die erwartete Selbstfinanzierung die Zielstellenzahl: erwarteter Umsatz abzüglich erwarteter Energie und Schuldendienst muss die festen Löhne tragen können. Ein niedrigerer oder höherer Bedarf muss zwei Monatsabschlüsse in derselben Richtung bestehen. Zielstellen sind auf vier je Betrieb begrenzt. Pro Betrieb und Monat wird höchstens eine Stelle verändert. Neueinstellungen benötigen eine verfügbare Person und liquide Mittel für zwei geplante Lohnrunden plus Energie/Schuldendienst. Änderungen gelten ab der folgenden Lohnphase. Zahlungsengpässe, tatsächliche Lohnzahlung und formales Arbeitsverhältnis bleiben getrennt.

Die grobe Ein-Personen-Stückelung ist eine Modellgrenze. Keine Deutung als reale Personalpolitik, Psychologie oder gesetzliche Kündigungsregel.

### Gewinnverwendung und Eigentum

Die sechs bestehenden Haushalte besitzen in diesem Test jeweils denselben Anteil an beiden Betrieben. Das ist eine eigene Startannahme, keine empirische Vermögensverteilung. Bis zu 50 % des positiven Nachsteuerergebnisses können am Monatsende an diese Eigentümer ausgezahlt werden; der übrige Teil bleibt im Betrieb. Ausschüttungen sind echte Überweisungen und werden für die Haushaltsplanung im Folgemonat verfügbar; in diesem begrenzten Steuermodell werden sie nicht zusätzlich besteuert.

Ausschüttungen werden zusätzlich auf liquide Mittel oberhalb von zwei Lohnrunden für die größere Zahl aus aktuellen und Zielstellen, erwarteter Energie und dem nächsten Schuldendienst begrenzt. Bestehende fällige Rückstände sperren sie. Anfangspuffer und neu aufgenommenes Kreditgeld gelten nicht als ausschüttbarer Gewinn. Ein Verlust löst keine Ausschüttung aus. Im Betrieb belassene Mittel stehen für Arbeitskapital und den bestehenden Maschinenkauf bereit.

Ein eigenfinanzierter Maschinenkauf erfordert zwei Monate finanzierbarer, wegen Kapazität/Ware nicht bedienter Nachfrage, ausreichenden verbleibenden Arbeitspuffer und verfügbare Werkstattware. Höchstens eine Anlage in drei Monaten. Der explizit angefragte Bankfall behält seinen bisherigen separaten Ablauf. Bei später Kreditanfrage kann am Ende eines gewählten Beobachtungsfensters eine Restschuld bestehen; sie wird ausgewiesen und exportiert, nicht automatisch erlassen.

## Sichtbare Größen und Prüfungen

Je Betrieb: erwartete/finanzierbare Nachfrage, Ziel- und Ist-Lager, geplante/tatsächliche Produktion, Kapazitäts-/Geldgrenze, derzeitige/Zielstellen und Entscheidungsgrund sowie Umsatz, Warenkosten, Ergebnis, Steuer, Ausschüttung und im Betrieb belassenes Ergebnis. Kontobewegungen bleiben über den vorhandenen Kontoauszug abrufbar.

Kontrollen: Anfangslager + Produktion − Verkäufe = Endlager; Anfangskostenwert + produktive Kosten − entnommene Warenkosten = Endkostenwert; Konten und Bankbilanz nach jeder Buchung; Verkäufe nicht größer als verfügbare Ware; keine Ausschüttung aus Kreditgutschrift/Verlust oder bei fälligen Rückständen; keine Einstellung wegen bloßem Geldmangel des Käufers; Entscheidungsverzögerung; Wiederholung identischer Eingriffe; Kredit-/Zins-/Tilgungsprüfungen bleiben bestehen.

Ausgewählte Läufe: Baseline ohne Eingriff, Energieanstieg, Konsumrückgang, beide Eingriffe, Konsumrückgang mit anschließender Normalisierung sowie der Maschinenkredit. Ein begründeter Rückgang oder Engpass ist zulässig. Parameter werden nicht allein so gewählt, dass ein erwünschtes Ergebnis entsteht. Der vollständige 24-Monats-Verlauf und offene Einschränkungen werden mit den tatsächlichen Eingaben dokumentiert.

### Bedienpersonal bei hoher Anlagenkapazität

Zusätzliche Anlagen können Arbeit ersetzen, benötigen aber weiterhin mindestens eine Bedienkraft bei positiver Absatzerwartung und finanziell tragfähiger Beschäftigung. Der Personalbedarf darf daher nicht allein durch hohe Anlagenkapazität auf null sinken, während die Produktionsregel zugleich einen aktiven Grundbetrieb verlangt. V9 korrigiert diesen Widerspruch. Absatzmangel oder fehlende Finanzierbarkeit können weiterhin zu null Stellen führen. Ein dadurch erzwungener Stillstand ist von einem Implementierungsfehler zu unterscheiden.
