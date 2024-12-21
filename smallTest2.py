from vboxAutomation import VirtualBoxAutomation, installPostgreSQL, installPackage, executeCommand, runKeyboardCommand, ModifyFiles
import subprocess
import logging

# Logging konfigurieren
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)



vbox = VirtualBoxAutomation()

print(vbox.VM_NAME)
print(vbox.USERNAME)
print(vbox.PASSWORD)

vboxmanage_path = VirtualBoxAutomation()._get_vboxmanage_path()

"""
installPostgreSQL(
    vm_name="ForensicVM",
    username="forensicuser",
    password="password123",
    external_access=False
)

installPackage(
    vm_name="ForensicVM",
    username="forensicuser",
    password="password123",
    package="tilix"
)

# funktioniert für alleinstehende Pakete
# für Pakete die erst ein wget oder etwas anderes benötigen müsste noch eine Funktion erstellt werden

executeCommand(
    vm_name="ForensicVM",
    username="forensicuser",
    password="password123",
    user_commands=["wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb",
                   "dpkg -i google-chrome-stable_current_amd64.deb"]
)

# natürlich können damit auch einzelne Pakete installiert werden
# Befehle werden alle mit su -c ausgeführt
"""


modifier = ModifyFiles()
modifier.createFile(vm_name="ForensicVMX",
                    username="forensicuserb",
                    password="password123",
                    filename="test",
                    file_type="txt",
                    path_to_file="/home/forensicuserb",
                    content="Hallo ich bein ein Text. Wenn du mich in Autopsy findest, war das Skript erfolgreich",
                    operation="delete") # --- hierfür können die Optionen: delete, edit, create verwendet werden ---











