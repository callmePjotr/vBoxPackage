import subprocess
import logging
from typing import List

# Logging konfigurieren
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

def run_commands(commands: List[str]):
    """
    Führt eine Liste von Shell-Befehlen aus.

    :param commands: Liste der auszuführenden Befehle.
    """
    for command in commands:
        try:
            logger.info(f"Führe Befehl aus: {command}")
            result = subprocess.run(
                command,
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

def installSSH(vm_name: str, username: str, password: str):
    """
    Führt Konfigurationsbefehle auf einer virtuellen Maschine aus.

    :param vm_name: Name der virtuellen Maschine.
    :param username: Benutzername für den Gast.
    :param password: Passwort für den Benutzer.
    """
    commands = [
        f'VBoxManage guestcontrol {vm_name} run --exe /bin/bash --username {username} --password {password} -- /bin/bash -c "echo {password} | su -c \'apt-get update\'"',
        f'VBoxManage guestcontrol {vm_name} run --exe /bin/bash --username {username} --password {password} -- /bin/bash -c "echo {password} | su -c \'apt-get install -y openssh-server\'"',
        f'VBoxManage guestcontrol {vm_name} run --exe /bin/bash --username {username} --password {password} -- /bin/bash -c "echo {password} | su -c \'ufw allow ssh\'"',
        f'VBoxManage guestcontrol {vm_name} run --exe /bin/bash --username {username} --password {password} -- /bin/bash -c "echo {password} | su -c \'systemctl enable ssh\'"',
        f'VBoxManage guestcontrol {vm_name} run --exe /bin/bash --username {username} --password {password} -- /bin/bash -c "echo {password} | su -c \'systemctl start ssh\'"'
    ]
    run_commands(commands)
