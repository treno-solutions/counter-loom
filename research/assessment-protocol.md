# Prüfprotokoll für bestehende Frameworks

Version 1.3 · 2. November 2026. Grundlage: [Anforderungen R01–R24](requirements.md).

## Statusmodell

| Status | Bedeutung |
|---|---|
| `candidate` | Projekt gefunden; Eignung und Betrieb nicht geprüft |
| `documentation_reviewed` | Dokumentation/ausgewählte Quellen geprüft; Fähigkeiten noch nicht praktisch nachgewiesen |
| `pilot_planned` | Version, Eingaben, Bedingungen, Kostenlimit und Auswertung festgelegt |
| `pilot_tested` | Kleiner Test ausgeführt; Ergebnis und Artefakte dokumentiert |
| `workshop_tested` | Pädagogischer Einsatz zusätzlich untersucht |

Eignung wird separat als `unassessed`, `conditional`, `suitable_for_pilot` oder `unsuitable_for_current_goal` festgehalten. Ein erfolgreicher Programmstart ist keine fachliche Eignungsentscheidung. Ein öffentliches Benchmarkresultat wird nicht als eigener Test ausgegeben.

## 0 · Grundlagen vor jedem neuen Framework-Piloten

- MiroFish-Bewertung und Ableitung der Anforderungen sind vorhanden.
- Version des Prüfprotokolls festgehalten.
- Es wurde noch keine Plattform aufgrund bloßer Produktversprechen ausgewählt.
- Für den konkreten Pilot: Lizenz, Dienstabhängigkeiten, erlaubte Daten, Budget und Datenablage geklärt.

Diese Vorarbeiten sind vor weiteren Piloten verbindlich. Es gibt keine automatische Freigabe für zusätzliche Rechenläufe oder eine Eigenentwicklung.

## 1 · Markt- und Literaturrecherche

Projekt, Träger, Repo, Lizenz, Versionsstand und erforderliche Dienste erfassen. Dokumentation, veröffentlichte Studien, Herstellerdemonstration und unabhängige Validierung getrennt behandeln. Auf veraltete Versionen achten. Für jede Anforderung notieren: dokumentiert, praktisch bestätigt, nicht unterstützt oder unbekannt. Keine addierten Marketing-Punktwerte.

## 2 · Einheitlicher kleiner Prüfgegenstand

Vorgeschlagen sind zwei bis drei soziale Gruppen mit insgesamt acht bis zwölf fiktiven Personen. Vor dem Test dieselbe Fallauswahl für alle Kandidaten festschreiben. Ausreichend Unterschiede innerhalb der Gruppen vorsehen. Keine empirischen Bevölkerungsanteile behaupten. Nicht alle Personen müssen Gold besitzen oder Anlageerfahrung haben.

Eine klar als hypothetisch markierte Nachricht wird zugestellt, beispielsweise ein Energiepreisanstieg unter geopolitischer Unsicherheit. Ein Gegenargument beziehungsweise eine spätere Entspannung kann als zweite Variante vorbereitet werden. Die genaue Ereignisbeschreibung und Sichtbarkeit bleiben zwischen Kandidaten gleich; der Reaktionsverlauf wird nicht vorgeschrieben.

Neutrale Vorher-/Nachher-Fragen: Was bedeutet die Information? Was bleibt unsicher? Welches Bedürfnis ist betroffen? Hat sich eine Erwartung oder Absicht verändert? Warum beziehungsweise warum nicht? Keine Aufforderung, sich überzeugen zu lassen.

## 3 · Technische Eingangskontrolle

Prüfen: Profilerzeugung ohne stereotype Zwangskopplung, getrenntes Wissen, gezielte Zustellung, eigener Gedächtnisspeicher, gespeicherte Ausgangszustände, Abbruch-/Wiederherstellung und lesbarer Export. Erst anschließend den begrenzten Dialogtest starten. Fehler nicht durch wiederholte große Läufe verdecken.

## 4 · Einfluss untersuchen

A: Nachricht ohne sozialen Austausch. B: dieselbe Ausgangspopulation mit Gruppengespräch. Optional C: wie B mit wenigen Brückenkontakten. Bedingungen aus demselben gespeicherten Ausgangszustand beginnen, keine bereits beeinflusste Population wiederverwenden.

Modellversion, Parameter, tatsächliche Nachrichten, Kontakte und Zufallssteuerung dokumentieren. LLM-Ausgaben können trotz gleicher Einstellungen variieren; begrenzte Wiederholungen nötig. Zunächst Unterschiede innerhalb des Modells untersuchen. Übertragung auf reale gesellschaftliche Effekte benötigt gesonderte Evidenz.

## 5 · Ergebnisse und Zusatznutzen bewerten

Pro Person Vorzustand, erhaltene Information, Kontaktbeleg, Nachzustand und Unsicherheit festhalten. Aussagen des Reporters getrennt bewerten. Beispiele müssen auf tatsächliche Interaktionen verweisen. Konsens, Polarisierung, Nichtänderung und zunehmende Unsicherheit sind zulässige Ergebnisse.

Mit einer direkten Analyse derselben Eingaben vergleichen. Neuheit nicht allein durch längeren Text oder überraschende Erzählung bewerten. Welche zusätzliche, belegbare Frage oder Wechselwirkung wurde sichtbar? Welche Ergebnisse sind bereits im Seed angelegt? Gemessene Laufzeit, Verbrauch und Kosten zusammen mit fehlenden Messdaten berichten.

## 6 · Pädagogische Prüfung

Erst nach technischem und fachlichem Pilot im kleinen Workshop prüfen. Vorher-/Nachher-Aufgaben untersuchen, ob Teilnehmer mehr unterschiedliche Reaktionen erklären und eigene Bedürfnisse von Lebensumständen oder momentaner Stimmung unterscheiden können. Persönliche Reflexion freiwillig halten. Keine medizinische oder psychologische Diagnose und keine individuelle Anlageempfehlung ableiten.

## Entscheidung

- **Nicht geeignet:** erforderliche Erinnerungen/Belege fehlen, Isolation des Wissens scheitert oder der zusätzliche Nutzen bleibt unbelegt. Keine Vergrößerung.
- **Bedingt geeignet:** Nutzen erkennbar, aber klar benannte Ergänzungen nötig. Aufwand gegen Alternativen abwägen.
- **Für Pilot geeignet:** Mindestfunktionen sind praktisch nachgewiesen. Das ist noch keine gesellschaftliche oder pädagogische Validierung.

Jede Entscheidung enthält Belege, Grenzen, tatsächliche Kosten, offene Anforderungen und eine begründete nächste Handlung. [Vorlage](frameworks/_template.md).


## Ergänzung 1.1 · Mehrperiodenwelt unter Schocks

Gilt für neu geplante Piloten; die ausgeführten Gesprächsversuche 004/005 bleiben nach ihrem damaligen Design eingeordnet. [Zielentscheidung 0002](decisions/0002-world-state-and-shocks.md).

Vor dem Start Bezugsraum und Fälle einschließlich Nichtanlegern, finanzielle Ausgangszustände, Periodenlänge, Informationskanäle, zulässige Handlungen und Abrechnungsregeln festlegen. Archetypen und Gewichte benötigen Quellen oder eine ausdrückliche Kennzeichnung als hypothetische Auswahl.

Aus identischen Anfangszuständen mindestens eine Welt ohne Schock und eine mit eindeutig spezifiziertem Schock fortführen. Eine Kriegsmeldung zunächst als Informationsereignis behandeln; Energiepreise, Einkommen und weitere wirtschaftliche Folgen als gesonderte Szenariopfade ausweisen. Für Zinsänderungen Einlagen-/Kreditarten und Zinsbindungen berücksichtigen. Keine gewünschte Panik, Umschichtung oder Anpassung vorgeben.

Pro Zeitschritt erhaltene Information, Zustandsauszug, Handlungsantrag, Zulässigkeitsentscheidung, realisierte Folgen und Folgezustand sichern. Beispielsweise reicht „ich brauche bald Geld“ nicht als Nachweis einer Deckungslücke. Eine Deckungslücke erfordert eine nachvollziehbare Rechnung mit den vereinbarten Regeln.

Eine einfache zustandsbasierte regelgesteuerte Variante mit gleichem wirtschaftlichem Kern als Vergleich vorbereiten. Ein direkter Persona-Prompt bleibt eine günstige Vergleichsmethode für Interpretationen, ersetzt aber keine mehrperiodige Kontrolle. Wiederholungen, Modell-/Promptvariation und eine isolierte Änderung je Vergleich einplanen. Erst dann prüfen, ob generative Entscheidungen zusätzlichen nachvollziehbaren Lernstoff liefern.

Neue Abbruchkriterien: inkonsistente Buchungen, verlorene Verpflichtungen, erfundene Mittel, Zugriff auf nicht erhaltene Weltinformationen, nicht reproduzierbare Zustandswiederherstellung oder fehlende Trennung von Absicht und ausgeführter Aktion. Fehlgeschlagene Pfade sichtbar erhalten. Größe und Laufzeit nicht erhöhen, solange diese Mindestfunktionen ungeprüft sind.


## Ergänzung 1.2 · Makroökonomische Grundlage zuerst prüfen

[Zielentscheidung 0003](decisions/0003-macroeconomic-world.md) verlangt zusätzlich den Nachweis eines über Sektoren gekoppelten Kerns. Vor einer generativen Erweiterung vorhandene Makromodelle auf Konten, Gegenbuchungen, Staatsschulden, Kredit-/Geldschöpfung, Zinsübertragung und messbare Investitionen prüfen. Wirtschaftliche Verhaltensgleichungen, institutionelle Regeln und empirische Kalibrierung getrennt erfassen. Eine makroökonomische Basis zunächst mit ihren vorhandenen Entscheidungen reproduzieren; LLM-Entscheidungen danach als begrenzte, vergleichbare Erweiterung betrachten. Kein automatischer Rechenlauf durch diese Protokolländerung.

Die Oberfläche ist eine Projektion tatsächlich berechneter Zustände und Ereignisse. Schematische Sektorboxen mit aktivierten Verbindungen und räumliche Ansichten bleiben Optionen. Ursache, Periode, Größe und Empfänger jeder dargestellten Wirkung müssen überprüfbar sein; eine vorgefertigte Animation ersetzt den Modelllauf nicht.


## Ergänzung 1.3 · Lernumfang begrenzt, Kernel zuerst algorithmisch

[Entscheidung 0004](decisions/0004-reduced-hybrid-learning-model.md) priorisiert System Dynamics mit Ereignis-/Zustandsmodellen und optionalen generativen Entscheidungen. Die in Ergänzung 1.2 geforderte Prüfung einer vollständigen Makrogrundlage ist kein zwingender erster Schritt mehr. Prüfumfang und Aussagen müssen zum gewählten Lernmodul passen; ausgelassene Sektoren oder Mechanismen sichtbar benennen.

Zuerst vorhandene SD-/Hybridwerkzeuge gegen einen kleinen fachlichen Durchstich prüfen. Routinen und Folgen ohne LLM testen, anschließend eine begrenzte Entscheidung anbinden. Ereignisrelevanz, aufgelaufene Änderungen und geplante Reviews getrennt prüfen, damit eingesparte Anfragen keine schleichenden Entwicklungen unsichtbar machen. Obergrenzen umfassen auch Diagnose- und Wiederholungsaufrufe. Replay benötigt keine erneuten Modellentscheidungen; echte Wiederholungen dürfen nicht unbemerkt aus einem Antwortcache kommen.
