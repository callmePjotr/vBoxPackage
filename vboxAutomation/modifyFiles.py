import subprocess
import logging
import sys
from pathlib import Path
from typing import List
import time



# Logging konfigurieren
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class ModifyFiles:
    def __init__(
        self,
        vm_name="ForensicVMC",
        username="forensicuserb",
        password="password123",
        filename="i_am_a_file",
        file_type="txt",
        path_to_file="/home/forensicuser",
        operation="create", # options: create, delete, edit
        content="Hallo ich bein ein Text. Wenn du mich in Autopsy findest, war das Skript erfolgreich" # hier einfach einen String übergeben, der ins File soll
    ):
        self.vm_name = vm_name
        self.USERNAME = username
        self.PASSWORD = password
        self.FILENAME = filename
        self.FILETYPE = file_type
        self.FILEPATH = path_to_file
        self.OPERATION = operation
        self.CONTENT = content
        self.vboxmanage_path = self._get_vboxmanage_path()


    def _get_vboxmanage_path(self) -> Path:
        """Ermittelt den korrekten Pfad zu VBoxManage basierend auf dem Betriebssystem."""
        if sys.platform == "win32":
            return Path("C:/Program Files/Oracle/VirtualBox/VBoxManage.exe")
        elif sys.platform == "linux":
            return Path("/usr/bin/VBoxManage")
        elif sys.platform == "darwin":
            return Path("/usr/local/bin/VBoxManage")
        else:
            raise OSError(f"Nicht unterstütztes Betriebssystem: {sys.platform}")

    def run_commands(self, commands: List[str]):
        """
        Führt eine Liste von Shell-Befehlen aus.

        :param commands: Liste der auszuführenden Befehle.
        """
        path = self.vboxmanage_path
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

    def createFile(
            self,
            vm_name: str,
            username: str,
            password: str,
            filename: str,
            file_type: str,
            path_to_file: str,
            content: str,
            operation="create"
    ):
        create_file = f"{filename}.{file_type}"
        full_path = f"{path_to_file}/{create_file}"

        commands = [
            f'guestcontrol {vm_name} run --exe /bin/bash --username {username} --password {password} '
            f'-- /bin/bash -c "echo {password} | su -c \'mkdir -p {path_to_file}\'"',
            f'guestcontrol {vm_name} run --exe /bin/bash --username {username} --password {password} '
            f'-- /bin/bash -c "echo {password} | su -c \'echo \\"{content}\\" > {full_path}\'"',
            f'guestcontrol {vm_name} run --exe /bin/bash --username {username} --password {password} '
            f'-- /bin/bash -c "echo {password} | su -c \'chmod 644 {full_path}\'"'
        ]

        if operation == "create":
            logger.info("Erstelle Datei mit Inhalt...")
            self.run_commands(commands)
        elif operation == "delete":
            logger.info("Lösche Datei...")
            delete_command = [
                f'guestcontrol {vm_name} run --exe /bin/bash --username {username} --password {password} '
                f'-- /bin/bash -c "echo {password} | su -c \'rm -f {full_path}\'"'
            ]
            self.run_commands(delete_command)
        elif operation == "edit":
            logger.info("Bearbeite Datei...")
            edit_command = [
                f'guestcontrol {vm_name} run --exe /bin/bash --username {username} --password {password} '
                f'-- /bin/bash -c "echo {password} | su -c \'echo \\"{content}\\" > {full_path}\'"'
            ]
            self.run_commands(edit_command)


        """
        kann natürlich auch mit putscancodes gesteuert werden
        erweiterbares Beispiel: 
        
        path = self.vboxmanage_path
        # hier kommt das Speichern und Verlassen von Nano
        logger.info("Drücke Strg+S zum Speichern...")
        subprocess.run(f'"{path}" controlvm {vm_name} keyboardputscancode 1D', shell=True)  # Ctrl drücken
        subprocess.run(f'"{path}" controlvm {vm_name} keyboardputscancode 1F', shell=True)  # S drücken
        time.sleep(0.1)

        logger.info("Lasse die Tasten wieder los...")
        subprocess.run(f'"{path}" controlvm {vm_name} keyboardputscancode 9F', shell=True)  # S loslassen
        subprocess.run(f'"{path}" controlvm {vm_name} keyboardputscancode 9D', shell=True)  # Ctrl loslassen
        time.sleep(0.1)

        logger.info("Drücke Strg+X zum verlassen von Nano...")
        subprocess.run(f'"{path}" controlvm {vm_name} keyboardputscancode 1D', shell=True)  # Ctrl drücken
        subprocess.run(f'"{path}" controlvm {vm_name} keyboardputscancode 2D', shell=True)  # X drücken
        time.sleep(0.1)

        logger.info("Lasse die Tasten wieder los...")
        subprocess.run(f'"{path}" controlvm {vm_name} keyboardputscancode AD', shell=True)  # X loslassen
        subprocess.run(f'"{path}" controlvm {vm_name} keyboardputscancode 9D', shell=True)  # Ctrl loslassen
        time.sleep(0.1)
        """


