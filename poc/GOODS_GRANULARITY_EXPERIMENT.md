# Prüfung kleinerer Gütereinheiten

Der kontrollierte Vergleich untersucht, wie die bisherige grobe Stückelung die Modellwirtschaft über 600 Monate verändert. Seit v15 verwendet die normale Modellkonfiguration 100 Teile je bisheriger Gütermenge. Der archivierte Forschungsgegenlauf prüfte vor dieser Übernahme dieselbe feinere Auflösung gegen die ursprüngliche Stückelung. [Ergebnisse und Diagramme](../qa/goods-granularity-comparison.md).

## Einheitenumrechnung

`World()` beziehungsweise `World(goods_unit_scale=100)` ersetzt jede ursprüngliche Gütereinheit durch 100 Teile. Unterstützt werden die Teilungsfaktoren 1, 10 und 100, sodass Grundpreise und Energie je Einheit weiterhin in ganzen Cent darstellbar sind. Der Faktor wird mit dem Zustand exportiert. `export_orders_units` in der Konstruktion bleibt in ursprünglichen Einheiten definiert und wird intern umgerechnet.

| Grösse | Umrechnung bei Faktor 100 |
| --- | --- |
| Stückpreis | durch 100 |
| Energie je produzierter Einheit | durch 100 |
| Produktivität je Arbeitskraft | mal 100 |
| Anfangsabsatzplan | mal 100 |
| Auslandsbestellmengen | mal 100 |
| Material je Maschine | 800 Teile statt 8 ursprünglicher Einheiten |
| Kapazitätszuwachs je Maschine | 400 Teile statt 4 ursprünglicher Einheiten |
| Mengen im Kaufkraft-Warenkorb | mal 100 |
| Mindestnachfrage für Weiterbetrieb | ein ursprüngliches Gut, entsprechend 100 Teilen |

Geldbestände und alle Geldregeln bleiben unverändert. Lager, verkaufte und produzierte Mengen sowie ihre Prognosen werden in der gewählten Teilmenge geführt. Lagerkosten und Zahlungsbuchungen bleiben in Cent. Die Personenzahl, Personalgrenzen, Leitzinsen, Steuersätze, Transferhöhe, Konsumquote, Verlustbrücke, Reserveformeln und Entscheidungsfristen werden nicht verändert.

## Gegenstand des Vergleichs

Die Auflösung aller Gütermengen ändert sich, einschliesslich Rundung von Produktion, Lagerzielen und Absatzprognosen. Nachfolgende Beschäftigung und Finanzströme können sich dadurch verändern. Der Versuch isoliert diese gemeinsame Güterauflösung; er trennt nicht die Wirkung jeder einzelnen Rundungsstelle. Er enthält keine externen Schocks. Preis- und Energiekostenrundung bei veränderten Energiepreisen wird durch diesen Lauf nicht untersucht.

Der Stückelungsrest der Haushalte wird getrennt von Geldmangel und fehlender Ware ausgewiesen:

`finanzierbares Budget = bezahlte Käufe + Warenlücke + Stückelungsrest`

`Konsumwunsch = finanzierbares Budget + Finanzierungslücke`

Der Stückelungsrest ist Geld, das wegen ganzer Teile nicht in einen Kauf umgesetzt wird. Er verbleibt auf dem Konto und ist kein Verlust von Zahlungsmitteln. Ein über Monate summierter Rest ist keine zusätzliche Geldmenge und kein gleich hoher Steuerverlust.

## Prüfungen

- Faktor 1 reproduziert jeden der 600 archivierten Abschlüsse des v14-Laufs mit 25 % Ausschüttungssteuer.
- Anfangsguthaben, Bankbilanz, realer Preis je ursprünglichem Gut und Gesamtwarenkorb bleiben gleich.
- Anfangskapazität, Energieaufwand und Personalbedarf werden auf äquivalente physische Mengen geprüft.
- Im ersten Kaufmonat bleiben Konsumwunsch und finanzierbares Budget gleich; ausschliesslich die Ausführung mit kleineren Teilen verändert die Käufe.
- Maschinenpreis und Kapazitätszuwachs werden gemeinsam geprüft, ebenso reserviertes Material und Lieferung.
- Jede Buchung eines feinen Laufs mit Maschinenkredit und Betriebsschliessung wird unabhängig aus den Ausgangskonten rekonstruiert.
- Die Antwortprüfung der Oberfläche berücksichtigt den Teilungsfaktor beim Warenkorb und den exportierten Mengenfeldern.

Die Batchauswertung benötigt keine Änderung der normalen Oberfläche oder eines bereits laufenden Experiments. Rohdaten enthalten alle Monatsbudgets, Haushaltskäufe, Firmenpläne und Quellprüfsummen. Tests und Startanleitung stehen in [README](README.md).
