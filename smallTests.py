from vboxAutomation import VirtualBoxAutomation, PortForwarding
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

def return_ip():
    command = f'"{vboxmanage_path}" guestproperty get "{vbox.VM_NAME}" "/VirtualBox/GuestInfo/Net/0/V4/IP"'
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
            return ip_address  # Nur zurückgeben, wenn eine gültige IP gefunden wurde

# Ip der vm holen
# aktuell ist in der Klasse VirtualBoxAutomation der Name noch hart-gecoded
vm_ip = return_ip()

port_forward = PortForwarding(vm_name=vbox.VM_NAME)
port = port_forward.setup_port_forwarding(vm_ip)
print(port)
