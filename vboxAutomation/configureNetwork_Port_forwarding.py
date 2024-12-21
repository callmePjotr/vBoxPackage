import subprocess
import logging
from typing import Tuple
import sys
from pathlib import Path
import os

# Logging konfigurieren
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class PortForwarding:
    def __init__(
        self,
        vm_name="ForensicVMC",
        network_name="ForensicNetwork",
        base_ssh_port=10000
    ):
        self.vm_name = vm_name
        self.network_name = network_name
        self.base_ssh_port = base_ssh_port
        self.vboxmanage_path = self._get_vboxmanage_path()
        self.filename = 'used_port_numbers.txt'

    def read_numbers_from_file(self):
        """Liest die Zahlen aus der Datei und gibt sie als Liste zurück."""
        if not os.path.exists(self.filename):
            return []  # Falls die Datei nicht existiert, geben wir eine leere Liste zurück
        with open(self.filename, 'r') as file:
            content = file.read()
            if not content.strip():
                return []
            return list(map(int, content.split(', ')))

    def write_numbers_to_file(self, numbers):
        """Schreibt die Liste von Zahlen in die Datei."""
        with open(self.filename, 'w') as file:
            file.write(', '.join(map(str, numbers)))

    def increment_and_store(self):
        """Liest die Zahlen aus der Datei, erhöht die größte Zahl um 1, und speichert sie zurück."""
        numbers = self.read_numbers_from_file()
        next_number = max(numbers, default=0) + 1
        numbers.append(next_number)
        self.write_numbers_to_file(numbers)
        logger.info(f"Benutzte Portnummern: {numbers}")
        return next_number

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

    def _run_command(self, command: str) -> Tuple[str, str]:
        """Führt einen VBoxManage-Befehl aus und gibt stdout und stderr zurück."""
        try:
            full_command = f'"{self.vboxmanage_path}" {command}'
            logger.debug(f"Ausführe Befehl: {full_command}")  # Logging des Befehls
            process = subprocess.run(
                full_command,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                check=True
            )
            return process.stdout, process.stderr
        except subprocess.CalledProcessError as e:
            logger.error(f"Fehler beim Ausführen des Befehls: {command}")
            logger.error(f"Fehlermeldung: {e.stderr}")
            raise

    def setup_port_forwarding(self, vm_ip, vm_index=0):
        """SSH Port Forwarding für eine VM einrichten"""
        ssh_port = self.increment_and_store()
        ssh_port_as_string = str(ssh_port)

        try:
            # Überprüfe existierende Regeln
            stdout, _ = self._run_command(f'natnetwork list --netname {self.network_name}')
            existing_rule = f"ssh-{self.vm_name+ssh_port_as_string}:tcp:[127.0.0.1]:{ssh_port}:[{vm_ip}]:22"

            if existing_rule in stdout:
                logger.warning(f"Port-Forwarding-Regel existiert bereits: {existing_rule}")
                return False

            # Erstelle Regel, wenn nicht vorhanden
            self._run_command(
                f'natnetwork modify --netname {self.network_name} '
                f'--port-forward-4 "{existing_rule}"'
            )
            logger.info(f"Port Forwarding für {self.vm_name} eingerichtet: Lokaler Port {ssh_port}")
            return ssh_port

        except Exception as e:
            logger.error(f"Fehler beim Port Forwarding: {e}")
            return False
