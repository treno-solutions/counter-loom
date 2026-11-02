# MiroFish · Bewertung des ersten Methodenversuchs

Bewertungsstand: 2. November 2026 · Ergebnis: **für den aktuellen Workshop-Zweck in der getesteten Konfiguration ungeeignet**.

Der erste Versuch gilt als gescheitert hinsichtlich des angestrebten Erkenntnisgewinns. Die Bewertung betrifft den dokumentierten Lauf und seine verfügbare Auswertung. Sie ist kein allgemeines Urteil über alle Versionen oder Anwendungsmöglichkeiten von MiroFish.

## Prüfgegenstand und Nachweise

- Projekt `proj_1a8710f2603c`, Simulation `sim_30812a387855`, Bericht `report_fd221991e032`.
- E01: [angezeigter Bericht als Markdown gesichert](../../runs/001-first-simulation/exports/report-page-capture.md), Abruf vom 1. November 2026. Eine gerenderte Seitenaufnahme einschließlich Oberflächentext; kein vollständiger Serverexport. Der erste Abschnitt endet in der Aufnahme unvollständig. Belegstellen unten nennen deshalb Abschnitt und Zwischenüberschrift.
- E02: [Prüfvermerk zu Status und Interviewversuch](../../runs/001-first-simulation/exports/inspection-record.json). Zusammenfassung der beobachteten API-Werte und Fehlermeldung; keine unveränderte Originalantwort.
- E03: [archivierter Seed](../../runs/001-first-simulation/inputs/precious-metals-research-seed.md), insbesondere Kapitel 8, 10–13. Die Identität mit den tatsächlich verarbeiteten Servereingaben ist nicht unabhängig bestätigt.
- E04: [detaillierte inhaltliche Berichtsauswertung](../../notes/report-fd221991e032-analysis.md).
- E05: Betreiberauskunft: Erinnerungsdaten für diesen Lauf nicht verfügbar; Verbesserung für spätere Läufe angefordert. In E02 als Auskunft gekennzeichnet.
- Externe Einordnung: [offizielle FAQ](https://github.com/666ghj/MiroFish/issues/725) und [technische Erläuterung](https://github.com/666ghj/MiroFish/issues/691#issuecomment-5016095160). Sie beziehen sich auf dort benannte Code-Stände, nicht auf eine verifizierte Versionskennung unserer Installation.

## Was der Versuch tatsächlich zeigte

| Befund | Nachweis | Was daraus nicht folgt |
|---|---|---|
| Der Bericht erklärt in allen drei Abschnitten, dass keine Agentenbeobachtungen zurückgegeben wurden. | E01: Einleitungen von Abschnitt 1–3; Abschnitt 3 „Epistemic Status“ | Dass keine Aktionen stattgefunden haben. |
| Die Inhalte werden als Designableitungen statt emergenter Ergebnisse eingeordnet. | E01: Abschnitt 2 „Limitation Statement“, Abschnitt 3 Schlussabsätze | Dass diese Thesen empirisch oder durch den Lauf bestätigt wären. |
| Fünf Szenarien werden erwähnt, aber nicht einzeln benannt oder mit Ergebnissen verglichen. | E01: Abschnitt 1 „The Five Competing Scenarios“ | Dass fünf eigenständige Varianten tatsächlich ausgeführt wurden. |
| Ein Einzelgespräch mit `central_banks_354` endet mit „Simulation environment not running or closed“. | E02 | Dass alle Erinnerungsdaten prinzipiell dauerhaft gelöscht oder technisch irreparabel waren. |
| Laufstatus meldet 86 Aktionen und 24 Runden; Plattform- und übergeordnete Statuswerte widersprechen sich teilweise. | E02 | Dass 86 autonome, inhaltlich bewertete Entscheidungen vorliegen oder beide Plattformen vollständig abgeschlossen sind. |
| Für diesen Durchlauf sind Erinnerungen laut Betreiber nicht verfügbar. | E05/E02 | Dass jede andere Installation dasselbe Problem hätte. |

## Warum der Erkenntnisgewinn gering war

### A. Unpassende Untersuchungsebene – plausibler Beitrag des Designs

Der Seed und die erzeugte Akteurslandschaft richteten sich auf Marktakteure, Institutionen und makroökonomische Treiber. Das später präzisierte Lernziel betrifft unterschiedliche Menschen und die Interpretation von Nachrichten aus ihrer Lebenslage. Das ist eine Passungslücke, kein Nachweis, dass die Marktinformationen falsch waren. Mehr Originalberichte hätten diese Lücke allein nicht geschlossen.

**Ableitung:** R01 individuelle Personas, R02 Lebenslage/Disposition/Zustand trennen, R03 plausible Gruppen statt gemeinsamer Diskussionsraum aller Wirtschaftsakteure.

### B. Bericht ohne zugängliche Verhaltensbelege – direkt belegt

Ohne zitierte Aktionen oder Gespräche bleibt offen, ob sich eine Einschätzung durch Austausch änderte. Der ReportAgent lieferte trotzdem einen langen Text. Dessen Umfang wurde zunächst mit Erkenntnisgewinn verwechselt. Eine Gedächtnis- oder Abrufstörung ist als technische Ursache möglich; ihre genaue Ursache lässt sich ohne weitere Originalartefakte nicht bestimmen.

**Ableitung:** R04 Gedächtnis und Zustände prüfen, R05 Beiträge mit Änderungen verknüpfen, R08 Fehlzustände sichtbar machen.

### C. Kein nachgewiesener sozialer Einfluss – Evidenz fehlt

Ein Feed, viele Aktionen oder unterschiedliche Ausgangsmeinungen belegen noch keine gegenseitige Beeinflussung. Im Bericht fehlen Vorher-/Nachher-Zustände, erhaltene Beiträge und eine Vergleichsbedingung ohne Austausch. Das Fehlen solcher Nachweise wird nicht als Beweis interpretiert, dass OASIS keinerlei sozialen Einfluss erzeugen kann.

**Ableitung:** R05 nachvollziehbare Einflusskette und R06 Vergleichsbedingungen.

### D. Zu breite Fragestellung für den geprüften Nachweis – Designbewertung

Mehrere Metalle, fünf Szenarien und ein langer Zukunftshorizont sollten gleichzeitig betrachtet werden. Der Bericht wies weder die Szenarienausführung noch die Ergebnisse aus. Viele Zielgrößen erschwerten eine klare Beurteilung, ob überhaupt eine neue Erkenntnis entstanden war.

**Ableitung:** R07 kurzer Pilot mit einem Informationsanlass und begrenzten Gruppen; keine Kalenderjahre aus Gesprächsrunden ableiten.

### E. Annahmen wurden teilweise stärker als der Seed formuliert – inhaltliche Prüfung

Beispiele aus E04: soziale Medien nur als nachlaufender Verstärker; Reservediversifikation als struktureller Nachfrageboden; aus zwei Nachfragekanälen abgeleitete höhere Volatilität. Diese Aussagen wurden nicht durch Laufbelege gestützt. Eine offene Frage wurde stellenweise zu einer scheinbar feststehenden Eigenschaft.

**Ableitung:** R09 Quellen, Annahmen und erzeugte Aussagen getrennt halten; Ausgangspositionen dürfen sich verändern, ohne Ergebnisse vorzugeben.

### F. Kein belegter Zusatznutzen zum Aufwand – offen statt quantifiziert

Es gab keinen vorab festgelegten Vergleich mit einer direkten Analyse und keine vollständige Kostenmessung. Der dokumentierte Erkenntnisgewinn war gering; eine konkrete Kosten-Nutzen-Kennzahl lässt sich nicht berechnen. Der Lernerfolg im Workshop wurde nicht getestet.

**Ableitung:** R07 Kostenlimit und einfacher Vergleich; R10 pädagogischer Nachweis als eigene Prüfung.

## Erhaltene Stärken und begrenzter Nutzen

Das Konzept eines sozialen Feeds, generierte Akteure und spätere Gespräche bleiben interessante Bausteine. Der Bericht machte seine fehlende Datengrundlage vielfach ausdrücklich sichtbar und vermied konkrete Preisziele. Die vorhandene Recherche bleibt als Informationsmaterial verwendbar. Diese Stärken reichen für unseren Anwendungsfall ohne verlässliche Erinnerungen und nachvollziehbaren Einfluss nicht aus.

## Entscheidung und Wiederaufnahmebedingung

Kein weiterer großer MiroFish-Lauf in dieser Projektphase. Zunächst bestehende Alternativen anhand der [Anforderungen](../requirements.md) und des [Prüfprotokolls](../assessment-protocol.md) untersuchen. MiroFish könnte später erneut betrachtet werden, wenn ein kleiner Test die relevanten Lücken schließt; eine bloße Zusage oder ein neuer Bericht genügt nicht.

Die Originaleingaben werden nicht rückwirkend umgeschrieben. Frühere Reportthesen werden als Hypothesen, nicht als bestätigte soziale oder finanzielle Ergebnisse übernommen.
