# 005 · TinyTroupe: kleiner Gruppenvergleich

2. November 2026 · **Korrigierter Versuch abgeschlossen: 20 Anfragen in 118,8 Sekunden.** Explorativer Frameworktest. Keine empirische Bevölkerung und keine Workshop-Validierung.

## Frage und Vergleich

Bringt TinyTroupes Personen-, Gedächtnis- und Gesprächsablauf gegenüber einem direkten Persona-Prompt zusätzlichen, belegbaren Lernstoff? Außerdem: Welche Unterschiede zeigen sich nach Austausch innerhalb der Gruppe gegenüber einer Bedingung ohne Austausch?

Nach einer abgebrochenen Anbindungsvariante verwendet der korrigierte Versuch vier unveränderte Personenprofile aus Lauf 004: Nora, Derya, Alva und Sam. Zwei getrennte `TinyWorld`-Räume mit jeweils zwei Personen; die Gruppenbeschreibung wird von vier auf zwei Bekannte angepasst. Dieselbe hypothetische Nachricht und dieselben neutralen Fragen wie in Lauf 004. Keine vom Vorgängermodell erfundenen Biografiedetails werden als Eingabefakten übernommen.

- Gemeinsame Ausgangsbefragung; individuelle Gedächtnisse und Zustände speichern.
- A: gespeicherte Ausgangszustände wiederherstellen, Schlussbefragung ohne Austausch.
- B: dieselben Zustände wiederherstellen, je eine vollständige Gesprächsaktion pro Person innerhalb der Gruppe, identische Schlussbefragung.
- Einfacher Vergleich: vier unabhängige direkte Modellprompts mit denselben Fällen, der Gruppenbeschreibung, Nachricht und Ausgangsfrage; ohne Framework, Gesprächsverlauf oder kognitiven Zustand.

Die einfache Vergleichsmethode bezieht sich zuerst auf die Ausgangsreaktion. Sie isoliert nicht den Effekt eines einzelnen Speicherbausteins. Der Vergleich mit Lauf 004 ist ebenfalls eingeschränkt: Gruppengröße, Framework-Systemprompt, Zustandsformat und Ausgabebegrenzung unterscheiden sich. Keine Rangliste aus einem einzigen Lauf ableiten.

## Dokumente und Belege

- [Fälle und Gruppen](inputs/people.json), [Nachricht und Fragen](inputs/scenario.json), [Ausführungsdesign](inputs/design.json), [Eingabeprüfsummen](inputs/input-manifest.json).
- [Auswertung](analysis/evaluation.md), [Laufmetadaten](run.json).
- [Erster, gestoppter Versuch](exports/attempt-01/termination-record.json) mit ursprünglichem Eingabesnapshot und ausgeführtem Ablaufskript.
- [Korrigierter Versuch: Eingabesnapshot](exports/attempt-02/input-snapshot.json), [Antworten und Aktionen](exports/attempt-02/responses.json), [Modellaufrufe](exports/attempt-02/model-calls.jsonl), [Zustellungen mit Speicheränderungen](exports/attempt-02/deliveries.json), [Ausführungsstatus](exports/attempt-02/status.json).
- [Ablaufskript](../../tools/run_tinytroupe_pilot.py), [Offline-Prüfung](../../qa/tinytroupe-pilot-workflow-test.json), [Artefaktprüfsummen](artifact-manifest.json).

## Methode und Ressourcen

TinyTroupe 0.8.1, MIT, Quellstand `7ce8be378a37ee73f9745d6781452712318afa04`. Vollständige echte `TinyPerson`- und `TinyWorld`-Klassen, keine AST-Testdoubles und keine Änderungen am Frameworkquellcode. Die importseitig benötigten Abhängigkeiten wurden in der privaten Prüfumgebung installiert; nicht das komplette Notebook-, Azure- und HuggingFace-Paket. Import- und Ablaufprüfung ersetzen keinen vollständigen Upstream-Testlauf.

Ein registrierter Modellclient verbindet den bereitgestellten Server mit dem Framework. Modellalias `local:default`; dieselbe Route wie in Lauf 004, ohne unabhängige Prüfung der Modellgewichte. Keine Standardaufrufe an andere Modellanbieter. Lokale Zugangsdaten und Serveradresse werden nicht veröffentlicht. Client-Umgebungsvariablen entsprechen dem Concordia-Piloten; `TINYTROUPE_SOURCE` kann den privaten Quellcheckout bestimmen.

Der korrigierte Ablauf verwendet die native Aktionsfolge THINK/TALK/DONE in einer strukturierten Antwort pro Zug. Gedächtniskonsolidierung, kontinuierliche semantische Suche, Qualitätskorrekturen und Regenerierung sind deaktiviert. Episodische Erinnerungen bleiben aktiv. Die Wiederholungsunterdrückung ist ausdrücklich abgeschaltet, damit Nichtänderung nicht automatisch in DONE umgewandelt wird. Ein Konstruktorparameter allein bewirkte dies am geprüften Quellstand nicht; die Instanzoption wird zusätzlich gesetzt. Diese Auswahl prüft nicht den vollständigen Standardbetrieb mit semantischem Langzeitgedächtnis.

Geplant: 20 Anfragen im korrigierten Versuch, maximal 1.200 Ausgabetokens je Anfrage, 60 Sekunden je Anfrage und 900 Sekunden insgesamt. Die größere Ausgabegrenze gegenüber Concordia berücksichtigt Aktions- und Zustands-JSON. Temperatur 0,7, top_p 0,95, Denken über die Modell-Template-Einstellung deaktiviert, kein festgelegter Zufallsseed. Die modellierte THINK-Aktion ist eine vom Framework verlangte Persona-Aktion und vom deaktivierten internen Modellmodus zu unterscheiden.

Der erste Versuch wurde nach 17 begonnenen Anfragen gestoppt: Die eigene Anbindung begrenzte einen Zug auf eine Einzelaktion, obwohl das Framework THINK vor TALK verlangt. Manche Antworten endeten deshalb vor einer Sprechaktion. Dies ist ein Fehler des Pilotaufbaus und kein Nachweis einer grundsätzlichen TinyTroupe-Unfähigkeit. Ursprüngliche Artefakte bleiben erhalten; der ergänzende Abbruchvermerk erläutert den zuletzt noch laufenden Status. Eine angefangene Serveranfrage kann trotz lokalem Abbruch weitergerechnet worden sein. Zusammen höchstens 37 begonnene Anfragen, unter der zuerst angekündigten Grenze von 40. Keine automatischen Transportwiederholungen; der Adapter bricht bei Transport-, Format- und Grenzfehlern ab.

Zeit und vom Server gemeldete Tokens werden dokumentiert. Geldkosten und Stromverbrauch sind nicht unabhängig gemessen. Nur ein Durchgang, feste Sprecherfolge, zusätzliche Beschäftigung in B und ein gemeinsames Sprachmodell: kein isolierter kausaler Einflussnachweis.

Die Protokolle enthalten auch die verwendeten Framework-Prompts; [Lizenz- und Herkunftshinweise](../../research/frameworks/licenses/README.md).

Für die Veröffentlichung wurde ausschließlich der lokale Installationspfad der Promptvorlage in den Zustandsdateien durch den paketrelativen Namen ersetzt. Unveränderte Originalexporte liegen im privaten Archiv. [Redaktionsprotokoll mit Original- und Veröffentlichungsprüfsummen](exports/publication-redactions.json). Die beim Lauf verglichenen Ausgangshashes beziehen sich weiterhin auf die Originalzustände; zusätzliche Hashes der öffentlichen Anfangszustände liegen je Versuch bei. Personeninhalte, Prompts und tatsächlich verwendete Eingaben wurden nicht geändert.
