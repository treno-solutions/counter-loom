# Historischer Edelmetall-Recherchebestand

Stand: **1. November 2026**. Der ursprüngliche Research Seed im Projektstamm bleibt unverändert.

Die folgenden Angaben zum vollständigen Archiv beziehen sich auf das lokale Arbeitsverzeichnis. Originalberichte, vollständige Extraktionen, Webseitenkopien und Abbildungen sind nicht im öffentlichen Git-Repository enthalten. Quellenregister und `file-manifest.json` dokumentieren auch diese lokalen Dateien. Siehe [Daten und Quellenrechte](../DATA_POLICY.md).

## Direkt verwendbare Dateien

- [Recherchepaket für MiroFish](../mirofish/precious-metals-evidence-pack.md): Fakten, benannte Akteure, dokumentierte Beziehungen, Gegenargumente und Quellen.
- [Historische Preisauswertung](../mirofish/historical-price-evidence.md): berechnete Kennzahlen mit Definitionen und Grenzen.
- [Separater Simulationsprompt](../mirofish/next-run-prompt.md): in das Promptfeld; nicht als Rechercheersatz hochladen.
- [Quellenverzeichnis](../sources/README.md): Originaladressen, Datenstände und lokale Dateien.
- [Recherchebefunde und offene Lücken](../notes/research-findings.md).
- [Konvertierung und Prüfung](../qa/conversion-and-validation.md).

## Was abgelegt ist

`raw/` enthält die Original-PDFs von **In Gold We Trust 2026 (486 Seiten)**, **World Silver Survey 2026 (92 Seiten)**, USGS Mineral Commodity Summaries 2026 und zwei IEA-Berichten. Hinzu kommen die Weltbank-Originalarbeitsmappe, FRED-Originaldaten sowie acht frei zugängliche Gold-Demand-Trends-Kapitel mitsamt Tabellen. WGC-PDF-/Excel-Downloads verlangten Anmeldung; diese Dateien sind deshalb nicht enthalten.

`processed/` enthält bildfreie vollständige Textextraktionen, seitenweise JSON-Dateien, bereinigtes Markdown sowie strukturierte Preis-, Nachfrage-, Akteurs- und Beziehungsdaten. Die vollständigen Textfassungen können weiterhin Sponsorenmaterial und Diagrammbeschriftungen enthalten. Für frühere Folgelaufplanungen waren die **zwei kuratierten MiroFish-Evidenzdateien** vorgesehen. Dieser Bestand ist keine Startfreigabe für einen weiteren MiroFish-Lauf. Bilder und Charts sind im Originalarchiv weiterhin verfügbar.

Die Weltbankreihe umfasst Januar 1960 bis September 2026. Gold und Silber: nominale USD je Feinunze; Kupfer: nominale USD je metrischer Tonne. Die Preise sind Monatsmittel, keine Barrenpreise. Die FRED-Reihe DFII10 umfasst tägliche reale Treasury-Marktrenditen von Januar 2003 bis Oktober 2026.

## Nachvollziehbarkeit

- Quellen-IDs verbinden Fakten, Rohdateien und Textstellen.
- Originaldateien werden nicht verändert. SHA-256-Prüfsummen stehen im Quellenregister und Dateimanifest.
- Beobachtungen, historische Schätzungen, externe Prognosen, Autorenmeinungen und eigene Berechnungen werden getrennt ausgewiesen.
- Stichproben-Sichtprüfung und Zahlenkontrollen sind dokumentiert. Vollständige Konvertierung ist keine vollständige visuelle oder inhaltliche Prüfung aller Berichtsseiten.
- Verarbeitung ist in tools/ reproduzierbar. Benötigt werden Python mit PyMuPDF, pandas, numpy, openpyxl und pypdf; es werden keine Webzugänge oder Schlüssel benötigt, sobald die Rohdateien vorliegen.

## Noch nicht enthalten

Ein durchgehender Händlerprämien-Datensatz, ein überprüftes Netzwerk industrieller Lieferverträge, eine empirisch kalibrierte Markträumung oder ein belastbares Preisprognosemodell. Die erneute Verifikation der IMF-Schuldenzahlen scheiterte am Seitenzugriff. Diese Lücken werden nicht durch erfundene Daten ersetzt.
