import os
from config import password, username, hostname, port
import unittest
import sys

try:
    sys.path.append("../")
    from fabric import Fabric

except:
    pass


class TestShowCommands(unittest.TestCase):

    def setUp(self) -> None:
        self.coneceted_sw = Fabric(hostname, username, password, port)
        return super().setUp()

    def test_fabric_info(self):
        text = self.coneceted_sw.fabric_info()

        self.assertIsInstance(text, str)
        self.assertNotEqual(text, "")

    def test_fabric_node_show(self):
        text = self.coneceted_sw.fabric_node_show()

        self.assertIsInstance(text, str)
        self.assertNotEqual(text, "")

    def test_node_show(self):
        text = self.coneceted_sw.node_show()

        self.assertIsInstance(text, str)
        self.assertNotEqual(text, "")

    def test_port_show(self):
        text = self.coneceted_sw.node_show()

        self.assertIsInstance(text, str)
        self.assertNotEqual(text, "")

    def test_port_phy_show(self):
        text = self.coneceted_sw.node_show()

        self.assertIsInstance(text, str)
        self.assertNotEqual(text, "")

    def test_port_software_show(self):
        text = self.coneceted_sw.node_show()

        self.assertIsInstance(text, str)
        self.assertNotEqual(text, "")

    def test_switch_config_show(self):
        text = self.coneceted_sw.node_show()

        self.assertIsInstance(text, str)
        self.assertNotEqual(text, "")

    def test_switch_setup_show(self):
        text = self.coneceted_sw.node_show()

        self.assertIsInstance(text, str)
        self.assertNotEqual(text, "")

    def test_switch_setup_show(self):
        text = self.coneceted_sw.node_show()

        self.assertIsInstance(text, str)
        self.assertNotEqual(text, "")

    def test_vlan_show(self):
        text = self.coneceted_sw.node_show()

        self.assertIsInstance(text, str)
        self.assertNotEqual(text, "")


if __name__ == "__main__":
    print("testuju")
    unittest.main()
