# Auswertung · kleiner Concordia-Gruppenversuch

2. November 2026 · Eigene qualitative Auswertung simulierter Aussagen, keine Beobachtung realer Anleger.

## Befund

Der technische Personenversuch ist vollständig. Der inhaltliche Mehrwert gegenüber den Ausgangsprofilen ist gering: Alle acht Personen äußern bereits vor dem Gespräch Zurückhaltung und ändern ihre Handlungsabsicht in keiner der beiden Bedingungen. Die Gruppen erzeugen Unterschiede in Formulierung und Bezugnahme, aber keinen klaren Meinungsumschwung. Das ist ein zulässiges Ergebnis, kein Anlass, Veränderungen zu erzwingen.

Die Beleg-IDs beziehen sich auf [responses.json](../exports/attempt-02/responses.json). Tatsächliche Empfänger und Beiträge stehen in den [Zustellungen](../exports/attempt-02/B_within_group_exchange-deliveries.json). Jedes Gruppenmitglied erhält die drei anderen Beiträge; sie wurden in der Reihenfolge P01 bis P08 erzeugt. Frühere Sprecher konnten spätere Beiträge erst bei der Schlussbefragung berücksichtigen.

## Pro Person

| Person | Ausgangspunkt | A ohne Austausch | B mit Austausch | Beurteilung |
|---|---|---|---|---|
| Nora | Liquidität sichern, keine Anlage; E001 | Unverändert; E009 | Gold zusätzlich als teuer im Handel beschrieben; E025 | Mögliche Übernahme von Milans Kostenargument aus E018, aber keine Änderung der Absicht; kein Ursachenbeweis. |
| Milan | Sachwert grundsätzlich interessant, Kosten/Zeithorizont fraglich; E002 | Abwarten; E010 | Gleiche Vorbehalte; E026 | Kein zusätzlicher klarer Meinungswechsel. Im Gespräch E018 ausdrücklich auf Nora bezogen. |
| Derya | Schmuck als Notreserve, Verwertung unsicher; E003 | Unverändert; E011 | Teilt Noras und Milans Skepsis; E027 | Soziale Bestätigung, Kerngedanke schon vorher vorhanden. |
| Robin | Erst Notgroschen, Verständnis fehlt; E004 | Unverändert; E012 | Nennt Noras und Milans Skepsis; E028 | Liquidität stärker betont, keine neue Absicht. |
| Alva | Moderate Goldquote halten; E005 | Unverändert; E013 | Aussagen von Sam und Jule bestärkten sie; E029 | Explizite Modell-Selbsterklärung einer Bestärkung, kein unabhängiger Einflussnachweis. |
| Alex | Diversifiziert bleiben, kein Kauf/Verkauf; E006 | Unverändert; E014 | Zugang zu Mitteln stärker betont; E030 | Bereits im Profil angelegt, kein neuer Befund. |
| Sam | Sparplan, skeptisch zu Gold; E007 | Unverändert; E015 | Spricht Jule direkt an; E031 | Bezug auf E024 belegt Gesprächsaufnahme; Alltagsrisiko bereits vorher vorhanden. |
| Jule | Nach Verlust vorsichtig, kein neuer Kauf; E008 | Unverändert; E016 | Verweist auf Sams Budgetrisiko; E032 | Bestätigung statt Richtungsänderung; Thema bereits in E008. |

Gruppen G01: P01–P04, Beiträge E017–E020 entsprechen `G01/post-0` bis `post-3`. G02: P05–P08, E021–E024 entsprechen `G02/post-0` bis `post-3`. Die Zuordnung erlaubt es, konkrete Bezugnahmen gegen tatsächlich verfügbare Inhalte zu prüfen.

## Qualitätsprobleme und Alternativerklärungen

- Bereits die Fallauswahl enthält viele vorsichtige Ausgangshaltungen. Die gemeinsame Nachricht betont fehlende verlässliche Prognosen, die Fragen erbitten begründete Abwägungen. Diese Kombination kann Homogenität begünstigen; welcher Anteil auf Modell, Profil oder Prompt entfällt, ist nicht bestimmt.
- Das Modell ergänzt unbelegte Einzelheiten: Nora nennt in E001 unregelmäßige Einkünfte, obwohl das Profil zunächst nur unregelmäßige Arbeitszeiten nennt. Alex wird in E006 zum Techniker mit Betriebskosten, obwohl nur technisches Interesse vorgegeben war. Solche Ergänzungen dürfen nicht als Eingabefakten weiterverwendet werden.
- Die Aliasantworten stammen aus einem Modell; acht Personas sind keine acht unabhängigen Erkenntnisquellen. Es gibt keine empirischen Gruppenanteile, keine repräsentative Bevölkerung und keine kalibrierte Angstskala.
- Eine Wiederholung, feste Sprecherreihenfolge, keine gepaarte Zufallssteuerung. Bedingung B hat zusätzlich eine eigene Äußerung und mehr Beschäftigung. Unterschiede lassen sich deshalb nicht allein den anderen Personen zuschreiben.
- Ein Gesprächsdurchgang ist kein langfristiger Gedächtnistest. Keine freie Recherche, realen Käufe, autonomen Ziele oder gemessenen Workshop-Lerneffekte.

## Technische Prüfung und Aufwand

32 echte Modellantworten in 92,88 Sekunden. Acht initiale Antworten, acht Schlussantworten A, acht Gruppenbeiträge und acht Schlussantworten B. Identische wiederhergestellte Ausgangshashes, 24 Zustellungen innerhalb der jeweiligen Gruppe, keine Zustellung über Gruppengrenzen. Einzelantworten, Prompts, Speicherzustände und Foren sind erhalten. Sichtbare Antworten wurden auf Vollständigkeit geprüft; alle 32 beendete der Server mit `stop`. Verbrauch und Ressourcengrenzen: [Laufmetadaten](../run.json). Fehlversuch und Verbindungstest separat archiviert, insgesamt 34 Anfragen.

## Entscheidung für einen nächsten Versuch

Concordia kann unsere kleine Vergleichsanordnung technisch tragen. Der Pilot rechtfertigt noch keine große Modellgesellschaft. Zunächst die Quellen unbelegter Biografieergänzungen eingrenzen und die bereits vor dem Austausch entstandene Einheitlichkeit untersuchen.

Ein sinnvoller nächster Vergleich verändert nur einen Faktor: dieselben Fälle auf einer unabhängigen Modellroute oder mit einer sachlich ausgewogenen zweiten Nachricht prüfen. Bei weiterhin ähnlichen Ausgangsreaktionen liegt kein Grund vor, mehr Gesprächsrunden zu kaufen. Falls relevante Unterschiede entstehen, wiederholte, umgekehrte Sprecherfolgen und eine gleich lange Kontrollbedingung mit Selbstreflexion statt Peer-Text hinzufügen. Ein einfacher direkter Modellprompt mit denselben Fällen dient als günstige Vergleichsmethode. Erfolg bleibt zusätzlicher nachvollziehbarer Lernstoff, nicht ein erzwungener Meinungswechsel.
