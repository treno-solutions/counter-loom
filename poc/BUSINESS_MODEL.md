# Arbeitszeit, Verlustbrücke und Betriebszustand · Modell v10

Stand: 3. November 2026. Eigene illustrative Regeln, keine empirische Kalibrierung, rechtliche Kurzarbeitsregelung oder Insolvenzordnung. Die offene Modellwirtschaft und ihre elf Akteure bleiben erhalten. Diese Regeln ersetzen die V9-Schwelle, die eine ganze Stelle aus dem erwarteten Deckungsbeitrag finanzieren musste.

## Arbeitszeit, Lohn und Kapazität

Der Vollzeitlohnsatz bleibt 2.400 € pro Vertrag und Monat. Jeder aktive Betrieb setzt eine gemeinsame Arbeitszeitquote zwischen 25 und 100 % für seine Beschäftigten fest; die Quote wird in ganzen Basispunkten geführt. Pro aktivem Monatsübergang verändert sie sich höchstens um 25 Prozentpunkte. Der Bedarf ergibt sich aus geglätteter finanzierbarer Nachfrage, Zielbestand und frei verfügbarem Lager, geteilt durch die Vollzeitkapazität. Der Stillstand hat null Arbeitszeit. Ein neu gestarteter Betrieb erhält seine aus dem Bedarf berechnete Startquote.

`Lohn je Vertrag = 2.400 € × Arbeitszeitquote`.

`Geplante Kapazität = floor((Beschäftigte × Produktivität + Anlagen × 4) × Arbeitszeitquote)`.

Anlagen setzen mindestens einen Bediener voraus. Die tatsächliche Kapazität verwendet statt der zugesagten Arbeitszeit den tatsächlich bezahlten Anteil an einer vollen Lohnsumme. Arbeits- und Anlagenanteil werden gemeinsam einmal abgerundet; dadurch stimmen Plan und Ausführung bei vollständig bezahltem anteiligem Lohn überein. Unbezahlte Löhne erzeugen keine kostenlose Kapazität. Ganzzahlige Ware und bezahlbare Energie begrenzen die tatsächlich hergestellte Menge zusätzlich.

Der technische Personalbedarf bleibt auf höchstens vier Verträge je Betrieb begrenzt. Im laufenden Betrieb muss eine Bedarfsrichtung zwei Abschlüsse anhalten; dann wird höchstens eine Stelle geändert. Eine Neueinstellung wird mit der tatsächlich erreichbaren Folgequote geprüft, nicht mit einer durch die Schrittgrenze unerreichbaren Idealquote. Sie benötigt freie Arbeitskraft und einen Puffer für zwei anteilige Lohnrunden plus geplante Energie und Schuldendienst. Ein kleiner vorübergehender Finanzierungsbedarf darf dieselbe begrenzte Verlustbrücke nutzen. Eine vollständige Stilllegung beendet sämtliche betrieblichen Arbeitsverträge für die nächste Lohnrunde.

## Vorschau und tatsächliches Ergebnis

Beim Abschluss nach Verkäufen und Gewinnsteuer wird ein Folgeplan berechnet:

- Erwartete Erlöse: kleinere Menge aus prognostizierten Verkäufen und verfügbarer Ware inklusive geplanter Produktion, zum aktuellen Stückpreis.
- Benötigte Vorfinanzierung: anteilige Löhne, Energie für geplante Produktion, Betriebskreditzins des nächsten Monats und Maschinen-Schuldendienst.
- Erwartete Finanzierungslücke: positiver Unterschied zwischen dieser Vorfinanzierung und den erwarteten Erlösen.
- Betriebspuffer: zwei anteilige Lohnrunden plus Energie und Schuldendienst.

Eine Prognose ist kein Zahlungsversprechen. Die eigene Kasse muss die Kosten vorfinanzieren können; erwartete künftige Umsätze werden nicht als vorhandenes Geld gebucht. Kreditaufnahme, Tilgung und Investitionen bleiben getrennte Geldbewegungen. Lagerkosten und tatsächliche GuV werden wie bisher aus bezahlten Produktionsinputs, tatsächlichem Wareneinsatz, Leerlauf, unbezahltem Lohnaufwand und Zinsaufwand ermittelt.

## Vier Betriebszustände

| Zustand | Bedeutung |
|---|---|
| Regelbetrieb | Folgeplan hat Nachfrage, keine erwartete Finanzierungslücke und ist vorfinanzierbar. |
| Befristete Verlustbrücke | Vorfinanzierbar, aber erwartete Erlöse decken die Planauszahlungen noch nicht. Betrieb nutzt vorhandene Liquidität innerhalb der Toleranz. |
| Stillgelegt | Keine neue Produktion oder Lohnrunde; alte Ware kann weiter verkauft werden. Anlagen, Bankverbindlichkeiten und offene Ansprüche bleiben bestehen. Zinsen und Tilgung verschwinden nicht. |
| Wiederanlauf | Eine Arbeitskraft ist nach zwei bestandenen Prüfungen für den nächsten Monat eingestellt; die neue Produktionsrunde beginnt erst dann. |

Aktueller Zustand und Folgezustand sind getrennt. Entscheidungen beim Abschluss verändern nicht rückwirkend die schon bezahlte Monatsarbeit.

## Begrenzte Verlusttoleranz

Jeder Betrieb beginnt mit 4.800 € Verlusttoleranz. Seit der letzten Freigabe angefallene negative GuV-Ergebnisse zählen gegen diese Schwelle. Das ist kein separates Guthaben und erzeugt keine Einlage. Gehalt, Energie und Zinsen werden ausschließlich vom wirklichen Firmenkonto bezahlt.

Eine neue Brückenentscheidung setzt voraus: ausreichend Kasse für die Planauszahlungen, erwartete Finanzierungslücke höchstens gleich verbleibender Verlusttoleranz und weniger als drei unmittelbar vorangegangene Brückenentscheidungen. Die nächste Brücke erhöht den Zähler. Ein tragfähiger Folgeplan unterbricht die Brückenfolge. Unerwartete tatsächliche Verluste können die Toleranz überschreiten; dadurch entsteht kein negatives Geldkonto, die nächste weitere verlustfinanzierte Fortsetzung kann aber abgelehnt werden.

Nach zwei tatsächlich profitablen Monaten und gedecktem Betriebspuffer wird die Verlusttoleranz vor der neuen Planprüfung wieder freigegeben. Das setzt einen Entscheidungszähler zurück, erstattet keine historischen Kosten und erhöht kein Konto. Ein alter Buchverlust allein erzwingt keine Stilllegung, wenn ein neuer Plan ohne zusätzliche Finanzierungslücke tragfähig ist.

## Stilllegung und Wiederanlauf

Fehlt Vorfinanzierung oder reicht die begrenzte Brücke nicht, wird für den folgenden Monat stillgelegt. Es gibt keine Zwangsverkäufe, Schuldenstreichung oder automatische Insolvenz. Reservierte Waren und Maschinenverträge werden weiter respektiert. Feste Kosten des Schuldendienstes können auch einen stillgelegten Betrieb weiter belasten.

Ein stillgelegter Betrieb prüft jeden Abschluss einen Plan mit einer Arbeitskraft. Wiederanlauf benötigt zwei unmittelbar aufeinanderfolgende Abschlüsse mit positiver Nachfrageprognose, keiner erwarteten Finanzierungslücke und Kasse für den Betriebspuffer. Zum tatsächlichen Einstellen muss eine freie Arbeitskraft verfügbar sein. Eine fehlgeschlagene Wirtschafts-/Liquiditätsprüfung setzt die Bestätigungsfolge zurück. Nach erfolgreichem Wiederanlauf beginnt eine neue mögliche Brückenfolge; frühere GuV-Verluste werden dadurch nicht automatisch aus der Verlusttoleranz gelöscht.

## Ausschüttungen

Nur positives Nachsteuerergebnis kann weiterhin höchstens zur Hälfte ausgeschüttet werden, begrenzt auf Kasse oberhalb des Folgepuffers. Rückstände oder ein Folgezustand außerhalb des Regelbetriebs sperren die Ausschüttung. Die sechs Haushalte bleiben gleiche Eigentümer; diese vereinfachte Eigentumsverteilung ist unverändert.

## Grafische Nachvollziehbarkeit

**Unternehmen → Betrieb** zeigt die vier Zustände, aktuelle/folgende Arbeitszeit, Verträge und Vollzeitäquivalente, anteiligen Lohn, Firmenkonto, Verlusttoleranz, Brückenzähler und die konkrete Folgeentscheidung. Voraussetzungen für den geprüften Folgeplan und bestätigte Wiederanlaufprüfungen stehen daneben. Eine gemeinsame Prozentkurve zeigt ausgeführte Quote und Folgeplan über die letzten 36 Abschlüsse. Historische Quoten, Zustände, Kasse, Verlusttoleranz und Entscheidungstexte bleiben im Export erhalten.

## Bewusste verbleibende Grenzen

Seit V11 gilt für angeordnete befristete Schliessungen die separate [Kurzarbeitsregel](CRISIS_MODEL.md). Ausserhalb dieser Episoden ist die Transferregel nicht erweitert: Nur unbeschäftigte Haushalte erhalten bei ausreichender Staatskasse bis zu 1.000 €; reduzierte betriebliche Arbeitszeit löst keine Aufstockung aus. Eine 25-%-Stelle zahlt 600 € brutto beziehungsweise 420 € nach Modellsteuer und kann deshalb weniger laufendes Einkommen als Arbeitslosigkeit mit Transfer bedeuten. Dies ist eine Grenze des bestehenden Sozialmodells und keine Aussage über reale Anreize oder Kurzarbeit.

Kein Insolvenzverfahren, keine allgemeine Nachzahlung alter Lohnansprüche, keine Abschreibung, kein neuer Firmenkreditmarkt und keine Nachfragepreisbildung. Lange Läufe können weiterhin Stagnation, Zahlungslücken oder erneute Stilllegung zeigen. Es wird kein dauerndes Wachstum oder permanenter Wiederanlauf erzwungen. Frühere V9-Ergebnisse bleiben Befunde anderer Regeln.

Prüfung: [unabhängiger V10-Audit](../qa/company-v10-plausibility.md). Er trennt reguläre Weltläufe und kontrollierte Entscheidungsports.
