# Originalexporte

Hier die verfügbaren Dateien unverändert ablegen. Die Namen sind Vorschläge; es müssen nicht alle Formate verfügbar sein.

| Datei | Zweck |
|---|---|
| `report.md` oder `report.pdf` | Generierter Ergebnisbericht |
| `actions.jsonl`, `actions.json` oder `actions.csv` | Agentenaktionen mit Plattform, Runde, Zeit, Akteur und Inhalt |
| `graph.json` | Wissensgraph mit Knoten und Beziehungen |
| `config.json` | Tatsächliche Laufkonfiguration |
| `profiles.json` | Verwendete Agentenprofile |
| `status.json` | Abschließender Serverstatus, möglichst je Plattform |
| `logs.txt` | Fehler, Warnungen, Start-/Endmeldungen und Abbruchursachen |

Abweichende Originalnamen erhalten und in `../run.json` unter `exports` eintragen. Bei mehreren Exportständen Unterordner mit Exportdatum verwenden. Fehlende Dateien als fehlend dokumentieren; keine Platzhalter als echte Ergebnisdateien anlegen.

Bitte keine Zugangstokens, Sitzungs-Cookies oder Passwörter in die Ablage übernehmen.
