import time
import logging
from vboxAutomation import VirtualBoxAutomation, installSSH, installMySQL, PortForwarding, fill_sampleDataMySQL
import subprocess
import sys

# Logging konfigurieren
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def wait_for_vm_ip(vm_name: str, timeout: int = 900, interval: int = 10) -> str:
    """
    Wartet darauf, dass eine VM eine IP-Adresse erhält.

    :param vm_name: Name der virtuellen Maschine.
    :param timeout: Maximale Wartezeit in Sekunden (Standard: 1800 Sekunden = 30 Minuten).
    :param interval: Intervall zwischen den Abfragen in Sekunden (Standard: 10).
    :return: Die IP-Adresse der VM.
    :raises TimeoutError: Wenn die Wartezeit abgelaufen ist.
    """
    vboxmanage_path = VirtualBoxAutomation()._get_vboxmanage_path()
    start_time = time.time()

    while time.time() - start_time < timeout:
        try:
            # Befehl zum Abrufen der IP-Adresse
            command = f'"{vboxmanage_path}" guestproperty get "{vm_name}" "/VirtualBox/GuestInfo/Net/0/V4/IP"'
            process = subprocess.run(
                command,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )

            # IP-Adresse aus der Ausgabe extrahieren
            output = process.stdout.strip()
            if "Value:" in output:
                ip_address = output.split("Value:")[1].strip()
                if ip_address and ip_address != "0.0.0.0":
                    logger.info(f"VM hat die IP-Adresse erhalten: {ip_address}")
                    return ip_address

        except Exception as e:
            logger.warning(f"Fehler beim Abrufen der IP-Adresse: {e}")

        # Wartezeit zwischen den Abfragen
        logger.info("Warte auf IP-Adresse...")
        time.sleep(interval)

    raise TimeoutError(f"VM hat nach {timeout // 60} Minuten keine IP-Adresse erhalten.")


if __name__ == "__main__":
    vbox = VirtualBoxAutomation()

    if vbox.create_vm():
        logger.info("VM-Erstellung erfolgreich abgeschlossen. Warte auf IP-Adresse...")
        try:
            """
            Timeout auf 30 Minuten setzen
            ip = wait_for_vm_ip(vbox.VM_NAME, timeout=1800)
            dauert so um die 15 Minuten, zumindest auf meiner Maschine
            man könnte auch einfach einer fertige vdi nehmen
            """
            # TODO wir brauchen auch noch eine Postgres Installation
            # TODO VDI in EO1 umwandeln
            ip = wait_for_vm_ip(vbox.VM_NAME, timeout=900)
            logger.info(f"IP-Adresse der VM: {ip}")

            # nachdem eine IP gefunden wurde, setze das Port Forwarding um
            """
            Was passiert hier?
            Es wird in einer Liste von Ports geschaut, ob dieser jemals belegt wurde. Das ist deswegen wichtig, weil sonst der Key in der Hosts.txt nicht zu dem angegebenen Host passt

            VBoxManage natnetwork list
            - hiermit werden alle NAT-Netzwerke angezeigt
            - wenn wir die Regeln bearbeiten wollen: 
            VBoxManage natnetwork modify --netname <NetzwerkName> --port-forward-4 delete <Regelname>
            - der Regelname setzt sich aus dem Namen der VM und dem Port zusammen 
            - und so sieht eine Regel dann aus: 
            ssh-ForensicVMC10001:tcp:[127.0.0.1]:10001:[10.0.2.7]:22

            - so werden Konflikte in der Hosts.txt und doppelten Regelnamen vermieden
            - es sei denn, man ändert manuell die used_port_numbers.txt
            - dann kommt es vermutlich zu Problemen
            """
            port_forward = PortForwarding(vm_name=vbox.VM_NAME)
            port = port_forward.setup_port_forwarding(ip)
            if not port:
                logger.error("Fehler beim Einrichten des Port Forwardings. Abbruch.")
                sys.exit(1)  # Skript abbrechen bei schwerwiegendem Fehler

        except TimeoutError as e:
            logger.error(f"Timeout beim Warten auf die IP-Adresse: {e}")
            sys.exit(1)  # Skript abbrechen bei Timeout-Fehler

        logger.info("Erfolgreich IP-Adresse erhalten. Starte Konfiguration...")
        installSSH(
            vm_name=vbox.VM_NAME,
            username=vbox.USERNAME,
            password=vbox.PASSWORD
        )
        logger.info("VM-Konfiguration abgeschlossen.")

        """
        hostname = "192.168.178.56"
        hier muss entweder die IP der VM stehen, die das vorherige Skript ermittelt hat oder halt einfach die Loopback Adresse
        das kommt jetzt ganz auf die Netzwerkkonfiguration an
        Momentan liegen die VMs in einem NAT-Netzwerk
        - diese muss noch vorher automatisch erstellt werden
        - die Maschinen müssen automatisch zu diesem Netzwerk hinzugefügt werden
        - außerdem brauchen wir noch eine Regel pro neuer Maschine für das Port-Forwarding
        - deswegen braucht auch jede neue Maschine, die in dieses Netzwerk soll, eine fortlaufende Portnummer

        Name                Protokoll       Host-IP         Host-Port           Gast-IP         Gast-Port
        ForTrace            TCP             127.0.0.1       2224                10.0.2.15       22
        SSH-ForensicVM      TCP             127.0.0.1       2222                10.0.2.4        22
        SSH-ForensicVMB     TCP             127.0.0.1       2223                10.0.2.6        22

        - Port Zuweisung muss durch das Skript erfolgen
        - IP Zuweisung muss durch das Skript erfolgen
        - diese Funktionalität muss in ein eigenes Skript
        - muss als allererste Funktion ausgeführt werden    

        """

        """
        - hier wird einfach die installMySQL() aufgerufen
        - die Installation erfolgt über das vorher eingerichtete SSH
        """
        if ip:
            hostname = "localhost"
        else:
            logger.error("Konnte keine IP ermitteln")
            sys.exit(1)  # Abbruch bei fehlender IP-Adresse

        username = vbox.USERNAME
        password = vbox.PASSWORD
        root_password = password  # Root-Passwort, müsste entweder in der CreateVM.py explizit gesetzt werden, ansonsten ist das Root-Passwort standardmäßig das des angelegten Users

        if hostname:
            # Funktion aufrufen, um die Datenbank zu installieren
            installMySQL(hostname, port, username, password, root_password)
            logger.info(f"Done installing MySQL onto the System: {vbox.VM_NAME}")
            fill_sampleDataMySQL(hostname, port, username, password, root_password)
            logger.info(f"Done initializing sample Data on System: {vbox.VM_NAME}")
        else:
            logger.error(
                "Es konnte kein Hostname ermittelt werden, vermutlich Fehler bei der Erstellung des Images!"
            )
        # --- hier wäre dann der Installationsprozess für eine einzelne Maschine fertiggestellt ---
        # --- meine Idee wäre es jetzt, UseCases zu definieren, zum Beispiel UseCase: SQL-Injection ---
        # --- dafür würde man dann diese Datei ebenfalls in die Library mit aufnehmen ---
        # --- unser UseCase würde dann noch aus einer weitere VM bestehen ---

        # --- für jedes UseCase bräuchte man eigene Funktionen, diese könnte man dann aber Ordner für ordner auseinanderhalten ---
    else:
        logger.error("VM-Erstellung fehlgeschlagen. Abbruch.")

