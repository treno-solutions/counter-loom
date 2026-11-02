# Auswertung · TinyTroupe-Gruppenvergleich

2. November 2026 · Eigene qualitative Auswertung simulierter Aussagen. Keine realen Anlegerbeobachtungen.

## Ergebnis

Der korrigierte Versuch ist technisch vollständig: vier fiktive Personen, zwei getrennte Gruppen, gespeicherte Ausgangs- und Endzustände, vier tatsächliche Gesprächszustellungen und vier unabhängige direkte Vergleichsantworten. Im Gruppengespräch beziehen sich Nora, Derya, Alva und Sam auf erhaltene Aussagen. Eine deutliche Änderung ihrer Handlungsabsichten ist nicht erkennbar. Der zusätzliche Lernstoff gegenüber einem einfachen direkten Persona-Prompt bleibt gering.

TinyTroupe löst damit ein wichtiges Problem des ersten MiroFish-Versuchs: individuelle Verläufe und Kontakte sind zugänglich. Zugängliche Belege sind aber noch keine Erklärung realer sozialer Reaktionen. Technische Nachvollziehbarkeit und fachlicher Erkenntnisgewinn bleiben getrennt.

Alle T-IDs beziehen sich auf [die Antworten des korrigierten Versuchs](../exports/attempt-02/responses.json). Für die Bewertung der gesprochenen Aussagen wurde jeweils die `TALK`-Aktion betrachtet; `THINK`, `DONE` und der kognitive Zustand wurden nicht als zusätzliche Gesprächsbeiträge gezählt. Die modellierten Emotionen sind Textfelder, keine validierte Angstskala.

## Einzelvergleich

| Person | Ausgangspunkt | A ohne Austausch | B mit Austausch | Direkter Prompt ohne Framework |
|---|---|---|---|---|
| Nora | Sorge um laufende Ausgaben, liquide bleiben, kein Kauf; T001 | Gleich, Gold als unbrauchbar bezeichnet; T005 | Spricht Deryas Schmucksorge an, eigene Absicht gleich; T013 | Ebenfalls Liquidität, Unsicherheit und kein Kauf; T017 |
| Derya | Schmuck als Notreserve, Gold positiv, abwarten; T002 | Gleiche Ausrichtung; T006 | Notfallverwertung nochmals betont, kein Neukauf; T014 | Schmuckverwertung prüfen statt neu kaufen; T018 |
| Alva | Unabhängigkeit, keine schnellen Entscheidungen; T003 | Abwarten, keine Impulskäufe; T007 | Stimmt Sam bei fehlenden harten Daten zu, keine Impulskäufe; T015 | Ähnliche Vorsicht, ergänzt jedoch ein bestehendes Goldportfolio und vorsichtige Diversifikation; T019 |
| Sam | Gold als kleiner Portfoliobaustein, Sparplan beibehalten; T004 | Gleich; T008 | Gleich; T016 | Gold noch positiver als Inflationsanker beschrieben, ebenfalls keine impulsive Umschichtung; T020 |

Die Vergleichsantworten sind nicht wortgleich. Bei Alva enthält der direkte Prompt eine zusätzliche Absicht zur Diversifikation; bei Sam unterscheidet sich die positive Gewichtung von Gold. Solche Unterschiede können auch ohne soziale Kontakte entstehen. Sie sind keine unabhängigen ökonomischen Erkenntnisse.

## Gesprächsbelege

Die [Zustellungen](../exports/attempt-02/deliveries.json) wurden anhand tatsächlich veränderter Erinnerungszustände erfasst. Es gab genau diese vier Verbindungen:

- Nora → Derya: T009; Derya nimmt in T010 auf Noras Fixkostenfokus Bezug.
- Derya → Nora: T010; Nora spricht Deryas Sorge in T013 ausdrücklich an.
- Alva → Sam: T011; Sam greift in T012 Alvas Angstargument auf.
- Sam → Alva: T012; Alva stimmt Sam in T015 bei fehlenden harten Daten zu.

Keine Zustellung über Gruppengrenzen. Die grundlegenden Themen waren überwiegend bereits im Profil, der Nachricht oder den Ausgangsantworten vorhanden. Diese Belege zeigen aufgenommene Beiträge und Bestätigung, keinen isolierten kausalen Meinungswechsel. Bedingung B umfasst zusätzliche Beschäftigung und eine eigene Äußerung; es fehlt eine gleich lange Selbstreflexionskontrolle. Eine feste Reihenfolge und nur eine Wiederholung begrenzen die Aussage zusätzlich.

## Datenqualität und Vergleich mit Lauf 004

Unbelegte Biografieergänzungen bleiben ein Problem. Nora hat laut Eingabe unregelmäßige Arbeitszeiten; T001 und T005 machen daraus unregelmäßiges Einkommen. Derya hat wenig Depot-Erfahrung; T002 macht daraus, dass sie kein Depot habe. Im direkten Vergleich T019 wird aus Alvas erster Goldanlage-Erfahrung ein bestehendes Goldportfolio. T020 ergänzt bei Sam ein bestehendes Mischportfolio. Diese Aussagen dürfen nicht als gesicherte Fakten in spätere Seeds übernommen werden.

Im Concordia-Lauf wurde Sam in E007/E015/E031 deutlich goldskeptischer dargestellt. TinyTroupe und der direkte Prompt beschreiben ihn dagegen positiv bis moderat gegenüber Gold. Das Ausgangsprofil legt eine solche konkrete Goldposition nicht fest. Der Unterschied entsteht bereits vor einem Gruppeneffekt und ist ein Hinweis auf Modell-/Promptabhängigkeit, nicht auf einen gesellschaftlichen Trend. Frameworks, Gruppengrößen und instruktionale Kontexte unterscheiden sich; keine methodisch saubere Rangfolge aus diesen Läufen ableiten.

Die Fallauswahl enthält viele vorsichtige Ausgangshaltungen, die Nachricht betont Prognoseunsicherheit. Die gemeinsame Modellroute kann die ähnliche Grundrichtung weiter begünstigen. Acht oder vier Personas aus demselben Modell sind keine unabhängigen menschlichen Sichtweisen.

## Gemessener Aufwand

| Phase des erfolgreichen Versuchs | Anfragen | Eingabetokens | Ausgabetokens | Gesamttokens |
|---|---:|---:|---:|---:|
| TinyTroupe-Ausgangsbefragung | 4 | 23.238 | 2.049 | 25.287 |
| A: Schlussbefragung ohne Austausch | 4 | 25.973 | 1.980 | 27.953 |
| B: Gespräch und Schlussbefragung | 8 | 54.662 | 3.627 | 58.289 |
| Direkte Persona-Prompts | 4 | 1.531 | 705 | 2.236 |
| Gesamt | 20 | 105.404 | 8.361 | 113.765 |

Servergemeldete Tokens, keine gemessenen Geld- oder Stromkosten. Laufzeit des erfolgreichen Versuchs: 118,8 Sekunden, ohne Installation und Imports. Die Ausgangsbefragung mit Framework benötigt hier etwa 11,3-mal so viele Gesamttokens wie die vier direkten Antworten. Das misst diese konkrete Konfiguration einschließlich Systemprompt, THINK und Zustands-JSON; es ist kein allgemeiner Effizienzbenchmark gegen andere Frameworks.

Zusätzlich: 17 begonnene Anfragen im abgebrochenen Aufbau, davon für 16 zusammen 100.619 Tokens gemeldet. Der Verbrauch einer unterbrochenen Anfrage bleibt unbekannt. Über beide Versuche 37 begonnene Anfragen und mindestens 214.384 gemeldete Tokens. Offline-Testantworten sind dabei nicht mitgezählt und nicht als Persona-Befunde archiviert.

## Abbruch und Grenzen des Aufbaus

Der erste Aufbau forderte nur eine Einzelaktion an, während TinyTroupes vorhandener Systemprompt THINK vor TALK verlangt. Dadurch waren manche Anfangsantworten lediglich Denkaktionen. Der Versuch wurde gestoppt und getrennt erhalten; [Abbruchvermerk](../exports/attempt-01/termination-record.json), ursprünglicher Snapshot und ausgeführtes Skript liegen im Archiv. Das ist ein Fehler unserer Anbindung und kein Grund, TinyTroupe als grundsätzlich ungeeignet abzuschreiben.

Der korrigierte Versuch nutzt einen vollständigen THINK/TALK/DONE-Zug in einer Modellantwort. Um die ursprüngliche Anfragegrenze einzuhalten, wurde auf vier bekannte Fälle reduziert. Die Profile bleiben unverändert, die Gruppengröße und Kontextbeschreibung wurden angepasst. Die lokale Ablaufprüfung wurde mit echten Frameworkklassen und technischen Antwortfixtures wiederholt; [Prüfbeleg](../../../qa/tinytroupe-pilot-workflow-test.json).

Die Wiederholungsunterdrückung wurde ausdrücklich deaktiviert: Der Konstruktor ignoriert in diesem Quellstand den übergebenen False-Wert, weshalb die Instanzeigenschaft zusätzlich gesetzt wird. Standardmäßige Gedächtniskonsolidierung, semantische Suche und Qualitätskorrekturen sind ebenfalls aus. Der Versuch prüft episodisches Gedächtnis und Gruppenaustausch, nicht alle TinyTroupe-Fähigkeiten. Kein freier Interneteinsatz, keine realen Käufe und keine pädagogische Wirkungsmessung.

## Entscheidung

TinyTroupe bleibt bedingt geeignet als nachvollziehbare technische Grundlage. Für den Workshopzweck ist in diesem kleinen Versuch kein hinreichender Zusatznutzen gegenüber direkten Persona-Prompts belegt. Kein größerer Lauf auf dieser Grundlage.

Vor dem nächsten aufwendigen Framework-Pilot zuerst die Modell-/Eingabeabhängigkeit prüfen: bekannte Fälle und direkte Vergleichsmethode beibehalten, jeweils nur Modellroute oder Nachrichtenformulierung verändern und unbelegte Ergänzungen getrennt zählen. Erst bei relevantem zusätzlichem Lernstoff lohnen sich wiederholte Gruppendurchläufe mit besserer Kontrolle. AgentSociety bleibt ein Kandidat für eine technische Vorauswahl, keine bereits gerechtfertigte große Folgesimulation.

## Veröffentlichungsfassung

Die Originalhashes des Zustandsvergleichs bleiben erhalten. Ein rein lokaler Vorlagenpfad wurde in den öffentlichen Zustandsdateien ersetzt; deshalb sind Original- und öffentliche Dateihashes getrennt dokumentiert. [Redaktionsnachweis](../exports/publication-redactions.json). Das verändert weder Aussagen noch Kontakte, verhindert aber eine direkte Rekonstruktion der ursprünglichen Rohzustandshashes aus der öffentlichen Fassung allein.
