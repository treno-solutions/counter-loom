# Stabilisierung der Modellwirtschaft

Stand: 3. November 2026. Prüf- und Reparaturplan für das bestehende Modell v16, Quellstand `98c20c8`. Die beschriebenen Mechanismen sind inzwischen als getrennte Varianten in [v18](STABILITY_MODEL.md) umgesetzt; [Prüfergebnisse](../qa/stability-v18-report.md) dokumentieren ihre Grenzen. Eine separate KI-Prüfinstanz hat Quellcode und vorhandene Diagnosen kritisch geprüft; dies ist keine externe empirische Validierung.

Die bisher gefundenen Personal- und Investitionsprobleme sind begründet. Ihre Reparatur allein garantiert aber keine stationäre Wirtschaft. Zuerst muss die Modellschliessung ausdrücklich festlegen, welche Bestände Haushalte langfristig halten möchten und welcher Sektor einen tatsächlich anhaltenden Geldüberschuss finanziert. Danach lassen sich die einzelnen Regler getrennt korrigieren, ohne immer neue Ausgleichszahlungen einzubauen.

## Befunde und ihre Bedeutung

| Befund | Einordnung | Konsequenz |
| --- | --- | --- |
| Kopfzahl richtet sich nach Absatz, Arbeitszeit zusätzlich nach Lagerbedarf | Inkonsistente Bedarfssignale im Firmenregler | Kopfzahl und gesamten Arbeitsumfang gemeinsam planen |
| Drei negative Einzelmonate lösen grosse Ausgabenkürzungen aus | Politische Modellannahme mit starken Schwellen und Kalendereffekten | Quartalssaldo und tatsächliche Finanzierungslage getrennt prüfen |
| Maschinen benötigen freie Restware nach den anderen Käufen | Beschränkter Investitionsablauf | Finanzierten Auftrag in die Produktion des Lieferanten übernehmen |
| Haushaltsvermögen erhöht den Konsum oberhalb des Grundbedarfs nicht | Unvollständige langfristige Verhaltensannahme | Gewünschten Liquiditätsbestand oder fortgesetzte Akkumulation ausdrücklich modellieren |
| Steigende Staatsschuld bei privatem Geldüberschuss | Möglicher korrekter Finanzierungspfad | Nicht allein als Buchungsfehler oder Inflationszwang behandeln |

Belege: [Firmenentscheidungen](../qa/firm-reactions-v16-diagnosis.md), [Sparen und Investitionen](../qa/saving-investment-v16-diagnosis.md), [Haushaltsregel](systems.py), [Firmenregeln](firms.py), [Staatsregel](public_budget.py) und [Buchungskern](world.py). Die archivierten 600-Monats-Läufe bleiben unverändert.

## Stationären Referenzfall festlegen

Der ruhige Referenzfall soll bei konstanten äusseren Bedingungen über längere Zeit erklärbare Einkommen, Beschäftigung sowie begrenzte Geld- und Schuldenbestände ermöglichen. Er verlangt weder Vollbeschäftigung noch zwei öffentliche Stellen, identische Kontostände oder einen ausgeglichenen Staatshaushalt in jedem Monat. Andere Annahmen und Schocks dürfen weiterhin zu Arbeitslosigkeit, Insolvenzen oder Finanzierungsgrenzen führen.

Nicht gleichzeitig stationär möglich sind dauerhaft positive Netto-Geldüberschüsse eines Sektors und dauerhaft begrenzte Gegenbestände aller anderen Sektoren. Die Konsumquote von 95 % erzwingt allerdings nicht für immer einen solchen Überschuss: Schon heute kann der Grundbedarf Rücklagen aufzehren. Entscheidend sind die tatsächlich gebuchten Nettoänderungen, nicht die Bezeichnung des Parameters.

Für den ruhigen Referenzfall wird eine begrenzte Liquiditätsvorsorge als erste zu prüfende Modellschliessung empfohlen: Haushalte bauen einen gewünschten Puffer auf und verwenden überhöhte Guthaben allmählich wieder. Die Höhe des Puffers und die Anpassungsgeschwindigkeit sind offene illustrative Szenarioparameter. Eine andere Variante darf dauerhaft zusätzliche Geldbestände anstreben; dann muss der korrespondierende Finanzierungsbedarf sichtbar bleiben.

Diese Haushaltsvarianten erhalten eigene Regelkennungen. Die archivierten 95-/100-%-Einkommensregeln werden weder nachträglich umgedeutet noch überschrieben. Ein Puffermechanismus ist eine zusätzliche Verhaltenshypothese, keine Bilanzidentität und keine bestätigte Beschreibung realer Haushalte.

## Kleine getrennte Korrekturen

### Gemeinsame Personalplanung

Eine einzige Mengenanforderung aus erwarteten Verkäufen, Lagerziel und freiem Lagerbestand verwenden. Zuerst den nötigen gesamten Arbeitsumfang bestimmen, dann auf vorhandene Verträge verteilen. Vertragsänderungen nur prüfen, wenn die verfügbare Arbeitszeitbandbreite nicht ausreicht. Finanzierung, Verlustbrücke, Stilllegung und Wiederanlauf bleiben eigene Bedingungen.

Im derzeitigen Kostenmodell gibt es keine fixen Kosten je Beschäftigtem. Eine geringere Kopfzahl bei gleicher Gesamtarbeitszeit bringt daher keinen modellierten Kostenvorteil. Eine solche Ersparnis darf nicht zur Begründung von Entlassungen behauptet werden.

Erfolg: Die belegten Wechsel knapp an der Vollzeitgrenze verschwinden, ohne dass notwendige Einstellungen oder Stilllegungen unterdrückt werden. Weniger Staatsschuld allein genügt nicht; Konsum, tatsächliche Arbeit, Transfers und verbleibender Kassenverbrauch werden gemeinsam ausgewertet.

### Fiskalische Zeitbasis

Im isolierten Gegenlauf zunächst nur die Beurteilungsperiode verändern: wiederkehrende Einnahmen und Bedarf über ein vollständiges Ausschüttungsquartal vergleichen. Die harte Finanzierungsgrenze weiterhin getrennt vor Arbeitsbeginn prüfen. Eingriffshöhe und Wiederaufbauregel bleiben im ersten Gegenlauf unverändert.

Erfolg: Eine Verschiebung von Ausschüttungen innerhalb desselben Quartals erzeugt bei gleichen Quartalssummen weniger unterschiedliche politische Entscheidungen. Tatsächlich fehlende Zahlungsmittel dürfen trotzdem Handlungen begrenzen. Eine Verbesserung des Staatssaldos wird nicht vorausgesetzt; beide Konsumvarianten können schlechter abschneiden. Die anschliessend getrennte Variante `buffered_quarterly` vergleicht die projizierte Finanzierungslücke mit tatsächlicher Kasse und nutzbarem Kreditraum. `funding_only` erhält die reine Vorfinanzierungsgrenze als weitere Kontrolle. Die Grösse fiskalischer Schritte wird nicht auf ein gewünschtes Endergebnis kalibriert.

### Bestellbarer Maschinenauftrag

Eine begründete Investitionsentscheidung erzeugt einen einzelnen finanzierten Auftrag. Der Lieferant berücksichtigt ihn in seiner Produktionsplanung und reserviert die entsprechende Ware. Zahlung und Lieferung werden gemeinsam verbucht; die zusätzliche Kapazität wirkt erst danach. Ein offener Auftrag verhindert Doppelbestellungen. Kein automatischer Maschinenkauf nur deshalb, weil Haushalte sparen.

Erfolg: Ein finanzierter Auftrag erreicht tatsächlich Produktion und Lieferung, sofern Arbeitszeit und Vorfinanzierung ausreichen. Es entstehen weder doppelte Ware noch zusätzliche Guthaben ohne Kreditbuchung. Bei freier Kapazität und fehlender Nachfrage darf weiterhin keine Erweiterungsinvestition stattfinden. Reines Vorziehen des Käufers in der Zahlungsreihenfolge würde nur bestehende Ware umverteilen und ersetzt diese Prüfung nicht.

Ersatzinvestitionen, Verschleiss und öffentliche Kapitalbildung bleiben spätere, getrennte Erweiterungen. Sie werden nicht gleichzeitig mit der Reparatur des Bestellablaufs eingeführt.

## Reihenfolge und Abbruchkriterien

1. Referenzfall, Bedeutung von Sparen und langfristige Bestandsziele festhalten. Gegenwärtig vorgeschlagen: Liquiditätspuffer als eigene Haushaltsvariante.
2. Personalplanung isoliert abschliessen und gegen die unveränderten 95-/100-%-Referenzen vergleichen.
3. Fiskalische Zeitbasis bei unveränderten übrigen Regeln prüfen.
4. Maschinenauftrag und Lieferfähigkeit isoliert prüfen.
5. Den zuvor fachlich festgelegten Haushaltsmechanismus implementieren und mehrere Pufferhöhen, Anpassungsgeschwindigkeiten sowie Anfangsguthaben vergleichen.

Jeder Schritt nennt vorab erwartete Wirkung und Widerlegungskriterium. Zunächst die betroffene Mechanik in kurzen Versuchen prüfen, danach 600 Monate mit vollständigen Buchungs- und Warenprüfungen vergleichen. Ein behaupteter stationärer Referenzfall benötigt anschliessend einen längeren Horizont; ein positiver Restbestand in M600 reicht nicht. Drift von Konten und Schulden wird ausgewiesen, damit langsam aufgebrauchte Anfangspuffer nicht als Gleichgewicht gelten.

Die Änderung wird angehalten, wenn sie lediglich den Finanzierungsengpass verschiebt, durch versteckte Zahlungen ausgleicht, vorher korrekte Buchungen verletzt oder ihre behauptete Wirkung nicht zeigt. Solche Ergebnisse bleiben dokumentiert. Die Kombination wird erst geprüft, wenn die einzelnen Mechanismen nachvollziehbar sind.

Es werden jetzt weder Wachstum, Inflation noch neue Steuern oder zusätzliche Subventionen als pauschaler Ausgleich eingeführt. Die Aufgabe ist ein begrenztes, nachvollziehbares Kreislaufmodell mit begründeten Krisen und Anpassungen; eine vollständige Volkswirtschaft ist dafür nicht erforderlich.
