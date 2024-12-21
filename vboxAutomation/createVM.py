import subprocess
import os
import sys
import logging
from pathlib import Path
from typing import Tuple, Optional, Dict

# TODO Netzwerkadapter auf Brücke ändern
# TODO vorher noch zwei Befehle nach dem Erstellen ausführen:
# sudo apt install openssh-server
# sudo ufw allow ssh

# Logging konfigurieren
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class VirtualBoxAutomation:
    IP_MAP_FILE = Path("old_getVm_IP.txt")  # Datei für die IP-Zuweisung
    BASE_NETWORK = "10.0.2."  # Basis für IP-Adressen
    START_IP = 16  # Erste verfügbare IP (z. B. 10.0.2.2)
    END_IP = 254  # Letzte verfügbare IP

    """
        def __init__(
        self,
        vm_name="ForensicVMC",
        username="forensicuser",
        password="password123"
        iso_path="C:/Users/llk02/Downloads/xubuntu-22.04.2-desktop-amd64.iso"
    ):
        self.VM_NAME = vm_name
        self.USERNAME = username
        self.PASSWORD = password
        self.ISO_PATH = iso_path
        
        - init lässt sich ganz einfach anpassen
        - so hat man die volle Kontrolle über die Parameter, auch beim Aufruf
    """

    def __init__(self):
        # Grundlegende Konfiguration
        self.VM_NAME = "ForensicVMX"
        self.OSTYPE = "Ubuntu_64"
        self.ISO_PATH = Path("C:/Users/llk02/Downloads/xubuntu-22.04.2-desktop-amd64.iso")
        self.VM_BASE_PATH = Path("/VMs")
        self.HDD_PATH = self.VM_BASE_PATH / f"{self.VM_NAME}.vdi"

        # Pfad zur VBoxGuestAdditions.iso
        self.GUEST_ADDITIONS_ISO = Path("C:/Program Files/Oracle/VirtualBox/VBoxGuestAdditions.iso")

        # VM-Spezifikationen
        self.RAM_SIZE = 2048
        self.VRAM_SIZE = 16
        self.CPU_COUNT = 2
        self.HDD_SIZE = 20000  # in MB

        # Benutzereinstellungen
        self.USERNAME = "forensicuserb"
        self.PASSWORD = "password123"
        self.TIMEZONE = "Europe/Berlin"
        self.HOSTNAME = f"{self.VM_NAME}.local"  # Korrigiert: Vollständiger Hostname mit Domain

        # VBoxManage Pfad ermitteln
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

    def check_prerequisites(self) -> bool:
        """Überprüft alle Voraussetzungen vor der Installation."""
        try:
            # Prüfe VBoxManage
            if not self.vboxmanage_path.exists():
                logger.error(f"VBoxManage nicht gefunden unter: {self.vboxmanage_path}")
                return False

            # Prüfe ISO-Datei
            if not self.ISO_PATH.exists():
                logger.error(f"ISO-Datei nicht gefunden: {self.ISO_PATH}")
                return False

            # Prüfe Zielverzeichnis
            self.VM_BASE_PATH.mkdir(parents=True, exist_ok=True)

            # Prüfe ob VM bereits existiert
            stdout, _ = self._run_command("list vms")
            if self.VM_NAME in stdout:
                logger.error(f"VM mit Namen {self.VM_NAME} existiert bereits")
                return False

            return True

        except Exception as e:
            logger.error(f"Fehler bei der Überprüfung der Voraussetzungen: {e}")
            return False

    def create_vm(self) -> bool:
        """Erstellt und konfiguriert die komplette VM."""
        try:
            # Prüfe Voraussetzungen
            if not self.check_prerequisites():
                return False

            steps = [
                (self._create_base_vm, "Erstelle Basis-VM"),
                (self._create_hard_disk, "Erstelle Festplatte"),
                (self._configure_hardware, "Konfiguriere Hardware"),
                (self._configure_storage, "Konfiguriere Storage"),
                (self._configure_network, "Konfiguriere Netzwerk"),
                (self._setup_unattended_install, "Konfiguriere unattended Installation"),
                (self._start_vm, "Starte VM")
            ]

            for step_func, step_description in steps:
                logger.info(f"Starte: {step_description}")
                step_func()
                logger.info(f"Abgeschlossen: {step_description}")

            return True

        except Exception as e:
            logger.error(f"Fehler bei der VM-Erstellung: {e}")
            self._cleanup_on_failure()
            return False

    def _create_base_vm(self):
        self._run_command(f'createvm --name "{self.VM_NAME}" --ostype "{self.OSTYPE}" --register')

    def _create_hard_disk(self):
        self._run_command(f'createhd --filename "{self.HDD_PATH}" --size {self.HDD_SIZE}')

    def _configure_hardware(self):
        self._run_command(
            f'modifyvm "{self.VM_NAME}" '
            f'--memory {self.RAM_SIZE} '
            f'--vram {self.VRAM_SIZE} '
            f'--cpus {self.CPU_COUNT} '
            '--graphicscontroller vmsvga '
            '--acpi on '
            '--ioapic on '
            '--boot1 dvd --boot2 disk --boot3 none --boot4 none'
        )

    def _configure_storage(self):
        self._run_command(f'storagectl "{self.VM_NAME}" --name "IDE Controller" --add ide')
        self._run_command(f'storageattach "{self.VM_NAME}" --storagectl "IDE Controller" '
                          f'--port 0 --device 0 --type hdd --medium "{self.HDD_PATH}"')
        self._run_command(f'storageattach "{self.VM_NAME}" --storagectl "IDE Controller" '
                          f'--port 1 --device 0 --type dvddrive --medium "{self.ISO_PATH}"')

        # Füge Konfiguration für VBoxGuestAdditions.iso hinzu
        self._run_command(f'storageattach "{self.VM_NAME}" --storagectl "IDE Controller" '
                          f'--port 1 --device 1 --type dvddrive --medium "{self.GUEST_ADDITIONS_ISO}"')

    """
    das Netzwerk kann natürlich bei Bedarf so angepasst werden wie es gewünscht ist, also auch mit einem variablen Namen oder einem 
    anderen Adressbereich
    
    im Folgenden ist das Gnaze mit der statischen IP-Zuweisung, vergebene Adressen werden in eine .txt gespeichert
    """

    def load_ip_map(self) -> Dict[str, str]:
        """Lädt die bestehende IP-Zuordnung aus einer Datei."""
        ip_map = {}
        if self.IP_MAP_FILE.exists():
            with self.IP_MAP_FILE.open("r") as file:
                for line in file:
                    vm_name, ip_address = line.strip().split(",")
                    ip_map[vm_name] = ip_address
        return ip_map

    def save_ip_map(self, ip_map: Dict[str, str]):
        """Speichert die aktuelle IP-Zuordnung in eine Datei."""
        with self.IP_MAP_FILE.open("w") as file:
            for vm_name, ip_address in ip_map.items():
                file.write(f"{vm_name},{ip_address}\n")

    def get_next_available_ip(self, ip_map: Dict[str, str]) -> str:
        """Ermittelt die nächste verfügbare IP-Adresse."""
        used_ips = set(ip_map.values())
        for last_octet in range(self.START_IP, self.END_IP + 1):
            candidate_ip = f"{self.BASE_NETWORK}{last_octet}"
            if candidate_ip not in used_ips:
                return candidate_ip
        raise ValueError("Keine verfügbaren IP-Adressen im Netzwerkbereich.")





    def _configure_network(self):
        # Check if NAT Network exists, create if not
        try:
            stdout, _ = self._run_command('list natnetworks')
            nat_network_exists = 'ForensicNetwork' in stdout
        except Exception:
            nat_network_exists = False

        # Create NAT Network if it doesn't exist
        if not nat_network_exists:
            self._run_command('natnetwork add --netname ForensicNetwork --network 10.0.2.0/24 --enable')

        # Configure VM to use NAT Network
        self._run_command(f'modifyvm "{self.VM_NAME}" --nic1 natnetwork --nat-network1 ForensicNetwork')

    def _setup_unattended_install(self):
        """
        hier muss überprüft werden ob die IP belegt ist
        :return:
        """
        ip_map = self.load_ip_map()

        # Prüfen, ob die VM bereits eine IP-Adresse hat
        if self.VM_NAME in ip_map:
            ip_address = ip_map[self.VM_NAME]
            logger.info(f"VM {self.VM_NAME} hat bereits eine IP-Adresse: {ip_address}")
        else:
            # Nächste verfügbare IP-Adresse holen
            ip_address = self.get_next_available_ip(ip_map)
            ip_map[self.VM_NAME] = ip_address
            self.save_ip_map(ip_map)
            logger.info(f"VM {self.VM_NAME} wird die IP-Adresse {ip_address} zugewiesen.")

        self._run_command(
            f'unattended install "{self.VM_NAME}" '
            f'--user="{self.USERNAME}" '
            f'--password="{self.PASSWORD}" '
            f'--full-user-name="{self.USERNAME}" '
            f'--install-additions '  # Installation der VBoxGuestAdditions
            f'--time-zone="{self.TIMEZONE}" '
            '--locale="de_DE" '
            '--country="DE" '
            f'--hostname="{self.HOSTNAME}" '
            f'--iso="{self.ISO_PATH}" '
        )

    def _start_vm(self):
        self._run_command(f'startvm "{self.VM_NAME}"')

    def _cleanup_on_failure(self):
        """Räumt bei Fehlern auf."""
        try:
            # Versuche VM zu löschen falls sie existiert
            self._run_command(f'unregistervm "{self.VM_NAME}" --delete')
        except:
            pass

        # Versuche Festplattendatei zu löschen
        try:
            if self.HDD_PATH.exists():
                self.HDD_PATH.unlink()
        except:
            pass


if __name__ == "__main__":
    vbox = VirtualBoxAutomation()
    if vbox.create_vm():
        logger.info("VM-Erstellung erfolgreich abgeschlossen")
    else:
        logger.error("VM-Erstellung fehlgeschlagen")