# Langzeitprüfung und Krisenvergleich · v11

Stand: 3. November 2026. Drei deterministische Läufe über je 600 Monate (3.000 Phasen), identischer Anfangszustand. Referenz ohne Eingriff; Vergleichsläufe mit Werkstattschliessung in Monat 25–27, einmal ohne und einmal mit 60 % Einkommensersatz. [Monatsdaten, Schwellen und kumulierte Zahlungsarten](crisis-v11-long-horizon-2026-11-03.json). Eigene Modellannahmen, keine wirtschaftliche Prognose.

## Befund im langen Lauf

| Lauf | Kreditgrenze erstmals erreicht | Staatskasse erstmals null | Haushaltsguthaben unter 10 % des Startwerts | Haushalte M600 | Unternehmen M600 |
| --- | ---: | ---: | ---: | ---: | ---: |
| Ohne Schock | M52 | M251 | M345 | 1.196,22 € | 194.632,78 € |
| Schliessung ohne Kurzarbeit | M51 | M247 | M357 | 1.230,51 € | 194.632,49 € |
| Schliessung mit Kurzarbeit | M48 | M260 | M364 | 1.163,37 € | 194.661,63 € |

Alle drei Läufe erreichen langfristig einen stark verarmten Haushaltssektor und eine erschöpfte Staatskasse. Die Bankkreditgrenze liegt jeweils bei 50.000 €. Die Haushaltskonten werden nicht negativ; sie haben im Modell keine Kredite. Negative Änderungen seit Start sind Guthabenverluste. Die Firmen halten am Ende ungefähr 194.600 € liquide Mittel, während die Haushalte zusammen nur ungefähr 1.200 € halten. Diese Konstellation entsteht bereits ohne Krisenschock.

## Erklärung aus den vorhandenen Regeln

1. Firmen behalten einen Teil ihrer positiven Ergebnisse ein. Die laufenden Ausschüttungen verteilen höchstens die Hälfte des aktuellen Nachsteuerergebnisses; angesammelte Überschussliquidität wird nicht später zusätzlich verteilt. Ein endlicher Investitionsbedarf führt deshalb nicht automatisch zu einem Rückfluss alter Firmenrücklagen.
2. Der Staat zahlt feste öffentliche Löhne, Transfers und Beschaffung, während seine Einnahmen von tatsächlich gezahlten Löhnen und Firmengewinnen abhängen. Seine Anfangskasse und sein begrenzter Bankkredit können die laufenden Defizite nur zeitweise tragen.
3. Wenn die staatliche Finanzierung an ihre Grenze kommt, bleiben Zahlungen aus. Öffentliche Arbeitsverträge bleiben trotzdem bestehen und unbezahlte Pflichtlöhne werden weiter als Verpflichtungen erfasst. Die im Langzeitprotokoll erfassten offenen Verpflichtungen wachsen bis M600 auf mehr als 2,6 Millionen Euro. Die ausgewiesene Bankschuld allein bildet diese Verpflichtungen nicht ab.
4. Die Haushalte dürfen den vorgegebenen Grundbedarfsplan aus vorhandenem Guthaben finanzieren. Sinkende Einkommen führen deshalb zunächst zum Verbrauch von Ersparnissen; später begrenzen fehlende Zahlungsmittel die Käufe. Betriebe reduzieren Arbeitszeit und Personal beziehungsweise werden stillgelegt.

Die Konten und Bankgegenbuchungen bleiben dabei rechnerisch konsistent. Daraus folgt keine langfristige ökonomische Plausibilität. Insbesondere ist ein Staat mit jahrelang weiterlaufenden unbezahlten öffentlichen Arbeitsverträgen ein fehlender institutioneller Anpassungsprozess.

## Was der Kurzarbeitsvergleich zeigt

Die Kurzarbeitsleistung schützt während der Schliessung einen Teil des Referenz-Nettoeinkommens und belastet die Staatsfinanzierung. Gesperrte Verkäufe können nicht durch zusätzliche Haushaltsliquidität ersetzt werden; deshalb müssen Konsum und Firmenumsatz nicht sofort steigen. Nach Wiederöffnung können Guthaben und Nachfrage unterschiedlich verlaufen.

Die leicht unterschiedlichen Endbeträge nach 600 Monaten sind keine robuste Rangfolge der Förderpolitik. Die gemeinsamen langfristigen Modellgrenzen dominieren diese Läufe. Beide Krisenvarianten erhalten während der angeordneten Schliessung dieselben Arbeitsverträge; der Vergleich isoliert den Einkommensersatz unter dieser Annahme.

## Nächste fachliche Arbeit

- Verwendung grosser Firmenrücklagen: zusätzliche Ausschüttungen, Investitionsbedarf und wirtschaftliche Gründe für Reservehaltung getrennt modellieren und mit Gegenläufen prüfen. Keine automatische Rückverteilung zur Erzwingung eines Gleichgewichts.
- Staatliche Budgetanpassung und Zahlungsunfähigkeit: Ausgabenentscheidungen, öffentliche Beschäftigung und die Behandlung alter Verpflichtungen begrenzen beziehungsweise erklären. Bankschuld und sonstige Rückstände gemeinsam sichtbar machen.
- Haushalts-Grundbedarf und ausbleibende Leistungen: individuelle Lücken und Folgen zeigen, ohne aus fehlenden Käufen automatisch Haushaltskredite zu erfinden.

Diese Anpassungen sind nicht stillschweigend in v11 vorgenommen worden. V11 ergänzt den begrenzten Schliessungs-/Ersatzmechanismus und macht die bestehende Langzeitgrenze messbar.

## Wiederholen

Vom Repository-Stamm mit eingerichteter Python-Umgebung:

```sh
poc/.venv/bin/python poc/scripts/stress_crisis.py --months 600
```

Der Standard schreibt neue Ergebnisse in die ignorierte lokale Prüfablage `.framework-review/crisis-long-horizon.json`. Mit `--output` kann ein anderer Zielpfad angegeben werden. Die veröffentlichte datierte Ergebnistabelle wird dadurch nicht überschrieben. Die Grafikoberfläche zeigt die letzten 36 Monate; das Langzeitprotokoll enthält alle 600 Monatswerte pro Lauf.
