- die ausführliche Dokumentation und wie die Funktionen zu verwenden sind, findet sich im DOKU Ordner

## vBoxPackage 

Für virtuelle Maschinen gibt es viele verschiedene Anwendungen. Ein großer Vorteil ist die Speicherung eines ganzen Systems innerhalb einer einzigen Datei. Im Falle von VirtualBox handelt es sich dabei um eine .vdi. Das ermöglicht eine relativ einfache Exportierung, um damit eine forensiche Datenanalyse durchzuführen. Dabei ist es wichtig, dass neu auszubildende Forensiker geschult werden, solche Images zu analysieren. Jedoch ist die manuelle Erstellung von Images recht zeitaufwendig und es kann immer passieren, dass die Images trotz einheitlicher Erstellung Unterschiede aufweisen. Deswegen bietet es sich an, den Prozess der Erstellung sowie Modifizierung zu automatisieren. Das bietet dann die Möglichkeit, diesen Vorgang zu vereinheitlichen um immer wieder ein identisches frisches Image erzeugen zu können. Dies ist nicht nur für eine forensiche Analyse interessant, sondern auch für Leute, die oft mit Virtuellen Maschinen arbeiten und nicht immer eigenständig Images erzeugen wollen. Diese eher "sporadische" Implementierung, versucht, genau diese Aufgabe umzusetzen und den Erstellungsprozess zu vereinheitlichen.

Vorab soll erwähnt werden, dass die Implementierung bisher nur für eine bestimmte Linux Distribution getestet wurde (xubuntu-22.04.2-desktop-amd64). Für weitere Distributionen oder Betriebssysteme, bedarf es noch vielen Anpassungen um die Bibliothek zu verbessern. Der Kernbestandteil dieser Bibliothek ist die **./vboxAutomation/createVM.py**. Dabei handelt es sich um eine Programm, welches einen unattended Install mithilfe von VboxManage durchführt. Weitere Funktionen bieten die Möglichkeit PostgreSQL und MySQl zu installieren, sowie alle gewünschten Pakete. Weiterhin ist es möglich, Scancodes (Definition einfügen von chatGPT) direkt an die VM zu schicken, um Tastatureingaben zu simulieren. 

Durch die Verwendung von VBoxManage werden kaum Spuren bei der Installation hinterlassen. Durch Scancodes, oder das Erstellen und Löschen von Dateien lassen sich auch automatisch forensische Spuren legen. Bisher sind diese Möglichkeiten noch relativ eingescränkt, jedoch beliebig erweiterbar.
Zusammengefasst werden folgende Funktionalitäten implementiert:
- Erstellen eines leeren Xubuntu Images
- Automatische Zuweisung zu einem NAT-Netzwerk
- Festlegen von Port-Forwarding Regeln, um einen Zugriff über SSH zu gewährleisten
- Installation von SSH
- Installation von MySQL
- füllen der MySQL-Datenbank mit Beispieldaten
- Installation von PostgreSQL
- Installation von alleinstehenden Paketen
- Ausführen von beliebigen Befehlsketten auf der VM
- Erstellen, Bearbeiten und Löschen von Dateien
- Umwandlung von Strings in Hexcodes (smallTest3.py)
- Einsetzen und Eingabe dieser Hexcodes in eine beliebige Anwendung auf der VM (simuliert Tastatureingabe, bisher für Firefox)

Beispiele für Images finden sich im unten stehenden Link. Dabei gibt es einmal ein komplett leeres Image, welches automatisch erstellt wurde und ein Image, bei dem die meisten der obigen Skripte getestet wurden.
(hier der Link)
