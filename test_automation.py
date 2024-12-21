import unittest
from vboxAutomation import VirtualBoxAutomation
from pathlib import Path
import sys

class TestVirtualBoxAutomation(unittest.TestCase):
    def setUp(self):
        # Erstelle ein Objekt der zu testenden Klasse
        self.vbox = VirtualBoxAutomation()

    def test_vboxmanage_path(self):
        """Testet, ob der Pfad zu VBoxManage korrekt ermittelt wird."""
        path = self.vbox._get_vboxmanage_path()
        self.assertTrue(path.exists(), f"Pfad zu VBoxManage nicht gefunden: {path}")

    def test_iso_path_exists(self):
        """Testet, ob die ISO-Datei vorhanden ist."""
        iso_path = self.vbox.ISO_PATH
        self.assertTrue(iso_path.exists(), f"ISO-Datei nicht gefunden: {iso_path}")

    def test_vm_base_path(self):
        """Testet, ob das Basisverzeichnis für die VM existiert oder erstellt wird."""
        vm_base_path = self.vbox.VM_BASE_PATH
        vm_base_path.mkdir(parents=True, exist_ok=True)  # Sicherstellen, dass es existiert
        self.assertTrue(vm_base_path.exists(), f"Basisverzeichnis nicht gefunden: {vm_base_path}")

    def test_check_prerequisites(self):
        """Testet die Funktion zur Überprüfung der Voraussetzungen."""
        try:
            result = self.vbox.check_prerequisites()
            self.assertTrue(result, "Voraussetzungen wurden nicht erfüllt.")
        except Exception as e:
            self.fail(f"check_prerequisites hat eine Ausnahme ausgelöst: {e}")

    # Weitere Tests für spezifische Methoden
    def test_create_vm(self):
        """Testet den Workflow zur VM-Erstellung."""
        # Dieser Test könnte simuliert werden oder man verwendet Mocking, um echte VM-Erstellungen zu vermeiden.
        try:
            result = self.vbox.create_vm()
            self.assertTrue(result, "VM-Erstellung fehlgeschlagen.")
        except Exception as e:
            self.fail(f"create_vm hat eine Ausnahme ausgelöst: {e}")

if __name__ == "__main__":
    unittest.main()
