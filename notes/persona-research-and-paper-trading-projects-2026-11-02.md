# Recherche: Personas mit Informationssuche, Gedächtnis und simulierten Konten

Stand: 2. November 2026. Prüfung anhand von Projektdokumentation und ausgewählten Quelldateien. Keine Installation, Ausführung oder Performancevalidierung durchgeführt.

## Trading Floor

[Repository](https://github.com/8ehrad/Trading-Floor).

Im geprüften Code sind die gesuchten technischen Elemente kombiniert: Ein Trader kann einen Recherche-Agenten aufrufen; dessen Werkzeuge umfassen Brave-Websuche, Seitenabruf und eine benannte lokale Gedächtnisdatenbank. Konten starten mit 10.000 simulierten Geldeinheiten. Kauf und Verkauf verändern Kontostand und Bestände; ein Spread ist vorgesehen. Strategien können geändert werden.

Kleiner Prototyp, keine belegte Simulation gewöhnlicher Haushalte. Der Code ist nicht als geprüftes Kontensystem zu behandeln. Dokumentation und Umsetzung der Gedächtnistrennung sind abzugleichen. Aktien und ETFs ersetzen keinen physischen Gold- oder Schmuckhandel.

Primärbelege: [Recherche und Memory](https://github.com/8ehrad/Trading-Floor/blob/master/trading_floor/mcp_params.py), [Konten](https://github.com/8ehrad/Trading-Floor/blob/master/trading_floor/accounts.py), [Trader](https://github.com/8ehrad/Trading-Floor/blob/master/trading_floor/traders.py).

## MarketAgents

[Repository](https://github.com/marketagents-ai/MarketAgents).

Das Framework enthält Persona-Vorlagen mit Anlageerfahrung und Risikoeigenschaften, Kurz- und Langzeitgedächtnis, Webrecherche sowie Bestands- und Marktmodule. Der Aktienmechanismus führt Kauf- und Verkaufsgebote zusammen. Das geht konzeptionell über reine Gesprächssimulation hinaus.

Die Bausteine sind im Code vorhanden; ihre integrierte Einsatzfähigkeit für die konkrete Counterloom-Frage ist noch nicht nachgewiesen. Ein Framework erfordert Konfiguration und gegebenenfalls Anpassungen.

Primärbelege: [Personas](https://github.com/marketagents-ai/MarketAgents/blob/main/market_agents/agents/personas/persona_template.yaml), [Gedächtnis](https://github.com/marketagents-ai/MarketAgents/blob/main/market_agents/memory/memory.py), [Webrecherche](https://github.com/marketagents-ai/MarketAgents/blob/main/market_agents/environments/mechanisms/web_research.py), [Marktmechanismus](https://github.com/marketagents-ai/MarketAgents/blob/main/market_agents/environments/mechanisms/stock_market.py).

## FinMem

[Forschungsimplementierung](https://github.com/pipiku915/FinMem-LLM-StockTrading).

Verbindet Charakterprofil, geschichtetes Gedächtnis und Handelsentscheidungen im historischen Test. Die geprüfte Dokumentation beschreibt vorbereitete Daten und Trainings-/Testphasen. Freie selbstständige Internetsuche und ein vollständiges Haushaltsbudget sind damit nicht belegt. Interessant als Gedächtnismodell; kein gleichwertiger Kompletttreffer.

## TradingAgents

[Repository](https://github.com/TauricResearch/TradingAgents).

Spezialisierte Analysten und gegensätzliche Research-Rollen arbeiten an Handelsentscheidungen. Aktuelle Dokumentation beschreibt persistente Entscheidungsprotokolle und portfoliobezogene Analysen. Der Ansatz bildet ein Anlageteam ab, keine soziale Bevölkerung mit eigenständigen Privatanlegerkonten. Ein Buy/Sell-Signal allein ist kein Nachweis ausgeführter simulierter Transaktionen.

## Einordnung für Counterloom

Die technischen Fähigkeiten sind bereits öffentlich implementiert. Zu unterscheiden sind jedoch: ein Research-Team für ein gemeinsames Portfolio, mehrere autonome Trader mit eigenen Konten und eine Gesellschaftssimulation mit Lebensumständen, sozialer Interaktion und finanziellen Konsequenzen.

Trading Floor ist ein konkreter kleiner Demonstrator der Werkzeugkette. MarketAgents ist der näher liegende Kandidat für eine anpassbare Markt- und Personensimulation. Ob eines davon Erkenntnisse über reale Anleger liefert, ist eine separate Validierungsfrage. Auf Basis dieser Recherche wird noch kein Plattformwechsel oder Implementierungsauftrag ausgelöst.
