# Research Seed: The Future of Permissionless Finance: 2026–2040

Version: **1.0** · Laufkennung: **002-permissionless-finance** · Sprache: Deutsch.
Informationsstichtag: **2026-11-01, Europe/Zurich**. Untersuchungszeitraum: Restjahr 2026 bis Ende 2040.
Regionen: global, mit getrennten Perspektiven für USA, Europa/Schweiz und Länder mit teuren Zahlungswegen oder eingeschränktem Finanzzugang. Nominale USD sind die Referenz für Geldbeträge; keine realen Renditen ohne Deflator.
Arbeitsstandard: [SIMULATION_TEMPLATE.md](SIMULATION_TEMPLATE.md), Version 1.0.
Vorgängerlauf-IDs: keine. Vorbereitung, kein simulierter Befund.

## Forschungsfrage und untersuchte Grössen

Unter welchen Bedingungen bleiben offene, permissionless Finanznetzwerke bis 2040 sicher und wirtschaftlich relevant, unter welchen verlieren sie Bedeutung, und wie verteilen sich Nutzen, Risiken und Wertabschöpfung zwischen Nutzern, Netzwerken, Tokenhaltern und Intermediären?

Ein zentraler Belastungstest lautet: Was geschieht, wenn spekulative Attraktivität schneller abnimmt, als dauerhaft bezahlte Nutzung wächst? Gleichrangiger Gegentest: Kann sinkende Spekulation bei besserer Sicherheit und UX eine tragfähigere Nutzung ermöglichen? Kein Akteur, Netzwerk oder Geschäftsmodell ist als Sieger vorgegeben.

Vier Ergebnisachsen getrennt beurteilen:

1. **Nutzung und Nutzen:** wiederkehrende Zahlungen, Abwicklung, offener Zugang, Portabilität, Kosten und funktionierende Alternativen.
2. **Sicherheit und Resilienz:** Konsens, Verwahrung, Anwendung, wirtschaftliche Anreize, Konzentration, Wiederherstellung und Haftung.
3. **Wirtschaftliche Tragfähigkeit:** bezahlte Nachfrage, Betriebskosten, Abhängigkeit von Subventionen und Fähigkeit zur Anpassung.
4. **Tokenwert und Wertabschöpfung:** Nachfrage nach BTC/ETH, Gebühren, Burn, Staking, Emittenten- und Intermediärerträge. Nutzungserfolg impliziert weder steigende Tokenpreise noch zwingend deren Stagnation.

Kursrekorde sind kein Erfolgsziel. Es werden keine persönlichen Anlageentscheidungen, Zielpreise oder realen Eintrittswahrscheinlichkeiten erzeugt. Edelmetalle, deren Nachfrage und Portfoliovergleiche gehören nicht zum Modell.

## Begriffe und Grenzen

**Permissionless** bezeichnet den Zugang zur Basisschicht ohne individuelle Betreiberzulassung. Frontends, Stablecoins, Brücken, L2-Sequencer und tokenisierte Rechtsansprüche können trotzdem Zulassungen, Sperren oder zentrale Kontrollrechte besitzen. **Permissioned** bezeichnet zugelassene Teilnehmer/Validatoren; das garantiert weder Fehlerfreiheit noch universelle Wiederherstellung. **Hybrid** umfasst öffentliche Abwicklung mit kontrollierten Produkten sowie Verbindungen zwischen privaten und öffentlichen Netzen. Architektur pro Schicht erfassen, keine binäre Einordnung der ganzen Finanzwelt erzwingen.

**Adoption** misst wiederkehrende, wirtschaftlich sinnvolle Verwendung. Adresszahl, Transaktionszahl, Bruttovolumen, TVL und Tokenpreis sind jeweils nur Teilindikatoren. TVL ist ein Bestandsproxy, keine frei entwendbare Summe und kein Zahlungsfluss. Bridged und native Stablecoins sowie mehrfach verwendete Sicherheiten nicht doppelt zählen. Verwahrung durch Intermediäre und Selbstverwahrung getrennt beobachten.

**Sicherheit** ist bedrohungsabhängig: Ausfall der Finalisierung, Reorganisation, Zensur, Custody-Diebstahl, Smart-Contract-/Oracle-/Bridge-Exploit, Phishing, verlorener Schlüssel, wirtschaftliche Insolvenz und Depeg sind verschiedene Ereignisse. Ein Börsendiebstahl beweist keinen Konsensbruch; ein stabiler Konsens beweist keine sichere Nutzererfahrung. Eine valide unerwünschte Überweisung ist kein Bruch der Signaturkryptografie.

## Quellenregister und belegte Ausgangswelt

Der [Evidence Pack](evidence-pack.md) mit Quellen PF-S01 bis PF-S19 und Fakten PF-F01 bis PF-F20 ist Bestandteil dieses Seeds. Maschinenlesbare Fassungen: [Quellen](source-register.json), [Fakten](fact-register.json). Jede empirische Anfangsaussage muss auf diese IDs zurückführen. Technische Spezifikationen sind Belege für Regeln und Möglichkeiten; deren Wirtschaftserfolg bleibt offen.

- Bitcoin-Code dokumentiert Subventionshalbierungen nach Blockhöhe und die Summe aus Subvention und Gebühren als maximale Blockvergütung (PF-F01/F02). Ein hohes übertragenes Geldvolumen erzeugt nicht automatisch hohe Gebühren.
- Ein ökonomisches Forschungsmodell begründet Grenzen kontinuierlicher PoW-Sicherheitsfinanzierung unter seinen Annahmen (PF-F03). Es beweist keinen zwangsläufigen Kollaps oder eine konkrete Gebührenuntergrenze.
- Ethereum beschreibt unterschiedliche Konsensangriffe, Slashing, Inactivity Leak und soziale Gegenwehr (PF-F04). Ein bestimmter ETH-Kurs ist kein vollständiges Angriffsmodell.
- ERC-4337 und EIP-7702 dokumentieren Möglichkeiten für Smart Accounts, Sponsoring, Bündelung und begrenzte Berechtigungen sowie neue Sicherheitsanforderungen (PF-F05/F06). Sie belegen keine bereits gelöste Massen-UX.
- Gebührenverbrennung und Blob-Datenmärkte verändern die Wertabschöpfung (PF-F07/F08). Eine L2-Nutzergebühr ist nicht insgesamt L1-Sicherheitsbudget.
- Der belegte Bybit-Vorfall und eine datierte Branchenauswertung zeigen erhebliche Verwahrungs-/Ökosystemrisiken, keine allgemeine jährliche Verlustwahrscheinlichkeit (PF-F09/F10).
- Studien zu Aufmerksamkeit und grenzüberschreitenden Flüssen begründen konkurrierende Nachfragemotive, aber keine kausale KI-Verdrängung (PF-F11/F13/F14).
- Kinexys, Guardian und Agorá liefern konkrete institutionelle Vergleichsfälle; Produktangebot, Versuch, Prototyp und behaupteter Nutzen getrennt lesen (PF-F16/F18/F19).
- Emittentenreserven und Tokenbestände sind weder Zahlungsvolumen noch ein Renditeanspruch auf BTC/ETH (PF-F17). Allgemeine Schlüsselmanagementverfahren gelten auch ausserhalb offener Netze (PF-F20).

Zeitkritische Zustandswerte werden vor dem Start aktualisiert oder als historische Vintage verwendet. Aktuelle BTC-/ETH-Preise, Hashrate, Gebührenniveau, Stake-Verteilung, Stablecoin-Zahlungsanteile und reale UX-Quoten sind hier nicht numerisch kalibriert.

## Acht Hypothesen und gleichrangige Gegenhypothesen

Alle H-/G-Aussagen sind **Szenarioannahmen bzw. zu prüfende Mechanismen**, keine Tatsachen. IDs behalten ihre ursprüngliche Reihenfolge. Schwellen unten sind qualitative Entscheidungskriterien. Für eine spätere numerische Prüfung sind Effektgrösse, Zeitraum und Kontrollvariablen vorab festzulegen; ein einzelnes Ereignis entscheidet keine langfristige Hypothese.

### H1: Aufmerksamkeit, Entwickler und Kapital wandern zur KI ab

**H1:** KI und andere Technologien binden knappe Entwicklerzeit, Risikokapital und Nutzeraufmerksamkeit; offene Finanznetze verlieren dadurch Innovation und Nachfrage schneller, als neue Anwendungen entstehen.
**G1:** Aufmerksamkeit kann zyklisch sein; etablierte Teams bleiben produktiv. KI senkt Entwicklungs-/Sicherheitskosten oder schafft Nachfrage nach programmierbaren Zahlungen. Sinkender Medienanteil ist mit wachsendem Nutzen vereinbar.

Belegrahmen: PF-F11/F12; keine Quelle hier identifiziert bereits eine kausale Abwanderung zu KI. Mechanismus: Aufmerksamkeitsanteil → Finanzierung/Neueintritte → Wartung/Produktfortschritt → Nutzerbindung, mit Monaten bis Jahren Verzögerung. Gemeinsame Treiber wie Zinsen und Risikobereitschaft kontrollieren. KI-Unternehmen und Crypto können dieselben Personen beschäftigen; Commitzahlen sind keine Arbeitsstunden.

Prüfen: M01/M02/M03/M04. H1 wird geschwächt, wenn erfahrene Teams, bezahlte Nutzung und Nutzerbindung trotz sinkender öffentlicher Aufmerksamkeit stabil bleiben/steigen. G1 wird geschwächt, wenn vermeintliche KI-Zahlungen nur Bots, interne Transfers oder Subventionen sind. Entkopplung zwischen Medienhype und funktionierendem Geschäft ausdrücklich zulassen.

### H2: Bitcoin benötigt dauerhaft spekulative Kurssteigerungserwartungen

**H2:** Sinkende Renditeerwartungen reduzieren Halte- und Kaufnachfrage so stark, dass Bitcoin wirtschaftlich an Bedeutung verliert.
**G2:** Nachfrage nach offener Übertragbarkeit, zensurresistenter Abwicklung, knapper monetärer Reserve oder Portfoliooption besteht auch ohne dauerhaft steigende reale Preise. Eine kleine, zahlungsbereite Nische kann tragfähig sein.

PF-F13/F14 enthalten sowohl spekulative als auch transaktionale Motive. Nicht aus fehlenden Dividenden auf fehlenden monetären Nutzen schliessen. Narrative, Liquidität, Hebel und Nutzung unterscheiden; ETF-/Börsenbestände können Nachfrage bündeln, ohne Zahlungsadoption zu messen. Keine lineare Nachfragekurve aus Kursgeschichte erfinden.

Prüfen: M03/M04/M05/M06, insbesondere Nutzung/Haltebereitschaft bei stagnierenden Erwartungen gegenüber einer Kontrollvariante. H2 wird durch wiederkehrende freiwillige Nachfrage ohne Renditeversprechen geschwächt; G2 durch Abwanderung selbst der funktionalen Nutzer bei vergleichbaren Alternativen. Beobachtete Korrelation von Kurs und Aktivität identifiziert keine Richtung.

### H3: Sinkende Bitcoin-Subvention untergräbt die Sicherheit

**H3:** Wiederkehrende Gebühren reichen bei stabilen/fallenden Preisen nicht für eine robuste Minerlandschaft; Konzentration und Reorganisations-/Zensurrisiken wachsen.
**G3:** Knapper Blockraum, spezialisierte Settlement-Nachfrage, Kostensenkungen und flexible Difficulty können einen tragfähigen Gebührenmarkt ermöglichen. Niedrigere Hashrate muss nicht dieselbe Änderung realer Angriffsmöglichkeiten bedeuten.

PF-F01/F02/F03; Bezugsgrösse ist nicht das Transfervolumen, sondern Nachfrage nach Blockraum und deren Zahlungsbereitschaft. Lightning, Batching und andere L2 können L1-Gebühren verdrängen oder zusätzliche Settlement-Nachfrage erzeugen. Poolanteile nicht automatisch als Eigentum an Hashleistung lesen. Difficulty stabilisiert das Blockintervall, ersetzt aber keine verlorene ökonomische Abschreckung. ASIC-Verfügbarkeit, Energie, Finanzierung, Standortpolitik und Angreiferziele wirken mit.

Prüfen: M07/M08/M09/M10/M11. H3 wird geschwächt, wenn Gebühren und Kostenanpassung über mehrere Belastungsphasen verteilte Sicherheitsbereitstellung tragen. G3 wird geschwächt, wenn Erträge nur kurzzeitige Spitzen oder externe Subventionen sind. Hohes Gebührenaufkommen bei dauerhaft ausgeschlossenen Kleinbeträgen ist ein Zielkonflikt, kein ungeteilter Erfolg. Ein 51%-Angriff erlaubt keine beliebigen fremden Signaturen oder freie Ausgabe neuer Coins.

### H4: Ethereum-Nutzung ohne starken ETH-Wert gefährdet PoS

**H4:** Wert und Nutzungsabhängigkeit externer Vermögenswerte wachsen schneller als die verfügbare kryptökonomische Absicherung. Ein ETH-Preisrückgang begünstigt bestimmte Angriffe oder Konzentration.
**G4:** Effektiver Stake, Slashing, Aktivierungs-/Austrittsbedingungen, Angreiferliquidität, technische Diversität und soziale Wiederherstellung halten Angriffe auch bei stagnierendem Tokenpreis unattraktiv. Nutzung kann mittelbar zusätzliche ETH-Nachfrage und langfristige Sicherheit erzeugen.

PF-F04/F07/F08. ETH-Marktkapitalisierung ist weder beschaffbarer Stake noch Angriffsbudget. Der marktbewertete Stake ist nur ein Proxy; Preiswirkung beim Erwerb, Kontrollrechte bei Pools/Custodians, entziehbare Sicherheiten, Hebel, Bestechung, Slashing-Verluste und Gegenwehr getrennt behandeln. Mehr als ein Drittel kann in bestimmten Modellen Finalisierung behindern; daraus folgt keine beliebige Entwendung sämtlicher Stablecoins. Finalitätsstörung, widersprüchliche Finalisierung und Anwendungsexploit sind getrennte Bedrohungen.

Prüfen: M12/M13/M14/M15 und M20. H4 wird geschwächt, wenn trotz niedrigerem Stake-Marktwert Angriffe praktisch blockiert und Dienste resilient bleiben. G4 wird geschwächt, wenn Konzentration/Clients gemeinsames Fehlverhalten ermöglichen oder soziale Gegenwehr Nutzeransprüche beschädigt. Tokeninflation kann Validatoren finanzieren und zugleich Halter verwässern; Burn ist keine direkte Validatorzahlung.

### H5: Hacks, Schlüsselverlust und Endgültigkeit verhindern breite Adoption

**H5:** Erwartete und wahrgenommene Verluste, irreversible Fehlbedienung und fehlende Haftung überwiegen den Nutzen für viele Nutzer und Institutionen.
**G5:** Unterschiedliche Nutzer akzeptieren unterschiedliche Risiken. Sichere Verwahrung, Multisig/MPC, Limits, Versicherung und Recovery können Schäden senken; traditionelle Alternativen haben ebenfalls Angriffe, Ausschluss und Gegenparteirisiken.

PF-F09/F10/F20. Nach Angriffsschicht, Bruttoverlust, Rückgewinnung, Entschädigung, Assetpreis zum Vorfallzeitpunkt und Nutzungsbasis aufteilen. Rekordverluste in USD beweisen keine steigende individuelle Verlustquote; sinkende Summen beweisen ohne Nenner keine Verbesserung. Schlüsselverlust und Diebstahl sind getrennt, nicht gemeldete Verluste bleiben unbekannt. Fehlende Bankvergleichsdaten verbieten eine Überlegenheitsrangliste.

Prüfen: M16/M17/M18/M19 sowie Wechsel/Retention M04. H5 wird geschwächt durch robuste Wiederkehr nach Vorfällen bei transparenten Kosten und real funktionierender Recovery. G5 wird geschwächt durch anhaltende Nettoschäden, unversicherbare Risiken oder zentrale Recovery-Ausfälle. Zufälligen Verlust, Betrug und staatlichen Angreifer mit verschiedenen Zielen simulieren.

### H6: UX-Verbesserungen und Smart Wallets kommen zu spät

**H6:** Komplexität, Schlüsselverwaltung, Gas, Bridges und schwer verständliche Freigaben lassen Nutzer vor tragfähiger Verbesserung dauerhaft abwandern.
**G6:** Smart Accounts, Passkeys, gesponserte Transaktionen, verständliche Simulation vor Signatur und begrenzte Berechtigungen senken Hürden ausreichend schnell. Nutzer müssen die Infrastruktur nicht bewusst wahrnehmen.

PF-F05/F06, ergänzt PF-F20. ERC-4337 ist Account Abstraction auf höherer Infrastrukturebene; daraus keine bereits vorhandene native Protokolllösung behaupten. EIP-7702 erlaubt Delegation, garantiert aber weder sichere Recovery noch vertrauensfreie Bedienung. Passkeys, Recovery, Guardians, Session Keys, Sperrfristen und Versicherung sind Implementierungs-/Governanceentscheidungen mit eigenen Angriffsflächen.

Prüfen: M18/M19/M04/M10. Erfolg heisst Aufgabenabschluss, geringe Fehlerrate, kontrollierbare Wiederherstellung und Bindung ohne dauerhafte Zuschüsse. H6 wird geschwächt durch gemessene Verbesserung im gleichen Nutzersegment vor dessen Abwanderung; G6 durch versteckte Custody, Phishing/Delegationsschäden oder Paymaster-/Guardian-Ausfall. Wartefristen verbessern möglicherweise Schutz, können aber Liquidität und Sofortzahlungen beeinträchtigen.

### H7: Permissioned Netze verdrängen öffentliche Finanznetze

**H7:** Banken/Börsen bevorzugen Zugangskontrolle, Datenschutz, Rechtsklarheit und vertragliche Haftung; offene Infrastruktur verliert wesentliche institutionelle Anwendungen.
**G7:** Offene Erreichbarkeit, globale Liquidität, Komponierbarkeit und geringere Abhängigkeit von einzelnen Konsortien bleiben wertvoll. Institutionen nutzen öffentliche und private Schichten nebeneinander oder verbinden sie.

PF-F15/F16/F18/F19. Kinexys ist ein konkreter Anbieter, Agorá ein Projekt/Prototyp und Guardian ein Verbund von Versuchen/Anwendungen; nicht deren Ankündigungen zu flächendeckender Verdrängung hochrechnen. Kontrollierte Bankprodukte auf öffentlicher Basisschicht sind Gegenbeispiele zur einfachen Dichotomie. Auch keine DLT und modernisierte konventionelle Systeme als Handlungsoption zulassen.

Prüfen: M20/M21/M22/M23. H7 wird geschwächt durch bezahlte Produktion auf offenen Basisschichten, G7 durch geringe Endnutzung, Compliance-/Datenschutzkosten oder schlechtere Interoperabilität. Institutionelle Teilnahme beweist keine Dezentralität; öffentliche Basisschicht garantiert keinen offenen Zugang zum Wertpapier.

### H8: Stablecoins und Tokenisierung wachsen ohne BTC-/ETH-Wertsteigerung

**H8:** Nutzen und Einnahmen fallen überwiegend bei Nutzern, Emittenten, Verwahrern, L2-Betreibern oder Institutionen an; Basistoken erfassen davon wenig.
**G8:** Settlement-, Gas-, Sicherheiten- und Staking-Nachfrage sowie Gebührenverbrennung koppeln einen Teil des Nutzens an native Token. Steigende Nutzung kann auch bei kleinen Stückgebühren die Gesamtnachfrage erhöhen.

PF-F07/F08/F13/F14/F17. Stablecoinbestand ≠ Zahlungsvolumen; Tokenisierungsnennwert ≠ Liquidität oder zusätzlicher Wohlstand. Emittentenreservezins ≠ ETH-Protokollertrag. Sponsoring verbirgt die Gaszahlung für den Endnutzer, hebt sie nicht zwingend auf. Wachstum auf anderen Basisschichten darf nicht ETH zugeschrieben werden; BTC und ETH nicht als identische Wertabschöpfungsmodelle behandeln.

Prüfen: M03/M06/M07/M12/M20/M21/M24. H8 wird geschwächt durch nachvollziehbare dauerhafte native Nachfrage aus zusätzlicher Nutzung; G8 durch überwiegend offchain anfallende Gewinne, Preisrückgänge trotz Nutzung oder Migration auf alternative Daten-/Settlement-Schichten. Ein gemeinsamer Preisanstieg unter expansiver Liquidität belegt diesen Mechanismus noch nicht.

## Akteure und unterschiedliche Interessen

Kanonische IDs und Aliase stehen in [entities.json](entities.json). Die folgenden Rollen sind ausdrücklich **repräsentative Modellakteure**, keine unterstellten Positionen realer Personen oder Organisationen. Reale Entitäten dienen als belegte Infrastruktur-/Quellenanker; ihre Ziele werden nicht erfunden.

| Modellakteur | Ziel/Interesse | Informationen und Entscheidungen | Ressourcen/Beschränkungen |
|---|---|---|---|
| PF-A01: Kleinanwender Europa/Schweiz | günstiger, verständlicher und wiederherstellbarer Zugang | sichtbare Gebühren/Verlustgeschichten; Wallet-/Anbieterwahl, Abbruch, Rückkehr | geringe Zeit, begrenzte technische Kenntnisse; gute konventionelle Alternativen |
| PF-A02: Nutzer mit teuren Überweisungen/eingeschränktem Zugang | erreichbare Zahlung und verlässliche Kaufkraft | lokale Wechsel-/Auszahlungskosten; Stablecoin, Bank oder Bargeldkanal wählen | On-/Offramp, Netzversorgung, Identität, lokale Beschränkungen |
| PF-A03: BTC-Halter ohne Renditeziel | übertragbare unabhängige Reserve | Sicherheit/Verfügbarkeit; halten, selbst verwahren oder wechseln | trägt Volatilität/Verwahrungsrisiko; keine garantiert unelastische Nachfrage |
| PF-A04: Trader/Allocator | erwartete risikobereinigte Rendite | Preise, Narrative, Liquidität; BTC/ETH/KI/andere Geschäfte gewichten | Finanzierung, Risiko-/Liquiditätslimits; Erwartungen können irren |
| PF-A05: unabhängiger Miner | kostendeckender Betrieb | Gebühren, Erlös, Energie/ASIC-Preise; investieren, abschalten, Pool wechseln | Kapital, Hardware, Energieverträge, Jurisdiktion |
| PF-A06: Poolbetreiber | verlässliche Blockproduktion und Ertrag | Mitglieds-Hashrate, Blockauswahl; Konditionen, Transaktionsaufnahme | Mitglieder können wechseln; Pool ist nicht Eigentümer aller Hardware |
| PF-A07: Validator/Stakinganbieter | Ertrag bei akzeptablem Slashingrisiko | Stake, Clients, Erträge; Eintritt/Austritt, Client-/Anbieterwahl | technische Betreuung, Kapital, Kontroll- und Ausstiegsregeln |
| PF-A08: Protokoll-/Walletentwickler | Sicherheit, offene Nutzung oder kommerzieller Erfolg | Audits, Nutzerstudien, Budgets; Features, Wartung, Branchenwechsel | begrenzte Zeit, Haftung, Governance; Teams nicht homogen |
| PF-A09: Händler/Remittanceanbieter | wiederkehrende zuverlässige Zahlungen | Gebühren, Support, Ausfallrisiko; akzeptieren, routen, ersetzen | Kundenreichweite, On-/Offramp, Compliance |
| PF-A10: Börse/Custodian | Ertrag, Verfügbarkeit, Haftungsbegrenzung | Angriffe, Kundenabflüsse; Kontrollen, Recovery, Entschädigung | operative Konzentration, Kapital, Versicherung |
| PF-A11: Stablecoinemittent | liquide Rücknahme und rentables Angebot | Reserven, Rückgaben, Netzabhängigkeit; emittieren, einlösen, Netze wählen | Bankpartner, Liquidität, rechtliche Eingriffsbefugnisse |
| PF-A12: Bank/Börsenkonsortium | rechtssichere kostengünstige Abwicklung | Piloten, Integrationskosten; private/öffentliche/hybride/konventionelle Architektur | Datenschutz, Mitgliedschaft, Legacy-Systeme und Koordinationsprobleme |
| PF-A13: Aufsicht/Zentralbankrolle | Stabilität, Rechtsdurchsetzung, Zugang | Meldungen und unvollständige Daten; Auflagen, Standards, Experimente | Mandat/Jurisdiktion; Ziele können konkurrieren |
| PF-A14: Angreiferrolle | Diebstahl, Störung oder strategische Sabotage | technische und operative Schwächen; Ziel/Abbruch wählen | Kapital, Zugriff, Entdeckungs-/Verfolgungsrisiko; keine Exploit-Anleitung |
| PF-A15: KI-Unternehmen/Softwarezahler | Automatisierung bei beherrschbaren Kosten | APIs, Limits, Rücknahme; offene oder konventionelle Zahlungsschiene wählen | Finanzierung, Reputation, eigene Kontrollsysteme |
| PF-A16: L2-/Bridgebetreiber | günstige Nutzung und tragfähige Erlöse | Daten-/Settlementkosten; Gebühren, Schichtwahl, Kontrollrechte ändern | Fragmentierung, Exit-/Upgradebedingungen und Liquidität |

Nutzersegmente nicht nach identischen Präferenzen entscheiden lassen. Wohlhabende und kleine Nutzer, neue und erfahrene Entwickler sowie zugangsorientierte und haftungsorientierte Institutionen getrennt erhalten. Weder Institutionen noch Entwickler haben vollständige Information über künftige Adoption.

## Beziehungen und Rückkopplungen

[relationships.json](relationships.json) enthält gerichtete Kanten mit Subjekt-/Objekt-IDs, Herkunft, Zeitbezug und Gegenwirkung. Belegte Beziehungen (etwa Circle → USDC und J.P. Morgan → Kinexys) sind getrennt von angenommenen Verhaltensbeziehungen (etwa Gebühren → Minerinvestition).

| Mechanismus | Mögliche Verstärkung | Gegenwirkung / Verzögerung / Unsicherheit |
|---|---|---|
| D1: Nachfrage und PoW | weniger BTC-Nachfrage → geringerer Erlös → Minerexit → Konzentration → Vertrauensverlust | Kosten-/Difficultyanpassung, neue Settlementnachfrage; Markt reagiert schnell, Hardware über Monate/Jahre; kein deterministischer Kollaps |
| D2: ETH und Sicherheit | geringerer Stakewert bei wachsender Abhängigkeit → grösserer Anreiz für bestimmte Störungen → Abwanderung | Slashing, Beschaffungsengpässe, Clientdiversität, soziale Gegenwehr; keine Gleichung TVL/Marketcap = Angriffsrisiko |
| D3: Walletlernen | bessere Freigaben/Recovery → weniger Schäden → Vertrauen → Bindung → Wartungsbudget | Delegations-/Guardianfehler und Sponsoringkosten können Nutzen aufheben; Lernen über mehrere Kohorten |
| D4: institutionelle Skalierung | Standards/Haftung → mehr Teilnehmer → Liquidität → geringere Stückkosten | Konsortiumsgrenzen, Fragmentierung, Datenschutz; offene Schienen können komplementär sein; Integration dauert Jahre |
| D5: KI-Konkurrenz/Komplement | weniger Entwicklerfinanzierung → langsamere Produktverbesserung | KI kann Audits/Entwicklung und neue Zahlungen fördern; gemeinsame Liquiditätstreiber; Richtung empirisch offen |
| D6: L2-Wertabschöpfung | günstigere Transaktionen → mehr Nutzung, aber weniger Erlös je Transaktion für L1 | Gesamtnachfrage nach Daten/Settlement kann steigen; Alternativschichten, MEV und Betreibergewinne beachten |
| D7: Schock und Gegenwehr | Hack → Vertrauensverlust → Abflüsse → Liquiditätsstress | Rückgewinnung, Entschädigung, bessere Kontrollen oder Anbieterwechsel; Gegenwehr kann offene Nutzung beschränken |

Interessen können quer zur technischen Architektur liegen: Ein Emittent kann öffentliche Verbreitung und zentrale Sperrrechte zugleich bevorzugen. Ein Nutzer kann Unabhängigkeit wünschen und delegierte Recovery wählen. Diese Spannungen nicht durch simulierten Konsens glätten.

## Datenreihen, Messgrössen und eigene Berechnungen

[metrics.csv](metrics.csv) definiert M01–M24 mit Einheit, Frequenz, Nenner, gewünschter Quelle und Grenzen. Es ist ein **Erhebungsplan**, kein ausgefüllter Zeitreihendatensatz. Fehlende Baselines bleiben `null`; keine fehlende Zahl mit Null oder frei erfundenem Durchschnitt ersetzen. PF-F12 ist eine zeitpunktbezogene Anbieteranzeige, keine heruntergeladene Monatsreihe. Es liegen keine Kursregressionen oder kausal identifizierten KI-Effekte vor.

Nachvollziehbare Rechenbeispiele stehen in [derived-calculations.json](derived-calculations.json), erzeugt ausserhalb des Sprachmodells mit [dem Prüfsystem](../../../tools/validate_permissionless_seed.py). Sie sind **eigene Berechnungen aus Protokollregeln/Szenarioannahmen**, keine Prognosen:

- Subvention aus ganzzahliger Satoshi-Halbierung: `subsidy_sats = 5_000_000_000 >> floor(height/210_000)`, für Höhen ab 64 Intervallen Null. Kalenderdaten sind dabei nicht vorgegeben.
- Erlös über ein Intervall: `R_USD = Summe_b((subsidy_BTC,b + fee_BTC,b) × BTCUSD_b)`. Identität vor Kosten, keine Sicherheits- oder Preisfunktion.
- Gebührenanteil: `F/(F+S)` auf derselben Zeit-/Währungsbasis. Er kann auch allein wegen sinkender Subvention steigen; das ist kein Beweis hinreichender Einnahmen.
- Stake-Marktwertproxy: `effective_stake_ETH × ETHUSD`. Kein direkt käuflicher Angriffspreis und kein Vergleich mit dem gesamten TVL als Beutewert.
- Verlustquote: nur bei identischer Abdeckung `Nettoverlust_USD / durchschnittlicher_exponierter_Bestand_USD` oder pro Nutzerjahr; Quellen mit anderem Nenner getrennt führen. Ein Transferfluss ist kein Bestandsnenner.

Kein fester Preis-, Hashrate-, Adoptions- oder Angriffsalgorithmus ist implementiert. Die folgenden Entscheidungen werden im ersten Lauf **diskutiert und narrativ begründet**, nicht als Markträumung, Konsensprotokoll oder Vertragsausführung numerisch simuliert.

## Szenarien und Vergleichsvarianten

Alle Szenarien sind **Szenarioannahmen ohne Wahrscheinlichkeiten**. [scenarios.csv](scenarios.csv) enthält Ausgangsstand, Beginn, Dauer, veränderte Bedingungen und Gegenreaktionen. Beobachtete historische Schäden zählen zur Ausgangswelt, nicht erneut als zukünftiger Schock.

| ID | Rahmen | Beginn und Dauer | Konkurrierende Anpassung |
|---|---|---|---|
| S0 | offene Referenz, keine zusätzliche langfristige Siegerannahme | Restjahr 2026–2040 | alle Akteure wählen unter Unsicherheit; Ausgangsdaten bleiben lückenhaft |
| S1 | Bedeutungsverlust: schwächere spekulative Nachfrage, langsame UX-Fortschritte | graduell 2027–2032; danach Reaktionen bis 2040 | Kostensenkung, Nischennutzung, offene Zahlungsvorteile und Rückkehr zulassen |
| S2 | Koexistenz: segmentierte Nachfrage, mehrere interoperable Architekturen | 2027–2040 | private Fragmentierung und öffentliche Konzentration können Koexistenz verändern |
| S3 | Durchbruch: überprüfbar bessere Wallets und zuverlässige günstige Abwicklung | Einführung 2027–2030, Beobachtung bis 2040 | neue Angriffspunkte, Zentralisierung, keine automatische native Wertsteigerung |
| S4a/S4b | gleiche Gebührennachfrage, unterschiedliche Miner-Kostenanpassung | an den blockhöhenabhängigen Halbierungen bis 2040 | gleiche Preisannahme, nur Anpassungsfähigkeit variieren |
| S5a/S5b | wachsender externer Nutzen bei schwachem ETH-Wert; unterschiedliche Kontrolle/Abwehr | 2028–2032, Nachwirkungen bis 2040 | gleiche Nutzungs-/Preisannahme, nur Stake-/Clientkontrolle und Reaktion ändern |
| S6a/S6b | gleicher hypothetischer Custody-Schock, unterschiedliche Recovery/Entschädigung | einmal 2028, Reaktion 2028–2031 | Verlusthöhe offen; keine Behauptung eines realen künftigen Vorfalls |
| S7a/S7b | KI absorbiert Ressourcen / KI schafft komplementäre Zahlungs- und Entwicklungsnachfrage | 2027–2035; Langfristfolgen bis 2040 | gemeinsamen Finanzierungsrahmen konstant halten; Narrativ allein genügt nicht |
| S8a/S8b | institutionelle Einigung auf kontrollierte Plattform / offene hybride Integration | 2027–2034; Bindung bis 2040 | gleiche Regulierung und Endnachfrage; Architektur-/Interoperabilitätskosten variieren |

S1–S3 sind breite Bündel, daher keine Einzeleffektidentifikation. Die Paare S4–S8 ändern jeweils eine benannte Mechanismengruppe, halten übrige Annahmen möglichst konstant und dokumentieren verbleibende Unterschiede. Belastungen durch stabile Preise auch ohne Negativschock prüfen. Zusätzliche Varianten: geringe/hohe Blockraumelastizität; schnelle/langsame Walletumsetzung; starke/schwache institutionelle Interoperabilität. Für jede Veränderung Gegenvariante und Entscheidungsspur erhalten. Ein bisher unbekannter technologischer Durchbruch darf als neue, separat gekennzeichnete Annahme auftreten, nicht als historische Tatsache.

## Tatsächliche Simulation und Zeitzuordnung

Vorgesehener Typ: qualitative MiroFish-Szenarioerkundung mit heterogenen Rollen. Modellversion, Graphschema, Agentenzahl, Plattformen, Interviewfunktion, Runden, Temperatur und Zufallssteuerung sind **unbekannt** und bleiben in [run.json](../run.json) offen. Keine MiroFish-API oder Engine wurde hier getestet.

Zeit ist eine **narrative Szenarioachse**, keine behauptete Engine-Uhr: Ausgangspunkt Restjahr 2026; kurz 2027–2030; mittel 2031–2035; lang 2036–2040. Jede Aktion benötigt eine begründete Vorlauf-/Wirkungszeit. Diskussionsrunde ≠ Kalenderjahr. Falls MiroFish eine solche Zuordnung nicht unterstützt, lediglich spätere Auswertung nach diesen Horizonten; keine scheinbaren Jahresmessungen aus Runden ableiten. Bitcoin-Halbierungen nach Blockhöhe behandeln, ungefähre Vierjahresabstände nicht als feste Kalendertermine ausgeben.

Die Rollen entscheiden qualitativ über Anbieter-/Walletwahl, Halten/Abwandern, Investieren/Abschalten, Produkt-/Wartungsbudgets, Architekturwahl und Risikokontrollen. Kursbildung, Sicherheitswahrscheinlichkeiten, automatische Smart-Wallet-Transaktionen und makroökonomische Gleichgewichte werden nicht als tatsächlich implementiert behauptet. Für eine quantitative Erweiterung sind eigenständige Gleichungen, Daten, Bilanzgrenzen, Kalibrierung und unabhängige Tests erforderlich.

## Übernommene Ausgänge früherer Läufe

Keine. [prior-run-findings.json](prior-run-findings.json) enthält eine leere Liste mit Begründung. Die andere Untersuchung im Repository liefert keine Inputs dieses Themas. Es wurden keine Simulationsmehrheiten, unbelegten Prognosen oder unbestätigten Nachrichten als externe Evidenz übernommen. Die acht Prüfthesen bilden eine Forschungsagenda, keinen Quellenersatz.

## Erwartete Exporte und Auswertung

Erwartet werden, soweit verfügbar: tatsächlich importierte Dokumente/Graph, Rollen-/Agentenkontexte, Prompt, Konfiguration, Modell-/Versionsnachweis, Rohaktionen mit Runde/Zeit, Interviews, Bericht, Logs und tatsächlicher Abschluss-/Abbruchstatus. Fehlende Exportarten und technische Grenzen offen dokumentieren. Anfangsbeiträge, autonome Aktionen und Berichtinterpretation getrennt auswerten.

Für H1–H8 jeweils liefern: stützender Wirkungsweg, stärkster Gegenweg, Akteursentscheidungen, benötigte/fehlende Messgrössen, tatsächliche Belegstellen, Bedingungen des Scheiterns und Urteil `gestützt unter Annahmen` / `geschwächt unter Annahmen` / `gemischt` / `nicht unterscheidbar`. Diese Urteile betreffen die Simulation; keine empirische Hypothesenbestätigung behaupten. Schweigen eines Agenten ist keine Zustimmung, Wiederholung keine neue Evidenz.

[validation-plan.md](validation-plan.md) definiert Import-, Prozess-, Sensitivitäts- und externe Validierung. [analysis/evaluation.md](../analysis/evaluation.md) bewahrt auch Minderheitspositionen und fehlgeschlagene Mechanismen. Eine neue Erkenntnis muss über das Nachsprechen des Seeds hinausgehen und mit einer nachvollziehbaren Entscheidungskette belegt werden.

## Unsicherheiten, Lücken und nächste Evidenz

1. **Messung:** Nutzer/Adressen, Zahlungsvolumen/Handel, offene Basisschicht/kontrolliertes Produkt, Brutto-/Nettoschaden und nominelle/reale Werte sind nicht austauschbar.
2. **Kausalität:** Aufmerksamkeit, Preis, Liquidität und Entwickleraktivität beeinflussen einander. Zwei historische Studien mit anderer Stichprobe sind keine direkte Replikation und kein universelles Gesetz bis 2040.
3. **Sicherheitsmodelle:** Angreifer können Profit, Sabotage oder politische Ziele haben. Beschaffung/Koordination und Betreiberkonzentration sind unvollständig beobachtbar.
4. **Datenlücken:** keine harmonisierte Bank-/Crypto-Verlustquote, keine repräsentative Schlüsselverlust-/Recoveryreihe, keine bereinigte KI-Abwanderungsreihe, kein überprüftes globales Tokenisierungs-Produktionsvolumen.
5. **Quelleninteressen:** Protokollprojekte wollen Nutzung fördern; Anbieter verkaufen Produkte/Analysen; Zentralbankperspektiven priorisieren Stabilität und regulierte Geldformen. Keine Perspektive allein entscheidet H1–H8.
6. **Horizont:** technische und regulatorische Änderungen bis 2040 sind nicht vollständig antizipierbar. Roadmaps sind keine gelieferten Fähigkeiten, Pilotvolumen keine dauerhafte Nachfrage.
7. **Modell:** LLM-Rollen können sich angleichen, Vorgaben wiederholen und plausibel klingende Zahlen erfinden. Kontrafaktische Diskussion ersetzt keine empirische Identifikation.

Priorität vor einer quantitativen Auswertung: Block-/Gebühren- und Stakereihen mit Stichtag beschaffen, Wallet-Kohortenstudien prüfen, Verluste nach Schicht/Exposition normalisieren und institutionelle Produktion anhand unabhängiger Volumen-/Kostenbelege von Ankündigungen trennen. Regulatorische Rechtslage je Jurisdiktion vor entsprechenden Entscheidungen gesondert recherchieren; dieses Paket enthält keine aktuelle Rechtsberatung oder vollständige Gesetzesmatrix.
