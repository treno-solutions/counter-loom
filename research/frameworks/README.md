# Marktübersicht und Prüfstand

Stand: 2. November 2026. Die Tabelle unterscheidet dokumentierte Fähigkeiten von eigenen Tests. Keine Rangliste und keine bereits getroffene Auswahl.

| Projekt | Eigener Prüfstand | Einordnung für unseren Zweck | Nächster möglicher Schritt |
|---|---|---|---|
| [MiroFish](mirofish.md) | Erster Methodenversuch und Bericht ausgewertet; Originalartefakte nur teilweise vorhanden | `unsuitable_for_current_goal` in getesteter Konfiguration | Kein weiterer großer Lauf; nur bei gezieltem Nachweis geschlossener Lücken neu betrachten |
| [TinyTroupe](tinytroupe.md) | `documentation_reviewed`; fünf isolierte Quellcode-Grenzprüfungen, kein Persona-Pilot | `conditional`; Probleme im Netzwerkpfad | Getrennte Gruppenräume oder begrenzte Anpassung prüfen |
| [Concordia](concordia.md) | `pilot_tested`; 140 ausgewählte Upstream-Tests, drei Forum-Prüfungen und ein kleiner Personenvergleich | `conditional`; technische Machbarkeit, geringer inhaltlicher Mehrwert | [Versuch 004 auswerten](../../runs/004-concordia-group-influence/analysis/evaluation.md); keine Vergrößerung ohne zusätzlichen Nutzen |
| [AgentSociety](https://github.com/tsinghua-fib-lab/AgentSociety) | `documentation_reviewed`; kein eigener Pilot | `unassessed`; Version 1 und 2 auseinanderhalten | Passende Version und erforderliche Komponenten bestimmen |
| [OASIS](https://github.com/camel-ai/oasis) | Paper/Projekt recherchiert; kein isolierter eigener Test | `unassessed`; Basissystem unter MiroFish, kein unabhängiger Erfolgsnachweis | Nur als eigene technische Basis bewerten, falls dafür begründeter Bedarf besteht |

## Bereits recherchiert, aber anderer Schwerpunkt

[MarketAgents, Trading Floor, FinMem und TradingAgents](../../notes/persona-research-and-paper-trading-projects-2026-11-02.md) wurden wegen Recherche, Gedächtnis und simuliertem Handel betrachtet. Ausgeführte Käufe sind für den präzisierten Workshop-Zweck nicht erforderlich. Diese Projekte bleiben Vergleichsmaterial, keine priorisierte Auswahl für eine Bevölkerungssimulation.

## Bewertungsregeln

Vor weiteren Praxisprüfungen gelten [Anforderungen](../requirements.md), [Prüfprotokoll](../assessment-protocol.md) und [Bewertungsvorlage](_template.md). Eigene Messergebnisse, Betreiberangaben und Drittberichte bleiben getrennt. Projektlizenzen und Versionsstände beim konkreten Einsatz erneut prüfen.

## Erste vertiefte Gegenüberstellung

Am 2. November 2026 wurden TinyTroupe und Concordia an festen Quellständen untersucht. [Technische Befunde](evidence/boundary-checks-2026-11-02.json) und [Concordia-Tests](evidence/concordia-upstream-tests-2026-11-02.json) sind archiviert. Keine Sprachmodellaufrufe, keine autonomen Persona-Gespräche und kein Nachweis von Meinungsänderung wurden dabei ausgeführt.

Der technische Prüfumfang ist nicht gleich: Concordia wurde installiert und mit ausgewählten Originaltests ausgeführt; TinyTroupe nur mit isolierten Methoden und Testdoubles. Die Testzahlen sind deshalb keine vergleichbaren Qualitätsscores.
