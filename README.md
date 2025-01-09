- die ausführliche Dokumentation und wie die Funktionen zu verwenden sind, findet sich im DOKU Ordner

## vBoxPackage 

Für virtuelle Maschinen gibt es zahlreiche Anwendungen, wobei ein großer Vorteil darin besteht, ein komplettes System in einer einzigen Datei zu speichern. Bei VirtualBox handelt es sich dabei um eine .vdi-Datei. Dies ermöglicht eine relativ einfache Exportierung, beispielsweise für forensische Datenanalysen.

Insbesondere für die Ausbildung angehender Forensiker ist es entscheidend, dass sie geschult werden, solche Images zu analysieren. Die manuelle Erstellung von Images ist jedoch zeitaufwendig und kann trotz einheitlicher Erstellung zu Inkonsistenzen führen. Deshalb liegt es nahe, den Prozess der Erstellung und Modifikation zu automatisieren. Dadurch kann der Vorgang standardisiert werden, um jederzeit ein identisches, frisches Image zu erzeugen. Dies ist nicht nur für forensische Analysen relevant, sondern auch für Anwender, die regelmäßig mit virtuellen Maschinen arbeiten und nicht jedes Mal eigenständig Images erstellen möchten. Das vorgestellte Tool zielt darauf ab, diesen Prozess zu vereinfachen und zu vereinheitlichen.

Es sei angemerkt, dass die Implementierung bislang nur für eine spezifische Linux-Distribution getestet wurde (xubuntu-22.04.2-desktop-amd64). Anpassungen für weitere Distributionen oder Betriebssysteme sind notwendig, um die Bibliothek weiter zu optimieren. Der Kern der Bibliothek ist das Skript ./vboxAutomation/createVM.py, das eine unbeaufsichtigte Installation mithilfe von VBoxManage ermöglicht. Ergänzende Funktionen beinhalten die Installation von PostgreSQL und MySQL sowie beliebiger weiterer Pakete. Zudem können Scancodes direkt an die VM gesendet werden, um Tastatureingaben zu simulieren.

Die Verwendung von VBoxManage hinterlässt bei der Installation kaum Spuren. Mithilfe von Scancodes oder durch das Erstellen und Löschen von Dateien können zudem forensische Spuren automatisiert generiert werden. Obwohl diese Funktionalitäten aktuell noch begrenzt sind, lassen sie sich beliebig erweitern.

Zusammengefasst bietet die Bibliothek folgende Funktionen:

- Erstellung eines leeren Xubuntu-Images
- Automatische Zuweisung zu einem NAT-Netzwerk
- Festlegen von Port-Forwarding-Regeln für SSH-Zugriff
- Installation von SSH
- Installation von MySQL und Befüllen der Datenbank mit Beispieldaten
- Installation von PostgreSQL
- Installation beliebiger Pakete
- Ausführen von Befehlssequenzen auf der VM
- Erstellen, Bearbeiten und Löschen von Dateien
- Umwandlung von Strings in Hexcodes (siehe smallTest3.py)
- Verwendung dieser Hexcodes zur Simulation von Tastatureingaben in beliebigen Anwendungen auf der VM (bisher für Firefox getestet)

Beispiele für Images, die mit diesen Funktionen erstellt wurden, befinden sich im unten stehenden Link. Dazu gehört ein vollständig leeres Image sowie ein Image, auf dem die meisten der oben genannten Funktionen getestet wurden.

(Hier den Link einfügen)
