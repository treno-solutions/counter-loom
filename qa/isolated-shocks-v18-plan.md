# Einzelne Schocks in der bestehenden Modellwirtschaft

Stand: 3. November 2026. Vorab festgelegter Versuchsplan für die unveränderte Referenzkonfiguration v18, Quellstand `f59b47d`. Die Versuche sind eigene simulierte Befunde und keine Prognosen realer Volkswirtschaften.

## Gemeinsamer Ausgangszustand

Die Welt wird ohne Eingriff bis zum Abschluss M1440 fortgeschrieben. Alle gespeicherten wirtschaftlichen Vergleichsfelder werden für jeden Monat gegen den bereits geprüften [Referenzlauf](stability-v18/stable.json) abgeglichen. Dieser Zeitpunkt liegt im nachgewiesenen späten zyklischen Referenzbereich. Ein Start während der Anlaufphase würde deren Folgen mit dem Schock vermischen.

Von genau diesem vollständigen Zustand werden fünf getrennte Kopien fortgesetzt. Der erste Schockmonat ist M1441. Jede Fortsetzung läuft 60 Monate; zusätzlich werden die 24 Monate vor dem Eingriff ausgewiesen. Der ungestörte Kontrollzweig muss den archivierten Referenzverlauf auch nach dem Abzweigen exakt reproduzieren. Keine Verhaltensregel, Steuer, Lohnhöhe, Anfangsverteilung oder Finanzierungsgrenze wird für diese Versuche verändert.

## Eingriffe

| Variante | Eingriff | Rücknahme |
| --- | --- | --- |
| Kontrolle | Kein Schock | Entfällt |
| Leitzins | Von 2 auf 5 % ab M1441 | Zurück auf 2 % ab M1453 |
| Energie | Verdoppelte Produktionsenergiekosten ab M1441 | Ausgangskosten ab M1453 |
| Betrieb ohne Ersatzleistung | Alltag & Versorgung schliesst M1441–1443 | Freigabe ab M1444 |
| Betrieb mit Ersatzleistung | Identische Schliessung; 60 % des eingefrorenen Referenz-Nettoarbeitslohns | Freigabe ab M1444 |

Die Leitzinsänderung wirkt auf neue Kreditangebote sofort ab dem Eingriffsmonat, auf den variablen Betriebskredit mit einem Monat Verzögerung und nicht auf bestehende feste Vertragszinsen. Energiekosten und Verkaufspreise werden getrennt beobachtet; die bestehende Preisregel wirkt verzögert. Bei einer angeordneten Schliessung bleiben Verträge erhalten, während Produktion und Verkauf des betroffenen Betriebs ruhen. Bezahlte Arbeitszeit ist deshalb aussagekräftiger als Kopfzahl allein.

## Beobachtung und Auswertung

Je Haushalt: tatsächlich erhaltenes Nettoeinkommen, Löhne, Transfers und Kurzarbeitsleistung, aktuelle Ausschüttungen, nominale und zu Startpreisen bewertete Käufe, Kaufplan, nicht finanzierbarer beziehungsweise mangels Ware unerfüllter Kaufplan sowie Guthaben. Aktuelle Ausschüttungen und der frühere Ausschüttungsbetrag im Kaufplan bleiben zeitlich getrennt.

Je Betrieb: Erlöse, Ergebnis vor Steuer, Löhne, Zins- und Energiezahlungen, Produktion, Lager, Preise, tatsächliche bezahlte Vollzeitäquivalente, Verträge, Betriebszustand und Anlagen. Beim Staat: Steuern, Löhne, Sozialzahlungen, Beschaffung, Kasse, Schuld, Nettoposition und offene Finanzierungslücken. Beim Ausland: tatsächliche Waren- und Zahlungsströme. Eine Änderung der nominalen Käufe wird nicht automatisch als Mengenänderung ausgelegt.

Die Auswertung zeigt Abweichungen vom zeitgleichen ungestörten Verlauf. Drei Monate Schliessung, zwölf Eingriffsmonate und die gesamte 60-Monats-Fortsetzung werden getrennt ausgewiesen. Für Bestände werden Stichtagsdifferenzen, für Flüsse aufsummierte oder mittlere Periodendifferenzen verwendet. Ausbleibende oder kleine Reaktionen bleiben sichtbar; Schockhöhe und Regeln werden nicht nachträglich auf dramatische Ergebnisse eingestellt.

Jede Phase behält die bestehenden Bilanz- und Warenprüfungen. Neue Buchungen werden zusätzlich anhand der Guthaben vor und nach jeder Gegenbuchung unabhängig rekonstruiert. Der kompakte Zahlungsnachweis beginnt beim gemeinsamen Ankerzustand; das alte Journal bleibt in den berechneten Welten erhalten, wird aber nicht fünffach im Ergebnis dupliziert. Die Originalwelt darf durch einen Zweig nicht verändert werden.
