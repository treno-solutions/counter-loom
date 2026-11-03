# Counterloom · Treno-Gestaltung

Die aktuelle Wirtschaftsoberfläche übernimmt die Farbwelt, Poppins-Typografie, Wortmarke und runden Buttons der Treno-Website. Die Gestaltung ist in [`src/treno-theme.css`](src/treno-theme.css) zentral hinterlegt.

## Farben und Bedeutung

| Verwendung | Farbe |
| --- | --- |
| Navigation, Überschriften, Kennzahlenflächen | Petrol `#012d3b` |
| Hauptaktion, Auswahl und Markenakzente | Treno-Grün `#4dd700` |
| Inhaltsflächen | Weiß `#ffffff` |
| Hintergrund | Hellgrau `#f5f7f8` |
| Sekundärtext | Blaugrau `#526b77` |

Grüne Aktionsflächen verwenden dunkle Schrift. Sektorfarben bleiben unterscheidbar: Haushalte blau, Unternehmen ocker, Staat violett, Finanzsektor dunkelgrün und Ausland petrolblau. Farbe wird durch Namen, Beträge, Linienarten und Zustandsbeschriftungen ergänzt. Diagrammbeschriftungen haben deckende Flächen und liegen vor den Verbindungslinien.

## Typografie und Komponenten

- Poppins für Oberfläche und Überschriften; IBM Plex Sans für Kennzahlen und SVG-Beschriftungen. Beide Schriften werden lokal ausgeliefert.
- Die Poppins-Lizenz liegt unter [`public/licenses/Poppins-OFL.txt`](public/licenses/Poppins-OFL.txt). Die Treno-Wortmarke ist ein Markenbestandteil, kein generisches Icon.
- Runde Haupt- und Nebenaktionen, weiße Inhaltskarten und eine dunkle Kennzahlenleiste. Warnungen und Fehler behalten eigene semantische Farben.
- Die Zeitsteuerung bleibt beim Scrollen erreichbar. Auf schmalen Bildschirmen wird der Neustart als beschrifteter, für Hilfstechnologien benannter Icon-Button dargestellt. Breite Wirtschaftsdiagramme bleiben innerhalb ihrer Bereiche horizontal verschiebbar.
- Tastaturfokus bleibt sichtbar; Farbwechsel respektieren reduzierte Bewegung.

Die Gestaltung ändert keine Modellparameter oder wirtschaftlichen Berechnungsregeln. Sie liefert keine zusätzliche fachliche Validierung des Modells.
