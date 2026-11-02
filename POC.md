# POC 01 · Ein Ereignis, unterschiedliche Haushalte, sichtbare Folgen

Version 0.1 · 2. November 2026 · Status: vorgeschlagener begrenzter POC. Technische Kernprüfung vorhanden; Frontend und HTTP-Anbindung sind noch nicht gebaut. Der [Bauplan](BUILD_PLAN.md) bleibt der Erweiterungsrahmen.

## Eine Frage

Können wir einen veränderten wirtschaftlichen Parameter über unterschiedliche vertragliche Ausgangslagen bis zum verfügbaren Handlungsspielraum eines Haushalts berechnen und in einer interaktiven 2D-Webansicht verständlich zeigen?

Dieser POC prüft technische Durchgängigkeit und Verständlichkeit. Er beweist keine realistische Anlegerpopulation, makroökonomische Prognose oder psychologische Entscheidungsregel.

## Enger Vorschlag für den Durchstich

Die bereits ausgeführte BPTK-Prüfung verwendet drei ausdrücklich fiktive Rechenfälle: einen variabel verzinsten Kredit, einen fest verzinsten Kredit und eine verzinste Einlage. Ein vorgegebener Zinsparameter bleibt gleich, steigt oder fällt. Sechs monatliche Perioden zeigen Einnahmen, Ausgaben, Zinszahlungen/-einnahmen, verfügbares Geld und einen einfachen vorgemerkten Anlagebetrag.

Dies ist ein praktischer Vorschlag, weil die Rechenprüfung bereits vorliegt. Die zuvor im Gespräch genannten Ereignisse legen grundsätzlich keine Lernmodule fest. Der Zinsparameter dieses Tests ist direkt ein vertraglich wirksamer Satz; eine reale Übertragung vom EZB-Leitzins auf alle Vertragszinsen wird damit nicht behauptet. Der fest verzinste Kredit wird im Betrachtungszeitraum nicht angepasst.

Einkommen, notwendige Ausgaben und eine Zielvormerkung sind konstante Testannahmen. Eine einfache Regel begrenzt den vorgemerkten Betrag auf den laufenden Überschuss. Die Vormerkung ist ein interner Geldtopf, kein ausgeführter Aktienkauf. Gemeinsame Familienentscheidungen, Preisrisiko, Kreditvergabeverhalten und Geldschöpfung sind in diesem ersten Ausschnitt nicht enthalten. Quellen und Annahmen bleiben sichtbar.

## Was die erste Ansicht können soll

Eine einzelne lokale Webansicht im Counterloom-Projekt, mit React und Tailwind sowie an der bestehenden Gestaltung orientierten Komponenten. Das SaaS-Projekt dient als interne Referenz; es wird für diesen POC nicht verändert. Eine schematische 2D-Ansicht ist der Arbeitsvorschlag, kein Beschluss für die spätere gesamte Anwendung.

- Parameter beziehungsweise eine der drei Varianten wählen und den Modelllauf starten.
- Den gewählten Lauf über sechs Perioden abspielen, pausieren und schrittweise untersuchen.
- Eine kleine Kette aus Parameter → Vertragswirkung → Haushalt → verfügbarem Anlagebetrag anzeigen. Jede Verbindung verweist auf berechnete Größen und angewandte Regeln.
- Zwischen den drei Fällen wechseln und den Zustand einer Periode mit der unveränderten Vergleichsvariante betrachten.
- Einnahmen, notwendige Ausgaben, Zinseffekt, verfügbares Geld und Vormerkung in einer kompakten Detailansicht nachvollziehen.
- Kennzeichnung als fiktiver Technik-/Lerntest; keine vermeintlich realistische Bevölkerung oder autonomen Entscheidungen zeigen.

Der erste UI-Aufbau kann die schon berechneten Ergebnisse wiedergeben. Das ist Replay, keine freie Neuberechnung. Für den vollständigen POC soll ein Start mit geänderten erlaubten Eingaben den Python-Kern neu ausführen und dessen Ergebnis zurückgeben. Grafische Auswahl und Wiedergabe berechnen keine Wirtschaft in React nach und lösen keine LLM-Anfragen aus.

## Kleinste technische Aufteilung

| Teil | Aufgabe |
|---|---|
| BPTK-Py/Python | Bestände und Flüsse berechnen; Ereignis und technischen Statuswechsel protokollieren. |
| Schmale lokale Schnittstelle | Validierte Szenarioeingabe entgegennehmen, begrenzten Lauf starten, Ergebnisse/Fehler liefern. Keine allgemeine Plattform-API. |
| React/Tailwind | Parameterwahl, Zeitschritt/Replays, schematische Verbindungen und Zustandsdetails. |
| Ein gemeinsames Ergebnisformat | Szenariokennung, Annahmen, Perioden, Fallkennungen, Zustände und beobachtete Vorgänge. |

Keine zusätzliche Datenbank, Benutzerverwaltung, 3D-Welt, vollständige Volkswirtschaft, Produktionsbereitstellung oder freie Newsrecherche im ersten POC. Öffentliche SaaS-Abhängigkeiten und Gestaltungsmuster sind geprüft; private Produktquellen, Fonts und Designpakete werden nicht automatisch in das öffentliche Repo kopiert. Eine neue Graphbibliothek ist noch nicht gewählt und für wenige Boxen nicht vorausgesetzt.

## Fertig, wenn

1. Derselbe algorithmische Eingang erzeugt reproduzierbar denselben Verlauf; alle sechs Perioden und drei Fälle sind prüfbar.
2. Fixe und variable Vertragsbedingungen erzeugen die implementierten unterschiedlichen Zahlungswirkungen; Ergebnisse stimmen mit einer unabhängigen Rechnung überein.
3. Geld wird durch Ausgaben/Vormerkungen korrekt fortgeschrieben. Nicht gedeckte Verpflichtungen werden als solche ausgewiesen; negative verfügbare Mittel werden nicht still erzeugt.
4. Neuberechnung und Replay sind sichtbar unterscheidbar. Die Ansicht zeigt die tatsächlichen Daten des gewählten Laufs.
5. Man kann in der Ansicht erklären, warum sich der Handlungsspielraum zwischen zwei Fällen oder Varianten unterscheidet, und die zugrunde liegende Annahme finden.
6. Fehlerhafte Eingaben oder ein fehlgeschlagener Lauf werden als Fehler angezeigt; kein scheinbar erfolgreiches Ersatzresultat.
7. Für Modelllauf und Wiedergabe fallen null LLM-Anfragen an.

Ein erster qualitativer Verständlichkeitstest kann mit einer Person erfolgen. Das ist noch keine pädagogische Wirkungsstudie.

## LLM-Erweiterung danach

Nach dem sichtbaren algorithmischen Durchstich kann eine einzelne Persona ihren Anlageplan anhand des berechneten Zustands überprüfen. Das ist ein eigener begrenzter Folgeschritt. Ihre Entscheidung wird gegen Mittel und erlaubte Handlungen validiert; sie darf von der einfachen Vergleichsregel abweichen. Ein solcher Schritt testet den Zusatznutzen generativer Abwägung und erhält ein eigenes kleines Anfragebudget.

## Bereits vorhanden und noch offen

- **Vorhanden:** BPTK-Py 3.5.0 in getrennter Prüfumgebung; 36 ausgewählte Originaltests bestanden. [Prüfbeleg](research/frameworks/evidence/bptk-upstream-tests-2026-11-02.json).
- **Vorhanden:** Eigener Offline-Test mit nativen SD-, Agenten- und Ereignisbausteinen. 54 Perioden-/Fall-Datensätze über drei Varianten, zusätzliche Extremwertprüfung, unabhängiger Wiederaufbau identisch; null LLM-Aufrufe. [Daten und Grenzen](qa/bptk-technical-screen-2026-11-02.json), [Prüfskript](tools/probe_bptk_hybrid.py).
- **Offen:** UI-Konzept im vorgegebenen Stil, lokale Schnittstelle, Frontendimplementierung, visuelle Prüfung und eine verständliche Erklärung direkt in der Ansicht.
- **Offen:** Vollständige Zustandswiederherstellung zwischen Prozessen. Für diesen POC reicht zunächst ein neuer kurzer Lauf aus gespeicherten Eingaben; echtes Fortsetzen wird damit nicht behauptet.

Umsetzungsreihenfolge: Ergebnisformat und Ansichtsskizze → Replay der vorhandenen Daten → schmale Neuberechnung → die obigen Prüfungen. Erweiterungswünsche währenddessen separat sammeln, statt den POC zu vergrößern.
