# Kuratierte Evidenz: Permissionless Finance 2026–2040

Version 1.0 · Informations-/Abrufstichtag 2026-11-01 · Bestandteil des Research Seeds.

## Lesegrenzen

Beobachtungen über technische Spezifikationen beschreiben deren Regeln, nicht deren wirtschaftlichen Erfolg. Historische Schätzungen bleiben mit Anbieter, Vintage und Abdeckung verbunden. Autorenmeinungen umfassen externe ökonomische Interpretationen, nicht von Counterloom bestätigte Kausalgesetze. Es wurden keine externen Prognosen oder simulierten Befunde als Istwerte übernommen. Volltexte und Browserextraktionen werden nicht öffentlich reproduziert.

## Belegte Ausgangswelt

### PF-F01 · Beobachtung
Die geprüfte Bitcoin-Core-Version halbiert die anfängliche Subvention von 50 BTC alle 210000 Mainnet-Blöcke.

Zeitraum/Stand: Code v28.0. Beleg: PF-S01, PF-S02, GetBlockSubsidy; CMainParams.nSubsidyHalvingInterval.
Grenze: Protokollregel; aktuelle Blockhöhe und gegenwärtige Subvention wurden nicht erhoben.

### PF-F02 · Beobachtung
Die maximal zulässige Coinbase-Auszahlung enthält Transaktionsgebühren plus Subvention.

Zeitraum/Stand: Code v28.0. Beleg: PF-S01, ConnectBlock: blockReward.
Grenze: Regel über Einnahmen, keine Gleichung für Sicherheit oder Minerprofit.

### PF-F03 · Autorenmeinung
Das ökonomische Modell verknüpft Minerwettbewerb und Angriffsanreize mit wiederkehrenden Sicherheitszahlungen.

Zeitraum/Stand: Modell 2018. Beleg: PF-S03, Abstract: two equilibrium conditions.
Grenze: Theoretisches Argument unter Modellannahmen; Abstract geprüft, keine vollständige Replikation.

### PF-F04 · Beobachtung
Ethereum unterscheidet Reorganisationen, widersprüchliche Finalisierung und Finalitätsverzögerungen sowie ökonomische und soziale Gegenwehr.

Zeitraum/Stand: Seitenstand 2026-04-13. Beleg: PF-S04, What do attackers want?; Methods of Attack; Social layer.
Grenze: Stake-Schwellen sind angriffsabhängig; kein einfaches Marktwert/TVL-Verhältnis.

### PF-F05 · Beobachtung
ERC-4337 spezifiziert Account Abstraction über höhere Infrastruktur mit UserOperations, Bundlern und optionalen Paymastern.

Zeitraum/Stand: gelesene Spezifikation 2026-11-01. Beleg: PF-S05, Abstract; Definitions; Extension: paymasters; Security Considerations.
Grenze: Technische Möglichkeit, keine gemessene Massenadoption oder universelle Recovery.

### PF-F06 · Beobachtung
EIP-7702 spezifiziert Code-Delegation für EOAs; Motivation nennt Batching, Sponsoring und eingeschränkte Berechtigungen.

Zeitraum/Stand: gelesene Spezifikation 2026-11-01. Beleg: PF-S06, Abstract; Motivation; Security Considerations.
Grenze: Sichere Delegationsverträge und Initialisierung bleiben notwendig; kein Beleg für jedes Wallet.

### PF-F07 · Beobachtung
EIP-1559 unterscheidet verbrannte Base Fee und Priority Fee.

Zeitraum/Stand: Spezifikation, erstellt 2019. Beleg: PF-S07, Simple Summary; Abstract.
Grenze: Historische Minerterminologie nicht als heutiges vollständiges PoS-Vergütungsmodell lesen.

### PF-F08 · Beobachtung
EIP-4844 führt Blob-Transaktionen und einen gesonderten Blob-Gas-Gebührenmechanismus ein.

Zeitraum/Stand: Spezifikation, erstellt 2022. Beleg: PF-S08, Abstract; Gas accounting.
Grenze: Keine Übernahme historischer Motivations-Gebührenvergleiche als aktuelle Istwerte.

### PF-F09 · Historische Schätzung
Das FBI meldete einen Diebstahl von ungefähr 1.5 Milliarden USD bei Bybit um den 21. Februar 2025.

Zeitraum/Stand: Vorfall um 2025-02-21; Meldung 2025-02-26. Beleg: PF-S09, I-022625-PSA, erster Absatz.
Grenze: Behördliche ungefähre Vorfallsumme und Attribution; keine technische Root-Cause-Prüfung oder Verlustquote.

### PF-F10 · Historische Schätzung
Chainalysis schätzte im Dezember 2024 rund 2.2 Milliarden USD gestohlene Mittel in 303 Hacks im Jahr 2024.

Zeitraum/Stand: 2024, Vintage 2024-12-19. Beleg: PF-S10, Einleitung, zweiter Absatz.
Grenze: Vorläufige Anbieterauswertung; Nenner/Abdeckung unbekannt, keine jährliche Nutzerverlustquote; spätere Revisionen möglich.

### PF-F11 · Autorenmeinung
Die historische Studie findet Vorhersagezusammenhänge von Momentum und Aufmerksamkeitsproxies mit Kryptorenditen.

Zeitraum/Stand: Working Paper 2018. Beleg: PF-S11, Abstract.
Grenze: Kein Nachweis kausaler KI-Verdrängung; genaue Stichprobe/Modellspezifikation hier nicht repliziert.

### PF-F12 · Historische Schätzung
Die gelesene Developer-Report-Tabelle zeigt 25893 aktive Entwickler und 7364 Full-Time-Entwickler.

Zeitraum/Stand: Abruf 2026-11-01; Tabelle ohne eindeutigen Periodenstempel. Beleg: PF-S12, Developer Type table.
Grenze: Keine geprüfte Zeitreihe; öffentliche Repositories, Multi-Chain-Zuordnung und Definitionen begrenzen Vergleichbarkeit. Nicht als kalibrierte aktuelle Baseline verwenden.

### PF-F13 · Autorenmeinung
Die BIS-Studie zu grenzüberschreitenden Flüssen nennt spekulative Motive und globale Finanzierungsbedingungen als wichtige Treiber nativer Kryptoassets.

Zeitraum/Stand: 2017–Mitte 2024; 184 Länder. Beleg: PF-S13, Findings; Abstract.
Grenze: Flussstudie, keine Zerlegung aller BTC-/ETH-Preise; keine kausale 2040-Prognose.

### PF-F14 · Autorenmeinung
Dieselbe Studie findet transaktionale Motive bei Stablecoins und kleinen Bitcoin-Transfers, verbunden mit hohen traditionellen Überweisungskosten.

Zeitraum/Stand: 2017–Mitte 2024; 184 Länder. Beleg: PF-S13, Findings; Abstract.
Grenze: Wichtiger Gegenbefund zu rein spekulativer Nutzung; Länder-/Transaktionszuordnung und Selektion beachten.

### PF-F15 · Autorenmeinung
Die BIS bewertet tokenisierte Zentralbankreserven, Bankgeld und Staatsanleihen als mögliche Grundlage neuer Finanzinfrastruktur und kritisiert Stablecoins anhand eigener Geldkriterien.

Zeitraum/Stand: 2025-06-29. Beleg: PF-S14, Key takeaways; Box C.
Grenze: Institutionelle Position, kein gemessener künftiger Marktanteil oder zwangsläufige Verdrängung.

### PF-F16 · Beobachtung
J.P. Morgan beschreibt Kinexys-Produkte für Zahlungen, Tokenisierung und eine private-permissioned Asset-Plattform.

Zeitraum/Stand: Website beim Abruf 2026-11-01. Beleg: PF-S15, Solutions and Services; Kinexys Digital Assets Platform.
Grenze: Beobachtetes Produktangebot laut Anbieter; keine unabhängigen Skalierungs-/Kostendaten.

### PF-F17 · Historische Schätzung
Circle weist auf der gelesenen Seite 70.0 Milliarden USD USDC-Umlauf und 71.4 Milliarden USD Gesamtreserven zum 29. Oktober 2026 aus.

Zeitraum/Stand: 2026-10-29. Beleg: PF-S16, Reserves composition; Balances.
Grenze: Gerundete Emittentenangabe; verlinkte Attestierungen nicht geprüft. Keine Aussage über Zahlungsvolumen oder Tokenrendite.

### PF-F18 · Beobachtung
MAS beschreibt Guardian als grenzüberschreitenden Sandbox-Verbund für tokenisierte Finanzprodukte, mit Versuchen und ausgewählten Live-Anwendungen.

Zeitraum/Stand: Seite 2025-11-12, Abruf 2026-11-01. Beleg: PF-S17, Einleitung; Objectives; Use Cases.
Grenze: Programmträgerdarstellung; jede Anwendung und deren Zugangsschicht separat prüfen.

### PF-F19 · Beobachtung
Agorá wird als laufendes öffentlich-privates Projekt mit Prototyp für tokenisierte Bankeinlagen und Zentralbankreserven beschrieben.

Zeitraum/Stand: Seitenupdate 2026-05-27. Beleg: PF-S18, Status; project description; prototype paragraph.
Grenze: Prototyp demonstriert technische Möglichkeit laut Projektträger, kein Nachweis breiter Produktion.

### PF-F20 · Beobachtung
NIST SP 800-57 Part 1 Rev. 5 bietet allgemeine Leitlinien zum Management und Schutz kryptografischen Schlüsselmaterials.

Zeitraum/Stand: Version Mai 2020. Beleg: PF-S19, Abstract; Keywords.
Grenze: Normative Empfehlung; keine vergleichende Crypto-/Bankverluststatistik und keine Garantie für konkrete Recovery.

## Quellenregister und Perspektiven

Die JSON-Fassung enthält zusätzlich lokale Archivpfade und Prüfsummen. Fehlende Publikationsdaten sind dort `null`; Abrufdatum ist kein Publikationsdatum.

### PF-S01 · Bitcoin Core
[Bitcoin Core v28.0: validation.cpp](https://github.com/bitcoin/bitcoin/blob/v28.0/src/validation.cpp)

Publikation/Update: v28.0; Release-Datum hier nicht separat geprüft. Abruf: 2026-11-01. Daten-/Gegenstandszeitraum: versionierter Code, kein aktueller Netzzustand.
Geprüfte Belegstelle: GetBlockSubsidy; ConnectBlock: blockReward = nFees + GetBlockSubsidy.
Interesse/Grenze: Implementierungsquelle; keine Garantie wirtschaftlicher Tragfähigkeit.
Aktualisierung: Vor Start prüfen, ob relevante Konsensregeln geändert wurden; v28.0 bleibt historischer Regelbeleg.

### PF-S02 · Bitcoin Core
[Bitcoin Core v28.0: kernel/chainparams.cpp](https://github.com/bitcoin/bitcoin/blob/v28.0/src/kernel/chainparams.cpp)

Publikation/Update: v28.0; Release-Datum hier nicht separat geprüft. Abruf: 2026-11-01. Daten-/Gegenstandszeitraum: Mainnet-Regeln der Version.
Geprüfte Belegstelle: CMainParams: nSubsidyHalvingInterval; nPowTargetSpacing; nPowTargetTimespan.
Interesse/Grenze: Versionierter Regelbeleg, keine Hashrate-/Gebührenmessung.
Aktualisierung: Mit verwendeter Mainnet-Version abgleichen.

### PF-S03 · NBER
[The Economic Limits of Bitcoin and the Blockchain, Working Paper 24717](https://www.nber.org/papers/w24717)

Publikation/Update: 2018-06. Abruf: 2026-11-01. Daten-/Gegenstandszeitraum: theoretisches ökonomisches Modell.
Geprüfte Belegstelle: Landingpage: Abstract, Zero-profit und Incentive-compatibility conditions.
Interesse/Grenze: Forschungsmodell mit Annahmen; keine beobachtete Kollapsprognose.
Aktualisierung: Für quantitative Verwendung Volltext und spätere Literatur zusätzlich prüfen.

### PF-S04 · ethereum.org
[Proof-of-stake attack and defense](https://ethereum.org/developers/docs/consensus-mechanisms/pos/attack-and-defense/)

Publikation/Update: 2026-04-13, angezeigtes Seitenupdate. Abruf: 2026-11-01. Daten-/Gegenstandszeitraum: technische Erklärung; keine reale Angriffswahrscheinlichkeit.
Geprüfte Belegstelle: What do attackers want?; Attacking the protocol; 34%, 51%, 66%; Inactivity leak; Social layer.
Interesse/Grenze: Projektnahe technische Darstellung; Schutzmassnahmen und Restrisiken prüfen.
Aktualisierung: Konsensversion, Schwellen und Client-/Stake-Verteilung vor Start neu prüfen.

### PF-S05 · Ethereum Improvement Proposals
[ERC-4337: Account Abstraction Using Alt Mempool](https://eips.ethereum.org/EIPS/eip-4337)

Publikation/Update: 2021-09-29 erstellt; gelesene Webfassung 2026-11-01. Abruf: 2026-11-01. Daten-/Gegenstandszeitraum: Final laut gelesener Seite; technische Spezifikation.
Geprüfte Belegstelle: Abstract; Motivation; Extension: paymasters; Security Considerations.
Interesse/Grenze: Autoren-/Projektentwurf; Funktionalität nicht als bewiesene Adoption behandeln.
Aktualisierung: Bei konkretem Wallet/EntryPoint dessen Version, Audit und Nutzung nachprüfen.

### PF-S06 · Ethereum Improvement Proposals
[EIP-7702: Set Code for EOAs](https://eips.ethereum.org/EIPS/eip-7702)

Publikation/Update: 2024-05-07 erstellt; gelesene Webfassung 2026-11-01. Abruf: 2026-11-01. Daten-/Gegenstandszeitraum: Final laut gelesener Seite; technische Spezifikation.
Geprüfte Belegstelle: Abstract; Motivation; Security Considerations: secure delegate contracts, initialization, storage.
Interesse/Grenze: Technischer Entwurf; keine Garantie sicherer Implementierungen.
Aktualisierung: Aktivierung und konkrete Wallet-Implementierung vor operativen Aussagen prüfen.

### PF-S07 · Ethereum Improvement Proposals
[EIP-1559: Fee market change for ETH 1.0 chain](https://eips.ethereum.org/EIPS/eip-1559)

Publikation/Update: 2019-04-13 erstellt. Abruf: 2026-11-01. Daten-/Gegenstandszeitraum: historische Spezifikation; frühere Terminologie enthält Miner.
Geprüfte Belegstelle: Simple Summary; Abstract; Specification; Security Considerations.
Interesse/Grenze: Spezifikation erklärt Burn und Gebührenregeln, nicht heutige Validatorgesamtvergütung.
Aktualisierung: Aktuelle Fee-/Issuance-Regeln und Messdaten zusätzlich prüfen.

### PF-S08 · Ethereum Improvement Proposals
[EIP-4844: Shard Blob Transactions](https://eips.ethereum.org/EIPS/eip-4844)

Publikation/Update: 2022-02-25 erstellt. Abruf: 2026-11-01. Daten-/Gegenstandszeitraum: technische Spezifikation; historische Motivationszahlen nicht aktuelle Gebühren.
Geprüfte Belegstelle: Abstract; Gas accounting; Base fee per blob gas update rule.
Interesse/Grenze: Skalierungsentwurf; keine Garantie dauerhafter L1-Wertabschöpfung.
Aktualisierung: Aktuelle Blobparameter und tatsächliche Rollup-/L1-Zahlungen vor Start erheben.

### PF-S09 · FBI / IC3
[North Korea Responsible for $1.5 Billion Bybit Hack, I-022625-PSA](https://www.ic3.gov/PSA/2025/PSA250226)

Publikation/Update: 2025-02-26. Abruf: 2026-11-01. Daten-/Gegenstandszeitraum: Vorfall um 2025-02-21.
Geprüfte Belegstelle: Titel und erster Absatz; behördliche Attribution.
Interesse/Grenze: Behördenmeldung; ungefähre Vorfallsumme, kein allgemeiner Risikonenner.
Aktualisierung: Historischen Vorfall beibehalten; technische Ursache und Endschaden nur mit zusätzlicher Evidenz ergänzen.

### PF-S10 · Chainalysis
[$2.2 Billion Stolen from Crypto Platforms in 2024](https://www.chainalysis.com/blog/crypto-hacking-stolen-funds-2025/)

Publikation/Update: 2024-12-19. Abruf: 2026-11-01. Daten-/Gegenstandszeitraum: 2024, vorläufige damalige Jahresauswertung.
Geprüfte Belegstelle: Einleitung: 2.2 billion, 303 incidents; private key compromises 43.8%.
Interesse/Grenze: Kommerzieller Analyse-/Sicherheitsanbieter; eigene Klassifizierung und unvollständige Abdeckung.
Aktualisierung: Vintage bewahren; Revisionen und 2025/2026 getrennt erheben, keine stillschweigende Fortschreibung.

### PF-S11 · NBER
[Risks and Returns of Cryptocurrency, Working Paper 24877](https://www.nber.org/papers/w24877)

Publikation/Update: 2018-08; Landingpage nennt spätere Publikation 2021. Abruf: 2026-11-01. Daten-/Gegenstandszeitraum: historische Stichprobe; genauer Zeitraum nicht aus Abstract übernommen.
Geprüfte Belegstelle: Abstract: momentum, investor attention proxies.
Interesse/Grenze: Empirische Autoreninterpretation; weder kausaler KI-Effekt noch universelle Prognose.
Aktualisierung: Vor Replikation Volltext, Stichprobe und Modellversion prüfen.

### PF-S12 · Electric Capital / Developer Report
[Crypto developer data](https://www.developerreport.com/)

Publikation/Update: nicht festgestellt. Abruf: 2026-11-01. Daten-/Gegenstandszeitraum: angezeigte Monatsaktivität, Chart bis 2026-10-24; Tabelle ohne eindeutigen Periodenstempel.
Geprüfte Belegstelle: Total monthly active developers; Developer Type table; Crypto Ecosystems link.
Interesse/Grenze: Investor-/Branchenperspektive; öffentliche Repositories, Klassifizierungs- und Mehrfachzählungsrisiko.
Aktualisierung: Datenexport und genaue Periodendefinition vor quantitativer Verwendung sichern.

### PF-S13 · BIS
[DeFiying gravity? An empirical analysis of cross-border Bitcoin, Ether and stablecoin flows, Working Paper 1265](https://www.bis.org/publ/work1265.htm)

Publikation/Update: 2025-05-08. Abruf: 2026-11-01. Daten-/Gegenstandszeitraum: 2017 bis Mitte 2024; 184 Länder laut Contribution.
Geprüfte Belegstelle: Contribution; Findings; Abstract.
Interesse/Grenze: Autorenforschung, nicht notwendig Position der BIS; Geozuordnung/Modellabhängigkeit.
Aktualisierung: Für numerische Nutzung Volltext und bilaterale Datenmethodik prüfen.

### PF-S14 · BIS
[Annual Economic Report 2025, Chapter III: The next-generation monetary and financial system](https://www.bis.org/publications/aer-2025/next-generation-monetary-financial-system)

Publikation/Update: 2025-06-29. Abruf: 2026-11-01. Daten-/Gegenstandszeitraum: institutioneller Entwurf/Analyse 2025.
Geprüfte Belegstelle: Key takeaways; The promise of tokenisation; Box C.
Interesse/Grenze: Zentralbankperspektive; Bewertung von Stablecoins und tokenisiertem Bank-/Zentralbankgeld.
Aktualisierung: Als datierte Position verwenden; kein heutiger Marktanteil.

### PF-S15 · J.P. Morgan
[Kinexys: Solutions and Services](https://www.jpmorgan.com/kinexys/index)

Publikation/Update: nicht festgestellt. Abruf: 2026-11-01. Daten-/Gegenstandszeitraum: Produktdarstellung beim Abruf.
Geprüfte Belegstelle: Solutions and Services; Kinexys Digital Assets Platform: private-permissioned.
Interesse/Grenze: Anbieterwerbung; keine unabhängige Kosten-/Sicherheitsmessung.
Aktualisierung: Produktstatus und echte Produktionsdaten vor Start prüfen.

### PF-S16 · Circle
[Transparency & stability](https://www.circle.com/transparency)

Publikation/Update: nicht festgestellt. Abruf: 2026-11-01. Daten-/Gegenstandszeitraum: Reservezusammensetzung as of 2026-10-29.
Geprüfte Belegstelle: Reserves composition; Balances; Monthly assurance and transparency.
Interesse/Grenze: Emittentendarstellung; gelesene Seite ersetzt keine Prüfung der verlinkten Attestierungen.
Aktualisierung: Vor Start datierte Bestände und tatsächliche Attestierung prüfen; keine Zahlungsvolumen ableiten.

### PF-S17 · Monetary Authority of Singapore
[GUARDIAN](https://www.mas.gov.sg/schemes-and-initiatives/project-guardian)

Publikation/Update: 2025-11-12 laut Seite. Abruf: 2026-11-01. Daten-/Gegenstandszeitraum: Sandbox/Industrieversuche und beschriebene Live-Anwendungen.
Geprüfte Belegstelle: Einleitung; Objectives; Use Cases.
Interesse/Grenze: Programmverantwortliche Aufsicht; eigene Erfolgsdarstellung.
Aktualisierung: Je Anwendungsfall Netzwerk, Zulassung und reale Produktion gesondert prüfen.

### PF-S18 · BIS Innovation Hub
[Project Agorá](https://www.bis.org/project/agora)

Publikation/Update: 2026-05-27, letztes Seitenupdate. Abruf: 2026-11-01. Daten-/Gegenstandszeitraum: laufendes Projekt und Prototyp.
Geprüfte Belegstelle: Status; introductory project description; prototype paragraph.
Interesse/Grenze: Projektträgerdarstellung; Prototyp nicht gleich Produktivsystem.
Aktualisierung: Projekt-/Produktivstatus vor tatsächlichem Start erneut prüfen.

### PF-S19 · NIST
[Recommendation for Key Management: Part 1 – General, SP 800-57 Part 1 Rev. 5](https://csrc.nist.gov/pubs/sp/800/57/pt1/r5/final)

Publikation/Update: 2020-05. Abruf: 2026-11-01. Daten-/Gegenstandszeitraum: versionierte allgemeine Schlüsselmanagementempfehlung.
Geprüfte Belegstelle: Abstract; Keywords: backup, compromise, key recovery, split knowledge.
Interesse/Grenze: Normative technische Empfehlung; keine vergleichende Verluststudie.
Aktualisierung: Neue Revision bei Implementierungsentscheidungen prüfen; historischen Beleg erhalten.

## Quellenkonflikte und nicht geschlossene Evidenzlücken

- PF-S11 und PF-S13 untersuchen andere Zeiträume, Variablen und Methoden. Ältere Aussagen zu Renditefaktoren und spätere Flussbefunde dürfen nicht unbemerkt zusammengeführt werden. Beide Volltexte müssten für eine kausale Replikation zusätzlich geprüft werden.
- PF-S13 enthält ausdrücklich transaktionale Nutzung kleiner BTC-Transfers; eine Behauptung ausschliesslich spekulativer Nachfrage würde diesen Gegenbefund unterschlagen.
- PF-S03 begründet ein theoretisches Sicherheitsproblem; der Regelcode PF-S01/S02 liefert keine empirische Antwort auf seine langfristige Tragfähigkeit.
- PF-S05/S06 dokumentieren konkrete Gegenmechanismen zur UX-Skepsis und zugleich Sicherheitsanforderungen. Sie liefern keine nach Nutzersegment harmonisierten Abschluss-/Verlustquoten.
- Die institutionelle Perspektive PF-S14 und Anbieter-/Projektangaben PF-S15/S17/S18 ersetzen keinen direkten Vergleich offener, privater, hybrider und konventioneller Produktion.
- PF-S09 und PF-S10 haben unterschiedliche Zeiträume und Abdeckungen. Vorfallbetrag und jährliche Branchenschätzung weder addieren noch als Verlustquote vergleichen.
- Für eine kausale Abwanderung von Crypto zu KI fehlt hier ein unabhängiger Datensatz. Entwicklerzählungen und Medienaufmerksamkeit sind getrennte Proxies.
- Aktuelle Kursrekorde, ein behaupteter grosser Binance-Vorfall Ende Oktober 2026 und weitere nicht identifizierte Studien wurden nicht als Fakten übernommen. Suchtreffer oder Communityposts auf einer Anbieterdomain sind keine bestätigte Unternehmensmeldung. Das Fehlen eines geprüften Belegs ist seinerseits kein Beweis, dass ein Ereignis nicht stattgefunden hat.
- Keine umfassende Aktualitätsprüfung aller 2026er Marktereignisse; Stichtag bedeutet Informationsgrenze, keine lückenlose Ereignischronik.

## Daten und Reproduktion

Keine vollständigen Marktzeitreihen, PDF-Reproduktionen oder empirischen Regressionsresultate gehören zu diesem Paket. [Messgrössen](metrics.csv) definieren die nächste Datenerhebung. [Berechnungen](derived-calculations.json) enthalten nur reproduzierbare Regel-/Szenariobeispiele. [Validierungsplan](validation-plan.md) trennt inhaltliche Vorbereitung, Importnachweis, technische Ausführung und externe empirische Validierung.
