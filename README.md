- die ausführliche Dokumentation und wie die Funktionen zu verwenden sind, findet sich im DOKU Ordner

## vBoxPackage 

Für virtuelle Maschinen gibt es zahlreiche Anwendungen, wobei ein großer Vorteil darin besteht, ein komplettes System in einer einzigen Datei zu speichern. Bei VirtualBox handelt es sich dabei um eine .vdi-Datei. Dies ermöglicht eine relativ einfache Exportierung, beispielsweise für forensische Datenanalysen.

Insbesondere für die Ausbildung angehender Forensiker ist es entscheidend, dass sie geschult werden, solche Images zu analysieren. Die manuelle Erstellung von Images ist jedoch zeitaufwendig und kann trotz einheitlicher Erstellung zu Inkonsistenzen führen. Deshalb liegt es nahe, den Prozess der Erstellung und Modifikation zu automatisieren. Dadurch kann der Vorgang standardisiert werden, um jederzeit ein identisches, frisches Image zu erzeugen. Dies ist nicht nur für forensische Analysen relevant, sondern auch für Anwender, die regelmäßig mit virtuellen Maschinen arbeiten und nicht jedes Mal eigenständig Images erstellen möchten. Das vorgestellte Tool zielt darauf ab, diesen Prozess zu vereinfachen und zu vereinheitlichen.

Es sei angemerkt, dass die Implementierung bislang nur für eine spezifische Linux-Distribution getestet wurde (**xubuntu-22.04.2-desktop-amd64**). Anpassungen für weitere Distributionen oder Betriebssysteme sind notwendig, um die Bibliothek weiter zu optimieren. Der Kern der Bibliothek ist das Skript **./vboxAutomation/createVM.py**, das eine unbeaufsichtigte Installation mithilfe von VBoxManage ermöglicht. Ergänzende Funktionen beinhalten die Installation von PostgreSQL und MySQL sowie beliebiger weiterer Pakete. Zudem können Scancodes direkt an die VM gesendet werden, um Tastatureingaben zu simulieren.

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

- The detailed documentation and how to use the functions can be found in the DOKU folder

## vBoxPackage 

There are numerous applications for virtual machines, with one significant advantage being the ability to store an entire system within a single file. For VirtualBox, this is a .vdi file. This feature facilitates relatively simple exporting, such as for forensic data analysis.

Particularly in the training of future forensic analysts, it is essential to teach them how to analyze such images. However, manually creating images is time-consuming and may lead to inconsistencies despite standardized procedures. Automating the process of creation and modification is therefore a logical step. This approach enables a standardized process, allowing identical, fresh images to be generated repeatedly. This is not only valuable for forensic analysis but also for users who frequently work with virtual machines and wish to avoid manually creating images. The tool presented here aims to simplify and standardize this process.

It should be noted that the implementation has so far been tested on only one specific Linux distribution (**xubuntu-22.04.2-desktop-amd64**). Further adjustments are required to optimize the library for other distributions or operating systems. The core component of the library is the **./vboxAutomation/createVM.py** script, which performs unattended installations using VBoxManage. Additional features include the installation of PostgreSQL and MySQL, as well as any desired packages. Furthermore, scancodes can be sent directly to the VM to simulate keyboard inputs.

Using VBoxManage leaves minimal traces during installation. Scancodes or the creation and deletion of files can also be used to automatically generate forensic artifacts. While these capabilities are currently limited, they can be expanded as needed.

In summary, the library implements the following functionalities:

- Creation of a blank Xubuntu image
- Automatic assignment to a NAT network
- Configuration of port-forwarding rules for SSH access
- Installation of SSH
- Installation of MySQL and populating the database with sample data
- Installation of PostgreSQL
- Installation of standalone packages
- Execution of command sequences on the VM
- Creation, editing, and deletion of files
- Conversion of strings into hex codes (see smallTest3.py)
- Use of these hex codes to simulate keyboard input in any application on the VM (tested with Firefox)

Examples of images created with these functions can be found at the link below. This includes a completely blank image as well as an image on which most of the above scripts have been tested.

(Insert link here)
