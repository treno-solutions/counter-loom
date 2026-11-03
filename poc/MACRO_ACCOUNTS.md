# Makrokennzahlen der Modellwirtschaft

Modell v16 ergänzt eine beobachtende Makroebene. Sie wertet abgeschlossene Monate aus und verändert keine Produktions-, Kauf- oder Budgetentscheidung. Die normale Konfiguration bleibt bei kleinen Gütereinheiten und 95 % Konsumquote. [600-Monats-Gegenlauf mit 100 %](../qa/consumption-v16-comparison.md).

## Leistung und Wachstum

Das amtliche BIP erfasst den Wert der im Inland produzierten endgültigen Waren und Dienstleistungen. Nominale Werte enthalten aktuelle Preise; reale Werte bereinigen Preisänderungen. Diese Unterscheidung ist für die Interpretation von Wachstum wesentlich. Quelle: [BEA Gross Domestic Product](https://www.bea.gov/resources/learning-center/what-to-know-gdp), abgerufen am 3. November 2026.

Die kleine Modellwirtschaft erlaubt nur eine **nominale BIP-Näherung**:

`Haushaltskäufe + öffentliche Warenkäufe + Anlagenkäufe + Warenexporte − Energieimporte + Lagerwertänderung + öffentliche Arbeitsleistung`

Alle Zahlungsbestandteile stammen aus tatsächlich ausgeführten Vorgängen des jeweiligen Monats. Lageränderungen sind Schlusswert minus Anfangswert. Öffentliche Warenkäufe gelten als Endnachfrage, nicht als Vorleistungen der separat angenäherten öffentlichen Dienste. Öffentliche Arbeit wird ausschliesslich mit tatsächlich gezahlten aktuellen Löhnen angesetzt; alte Lohnnachzahlungen zählen nicht erneut als Produktion. Der Nutzen dieser Arbeit wird damit nicht bewertet.

Kredite, Tilgung, Zinsen, Steuern, Transfers und Ausschüttungen zählen nicht als zusätzliche Produktion. Der Kauf einer Maschine zählt als Anlagekauf; ihre Finanzierung wird getrennt behandelt. Lager werden zu den bestehenden Herstellungskosten geführt. Es fehlen eine vollständige Bewertung zu aktuellen Marktpreisen, Abschreibungen, ein allgemeiner Dienstleistungssektor und eine amtliche Kontensystematik. Die Näherung ist deshalb keine VGR-konforme BIP-Statistik. In Stressphasen sind auch negative monatliche Werte möglich, etwa durch Vorleistungen ohne ausreichenden Absatz oder Produktion.

Nominales Wachstum wird zum Vormonat und zum gleichen Vorjahresmonat berechnet. Bei fehlender oder nicht positiver Vergleichsbasis bleibt die Rate unbekannt. Es gibt keine Saisonbereinigung, Annualisierung oder Schätzung eines realen BIP. Der Vorjahresvergleich beginnt frühestens mit Monat 13.

## Warenmenge und Produktivität

Der Warenmengenindikator bewertet die produzierte Menge beider Warenarten mit unveränderten Startpreisen. Sein Index hat in Monat 1 den Wert 100. So verändert ein reiner Verkaufspreisanstieg diesen Mengenindikator nicht.

Die Produktionskennzahl je privatem Vollzeitäquivalent lautet:

`produzierte Waren zu Startpreisen / geplante private Vollzeitäquivalente`

Die Vollzeitäquivalente ergeben sich aus der Beschäftigtenzahl und Arbeitszeitquote des jeweiligen Produktionsplans. Während einer vollständigen privaten Schliessung sind sie null; die Produktivitätskennzahl ist dann nicht verfügbar. Die Kennzahl misst Warenproduktion, keine amtliche Wertschöpfung pro Arbeitsstunde. Öffentliche Arbeit ist darin nicht enthalten. Dadurch wird keine Produktivitätssteigerung allein aus ihrer Entlassung behauptet.

## Weitere Anzeigen

- **Leitzins:** Jahreszins im gewählten Monatsabschluss; der aktuelle Zinssatz wird daneben gezeigt. Vertragszinsen folgen weiterhin den vorhandenen Verzögerungen und Bindungen.
- **Beschäftigung:** Verträge in der tatsächlichen Lohnrunde, nicht die beim Abschluss für den nächsten Monat geplante Besetzung. Der Anteil ohne Vertrag bezieht sich auf die sechs modellierten Haushalts-Arbeitskräfte, nicht auf eine empirische Bevölkerung.
- **Warenpreisinflation:** Veränderung des festen Zwei-Waren-Korbs zum Vorjahresmonat. Das ist kein repräsentativer Verbraucherpreisindex.
- **Geburtenrate:** nicht modelliert und als `null` gespeichert. Die sechs Haushalte haben bislang keine Personen-, Alters-, Geburten-, Sterbe- oder Wanderungsstruktur. Eine Geburtenrate wird aus ihrer festen Zahl nicht abgeleitet.

## Verlauf und Export

Die Oberfläche zeigt Monatsauswahl und bis zu 120 abgeschlossene Monate mit Verläufen für Leistung, Warenmenge, Leitzins und Beschäftigung. Während eines laufenden Monats bleiben die letzten abgeschlossenen Makrowerte sichtbar. Ein neuer Zustand vor dem ersten Abschluss enthält noch keine Leistungswerte.

Der Export führt mit `all_macro_history` den gesamten Verlauf mit Bestandteilen und Ableitungen. Die Makroebene erstellt keine Ledgerbuchungen. Ein Vergleich mit ausgeschalteter Makrobeobachtung prüft identische Buchungen, Konten und wirtschaftliche Historien. Zusätzliche Tests prüfen die Summenidentität, fehlende Vorjahreswerte, Schliessungen und vollständigen Export.
