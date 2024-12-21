from typing import List, Optional
import subprocess
import logging
from pathlib import Path
import sys
import time

# Logging konfigurieren
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def get_vboxmanage_path():
    """Ermittelt den korrekten Pfad zu VBoxManage basierend auf dem Betriebssystem."""
    if sys.platform == "win32":
        return Path("C:/Program Files/Oracle/VirtualBox/VBoxManage.exe")
    elif sys.platform == "linux":
        return Path("/usr/bin/VBoxManage")
    elif sys.platform == "darwin":
        return Path("/usr/local/bin/VBoxManage")
    else:
        raise OSError(f"Nicht unterstütztes Betriebssystem: {sys.platform}")

def run_commands(commands: List[str]):
    """
    Führt eine Liste von Shell-Befehlen aus.

    :param commands: Liste der auszuführenden Befehle.
    """
    path = get_vboxmanage_path()
    for command in commands:
        try:
            logger.info(f"Führe Befehl aus: {command}")
            full_command = f'"{path}" {command}'
            result = subprocess.run(
                full_command,
                shell=True,
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            logger.info(result.stdout.decode())
            if result.stderr:
                logger.warning(result.stderr.decode())
        except subprocess.CalledProcessError as e:
            logger.error(f"Fehler beim Ausführen des Befehls: {e}")
            logger.error(f"Ausgabe: {e.output.decode()}")
            logger.error(f"Fehler: {e.stderr.decode()}")


def installPackage(vm_name: str, username: str, password: str, package: str):

    """
    :param vm_name: Name der Vm, erfordert Initialisierung der Klasse VirtualBoxAutomation
                                 self.VM_NAME
    :param username: Nutzername, self.USERNAME
    :param password: Passwort,   self.PASSWORD
    :param package: String, der ein einzelnes Package enthält
    :return: nothing
    """
    commands = [
        f'guestcontrol {vm_name} run --exe /bin/bash --username {username} --password {password} '
        f'-- /bin/bash -c "echo {password} | su - root -c \'apt-get update -y\'"',

        f'guestcontrol {vm_name} run --exe /bin/bash --username {username} --password {password} '
        f'-- /bin/bash -c "echo {password} | su -c \'apt-get install -y {package}\'"',

        f'guestcontrol {vm_name} run --exe /bin/bash --username {username} --password {password} '
        f'-- /bin/bash -c "echo {password} | su - root -c \'systemctl enable {package}\'"',

        f'guestcontrol {vm_name} run --exe /bin/bash --username {username} --password {password} '
        f'-- /bin/bash -c "echo {password} | su - root -c \'systemctl start {package}\'"'
    ]
    run_commands(commands)

def executeCommand(vm_name: str, username: str, password: str, user_commands: list):

    commands = [
        f'guestcontrol {vm_name} run --exe /bin/bash --username {username} --password {password} '
        f'-- /bin/bash -c "echo {password} | su - root -c \'apt-get update -y\'"'
    ]

    for command in user_commands:
        commands.append(
            f'guestcontrol {vm_name} run --exe /bin/bash --username {username} --password {password} '
            f'-- /bin/bash -c "echo {password} | su -c \'{command}\'"'
        )

    # VBoxManage guestcontrol "<vm_name>" run --exe "/usr/bin/firefox" --username "<username>" --password "<password>" --wait-stdout
    run_commands(commands)

def runKeyboardCommand(vm_name: str, username: str, password: str, scancodes: list):
    commands = []

    # firefox starten
    commands.append(
        f'guestcontrol {vm_name} run --exe "/snap/bin/firefox" --username {username} --password {password} --wait-stdout --putenv "DISPLAY=:0"'
    )

    """
    time.sleep(10)

    # die Scancodes werden dann beim Aufruf der Funktion übergeben
    for code in scancodes:
        commands.append(
            f'controlvm {vm_name} keyboardputscancode {code}'
        )
        time.sleep(0.1)  # Kurze Pause zwischen den Tastendrücken
    """



def get_vboxmanage_path():
    if sys.platform == "win32":
        return Path("C:/Program Files/Oracle/VirtualBox/VBoxManage.exe")
    elif sys.platform == "linux":
        return Path("/usr/bin/VBoxManage")
    elif sys.platform == "darwin":
        return Path("/usr/local/bin/VBoxManage")
    else:
        raise OSError(f"Nicht unterstütztes Betriebssystem: {sys.platform}")


def run_firefox_and_input_scancodes(vm_name: str, username: str, password: str, scancodes: list):
    path = get_vboxmanage_path()
    command = (
        f'"{path}" guestcontrol {vm_name} run --exe "/snap/bin/firefox" '
        f'--username {username} --password {password} --putenv "DISPLAY=:0"'
    )

    try:
        logger.info(f"Starte Firefox auf VM: {vm_name}")

        # Starte Firefox im Hintergrund ohne zu blockieren
        process = subprocess.Popen(
            command,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

        logger.info(f"Firefox-Prozess gestartet. PID: {process.pid}")
        time.sleep(20)

        # Focus auf das Firefox-Fenster mit Alt+Tab (d.h. Alt drücken, dann Tab drücken)
        logger.info("Fokussiere das Firefox-Fenster mit Alt+Tab...")
        subprocess.run(f'"{path}" controlvm {vm_name} keyboardputscancode 38', shell=True)  # Alt drücken
        subprocess.run(f'"{path}" controlvm {vm_name} keyboardputscancode 0F', shell=True)  # Tab drücken
        time.sleep(0.1)

        # Loslassen der Tasten (Alt und Tab)
        subprocess.run(f'"{path}" controlvm {vm_name} keyboardputscancode 8F', shell=True)  # Tab loslassen
        subprocess.run(f'"{path}" controlvm {vm_name} keyboardputscancode B8', shell=True)  # Alt loslassen
        time.sleep(0.1)

        # bis hier funktioniert das alles
        # ab der nächsten Zeile bisher nicht

        # Füge Scancodes für die Adressleiste ein (z.B. Ctrl+L)
        logger.info("Füge Tastenkombination für Adressleiste ein...")
        subprocess.run(f'"{path}" controlvm {vm_name} keyboardputscancode 1D', shell=True)  # Ctrl drücken
        subprocess.run(f'"{path}" controlvm {vm_name} keyboardputscancode 26', shell=True)  # L drücken
        time.sleep(0.1)

        # Lässt die Tasten los
        subprocess.run(f'"{path}" controlvm {vm_name} keyboardputscancode A6', shell=True)  # L loslassen
        subprocess.run(f'"{path}" controlvm {vm_name} keyboardputscancode 9D', shell=True)  # Ctrl loslassen
        time.sleep(1)

        # Scancodes für den Text "Hallo" eingeben
        logger.info("Füge Scancodes für Text ein...")
        for code in scancodes:
            logger.info(f"Sende Scancode: {code}")
            subprocess.run(f'"{path}" controlvm {vm_name} keyboardputscancode {code}', shell=True)
            time.sleep(0.1)  # Kurze Pause zwischen den Tastendrücken

        # und dann noch Enter drücken
        subprocess.run(f'"{path}" controlvm {vm_name} keyboardputscancode 1C', shell=True)  # Enter drücken
        subprocess.run(f'"{path}" controlvm {vm_name} keyboardputscancode 9C', shell=True)  # Enter loslassen
        time.sleep(1)


    except Exception as e:
        logger.error(f"Fehler beim Starten von Firefox und Eingeben der Scancodes: {e}")


# Beispielaufruf der Funktion mit Scancodes für "hi"
scancodes = [
    "23",  # h drücken
    "A3",  # h loslassen
    "17",  # i drücken
    "97"   # i loslassen
]

# gebe hs-wismar ein
hex_list = [
    "23", "A3", "14", "94", "14", "94", "19", "99", "1F", "9F", "2A", "34", "B4", "AA",
    "2A", "08", "88", "AA", "2A", "08", "88", "AA", "11", "91", "11", "91", "11", "91",
    "34", "B4", "23", "A3", "1F", "9F", "35", "B5", "11", "91", "17", "97", "1F", "9F",
    "32", "B2", "1E", "9E", "13", "93", "34", "B4", "20", "A0", "12", "92", "2A", "08", "88", "AA"
]



run_firefox_and_input_scancodes(vm_name="ForensicVM", username="forensicuser", password="password123",scancodes=hex_list)
