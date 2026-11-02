# The Future of Permissionless Finance: 2026–2040

Version **1.0** · Recherche-/Informationsstichtag **2026-11-01**, Europe/Zurich · Counterloom / Treno Solutions.

**Status: `prepared_for_import` für eine qualitative Szenarioerkundung; noch nicht importiert oder ausgeführt.** Das Paket ist keine empirisch kalibrierte Markt-, Sicherheits- oder Preisprognose. Laufkennung `002-permissionless-finance` bezeichnet die Ablage, keine bereits bestehende MiroFish-Simulation.

## Einstieg und Upload

1. [Research Seed](inputs/research-seed.md) und [kuratierte Evidenz](inputs/evidence-pack.md) als Forschungsdokumente hochladen. Der Seed enthält das Untersuchungsdesign, die Evidenzdatei die belegte Ausgangswelt und Quellenzuordnung.
2. [Simulationsprompt](inputs/prompt.md) separat in das Aufgabenfeld übernehmen.
3. [Startprüfung](inputs/start-check.md) und [Validierungsplan](inputs/validation-plan.md) beachten. Die technischen Fähigkeiten der eingesetzten MiroFish-Version sind noch offen. Ein Markdown-Upload, Graphimport, numerisches Zustandsmodell oder bestimmtes Exportformat wird hier nicht als unterstützt behauptet.
4. Die JSON-/CSV-Dateien sind ergänzende Forschungsdaten für Importprüfung und Auswertung. Ihre Übernahme gesondert bestätigen; sie werden durch das Vorhandensein im Ordner nicht automatisch verwendet.
5. Vor dem tatsächlichen Start Eingabestand einfrieren, Prüfsummen kontrollieren und tatsächlich verwendete Dateien/Parameter in [run.json](run.json) nachtragen. Danach Änderungen in einer neuen Laufablage vorbereiten.

## Inhalt

- [Quellenregister](inputs/source-register.json): Originaladressen, Fundstellen, Quelleninteressen, Datenstände, lokale Abrufnachweise und Aktualisierungsbedarf.
- [Faktenregister](inputs/fact-register.json): Beobachtungen, historische Schätzungen und externe Interpretationen getrennt.
- [Entitäten](inputs/entities.json), [gerichtete Beziehungen](inputs/relationships.json).
- [Messgrössen](inputs/metrics.csv), [Szenariomatrix](inputs/scenarios.csv).
- [Vorgängerübergabe](inputs/prior-run-findings.md): keine übernommenen Simulationsbefunde.
- [Eingabemanifest](inputs/input-manifest.json): vorbereitete Dateien mit SHA-256; kein Uploadnachweis.
- [Auswertung](analysis/evaluation.md), [erwartete Exporte](exports/README.md).
- Verwendeter Arbeitsstandard: [SIMULATION_TEMPLATE.md, Version 1.0](inputs/SIMULATION_TEMPLATE.md).

Die unveränderte Kopie des zentralen Arbeitsstandards behält dessen Verweisbasis im Repository-Stamm. Für die Navigation im Standard kann die [zentrale Fassung](../../SIMULATION_TEMPLATE.md) verwendet werden.

Die Untersuchung umfasst Bitcoin, Ethereum, weitere offene Netze als Konkurrenz, Wallets, Nutzer, Finanzinstitutionen, Stablecoins und Tokenisierung. Sie enthält keine Edelmetallperspektive. Die acht Hypothesen sind ergebnisoffen; Bedeutungsverlust, Koexistenz, Durchbruch und neue Entwicklungen sind zulässige Ausgänge.

## Evidenzgrenzen

Die Webquellen wurden am Stichtag im Browser geprüft. Die dokumentierte Prüfung bezieht sich auf benannte HTML-Abschnitte bzw. versionierten Programmcode, nicht auf eine vollständige Begutachtung aller verlinkten Studien/PDFs. Vollständige Browserextraktionen liegen nur im ausgeschlossenen lokalen `raw/`-Archiv. Öffentlich enthält dieses Paket eigene Zusammenfassungen und strukturierte Verweise, keine vollständigen Fremdberichte oder Chatprotokolle. Aktuelle Marktzeitreihen, repräsentative UX-/Schlüsselverlustdaten und eine vergleichbare Verlustquote traditioneller Systeme fehlen. Fehlwerte bleiben `null`.

Änderungsstand 1.0: erste eigenständige Vorbereitung; keine Ergebnisse und keine Schlussfolgerung zugunsten einer Hypothese.
