# Gewinnvortrag, Liquiditätspuffer und zusätzliche Ausschüttungen · v12

Stand: 3. November 2026. Illustrative Modellregeln, keine handelsrechtliche Ausschüttungsprüfung. Die normale Oberfläche verwendet `surplus`; `World(distribution_policy='legacy')` erhält für kontrollierte Vergleichsläufe die bisherige Auszahlungsregel. Staat, Steuersätze, Leitzinsen, Kreditgrenzen, Eigentumsanteile und Verhaltensregeln werden durch diese Ergänzung nicht geändert.

## Zwei verschiedene Bestände

Jeder Betrieb führt ab dem Anfangszustand einen **Gewinn-/Verlustvortrag** von null. Er verändert sich beim Monatsabschluss um das Ergebnis nach fälliger Gewinnsteuer und um tatsächlich ausgeführte reguläre und zusätzliche Ausschüttungen:

`Schlussvortrag = Anfangsvortrag + Ergebnis nach Steuer − reguläre Auszahlung − zusätzliche Auszahlung`

Der Vortrag darf negativ werden. Verluste werden nicht durch das Zurücksetzen der betrieblichen Verlusttoleranz gelöscht. Spätere Ergebnisse müssen negative Vorträge zunächst ausgleichen. Die Kontrolle rekonstruiert den Vortrag zusätzlich aus kumulierten Nachsteuerergebnissen abzüglich sämtlicher Gewinnausschüttungen.

Das **Firmenkonto** enthält hingegen tatsächlich verfügbare Zahlungsmittel. Anfangskapital und Kreditgutschriften sind keine Gewinne und erhöhen den Vortrag nicht. Ein positiver Vortrag kann in Lager oder Anlagen gebunden sein; er begründet keine zusätzliche Einlage und allein keine Auszahlung. Laufende Verluste können umgekehrt auch bei hohem Kontoguthaben einen ausschüttbaren Gewinn verhindern.

## Geschützte Liquidität

Vor einer Auszahlung werden folgende Beträge geschützt:

1. Der bestehende Betriebspuffer des Folgeplans: zwei anteilige Lohnrunden, geplante Produktionsenergie und nächster Schuldendienst.
2. Der volle Betrag eines bereits gutgeschriebenen, aber noch nicht gelieferten Maschinenvertrags. Das Kreditguthaben bleibt für diesen gebundenen Kauf verfügbar. Bereits bezahlte Investitionen sind schon vom Konto abgegangen; eine allgemeine zukünftige Investitionsplanung wird hier nicht neu eingeführt.

`Freie Liquidität = max(0, Firmenkonto vor Auszahlung − Betriebspuffer − gebundene Maschinenmittel)`

Die Schutzbeträge sind Rechengrenzen auf demselben Firmenkonto, keine zusätzlichen Geldkonten oder bereits getätigten Ausgaben. Reicht die vorhandene Kasse nicht für den Schutzbetrag, gibt es keine freie Liquidität.

## Monat und Quartal

Wie bisher wird monatlich höchstens die Hälfte des positiven Nachsteuerergebnisses regulär ausgeschüttet. Die neue Regel begrenzt zusätzlich auf den nach Verlustverrechnung verbleibenden positiven Vortrag und auf freie Liquidität.

In den Monaten 3, 6, 9 usw. wird anschliessend eine **zusätzliche Quartalsausschüttung** geprüft:

`Zusätzliche Auszahlung = min(positiver Vortrag nach Regelausschüttung, freie Liquidität nach Regelausschüttung)`

Die zusätzliche Zahlung kann frühere einbehaltene Gewinne und den noch verbleibenden aktuellen Gewinn erfassen. Die Summe beider Auszahlungen darf den positiven Vortrag vor Auszahlung und die freie Liquidität nicht überschreiten. Negative Monatsergebnisse bleiben möglich; eine zusätzliche Zahlung aus älteren Gewinnen benötigt dennoch einen regulär tragfähigen Folgeplan und alle übrigen Freigaben.

Angeordnete Schliessung, bestehende Rückstände oder ein Folgezustand ausserhalb des Regelbetriebs sperren beide Auszahlungen. Auch wirtschaftlich stillgelegte Betriebe schütten nicht automatisch ihren gesamten Bestand aus. Es gibt weiterhin keine Liquidation oder Auflösung des Anfangskapitals.

Beide Auszahlungen sind echte Überweisungen an die sechs bestehenden Eigentümerhaushalte mit denselben gleichen Anteilen und centgenauer Restverteilung. Zusätzliche Zahlungen haben die eigene Journalart `company_extra_dividend`. Firmenkonto und Gewinnvortrag sinken; Haushaltskonten steigen gleich hoch. Einlagen und Bankkapital werden dadurch nicht neu geschaffen. Die Beträge gehen wie bisherige Ausschüttungen in die nächste Kaufrunde ein. Ausschüttungen bleiben in diesem Vergleich steuerfrei; eine neue Besteuerung ist nicht Teil dieses Schritts.

## Darstellung und Export

**Unternehmen → Betrieb → Gewinnrücklagen und Ausschüttungen** zeigt die Fortschreibung des Gewinnvortrags, reguläre und zusätzliche Überweisungen, Firmenkonto vor Auszahlung, benötigte Schutzbeträge, freie Liquidität und Entscheidungsgrund. Der Liquiditätsbalken trennt gedeckten Betriebspuffer, gebundene Maschinenmittel und frei verfügbare Kasse. Fehlende Deckung bleibt über die Zahlen sichtbar.

Eine Monatsauswahl zeigt frühere Abschlussentscheidungen. Getrennte Diagramme zeigen Kontoguthaben gegenüber geschützter Liquidität, Gewinn-/Verlustvortrag und tatsächliche monatliche Ausschüttungen. Sie zeigen höchstens die letzten 36 Abschlüsse; der vollständige Verlauf bleibt im Export erhalten. Während eines offenen Monats ist die letzte abgeschlossene Gewinnverwendung ausdrücklich datiert. Die Systemkarte zählt beide Auszahlungsarten zum Gewinnfluss; Kontenbewegungen unterscheiden sie.

Der Betrag „Veränderung des Gewinnvortrags“ in der Ergebnisdarstellung darf durch eine Auszahlung älterer Gewinne negativ werden. Er ist nicht das operative Monatsergebnis.

## Referenz und Prüfung

Die Referenzregel `legacy` führt dieselbe neue Buchführung über den Vortrag, beschränkt ihre Auszahlung aber weiterhin nur auf 50 % des positiven Monatsergebnisses und den bisherigen Betriebspuffer. Sie zahlt keine zusätzliche Ausschüttung und verrechnet frühere Verluste nicht als weitere Grenze der laufenden Regelausschüttung. So bleibt ihr numerischer Verlauf mit dem bisherigen Modell vergleichbar.

[600-Monats-Vergleich und verbleibende Grenzen](../qa/profit-v12-comparison.md). Der Vergleich enthält keine neuen Schocks. Die Reproduktion prüft für den Referenzzweig jeden Monat Konten, Staatsschuld, Konsum, Produktion und Vertragszahl gegen den bereits archivierten v11-Basislauf. Die neue Regel darf andere endogene Nachfrage-, Personal- und Finanzierungsverläufe erzeugen. Ein ausgeglichener Staatshaushalt oder dauerhaftes Gleichgewicht wird nicht erzwungen.

Weitere Kontrollen: Verlustvortrag bleibt bestehen; keine Auszahlung allein aus Anfangsguthaben oder Kredit; Liquiditäts- und Gewinngrenze; Quartalsrhythmus; gesperrte Auszahlungen; gebundene Maschinenmittel; vollständige Überweisungen an Gegenparteien; Abgleich von kumulierten Ergebnissen, Vortrag und Journal; Verwendung im nächsten Haushaltskaufplan.
