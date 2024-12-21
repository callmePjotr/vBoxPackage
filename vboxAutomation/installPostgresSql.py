import subprocess
import logging
from typing import List, Optional
import sys
from pathlib import Path

"""
Hierbei handelt es sich um eine sehr komplexe Funktion, deswegen hier die gängigen Use-Cases:

1. Standardinstallation mit Zugriff von außen für alle
    installPostgreSQL(
        vm_name="UbuntuVM",
        username="user",
        password="pass",
        external_access=True
    )
2. Zugriff von einer bestimmten IP-Adresse erlauben
    installPostgreSQL(
        vm_name="UbuntuVM",
        username="user",
        password="pass",
        external_access=True,
        allowed_ip="192.168.1.100/32"
    )
3. Datenbank und Benutzer erstellen, Zugriff von außen für alle
    installPostgreSQL(
        vm_name="UbuntuVM",
        username="user",
        password="securepassword",  # Passwort wird für VM und PostgreSQL-Nutzer verwendet
        external_access=True,
        db_user="db_user",
        database="meine_datenbank"
    )
4. Datenbank und Benutzer erstellen, Zugriff auf eine spezifische IP beschränken
    installPostgreSQL(
        vm_name="UbuntuVM",
        username="user",
        password="securepassword",
        external_access=True,
        allowed_ip="192.168.1.100/32",
        db_user="db_user",
        database="meine_datenbank"
    )
5. Nur lokale Installation (kein externer Zugriff)
    installPostgreSQL(
        vm_name="UbuntuVM",
        username="user",
        password="pass",
        external_access=False
    )
"""
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


def configurePostgresAccess(vm_name: str, username: str, password: str,
                            external_access: bool = False,
                            allowed_ip: Optional[str] = None,
                            db_user: Optional[str] = None,
                            database: Optional[str] = None):
    commands = []

    # aufgrund von Problemen mit dem Parsen einiger Befehle, wenn su -c verwendet wird, muss der forensicuser zur sudoers Datei hinzugefügt werden,
    # um auch mit sudo BEfehle ausführen zu können
    commands.append(
        f'guestcontrol {vm_name} run --exe /bin/bash --username {username} --password {password} '
        f'-- /bin/bash -c "echo {password} | su -c \'echo \\\"{username} ALL=(ALL) NOPASSWD: ALL\\\" >> /etc/sudoers\'"'
    )
    # Zugriff von außen aktivieren, wenn angegeben
    if external_access:
        commands.append(
            f'guestcontrol {vm_name} run --exe /bin/bash --username {username} --password {password} '
            f'-- /bin/bash -c "echo {password} | su -c \'sed -i \"s/#listen_addresses.*/listen_addresses = ' * '/\" /etc/postgresql/*/main/postgresql.conf\'"'
        )

        # pg_hba.conf-Eintrag hinzufügen
        if allowed_ip:
            access_rule = f"host {database or 'all'} {db_user or 'all'} {allowed_ip} md5"
        else:
            access_rule = "host all all 0.0.0.0/0 md5"

        commands.append(
            f'guestcontrol {vm_name} run --exe /bin/bash --username {username} --password {password} '
            f'-- /bin/bash -c "echo {access_rule} | sudo -S tee -a /etc/postgresql/*/main/pg_hba.conf"'
        )
    else:
        # Wenn kein externer Zugriff, nur lokalen Zugriff erlauben
        access_rule = "host all all 127.0.0.1/32 md5"
        commands.append(
            f'guestcontrol {vm_name} run --exe /bin/bash --username {username} --password {password} '
            f'-- /bin/bash -c "echo {access_rule} | sudo -S tee -a /etc/postgresql/*/main/pg_hba.conf"'
        )

    # PostgreSQL neu starten, damit die Änderungen wirksam werden
    commands.append(
        f'guestcontrol {vm_name} run --exe /bin/bash --username {username} --password {password} '
        f'-- /bin/bash -c "echo {password} | su -c \'systemctl restart postgresql\'"'
    )

    run_commands(commands)

def executeSQL(vm_name: str, username: str, password: str, sql_commands: List[str]):
    """
    Führt SQL-Befehle in der PostgreSQL-Datenbank aus.

    :param vm_name: Name der virtuellen Maschine.
    :param username: Benutzername für den Gast.
    :param password: Passwort für den Benutzer.
    :param sql_commands: Liste der auszuführenden SQL-Befehle.
    """
    sql_script = "\n".join(sql_commands)
    command = (
        f'guestcontrol {vm_name} run --exe /bin/bash --username {username} --password {password} '
        f'-- /bin/bash -c "echo {password} | su -c \'psql -U postgres -c \"\"\"{sql_script}\"\"\"\'"'
    )
    run_commands([command])

def installPostgreSQL(vm_name: str, username: str, password: str,
                      external_access: bool = False,
                      allowed_ip: Optional[str] = None,
                      db_user: Optional[str] = None,
                      database: Optional[str] = None):
    """
    Installiert PostgreSQL auf einer virtuellen Maschine und konfiguriert den Zugriff.

    :param vm_name: Name der virtuellen Maschine.
    :param username: Benutzername für den Gast.
    :param password: Passwort für den Benutzer.
    :param external_access: Ob Zugriff von außen erlaubt sein soll.
    :param allowed_ip: IP-Adresse oder Subnetz, das Zugriff haben soll (optional).
    :param db_user: PostgreSQL-Benutzer, der Zugriff haben soll (optional).
    :param database: Datenbank, die zugänglich gemacht werden soll (optional).

    - wir installieren hiermit PostgreSQL
    - bietet die Möglichkeit, mit Zugriif von außen zu aktivieren
    - außerdem die möglichkeit, dann default alles zugreifen zu lassen (host    all     all         0.0.0.0/0       md5)
    - oder nur bestimmte hosts

    - bisher wird nur der Standardbenutzer Postgres verwendet
    - die Funktion einen neuen Nutzer zu erstellen müsste ergänzt werden



    """
    # PostgreSQL installieren
    commands = [
        f'guestcontrol {vm_name} run --exe /bin/bash --username {username} --password {password} '
        f'-- /bin/bash -c "echo {password} | su - root -c \'apt-get update -y\'"',

        # su - c \'apt-get install -y openssh-server\'"',

        f'guestcontrol {vm_name} run --exe /bin/bash --username {username} --password {password} '
        f'-- /bin/bash -c "echo {password} | su -c \'apt-get install -y postgresql\'"',

        f'guestcontrol {vm_name} run --exe /bin/bash --username {username} --password {password} '
        f'-- /bin/bash -c "echo {password} | su -c \'apt-get install -y postgresql-contrib\'"',

        f'guestcontrol {vm_name} run --exe /bin/bash --username {username} --password {password} '
        f'-- /bin/bash -c "echo {password} | su - root -c \'systemctl enable postgresql\'"',

        f'guestcontrol {vm_name} run --exe /bin/bash --username {username} --password {password} '
        f'-- /bin/bash -c "echo {password} | su - root -c \'systemctl start postgresql\'"'
    ]
    run_commands(commands)

    # Zugriff konfigurieren
    configurePostgresAccess(vm_name, username, password, external_access, allowed_ip, db_user, database)

    # Beispiel: Erstelle eine Datenbank und einen Benutzer, falls benötigt
    if db_user and database:
        sql_commands = [
            f"CREATE DATABASE {database};",
            f"CREATE USER {db_user} WITH ENCRYPTED PASSWORD '{password}';",
            f"GRANT ALL PRIVILEGES ON DATABASE {database} TO {db_user};"
        ]
        executeSQL(vm_name, username, password, sql_commands)
