# Liquiditätsziele Finanzierung und Maschinenaufträge

Modell v18. Die Oberfläche startet die ausdrücklich benannte Referenzvariante `World.stable()`. `World()` behält die historischen Einkommens-, Personal-, Staats- und Sofortkaufregeln als kontrollierbare Vergleichskombination. Die neuen Regeln ändern weder Steuersätze noch Transferhöhe, Anfangsguthaben oder Vollzeitlohnsatz. Sie sind illustrative Annahmen, keine empirisch kalibrierte Volkswirtschaft.

## Haushaltsguthaben als Bestand

Die neue Haushaltsregel `liquidity_target` verwendet ein Liquiditätsziel statt eines auf Dauer vorgeschriebenen positiven Netto-Geldüberschusses. Pro Haushalt gelten zunächst drei Monate des Grundbedarfs, also 3.000 Euro, und eine Anpassungsdauer von zwölf Monaten.

Mit `A` als tatsächlichem Kontoguthaben am Monatsanfang, `Z` als Liquiditätsziel, `Y` als Nettoeinkommen einschliesslich verfügbarer Nettoausschüttungen und `p` als Einkommensanteil lautet der Plan:

`Konsumwunsch = max(Grundbedarf, floor(p × Y / 100) + floor((A − Z) / Anpassungsmonate))`

Die Referenz verwendet `p = 100`. Bei geringerem Anfangsguthaben wird weniger geplant, bei höherem mehr. Der Grundbedarfsplan kann Rücklagen beanspruchen. Tatsächlich verfügbare Zahlungsmittel, Ware und Gütereinheiten begrenzen weiterhin die Käufe. Ein Konsumeingriff senkt den Einkommensanteil auf 65 %; Normalisierung stellt in dieser Variante 100 % wieder her.

Das Anfangsguthaben wird vor aktuellen Löhnen und Transfers eingefroren. Ausschüttungen vom letzten Abschluss liegen bereits auf diesem Konto und werden wie zuvor in der Einkommensbasis der nächsten Kaufrunde berücksichtigt. Es wird nicht das gesamte vorhandene Vermögen zusätzlich zum Einkommen als Kaufbudget angesetzt, sondern nur die verteilte Abweichung vom Ziel. Aktuelle Ausschüttungen nach der Kaufphase gehören erst zur nächsten Kaufrunde.

Das Ziel ist kein gesperrtes Konto und keine Auszahlungsgarantie. Fehlende Ware kann Guthaben auch oberhalb des Ziels halten. Die Variante `income` bleibt unverändert: 95 oder 100 % der Einkommensbasis, mindestens Grundbedarf, ohne Reservekorrektur. Sie wird nicht nachträglich als dieselbe Sparregel bezeichnet.

## Arbeitsumfang und Verträge

Die Variante `joint` plant Kopfzahl und Arbeitszeit aus derselben Anforderung:

`Neuproduktion = max(0, Absatzprognose + Lagerziel − freies Lager) + offene unreservierte Auftragsteile`

Bestehende Verträge bleiben, solange der Bedarf innerhalb der Arbeitszeitbandbreite von 25 bis 100 % je Person gedeckt werden kann. Eine Vertragsänderung benötigt zwei gleichgerichtete Abschlüsse, verfügbare Arbeitskräfte beziehungsweise einen reduzierbaren Vertrag und bestätigte Finanzierung. Die Grenze für die monatliche Anpassung gilt für den gesamten Arbeitsumfang: höchstens 0,25 Vollzeitäquivalente je bisherigem Vertrag. Rundung auf ganze Basispunkte darf höchstens `neue Kopfzahl − 1` Basispunkte zusätzlich erzeugen.

Verlustbudget, Liquidität, angeordnete Schliessung, Stilllegung und Wiederanlauf bleiben eigenständige Grenzen. Ein finanzierter Maschinenauftrag zählt auch beim Wiederanlauf eines stillgelegten Lieferanten als Nachfrage. Eine bestimmte Vertragszahl ist nicht garantiert. Die historische Variante `legacy` bleibt für Gegenläufe verfügbar.

## Staatsentscheidungen und Zahlungsfähigkeit

Die Referenzpolitik `buffered_quarterly` beurteilt vollständige Ausschüttungsquartale. Ein negativer Quartalssaldo löst nicht allein eine strukturelle Kürzung aus. Das vereinfachte Defizit wird über einen ausdrücklich gewählten Planungshorizont fortgeschrieben:

`Projizierte Lücke = max(0, −Quartalssaldo) × Planungshorizont / 3`

`Finanzierungsraum = max(0, Kasse + nutzbarer Kreditrahmen − bestehendes Reserveziel − fällige Altverpflichtungen)`

Der Horizont beträgt zunächst zwölf Monate. Kredit zählt nur bei vorhandenem positivem Bankeigenkapital und innerhalb der bestehenden Kreditgrenze. Die Fortschreibung ist keine Prognose zukünftiger Steuereinnahmen. Nur wenn die projizierte Lücke den Finanzierungsraum übersteigt, wird die bisherige strukturelle Kürzung geprüft: zuerst 25 Prozentpunkte Beschaffungsquote, danach gegebenenfalls eine öffentliche Stelle. Vor jeder Arbeitsrunde gilt weiterhin die harte bestätigte Finanzierung; knappe Sozialzahlungen bleiben anteilig und offen ausgewiesen.

Die Kontrollen `quarterly` (reine Quartals-Nullschwelle), `adaptive` (historische Einzelmonate), `funding_only` (nur harte Vorfinanzierungsgrenze) und `legacy` (historische feste Ausgaben) bleiben getrennt. Ein langfristiges Defizit darf auch unter der neuen Politik eine Finanzierungsgrenze erreichen. Zum Nachweis genügt deshalb weder eine positive Kasse noch null Staatsschuld. Kasse minus Schuld und deren Drift werden gemeinsam geprüft.

Exportierte Prüfwerte enthalten Quartalsbasis, Projektion, Horizont, Kasse, nutzbaren Kredit, Reserve, Altverpflichtungen und tatsächlichen Beobachtungsmonat. Ein im Folgemonat weiter angezeigter Quartalswert wird nicht als neue Prüfung ausgegeben.

## Produktion eines finanzierten Maschinenauftrags

Die Variante `orders` ersetzt den alleinigen Kauf aus Restbeständen durch einen Auftrag. Zwei vorherige Engpassmonate, der bestehende Investitionsabstand, ein aktiver Käufer und genügend Geld oberhalb des Betriebspuffers bleiben Voraussetzungen. Ohne Anlass wird keine Maschine gekauft.

Ein Auftrag bindet den angebotenen Preis für acht ursprüngliche Werkstatteinheiten und den vollen Kaufbetrag auf dem bestehenden Käuferkonto. Dieser Betrag kann weder ausgeschüttet noch für andere Zahlungen verwendet werden. Er bleibt Teil desselben Guthabens; es entsteht kein zweites Geldkonto. Ein offener Auftrag verhindert eine weitere Maschinenbestellung oder parallele manuelle Maschinenkreditanfrage.

Vorhandene und neu produzierte Teile werden reserviert. Fehlende Teile gehen in die Produktions- und Personalplanung der Werkstatt ein. Reservierte Teile bleiben physischer Lagerbestand, stehen aber nicht mehr für andere Verkäufe zur Verfügung. Teilproduktion ist kein Teilumsatz: Erst die vollständige lieferbare Maschine erzeugt Zahlung und Lagerabgang. Der Käufer erhält genau eine Anlage, der Lieferant genau den gebundenen Kaufbetrag. Kapazität wirkt erst in der nächsten Produktionsrunde. Schliessungen verzögern die Lieferung; sie erzeugen keine vorgezogene Kapazität.

Geld-, Forderungs-, Waren- und Kostenwertprüfungen gelten unverändert. Der historische Sofortkauf `spot` und der ausdrücklich angefragte Bankkredit bleiben gesonderte Vergleichswege. Ersatzinvestitionen, Abschreibung und öffentliche Kapitalbildung werden nicht gleichzeitig neu eingeführt.

## Sichtbare Nachweise

In der Makroübersicht öffnet **Liquiditätsziele und Kontodrift** Ziel und Guthaben je Haushalt, die staatliche Nettoposition sowie eine kurze Bestandsänderung über vollständige Sechsmonatsblöcke. Diese Anzeige ist keine Langzeitvalidierung.

**Unternehmen → Betrieb** zeigt die gemeinsame Personalplanung und den Maschinenauftrag von Finanzierung über reservierte Teile bis zur bezahlten Lieferung. **Staat → Details** zeigt die Finanzierungsprüfung und ihre beobachteten Eingaben. Der historische Kaufplan je Haushalt erklärt auch die Reserveanpassung.

Die Datenschnittstelle verwendet `illustrative_circular_flow_v18`. Nach einem Rechenkernwechsel sind ein neu geladener Client und ein neuer Lauf erforderlich. Frühere Ergebnisarchive bleiben erhalten. [Prüfplan](STABILITY_PLAN.md) und [Ergebnisvergleich](../qa/stability-v18-report.md) trennen technische Bilanzprüfung, mechanische Korrektur und wirtschaftlichen Stabilitätsbefund.

Die [getrennten Schockversuche](../qa/isolated-shocks-v18-report.md) vergleichen höhere Leitzinsen, teurere Energie und eine befristete Betriebsschliessung aus demselben eingeschwungenen Zustand. Ihre Eingriffe verändern keine Wirtschaftsregel; Monatswerte, Gegenbuchungen und verbleibende Abweichungen sind separat dokumentiert.

Die [Diagnose der schwachen Zinswirkung](../qa/rate-transmission-v18-diagnosis.md) verfolgt die tatsächlichen Zinszahlungen und Ausschüttungen, trennt die unterschiedliche Gewinnbesteuerung von inaktiven Kreditfunktionen und benennt fehlende Übertragungswege. Sie verändert keine Wirtschaftsregel.

Aktueller Zusatz v19: [Bankgewinnrechnung und Gewinnverwendung](BANK_PROFIT_MODEL.md). Die hier archivierten v18-Stabilitätsbefunde bleiben historische Vergleiche; für die neue Bankregel werden eigene Kontroll- und Zinsschockläufe dokumentiert.

Aktueller Zusatz v20: [Wirtschaftlichkeitsprüfung von Maschinen](INVESTMENT_MODEL.md) mit Kapitalwert, explizitem Eigenmittel-Bewertungszins und Kredit-Schuldendienst. Die tatsächliche Produktions-/Zahlungskette bleibt erhalten. Historische Referenzbefunde bleiben getrennt archiviert.
