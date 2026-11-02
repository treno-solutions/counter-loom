# Unabhängige Plausibilitätsprüfung: Fiskalpolitik V9

Prüfdatum: 2026-11-03. Illustrative Modellregeln, keine empirische Kalibrierung oder Aussage zur realen Schuldentragfähigkeit. Die acht Kernprüfsummen, Eingaben und kompakten Monatsbelege stehen in [fiscal-policy-v9-plausibility.json](fiscal-policy-v9-plausibility.json); vollständige Phasenbestände werden nicht dupliziert.

**Ergebnis:** Neun 24-Monats-Vergleichsläufe und vier offene 240-Monatsläufe bestanden die unabhängigen Buchungsrekonstruktionen: insgesamt 1.176 Weltmonate, 5.880 Phasen und 29.373 Buchungen. Zwölf Fiskalfälle, vier Horizont-/Ereignisfälle und ein isolierter Bedienerfall bestanden zusätzlich. Der bestätigte Widerspruch zwischen Personal- und Maschinenkapazitätsplanung ist im finalen Kern korrigiert. Die Langläufe zeigen trotzdem erhebliche Modellgrenzen: zeitweise Nullproduktion und stark wachsende öffentliche Lohnrückstände. Buchungskonsistenz ist hier kein wirtschaftliches Plausibilitätsurteil. Oberfläche und Unterrichtswirkung wurden nicht geprüft.

## Geprüfte Regeln und Brücken

Alle Geldkonten, Quell-/Zielstände vor und nach Buchung, Einlagen-/Kredit-/Bankkapitaländerungen sowie die Bankbilanz wurden aus Anfangsbeständen und jedem Journalbeleg neu berechnet. Bei veränderter staatlicher Anfangskasse wurde auch die anfängliche Geldsumme und Bankreserve unabhängig angepasst. Ein niedrigerer Anfangsbestand ist ein anderes Ausgangsszenario, keine Kreditbuchung und keine interne Geldumverteilung.

Die bisherigen Prüfungen bleiben enthalten: bezahlte Produktion, Warenmengen, historische Lagerkosten ohne Preisneubewertung, Warenzahlungen und Haushaltsmengen zu Startpreisen, GuV, Ausschüttungen, Firmen-Eigenkapital, Maschinenkredite, feste/variable Vertragszinsen, Staatskreditbeträge mit FIFO-Tilgung und Centverteilung sowie Auslandsbudget und Lieferbelege.

Das Reserveziel wird unabhängig aus dem **Personalstand am Monatsanfang**, geplanten Transfers, zwei Beschaffungsbudgets und neuen Monatszinsen berechnet. Die Abschlussentscheidung wird aus der Kasse nach Steuern und gegebenenfalls Zinsnachzahlung rekonstruiert:

- Unter dem Ziel: Kredit höchstens in Höhe der Lücke und des verbleibenden Rahmens, bei positivem Bankkapital.
- Über dem Ziel mit offener Schuld: Tilgung höchstens aus dem Überschuss und höchstens bis zur vollständigen Schuldentilgung. Keine geprüfte Abschlusstilgung senkt die Kasse unter das Ziel.
- Andernfalls: Halten. Eine rechnerische Tilgungskapazität erzeugt ohne Schuld keine Zahlung.

Untermonatliche Zwischenkredite werden als bereits vorhandene Kasse/Schuld berücksichtigt; sie werden beim Abschluss nicht nochmals als fehlende Liquidität finanziert. Jeder Monatsbeleg wurde mit den unabhängig berechneten Steuer-/Ausgaben-/Zins-/Finanzierungsflüssen verglichen. Insbesondere:

`Schlusskasse − Anfangskasse = Haushaltssaldo + Kreditaufnahme − Tilgung`

`Schlussschuld = Anfangsschuld + Kreditaufnahme − Tilgung`

Kassenabbau/-aufbau bezeichnet die positive beziehungsweise negative Seite der tatsächlichen **Netto-Kassenänderung**, nicht nochmals den Haushaltssaldo. Zinsansprüche verwenden die Anfangsrestschulden; neue Gutschriften werden erst im Folgemonat verzinst. Wiederholter Zinsdienst oder Abschluss eines geschlossenen Monats verändert den Zustand nicht.

## Neun Vergleichsfenster über 24 Monate

Diese Vergleichsläufe nutzen den optionalen Testhorizont von 24 Monaten. Der Standardlauf des Produkts hat keinen festen Endmonat. Energie-/Nachfrageschocks beginnen in Monat 3. „Kombiniert“ enthält beide und eine Leitzinserhöhung auf 4 % ab Monat 2. Standard: 80.000 € Anfangskasse, 50.000 € Kreditlimit, ein Reservemonat. Die kleine Anfangskasse beträgt 7.200 €. Der Maschinenlauf enthält zusätzlich den Energieschock und eine Anfrage vor Monat 1.

| Lauf | Buchungen | Erste Kreditaufnahme | Schuld Ende € | Kasse Ende € | Reserveziel Ende € | Entscheidung Ende |
|---|---:|---:|---:|---:|---:|---|
| Basis | 1.229 | keine | 0 | 20.058,22 | 7.200 | Halten |
| Energie | 1.158 | Monat 19 | 23.039,49 | 8.247,27 | 8.247,27 | Aufnehmen |
| Nachfrage | 1.111 | Monat 17 | 32.490,90 | 8.269,80 | 8.269,80 | Aufnehmen |
| Kombiniert | 1.112 | Monat 15 | 50.000 | 3.887,57 | 9.405,82 | Begrenzt |
| Anfangskasse 7.200 € | 1.268 | Monat 1 | 50.000 | 1.122,33 | 7.325 | Begrenzt |
| Kreditlimit null | 1.229 | keine | 0 | 20.058,22 | 7.200 | Halten |
| Null Reservemonate | 1.229 | keine | 0 | 20.058,22 | 0 | Halten |
| Zwei Reservemonate | 1.229 | keine | 0 | 20.058,22 | 14.400 | Halten |
| Maschine und Energie | 1.272 | keine | 0 | 26.022,97 | 7.200 | Halten |

Die Basis verbraucht im ersten Monat 2.413,60 € Kasse: 7.200 € bezahlte Primärausgaben minus 4.786,40 € Steuern. Ende stehen 77.586,40 € Guthaben und keine Staatsschuld; das Ziel von 7.200 € ist gedeckt. Die Anfangskasse wird also nicht auf 80.000 € aufgefüllt. Auch am Ende von Monat 24 ist die Kasse höher als die Ziele von null, einem oder zwei Ausgabenmonaten. Deshalb erzeugen diese drei Reservevarianten sowie das Nullkreditlimit hier dieselben wirtschaftlichen Verläufe. Das belegt keine allgemeine Wirkungslosigkeit der Reservepolitik.

Im kombinierten Lauf reicht der Kreditrahmen am Ende nicht für das Reserveziel. Trotzdem bestehen 3.887,57 € nutzbare Kasse und keine offenen staatlichen Lohn- oder Zinsansprüche. **Ein Finanzierungsstopp oder verfehltes Reserveziel ist hier keine nachgewiesene Zahlungsunfähigkeit.** Weitere Ausgaben können den Puffer aufbrauchen; der 24-Monatsbefund ist keine Aussage über unbegrenzte Fortführung.

Bei nur 7.200 € Anfangskasse bestehen dagegen am Ende 8.766,13 € offene öffentliche Lohnansprüche. Die sechs Arbeitsverhältnisse dieses Laufs bedeuten somit nicht sechs vollständig bezahlte Einkommen. Alte öffentliche Lohnrückstände werden weiterhin nicht automatisch nachgezahlt. Guthaben, fällige Zahlungen, Rückstände und Vertragsbeschäftigung müssen getrennt betrachtet werden. Staatszinsrückstände betragen am Ende aller neun vollständigen Läufe null.

Die Energievariante endet bei 7.133,50 € nominalem Konsum beziehungsweise gekauften Mengen mit 6.950 € Startpreiswert und fünf Arbeitsverhältnissen. Der kombinierte Lauf endet bei 4.571 € beziehungsweise 4.450 € und vier Arbeitsverhältnissen. Der Maschinenlauf erreicht 10.170 € beziehungsweise 9.900 € und sechs Arbeitsverhältnisse. Diese Pfade überlagern Haushaltsbudgets, Preise, Lager, Personal und Finanzierung; sie isolieren keine einzelne universelle Ursache.

## Zwölf isolierte Fälle

Die Fälle verwenden teils manuelle Testmonate und explizite Umbuchungen vor dem Monatsbeginn. Sie sind Schnittstellenprüfungen; sämtliche erzeugten Geldbelege und Bankgegenbuchungen wurden unabhängig rekonstruiert.

1. Erste Standardabrechnung: vorhandene Kasse finanziert den Fehlbetrag; keine Wiederauffüllung auf 80.000 €.
2. Anfangskasse null, ein Reservemonat: 9.613,60 € Nettokredit = 2.413,60 € bezahlter Fehlbetrag + 7.200 € Schlussreserve. Zwischenfinanzierung wird nicht verdoppelt; Abschluss idempotent.
3. Anfangskasse null, Reserve null: 4.800 € Zwischenkredit, davon 2.386,40 € zurückgezahlt; 2.413,60 € Restschuld, Kasse null. Null Reserve verbietet untermonatlichen Kredit nicht.
4. Teiltilgung: nach Zinsdienst bleibt genau das Ziel von 7.205 € Kasse erhalten; 1.490 € werden getilgt, 510 € Schuld bleiben.
5. Tilgung auf Schuld begrenzt: Restüberschuss bleibt in der Kasse, Bankkapital steigt durch Tilgung nicht.
6. Kasse genau auf Ziel: vorhandene Schuld wird gehalten; weder unnötige Aufnahme noch Tilgung.
7. Bindendes 1.000-€-Limit: 1.000 € Kasse, 6.200 € ungedecktes Reserveziel; keine daraus erfundenen Lohnrückstände.
8. Tatsächliche Zahlungslücke bei leerer Kasse und 1.000-€-Limit: 3.800 € öffentliche Löhne bleiben nach der Lohnphase explizit offen.
9. Späte 100 € Steuer bei Zinsrückstand: zuerst 2,50 € Zinsen bezahlt; 97,50 € bleiben als Puffer, keine Tilgung unter Ziel. Der Reservefehlbetrag bleibt separat sichtbar.
10. Zwei Reservemonate: Aufbau auf 14.400 € kann auch ohne laufenden Kassenfehlbetrag Kredit erfordern. Kreditbedarf und Haushaltssaldo sind verschiedene Größen.
11. Bankkapital null: keine neue Kreditgutschrift; fehlende Reservedeckung sichtbar.
12. Sechs ungültige Reserve-/Anfangskassenparameter werden abgewiesen.

## Vier offene Langläufe über 240 Monate

Alle vier Welten wurden frisch mit `horizon_months=None` gestartet. Das Ende bei Monat 240 ist nur das Ende dieses Beobachtungsfensters. Nach dem Export wurden weitere Energie-/Zinsvorgaben angenommen und Monat 241 gestartet. Ein separater Port bestätigt auch Maschinenanfragen nach Monat 24. Positive feste Testhorizonte bleiben optional und korrekt abgesichert.

- **Offene Basis:** unveränderte Bedingungen, 80.000 € Anfangskasse und 50.000 € Kreditlimit.
- **Später Schock:** Energieverdopplung, Nachfragerückgang und Leitzins 4 % ab Monat 25.
- **Wiederholte Zyklen:** gleiche Eingriffe ab Monat 25; Energie-/Nachfrageerholung und Leitzins 1 % ab Monat 49; erneute Schocks ab 73, Erholung ab 97, Schocks ab 121, Erholung ab 145, Schocks ab 169, Erholung ab 193. Der aktuelle Zustand bestimmt, welche erneute Vorgabe zulässig ist; doppelte und gegenläufige Vormerkungen desselben Bereichs werden ohne Zustandsänderung abgewiesen.
- **Armer Staat ohne Kredit:** 7.200 € Anfangskasse, Kreditlimit null, ansonsten Basisbedingungen.

Die ersten 24 Monate der offenen Basis sowie der beiden erst später veränderten Welten stimmen exakt mit den entsprechenden Monatswerten der kurzen Basis überein. Alle 240 Monatsgeschichten und das vollständige Journal bleiben intern und im Export erhalten; die normale `history`-Antwort enthält die letzten 36 Monate. Die unabhängigen Geld-/Bank-/Waren-/Kosten-/Eigenkapital-/Fiskalbrücken wurden über das gesamte Fenster weitergeführt. Es entstanden keine negativen Geldkonten oder unausgeglichenen Bankbilanzen. Auch die Firmen-Eigenkapitalpositionen blieben an allen geprüften Monatsabschlüssen positiv.

| Offener Lauf | Buchungen | Erste Nullproduktion beider Firmen | Erste offene Staatslöhne | Offene Staatslöhne Ende € | Offene Staatszinsen Ende € |
|---|---:|---:|---:|---:|---:|
| Basis | 5.978 | Monat 100 | Monat 53 | 880.331,25 | 18.363,58 |
| Schock ab Monat 25 | 4.662 | Monat 85 | Monat 39 | 968.500,64 | 34.299,53 |
| Wiederholte Zyklen | 5.114 | Monat 85 | Monat 39 | 965.115,31 | 33.538,28 |
| Armer Staat, kein Kredit | 2.782 | Monat 27 | Monat 2 | 1.136.780,43 | 0 |

„Erste Nullproduktion“ bedeutet einen einzelnen Monat ohne neue Produktion, keinen behaupteten dauerhaften Stillstand ab diesem Zeitpunkt: In späteren Monaten gab es nochmals kleine Produktionsphasen. Ende Monat 240 produzieren und konsumieren alle vier Welten null. Die Staatskasse ist dann jeweils leer; die drei kreditfähigen Welten halten 50.000 € Staatsschuld. Die monatlich weiter fälligen öffentlichen Löhne sammeln sich als offene Ansprüche, ohne automatische Personal- oder Rückstandsabwicklung.

Das ist keine Welt, in der insgesamt kein Geld mehr vorhanden wäre. Die offene Basis hält Ende Monat 240 noch 89.666 € Haushaltsguthaben und 106.064 € Firmenkasse. Ein aufschlussreicher Zustand liegt bereits in Monat 100 vor: Firmenkassen 71.444,36/39.625,60 €, keine Maschinen, Prognosen rund 24/13 Einheiten, kein Firmenpersonal und keine Produktion. Die starre Lohn-/Margenregel finanziert bei diesem erwarteten Absatz keine ganze Stelle; hohe vorhandene Guthaben allein lösen keinen Wiedereinstieg aus. Feste Budgets, Preise, ganze Arbeitskräfte, Verteilung, fehlende Lohnanpassung und fehlende staatliche Sanierung begrenzen hier den Kreislauf. Diese Ergebnisse bezeichnen Verhalten der Modellregeln und dürfen nicht als reale Wirtschaftsgesetze oder zwingende Krisenfolgen ausgegeben werden.

## Bedienerbefund und Nachprüfung

Unabhängig bestätigt wurde ein Widerspruch der früheren Personalregel: Bei zehn Maschinen und Absatzprognose 40 ergab der reine Kapazitätsbedarf null Beschäftigte, während die Produktionsregel Maschinenkapazität erst bei mindestens einer Arbeitskraft aktiviert. Der finale Kern fordert bei positiver Nachfrage mindestens einen Bediener als technischen Bedarf. Fehlende finanzierbare Marge darf den tatsächlich tragfähigen Personalbedarf weiterhin auf null begrenzen.

Der isolierte Nachtest mit null, einer und zwei bestehenden Arbeitskräften ergibt jeweils eine gewünschte Stelle; bei null Arbeitskräften bleibt aktuelle Produktion bis zur tatsächlichen Einstellung null. Bei fehlender Nachfrage oder zu hohem Schuldendienst kann der finanzierbare Personalbedarf weiterhin null sein. So werden Betrieb und finanzielle Tragfähigkeit nicht verwechselt.

Vier ergänzende Zustandstraces bis Monat 120 fanden in den untersuchten regulären Pfaden keinen Fall, in dem nur die Maschinenregel einen ansonsten finanzierbaren Bediener verhinderte. Der finale Bedienerfix verändert sämtliche numerischen Monatswerte der geprüften 24- und 240-Monatspfade nicht. Der latente Logikfehler ist damit behoben; er erklärt die hier beobachteten Stillstände nicht. Weitere Kernfehler wurden im geprüften Umfang nicht gefunden.

## Reichweite

Reserveziel, Anfangskasse, Ausgabenpläne und Kreditlimit sind gewählte Lernparameter. Das Ziel wird am Monatsanfang geplant; es ist weder gesperrtes Guthaben noch eine Garantie künftiger Zahlungsfähigkeit. Unbezahlte alte Ansprüche sind nicht bereits bezahlte Haushaltsausgaben und werden nicht durch eine Zielreserve automatisch abgewickelt.

Die neue Regel macht die Entscheidung aus vorhandener Kasse, Ziel und Schuld nachvollziehbar. Die geprüften Buchungs- und Vertragsbrücken stimmen. Die offenen Läufe erlauben, Regelgrenzen sichtbar zu machen, statt sie durch einen automatischen Abbruch nach 24 Monaten zu verdecken. Fiskalische Tragfähigkeit, repräsentative Verhaltensreaktionen und Unterrichtswirkung sind damit nicht validiert. Frühere Belege und Kerndateien wurden durch diese Prüfung nicht verändert.
