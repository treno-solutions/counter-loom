# Validierungsplan

Version 1.0 · 2026-11-01 · Plan, noch keine Modellvalidierung.

## 1. Paket und Quellen vor dem Import

- `python3 tools/validate_permissionless_seed.py` im Repository ausführen. Prüft Datenformate, IDs/Verweise, Hypothesen-/Metrik-/Szenarioabdeckung, relative Dokumentlinks, ausgewählte private Muster, Rechenbeispiele und Eingabeprüfsummen. Ein bestandener Paketcheck bestätigt weder Quellenwahrheit noch Simulationsqualität.
- Quelle und Behauptung in `fact-register.json` anhand der angegebenen HTML-Abschnitte bzw. Codefunktionen stichprobenweise abgleichen. Hier geprüft: Bitcoin-Vergütungs-/Halbierungsregel, Ethereum-Angriffsarten, Smart-Account-Möglichkeiten und Grenzen, Gebühren/Burn/Blobs, Vorfallsummen/Vintages und institutioneller Projektstatus. Die beiden Studienabstracts ersetzen keine Volltextreplikation.
- Alle zeitkritischen Zustände vor einem tatsächlichen Lauf aktualisieren oder explizit die historische Vintage verwenden. Rechtslage, konkrete Walletfähigkeit und Produktionsstatus nicht aus allgemeinen Projektseiten ableiten.
- Für quantitative Schlussfolgerungen zuerst harmonisierte Zeitreihen und Nenner beschaffen. Datendatei, Version, Zeitstempel, Einheit, Definition, Transformation und SHA-256 sichern; Test-/Kalibrierungsperioden vorab trennen. Überlappende Quellen auf gemeinsamen Ursprung prüfen.
- Öffentliches Paket enthält eigene Synthesen und Verweise. Vor Veröffentlichung neuer Originale Rechte separat prüfen; Roharchive bleiben ausgeschlossen. Kein Chatprotokoll ist erforderlich.

## 2. Nach Import: dokumentierte Akzeptanzprüfung

Je Punkt Graph-/Kontext-/Dokumentbeleg mit Exportpfad und Fundstelle in `start-check.md` erfassen:

| Prüfgegenstand | Akzeptanzkriterium |
|---|---|
| PF-F01/F02 | 210000 Blöcke, Subvention plus Gebühren; kein fester Kalendertermin, Transfervolumen nicht als Gebühr verstanden |
| PF-F04 und H4 | Finalitätsstörung von Diebstahl getrennt; kein Marketcap/TVL-Angriffsmodell |
| PF-F05/F06 und H6 | Smart-Wallet-Gegenmechanismus vorhanden; sichere Implementierung nicht vorausgesetzt |
| PF-F09/F10 | Bybit-Vorfall 2025 und vorläufige 2024er Schätzung getrennt, kein Konsensbruch unterstellt |
| PF-F13/F14 | sowohl spekulative als auch transaktionale Nachfrage übernommen |
| PF-F16/F18/F19 | Anbieterprodukt, Sandbox/Live-Anwendungen und Prototyp nicht gleichgesetzt |
| H1–H8/G1–G8 | keine Hypothese oder Gegenhypothese fehlt oder wurde als Fakt importiert |
| Akteure/Beziehungen | Nutzer, Miner, Validatoren, Walletentwickler, Institutionen, Emittent und KI-Rolle vertreten; reale Namen/IDs korrekt, Modellpräferenzen als Annahmen |
| Datenlücken | fehlende Baselines bleiben unbekannt; keine erfundene aktuelle Kurs-/Schadensreihe |

Fehlt Wesentliches, Inputs/Import korrigieren und neue prüfbare Fassung erstellen oder den Lauf auf einen ausdrücklich begrenzten Funktionstest herabstufen. Kein Status `import_checked` allein wegen erfolgreichem Upload.

## 3. Ausführung und Prozessgüte

Tatsächliche MiroFish-Projekt-/Laufkennung, Software-/Modellversion, Agentenzahl/-mischung, Plattformen, Temperatur, Zufallssteuerung, geplante/abgeschlossene Runden, Limits und Abschluss-/Abbruchstatus sichern, soweit verfügbar. Nicht verfügbare Parameter bleiben `null` mit Begründung.

Der erste Lauf ist eine Diskussion/Entscheidungserkundung. Für jeden Kernausgang mindestens eine konkrete Entscheidung mit Gegenreaktion und Exportbeleg verlangen; ein von der Berichtskomponente formulierter Satz ohne Rohaktionsbeleg ist nur Berichtinterpretation. Informationsverwendung mit konkreten Fakten-/Beziehungs-IDs nachweisen. Importierter Text allein ist kein Verwendungsnachweis. Initialisierung, autonome Beiträge, Interviews und spätere Zusammenfassung getrennt prüfen.

Warnzeichen: alle Akteure übernehmen dieselbe Meinung, Zahlen ohne Quellen entstehen, reale Organisationen erhalten erfundene Eigenschaften, das Thema kehrt zu Kurszielen zurück, oder Monate/Jahre werden aus Runden abgelesen. Solche Befunde als Modellfehler erhalten und Aussageumfang reduzieren.

## 4. Neutralität und Robustheit

- S0 sowie S1–S3 mit gleicher Ausgangsevidenz/vergleichbarer Akteursmischung untersuchen. Unterschiede zwischen diesen Bündeln erlauben keine Einzeleffektzuordnung.
- S4–S8 als separate Paare ausführen, wenn technisch möglich. Preis-/Nachfrageannahmen, Rollen, Informationszugang und Rechenregeln einfrieren; die jeweils veränderte Mechanismengruppe und verbleibende Unterschiede protokollieren.
- Reihenfolge und Framing der skeptischen/optimistischen Hypothesen variieren; starke Gegenpositionen erhalten. Verändert blosses Framing das Ergebnis, als Sensitivität berichten.
- Wenn unterstützt: drei oder mehr Wiederholungen mit verschiedenen dokumentierten Zufallsseeds; sonst drei dokumentierte Neuinitialisierungen mit unbekannter Zufallssteuerung. Das ist eine Planungsannahme, keine statistisch begründete Stichprobengrösse. Kein signifikanter Effekt oder reale Wahrscheinlichkeit aus drei Diskussionen ableiten.
- Akteursmischung variieren: erfahrene Nutzer gegen Neueinsteiger, unabhängige gegen gebündelte Sicherheitsanbieter, Regionen mit guten gegen teure/zugangsbeschränkte Zahlungssysteme. Keine rein skeptische oder rein werbende Gruppe als alleinigen Hauptlauf behandeln.
- Ablationen: Mechanismus KI-Konkurrenz aus-/einschalten; Recovery verfügbar/nicht verfügbar; institutionelle Interoperabilität hoch/niedrig. Bei mehreren gleichzeitigen Änderungen keine eindeutige Ursache behaupten.

## 5. Externe empirische Prüfung

Für H1–H8 vor einer empirischen Prüfung Messdefinition, Vergleichsgruppe, Zeitraum, relevante Effektgrösse und Umgang mit fehlenden Daten festlegen. Die qualitative Erkundung dient der Hypothesenerzeugung; sie ersetzt diese Registrierung nicht.

| Hypothesen | Mögliche externe Prüfung | Zentrale Störfaktoren |
|---|---|---|
| H1/H2 | Entwickler-/Nutzerkohorten und Finanzierung mit Aufmerksamkeit, Erwartungen und bezahlter Nutzung verbinden; KI-Wechsel über nachvollziehbare Tätigkeitsdaten prüfen | Zinsen, Marktzyklus, Multi-Chain-/Mehrfachbeschäftigung, Survivorship, umgekehrte Kausalität |
| H3 | historische Halbierungen mit Gebühren, Kostenschätzungen und Konzentration untersuchen; Erlös-/Kostenstress ausserhalb des Sprachmodells berechnen | Preis, Hardwareeffizienz, Energieverträge, Poolanteil statt Eigentum, kurze Gebührenspitzen |
| H4 | effektiven Stake, Kontrolldomänen, Clients, Ausstiegsregeln und Finalitätsereignisse nach Version erfassen | geringe Ereigniszahl, nicht beobachtbare Bestechung/Kontrolle, TVL-Doppelzählung |
| H5/H6 | vergleichbare Nutzeraufgaben/Kohorten, Verlustmeldungen und Recoveryfälle mit Bank-/Custodyalternativen untersuchen | Selbstselektion, Dunkelziffer, verschiedene Risikoexposition, Entschädigung, Preiseffekt |
| H7/H8 | bezahlte institutionelle Produktion, bereinigte Zahlungen und Wertabschöpfung pro Schicht verfolgen | Pilotankündigungen, Wash-/Botvolumen, doppelte Sicherheiten, private Daten und Rechtsansprüche |

Historische Plausibilitätskontrollen: 2024er Bitcoin-Halbierung, Umstellung auf Ethereum-PoS, Einführung neuer Gebühren-/Walletfunktionen und 2025er Bybit-Vorfall nur mit zusätzlich datierten Quelldaten rekonstruieren. Kein echter Backtest dieses Pakets behaupten: Mit Daten bis 2026 sind frühere Ereignisse bereits bekannt. Für einen belastbaren Hindcast separate Informationsstände vor dem Ereignis einfrieren, Kalibrierung und Prüfung trennen und gegen einfache Baselines vergleichen. Danach prospektiv beobachten; spätere Daten dürfen archivierte Anfangseingaben nicht überschreiben.

## 6. Ergebnisurteile und Weitergabe

Je Hypothese: simulationsinternes Urteil, Entscheidungskette, stärkste Gegenposition, Exportbelege, verwendete externe Fakten, Sensitivität und offene Daten. Ergebnisse nach Nutzersegment und vier Achsen des Seeds aufteilen. Keine Gesamtpunktzahl, die Sicherheits-/Zugangs-/Renditekonflikte versteckt.

Neue Mechanismen müssen benannt und von wiederholten Ausgangsbehauptungen unterschieden werden. Fehlgeschlagene Szenarien, uneinige Rollen und verworfene Anpassungen mit übergeben. Nur tatsächlich ausgeführte Läufe mit bestätigten Inputprüfsummen als Herkunft nennen. Folgelauf erhält neue ID, unveränderte Roharchive und separat klassifizierte neue Evidenz.
