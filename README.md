- das ganze ist im DOKU Ordner ausführlich dokumentiert


- Mega Link
- Volltextbeschreibung, was das Ganze eigentlich macht

Für virtuelle Maschinen gibt es viele verschiedene Anwendungen. Ein großer Vorteil ist die Speicherung eines ganzen Systems innerhalb einer einzigen Datei. Im Falle von VirtualBox handelt es sich dabei um eine .vdi. Das ermöglicht eine relativ einfache Exportierung, um damit eine forensiche Datenanalyse durchzuführen. Dabei ist es wichtig, dass neu auszubildende Forensiker geschult werden, solche Images zu analysieren. Jedoch ist die manuelle Erstellung von Images recht zeitaufwendig und es kann immer passieren, dass die Images trotz einheitlicher Erstellung Unterschiede aufweisen. Deswegen bietet es sich an, den Prozess der Erstellung sowie Modifizierung zu automatisieren. Das bietet dann die Möglichkeit, diesen Vorgang zu vereinheitlichen um immer wieder ein identisches frisches Image erzeugen zu können. Dies ist nicht nur für eine forensiche Analyse interessant, sondern auch für Leute, die oft mit Virtuellen Maschinen arbeiten und nicht immer eigenständig Images erzeugen wollen. Diese eher "sporadische" Implementierung, versucht, genau diese Aufgabe umzusetzen und den Erstellungsprozess zu vereinheitlichen.

Vorab soll erwähnt werden, dass die Implementierung bisher nur für eine bestimmte Linux Distribution getestet wurde (
