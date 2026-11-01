# Iran-Krieg und Energiepreise: Daten und Szenarioplan

Stand: 1. November 2026. Gesicherte Quellenstände: IEA vom 14. Oktober und Weltbank vom 28. Oktober 2026. Keine vollständige Chronik der militärischen Ereignisse und kein verifizierter Live-Frontbericht.

## Belegte Informationen und externe Prognosen

**IEAOIL26 – IEA Oil Market Report, Oktober 2026:** Der frei zugängliche Bericht beschreibt den Iran-Krieg, beeinträchtigte Produktverfügbarkeit und erneute Angriffe auf regionale Energieinfrastruktur und Tankerverkehr. Die IEA berichtet für September eine Erholung von Golf-Rohölexporten, zugleich anhaltend schwache Ausfuhren raffinierter Produkte. Der Bericht beschreibt starken Diesel- und Frachtdruck sowie sinkende reale Einkommen. Das sind datierte Quellenangaben, keine Behauptung einer dauerhaft vollständigen Hormus-Sperrung. [Quelle](https://www.iea.org/reports/oil-market-report-october-2026)

**WBENERGY26 – Weltbank, 28. Oktober 2026:** Die Weltbank prognostiziert einen Anstieg ihres Energiepreisaggregats um 32 % im Jahresdurchschnitt 2026. Sie erwartet Brent-Jahresmittel von 91 USD/Barrel für 2026 und 79 USD für 2027. Das Basisszenario unterstellt keine wesentliche zusätzliche Konfliktverschärfung. Ein kombiniertes Negativszenario nennt 105 USD für das Brent-Jahresmittel 2027; dabei wirken auch Risiken außerhalb Irans zusammen. Diese Werte sind Prognosen, keine aktuellen Spotnotierungen oder garantierten Pfade. [Quelle](https://www.worldbank.org/en/news/press-release/2026/10/28/commodity-markets-outlook-october-2026)

Berichtete Brent-Futures, physische Rohölpreise, Dieselpreise und Jahresprognosen dürfen nicht als identische Preisgröße verglichen werden. Die historischen Monatsmittel in der Weltbank-Arbeitsmappe enden im September 2026 und ersetzen keine aktuellen Tagespreise.

Quellenkopien und Prüfsummen: [Makro-Quellenregister](../sources/macro-2026-11-01/source-register.json).

## Datenstand für die Iteration

Die bekannten Kriegsfolgen gehören bereits in den Ausgangszustand des nächsten datenreicheren Laufs. Eine weitere Iteration variiert zusätzliche Dauer, Ausmaß und politische Reaktionen. Derselbe Schock darf nicht gleichzeitig im Basispreis stecken und nochmals unbemerkt als neuer Preisaufschlag gezählt werden.

Die ergänzend extrahierten historischen Reihen enthalten Brent, WTI und Erdgasreferenzen für USA, Europa und Japan. Sie sind monatliche Referenzpreise mit unterschiedlichen Einheiten und teils fehlenden frühen Beobachtungen. Kein Ersatz für Diesel, Strom oder Tankerfracht. Fehlwerte bleiben fehlend.

## Konkurrierende Wirkungswege für die Agenten

| Kanal | Zu untersuchende Reaktionen |
|---|---|
| Sicherheits- und Reserveinteressen | Käufe von Gold, USD oder CHF; unterschiedliche politische und institutionelle Präferenzen |
| Inflation und Geldpolitik | Höhere Inflationserwartungen; Zinsanhebung, Abwarten oder Lockerung bei Rezessionsrisiken. Nominale und reale Zinsen separat führen. |
| Bergbau und Verarbeitung | Höhere Diesel-, Strom-, Transport- und Finanzierungskosten; Margen, Investitionspläne und mögliche Produktionsausfälle. Steigende Metallpreise bedeuten nicht automatisch steigende Minengewinne. |
| Industrielle Nachfrage | Einsparungen und Produktionsrückgänge bei Silber-/Kupferverbrauchern; konkurrierend Investitionen in Netze, Effizienz und alternative Energie. |
| Haushalte und Liquidität | Einkommensdruck, geringere Sparfähigkeit, Notverkäufe und gehebelte Liquidationen trotz Sicherheitsinteresse. |
| Währung | Unterschiedliche Preisreaktionen in USD, EUR und CHF; Wechselkurse getrennt von Metallpreisbewegungen ausweisen. |

Diese Reaktionen sind Mechanismushypothesen. Richtung und Stärke des Nettoeffekts werden nicht vorgegeben.

## Diversität der nächsten Varianten

1. **Entspannung:** Transport und Exporte normalisieren sich; Risikoaufschläge gehen zurück.
2. **Anhaltende Störung:** Hohe Produkt- und Transportkosten bestehen über mehrere Monate, ohne weitere Eskalation.
3. **Neue Eskalation:** Zusätzliche, konkret spezifizierte Infrastruktur- oder Transportausfälle.
4. **Energieschock mit Nachfragerückgang:** Angebotsschock trifft auf schwache Industrie und Haushalte; Belastung von Silber/Kupfer kann Absicherungsinteresse überwiegen.

Für jede Variante werden Umfang, Beginn, Dauer, betroffene Regionen, politische Reaktionen und offene Unsicherheiten angegeben. Numerische Schockgrößen und Eintrittswahrscheinlichkeiten sind noch nicht festgelegt.

## Noch zu recherchieren

- Datierte Gas-, Diesel- und Strompreise sowie Tankerfracht und Versicherungsaufschläge; jeweilige regionale Referenz und Einheit.
- Exportvolumen, Durchfahrten und Bestände, ohne Rohöl und raffinierte Produkte zu vermischen.
- Dokumentierte Energieintensität konkreter Minen, Raffinerien und industrieller Verbraucher; keine pauschale Kostenquote erfinden.
- Geprüfte Konfliktchronik bis zum endgültigen Startstichtag. Neue Ereignisse nur in den nächsten Datenstand aufnehmen.

## Übergabe aus früheren Läufen

Frühere Ausgänge werden mit Lauf-ID und Exportbeleg als simulierte Aussagen übernommen. Mehrheitsmeinungen, abweichende Minderheitspositionen und gescheiterte Erwartungen werden nebeneinander erhalten. Neue Quellen können frühere simulierte Aussagen stützen oder widerlegen. Ablauf: [Iteratives Vorgehen](iterative-run-design.md).
