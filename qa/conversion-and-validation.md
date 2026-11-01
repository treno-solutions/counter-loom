# Konvertierung und Qualitätsprüfung

Vollständige Originale in raw/. Pro PDF: unveränderter Text je physischer Seite in .pages.json und .fulltext.txt; schlankere Textfassung in .clean.md. Keine Original-PDFs überschrieben.

|Dokument|PDF-Seiten|Original MB|Text-MD MB|Reduktion der Dateigröße|
|---|---:|---:|---:|---:|
|world-silver-survey-2026.pdf|92|15.26|0.237|98.4%|
|in-gold-we-trust-2026-de.pdf|486|53.01|1.339|97.5%|
|usgs-mcs-2026.pdf|226|17.65|0.810|95.4%|
|iea-energy-and-ai-2025.pdf|304|8.21|0.784|90.5%|
|iea-critical-minerals-2026.pdf|372|14.85|0.659|95.6%|

## Was bereinigt wurde

- Bilder sind nicht in den Textdateien enthalten; wiederkehrende Randzeilen wurden vorsichtig entfernt.
- Originalseitenzuordnung, Zahlen, Quellen und normaler Fließtext bleiben erhalten. Die vollständige Extraktion kann auch Sponsorentexte, Inhaltsverzeichnisse und Diagrammachsen enthalten.
- Das kompakte MiroFish-Paket ist deshalb eine separate, kuratierte Eingabe. Vollständige Konvertierung und redaktionelle Zusammenfassung sind ausdrücklich unterschiedliche Dateien.

## Prüfgrenzen

- Sichtprüfung: SI26 physische Seite 11 (gedruckt 9), IGWT26 Seite 368 und USGS26 physische Seite 177 (gedruckt 173). Prüfbilder liegen in qa/. Nicht jede Seite wurde visuell geprüft.
- Silber-Kerntabelle für 2024/2025/2026F aus dem Original kontrolliert; Summen und ETP-Bilanz mit Rundungstoleranz 0,21 Moz abgeglichen.
- WGC-Webtabellen separat strukturiert gespeichert. Keine erfolgreiche WGC-PDF-/XLSX-Anmeldung behauptet.
- Diagrammkurven wurden nicht automatisch digitalisiert. Achsenbeschriftungen in der Volltextextraktion sind keine vollständige Datenreihe.
- Niedrigtextseiten und wiederkehrende entfernte Zeilen sind in conversion-report.json protokolliert. Keine automatische OCR behauptet.
- Textdateien sind erheblich kleiner, aber weniger Bilder bedeuten nicht automatisch bessere oder vollständigere Modellinformationen.
