# Staatsfinanzierung und Liquiditätspolitik · Modell v9

Stand: 3. November 2026. Alle Beträge, Ziele und Regeln sind illustrative Annahmen. Keine Kalibrierung oder Beschreibung realer Staatsschuldenpolitik. Ergänzt [Unternehmen](COMPANY_MODEL.md), [Bankbilanz](BANKING_MODEL.md), [Preise](PRICES_MODEL.md) und [Leitzinsregeln](RATES_MODEL.md). Elf Akteure; der normale Lauf hat keine automatische Monatsgrenze.

Seit V13 ergänzt die [anpassende Budgetregel](PUBLIC_BUDGET_MODEL.md) die hier beschriebene Bankfinanzierung. Im Referenzmodus bleibt die bisherige Ausgabenregel erhalten.

## Kasse, Haushalt und Schuld

Die Anfangskasse beträgt weiter 80.000 €. Sie wird nicht mehr am Monatsende automatisch wiederhergestellt. Der zahlungsbezogene Haushaltssaldo ist:

`erhaltene Steuern − bezahlte öffentliche Löhne − Transfers − Beschaffung − bezahlte Staatszinsen`.

Kreditaufnahme ist Finanzierung, keine Steuereinnahme. Tilgung ist Finanzierung, kein laufender Staatsverbrauch. Tatsächlich unbezahlte Lohnansprüche sind eigene Verpflichtungen und werden nicht als bezahlte Ausgaben ausgegeben. Die reine Kasse sagt weder etwas über den Haushaltssaldo noch über die Staatsschuld aus.

## Begrenztes Liquiditätsziel

Am Monatsbeginn werden geplante Primärausgaben festgehalten: öffentliche Arbeitsverhältnisse × 2.400 € + unbeschäftigte Haushalte × 1.000 € Transfers + zweimal 1.200 € Beschaffungsbudget. Dazu kommen die neuen Monatszinsen auf die festen Anfangsrestschulden. Standardziel ist eine Ausgabenperiode:

`Reserveziel = 1 × (geplante Primärausgaben + neue Monatszinsen)`.

Anfangs entspricht das 7.200 €. Unbezahlte alte Ansprüche sind getrennt sichtbar; sie sind nicht nochmals als neue Monatszinsen im Ziel enthalten. Eine veränderte Beschäftigung kann den Transferplan und damit das nächste Monatsziel ändern. Planung ist keine Zusage, dass jede vorgesehene Beschaffung auch geliefert oder bezahlt wird.

Beim Abschluss nach den Unternehmenssteuern und einer möglichen Zinsnachzahlung:

1. Liegt die tatsächliche Kasse unter dem Ziel, wird nur die fehlende Ziel-Liquidität angefragt, begrenzt durch Kreditrahmen und positives Bankkapital.
2. Liegt die Kasse über dem Ziel und besteht Schuld, darf nur der darüber verfügbare Betrag tilgen. Älteste Kreditbeträge werden zuerst getilgt.
3. Sonst bleibt das verbleibende Geld auf dem Konto. Ein Überschuss unterhalb des Ziels führt nicht automatisch zur Tilgung; vorhandenes Guthaben oberhalb des Ziels kann umgekehrt auch bei einem Monatsdefizit bestehende Schuld zurückführen.

Die Reserve ist kein gesperrtes Konto. Laufende Ausgaben dürfen sie benutzen. Fehlende Zahlungsmittel für eine tatsächlich anstehende Zahlung können untermonatlich vorfinanziert werden; nicht verfügbare Ware löst keinen Beschaffungskredit aus. Diese Kredite sind beim Abschluss bereits in der Kasse enthalten. Der Abschluss finanziert daher nicht erneut denselben ursprünglichen Fehlbetrag.

Die eigene Annahme von einem Ausgabenmonat ist kein empirisch bestimmter optimaler Puffer. Für kontrollierte Offline-Vergleiche sind null bis sechs ganze Ausgabenmonate und eine andere Anfangskasse möglich. Die normale Oberfläche startet mit einem Monat und 80.000 €.

## Kreditgrenze und echte Zahlungsgrenzen

Eine Geschäftsbank kann insgesamt höchstens 50.000 € ausstehenden Staatskredit halten. Kredit erhöht Staatsguthaben, Staatsschuld und Bankforderung gleich hoch; Bankkapital wird nicht ausgezahlt. Die Bankbilanz und die Einlagenbrücke erfassen Maschinen- und Staatskredite gemeinsam.

Ein verfehltes Reserveziel ist eine Ziellücke, nicht automatisch eine unbezahlte Rechnung. Erst fehlende Zahlungsmittel bei konkreten Zahlungen erzeugen tatsächliche offene Lohnansprüche oder Zinsrückstände. Bei ausgeschöpftem Kreditrahmen kann vorhandenes Guthaben weitere Ausgaben bezahlen. Ein bestehendes Arbeitsverhältnis bedeutet nicht zwingend vollständige Lohnzahlung. Die Oberfläche zeigt öffentliche Lohnansprüche und Zinsrückstände ausdrücklich getrennt von der Reserve-Ziellücke.

Für offene Lohnansprüche besteht weiterhin keine allgemeine automatische Nachzahlungsabwicklung. Spätere Steuereinnahmen lösen deshalb nicht stillschweigend alle alten Ansprüche auf. Auch Insolvenzverfahren, Ausgabenkürzungen, Steueranpassungen, Schuldenrestrukturierung und politische Entscheidungen werden nicht automatisch ergänzt. Lange Läufe können gerade diese Modellgrenzen offenlegen.

## Zinsen und Tilgung

Neue Staatskreditbeträge erhalten bei Gutschrift den geltenden Modell-Leitzins plus einen Prozentpunkt und behalten diesen Festzins. Neue Zinsen fallen erst im Folgemonat an. Anfangsrestschulden und Zinsrückstände werden am Monatsbeginn festgehalten. Zinsen werden aus jedem Vertragsbetrag berechnet, die Summe wird einmal auf ganze Cents abgerundet und die Centreste werden nachvollziehbar zugeordnet; [Vertragsregeln](RATES_MODEL.md).

Zinsen werden nur einmal monatlich neu belastet. Spätere Steuern können bestehende Zinsrückstände beim Abschluss bezahlen. Es gibt keinen gesonderten Strafzins auf Rückstände; kreditfinanzierte Zinszahlungen erhöhen jedoch die Restschuld. Die Bank schüttet tatsächlich erhaltene Zinsen wie bisher an Haushalte aus. Tilgung senkt Kundenguthaben, Staatsschuld und Bankforderung ohne Bankertrag. Die Schuld wird durch das Weiterlaufen nicht erlassen.

## Darstellung und Export

**Staat → Details öffnen** zeigt aktuelle Kasse, Reserveziel, Schuld und Kasse abzüglich Bankschuld. Letzteres ist keine vollständige Staatsvermögensbilanz. Vier Diagramme stellen Kasse mit Ziel, Haushaltssaldo, Schuld und monatliche Zinszahlungen nebeneinander dar. Jedes hat eine eigene Euro-Skala. Eine gemeinsame Monatsauswahl zeigt die Abschlussentscheidung, Kasse vor Entscheidung, angefragten Zielbedarf, Tilgungskapazität, tatsächliche Finanzierung und verbleibende Ziellücke.

Die letzten 36 Abschlüsse bilden das Darstellungsfenster. Der vollständige Export enthält alle Monatsentscheidungen, Vertragsbeträge und Buchungen. Untermonatliche Zustände sind als Zwischenstände erkennbar. Kredit-, Zins- und Tilgungspfeile zeigen echte Buchungen; historische Monatsentscheidungen werden nicht nachträglich überschrieben.

## Prüfung und Grenzen

Konten- und Schuldbrücken: `Endkasse = Anfangskasse + Haushaltssaldo + Kredite − Tilgung`; `Endschuld = Anfangsschuld + Kredite − Tilgung`. Zusätzlich werden Zielformel, Abschlussentscheidung, Zwischenkredite, Zinsbasis, FIFO-Tilgung, Bankgegenforderung, öffentliche Rückstände und vollständiger Export geprüft. [Unabhängiger V9-Audit](../qa/fiscal-policy-v9-plausibility.md). Ältere V6–V8-Audits dokumentieren ihre jeweiligen Fassungen unverändert.

Die frühere Regel bewahrte die gesamte Anfangskasse durch vorrangige Defizitfinanzierung. V9 ersetzt diese Finanzierungsentscheidung; veränderte Ergebnisse sind daher nicht unmittelbar Belege eines anderen externen Schocks. Historische Ergebnisse behalten ihre Versionszuordnung. Korrekte Buchhaltung ist keine empirische Validierung oder Garantie langfristiger Stabilität.
