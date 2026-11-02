# Haushalts-Konsumhistorie: Prüfung

Stand: 2026-11-02. Ergänzung zu Modell v7; keine Änderung der Wirtschaftsregeln.

## Umsetzung

- Sechs Haushaltsverläufe für Konsumwunsch und tatsächliche Käufe, mit gemeinsamer Euro-Skala ab null und gemeinsamem Zeitbereich.
- Historische Kaufplan-Eingaben werden beim Kauf erfasst, beim Monatsabschluss archiviert und im Laufexport ausgegeben. Spätere Ausschüttungen überschreiben diese Eingaben nicht.
- Wunsch minus Käufe entspricht Geldmangel plus Warenmangel plus Restbeträgen wegen ganzer Einheiten. Warenmangel wird erst nach Begrenzung auf finanzierbare ganze Einheiten berechnet.
- Wirksame Szenarioänderungen, Leitzinsänderungen, spätere variable Kreditzinsanpassungen und Arbeitsplatzwechsel sind im Verlauf markiert. Vorgemerkte, noch nicht wirksame Eingriffe werden nicht als bereits eingetreten dargestellt.
- Eine gemeinsame Monatsauswahl aktualisiert alle sechs Betragsansichten und Ereignisse. Manuelle historische Auswahl bleibt bei weiteren Rechenschritten bestehen; eine Schaltfläche kehrt zum jeweils neuesten Abschluss zurück.

## Ausgeführte Prüfungen

- 77 Python-Tests erfolgreich, darunter fünf neue Tests für Haushaltsjournal-Abgleich, fehlende Finanzierung, Zeitpunkte der Ausschüttungen, unveränderliche exportierte Vergangenheit und vier vollständige Schock-/Basisläufe.
- TypeScript-Prüfung und Produktionsbuild erfolgreich.
- 484 Zustände aus Basislauf, Konsumschock, Energieschock und Leitzinsschock vom echten Oberflächenschema akzeptiert. Absichtlich verfälschte Haushaltszahlung abgewiesen.
- 480 Phasenzustände mit dem Vorgängerstand `821f526` verglichen: identische Knoten, Buchungen, Meldungen, Geldprüfung, Bank-, Außenhandels-, Staatsfinanzierungs- und Leitzinsdaten. Bisherige Monatsfelder ebenfalls identisch; nur die dokumentierten historischen Eingaben ergänzt.
- Browserprüfung: sechs Diagramme, gemeinsame Monatsauswahl, aufklappbare historische Kaufpläne und Ereignisse. Leitzinsänderung in Monat 2 und variable Anpassung in Monat 3 getrennt sichtbar. Nach einem Konsumeingriff erscheint der tatsächliche Arbeitsplatzverlust von Haushalt 4 in der Kaufrunde von Monat 3, einschließlich des Kaufbetrags von 950 €.
- Energieschock: bei Haushalt 1 in Monat 4 Konsumwunsch 1.718,60 €, Käufe 900 €, davon 750 € Warenmangel und 68,60 € Einheitenrest, ohne Finanzierungslücke.
- Mobilprüfung mit 390 CSS-Pixeln: kein horizontaler Überlauf des Dokuments; Monatsnavigation scrollt innerhalb ihrer eigenen Zeile.

## Grenzen

Das sind Prüfungen von Datenintegrität und Darstellung, keine empirische Validierung des Wirtschaftsmodells. Gleichzeitige Ereignisse beweisen keine isolierte Kausalwirkung. Haushalte besitzen weiterhin keine eigenen Kredite; ein direkter Zinseffekt auf Haushaltsraten wird nicht behauptet. Vor der Ergänzung begonnene Läufe benötigen einen Neustart.
