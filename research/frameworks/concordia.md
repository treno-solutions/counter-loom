# Concordia · vertiefte Vorauswahl

Stand: 2. November 2026 · Prüfprotokoll 1.0 · Status: `documentation_reviewed` mit lokalem technischem Screen · Eignung: `conditional`.

## Gegenstand und Umfang

[Google DeepMind/Concordia](https://github.com/google-deepmind/concordia), Quellstand `f1d3ae6da20b32f686cefc13458cafc695c3b6a2`, Paketversion 2.4.0, Python ab 3.12, Apache-2.0. In einer getrennten, nicht veröffentlichten Prüfungsumgebung installiert. Kein eigener Anwendungskern entwickelt, keine Produktivumgebung verändert.

140 ausgewählte Upstream-Tests ausgeführt: assoziatives Gedächtnis, Engine-Checkpoints, Forum, asynchroner Forum-Game-Master und Simulations-Checkpoints. Ergebnis: 140 Tests bestanden. Zusätzlich drei eigene Grenzprüfungen mit der echten `ForumState`-Klasse. Alle ohne Sprachmodellaufrufe. Diese Tests sind technische Belege, kein autonomer Persona-Pilot oder Nachweis gesellschaftlicher Realitätsnähe.

[Testergebnis und Umgebung](evidence/concordia-upstream-tests-2026-11-02.json), [Grenzprüfungen](evidence/boundary-checks-2026-11-02.json), [Prüfskript](../../tools/probe_framework_boundaries.py).

## Was gut passt

Concordia bringt generative Personen mit Komponenten für Gedächtnis und situationsbezogenes Handeln mit. Eine Umgebung organisiert Beobachtungen und Folgen. Es existieren bereits Forum-Komponenten mit Beiträgen, Antworten, Bewertungen, privaten Nachrichten und Zustandsablage. Für den sozialen Feed ist deshalb kein vollständiger Neubau notwendig.

Der einfache Personenbaustein verbindet Wahrnehmung der Situation, Selbstverständnis und situationsbezogenes Handeln. Das ist konzeptionell näher an unserem Lernziel als ein bloßes Team professioneller Marktanalysten. Wie überzeugend diese Personen im konkreten Finanzszenario reagieren, bleibt offen.

Primärquellen: [Personenbaustein](https://github.com/google-deepmind/concordia/blob/f1d3ae6da20b32f686cefc13458cafc695c3b6a2/concordia/prefabs/entity/basic.py), [Forum](https://github.com/google-deepmind/concordia/blob/f1d3ae6da20b32f686cefc13458cafc695c3b6a2/concordia/contrib/components/game_master/forum.py), [Forumumgebung](https://github.com/google-deepmind/concordia/blob/f1d3ae6da20b32f686cefc13458cafc695c3b6a2/concordia/prefabs/game_master/async_social_media.py).

## Technische Beobachtungen

- **C01:** Ein Forum zeigt öffentliche Beiträge seinen Teilnehmern. Getrennte Gruppen entstehen nicht automatisch aus der Biografie der Personen. Dafür getrennte Foren oder gezielte Zustellung verwenden.
- **C02:** Private Nachrichten erscheinen in der Benachrichtigung des Empfängers, nicht in der eines unbeteiligten Spielers. Im kleinen Test praktisch bestätigt; kein umfassendes Sicherheits-Audit.
- **C03:** Beiträge und gespeicherte private Gesprächsverläufe überleben einen JSON-Zustands-Export und Wiederimport. Praktisch für Forumzustand bestätigt, nicht mit der Prüfung menschlicher Erinnerung gleichzusetzen.
- Die ausgewählten Upstream-Tests decken weitere Speicher- und Ablaufmechanismen ab. Ein bestandener technischer Test sagt nichts darüber aus, ob eine generierte Meinung durch einen Kontakt kausal verändert wurde.

## Anforderungen R01–R10

| ID | Stand | Grenze / benötigter Nachweis |
|---|---|---|
| R01 | Dokumentiert | Personenbausteine vorhanden, kein fertiger validierter Querschnitt unserer Zielgesellschaft. |
| R02 | Erweiterbar | Komponenten und individuelle Erinnerungen ermöglichen Trennung; unsere Beobachtungsgrößen müssen noch festgelegt werden. |
| R03 | Teilweise technisch geprüft | C01/C02; Gruppen und Brücken müssen explizit eingerichtet werden. |
| R04 | Technische Grundlage geprüft | Forum-Roundtrip und ausgewählte Gedächtnis-/Checkpoint-Tests bestanden; kompletter Workshop-Lauf noch offen. |
| R05 | Offen | Gesprächsbelege möglich; tatsächliche Überzeugungsänderung im Pilot nachweisen. |
| R06 | Technische Grundlage geprüft | Checkpoint-/Wiederherstellungstests bestanden; kontrollierte Vergleichsbedingungen noch nicht ausgeführt. |
| R07 | Begrenzt konfigurierbar | Schritte und Modellaufrufe begrenzen. Die generative Wahrnehmung und Umgebung können viele Aufrufe benötigen; keine Kostenprognose aus den Offline-Tests ableiten. |
| R08 | Technische Grundlage teilweise geprüft | Aktions- und Zustandsbelege vorhanden; Reporter und Fehlerdarstellung unseres Szenarios noch nicht getestet. |
| R09 | Durch Prüfdesign zu ergänzen | Modell erlaubt Quellen-/Annahmentrennung, erzwingt aber keine wissenschaftliche Gültigkeit. |
| R10 | Noch nicht getestet | Bestehende Editor-/Log-Werkzeuge und Forumdarstellung prüfen; ein einfacher Workshop-Ablauf muss eingerichtet werden. |

## Entscheidung

**Vorrangiger Kandidat für den nächsten begrenzten Verhaltenstest.** Die im aktuellen Quellstand vorhandenen Foren- und Speicherbausteine sowie die bestandenen technischen Tests sprechen dafür, zuerst einen kleinen vorhandenen Concordia-Ansatz zu konfigurieren. Das ist keine abgeschlossene Frameworkwahl und kein Einflussnachweis.

Nicht erforderlich: eigene Agentenengine, reale Käufe, freie Internetrecherche oder eine sofort repräsentative Gesamtbevölkerung. Erforderlich: gleichbleibende Ausgangsprofile, zwei Gruppen, gezielte Nachrichtenzustellung, getrennte Vergleichsbedingungen und neutraler Vorher-/Nachher-Abruf. Ein bezahlter Modelllauf ist in dieser Prüfung nicht gestartet worden.
