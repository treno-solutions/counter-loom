# 004 · Erster Concordia-Gruppenversuch

2. November 2026 · Status: **Explorativer Personenversuch abgeschlossen; kein Einflussnachweis.**

Acht fiktive Personen in zwei Gruppen interpretieren eine hypothetische geopolitische Eskalation mit steigenden Energiepreisen. Nach der gemeinsamen Ausgangsbefragung werden ihre gespeicherten Zustände in zwei Bedingungen wiederhergestellt:

- A: neutrale Schlussbefragung ohne Austausch.
- B: eine Gesprächsrunde innerhalb der jeweiligen Vierergruppe, dann dieselbe Schlussbefragung.

## Ergebnis und Grenzen

32 Modellantworten in 92,88 Sekunden; acht Beiträge mit 24 Zustellungen ausschließlich innerhalb der Gruppen. Gleiche Ausgangszustände beider Bedingungen technisch bestätigt. Alle acht Personen bleiben bei ihrer bisherigen Handlungsabsicht. Einige beziehen sich ausdrücklich auf erhaltene Beiträge, ohne erkennbaren Strategiewechsel. Das zeigt aufgenommene Gesprächsinhalte, keinen isolierten kausalen Einfluss.

Der Erkenntnisgewinn bleibt klein. Bereits die Ausgangsantworten konvergieren stark auf Abwarten. Ein größerer Lauf ist damit noch nicht begründet. Siehe die [Auswertung mit Einzelbelegen](analysis/evaluation.md).

## Eingaben und Belege

- [Fiktive Fälle und Gruppen](inputs/people.json), [Nachricht und neutrale Fragen](inputs/scenario.json), [Design](inputs/design.json), [Startprüfung](inputs/start-check.md).
- [Unveränderter Eingabesnapshot des erfolgreichen Versuchs](exports/attempt-02/input-snapshot.json).
- [Alle Personenantworten](exports/attempt-02/responses.json), [Modellaufrufe mit Prompts](exports/attempt-02/model-calls.jsonl), [Zustellungen](exports/attempt-02/B_within_group_exchange-deliveries.json), [Forumzustände](exports/attempt-02/B_within_group_exchange-forums.json).
- [Ausführungsstatus und Tokenverbrauch](exports/attempt-02/status.json), [Laufmetadaten](run.json), [Artefaktprüfsummen](artifact-manifest.json).
- [Ablaufskript](../../tools/run_concordia_pilot.py), [Offline-Workflowtest](../../tools/check_concordia_pilot_workflow.py), [Prüfergebnis](../../qa/concordia-pilot-workflow-test.json).

## Technik und Ressourcen

Concordia 2.4.0, Quellstand `f1d3ae6da20b32f686cefc13458cafc695c3b6a2`; bestehendes minimales Personen-Prefab und getrennte `ForumState`-Instanzen. Der eigene Ablauf koordiniert Zustellung und Vergleich, ohne psychologische Einflusskoeffizienten. Das Gedächtnis nutzt jüngste Beobachtungen; ein konstanter Speichervektor ist keine semantische Suche. Die umfangreichere Reflexionsarchitektur wird nicht geprüft.

Modellalias `local:default`, angebunden über den vom Nutzer bereitgestellten kompatiblen Modellserver. Die Anbieter-Metadaten ordneten den Alias bei der Prüfung `openai/qwen3.8:27b-fp8` zu; Modellgewichte und interne Route wurden nicht unabhängig verifiziert. Die Aufrufprotokolle erhalten die vom Server gemeldete Modellkennung. Temperatur 0,7, top_p 0,95, maximal 400 Ausgabetokens, Denken über die Chat-Template-Einstellung deaktiviert, keine automatischen Wiederholungen. Kein festgelegter Generierungsseed; keine exakte Textreproduzierbarkeit behauptet.

Der [erste Versuch](exports/attempt-01/status.json) stoppte nach einer leeren sichtbaren Antwort. Die Ursache ist nicht belegt. Ein [kurzer Verbindungstest](exports/connection-probe.json) mit deaktiviertem Denken lieferte Text. Danach wurde die Gesprächszahl von zwei auf eine Runde reduziert. Insgesamt wurden 34 reale Anfragen einschließlich Fehlversuch und Probe ausgeführt, unter der ursprünglichen Obergrenze von 40. Jede Variante besitzt einen eigenen Eingabesnapshot; der Fehlversuch bleibt erhalten. Die gemessenen Tokens des erfolgreichen Versuchs stehen in `run.json`; der Verbrauch des Fehlversuchs ist unbekannt. Stromverbrauch und Geldkosten wurden nicht separat gemessen.

Modellzugang nur über lokale Umgebungsvariablen `CONCORDIA_BASE_URL`, `CONCORDIA_MODEL` und gegebenenfalls `CONCORDIA_API_KEY`. Private Adresse und Zugangsdaten werden nicht veröffentlicht.
