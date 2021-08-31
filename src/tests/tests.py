import os
from settings import password, username, hostname, port
import unittest
import sys
import re

try:
    sys.path.append("../")
    from fabric import Fabric

    sys.path.remove("../")

except:
    pass


class TestShowCommands(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.coneceted_sw = Fabric(hostname, username, password, port)

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


class TestVlanShow(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.coneceted_sw = Fabric(hostname, username, password, port)

    def parse_vlan_show(self, info_to_parse: str):
        pattern = "(?P<Sw_name>[a-zA-Z0-9_.-]*)\s+(?P<vlan_id>\d+)\s+(?P<type>\w+)\s+(?P<auto_vxlan>yes|no)\s+(?P<replicators>\w+)\s+(?P<scope>\w+)\s+(?P<description>[a-zA-Z0-9_.-]*)\s+(?P<active>yes|no)\s+(?P<stats>yes|no)\s+(?P<ports>[0-9,-]*|none)\s+(?P<untagged_ports>[0-9,-]*|none)\s+(?P<active_ports>none|[0-9,-]*)"
        # https://regexr.com/61s1p
        match = re.findall(pattern, info_to_parse)
        vlans = []
        for i in match:
            new_vlan = {
                "id": i[1],
                "type": i[2],
                "auto-vxlan": i[3],
                "replicators": i[4],
                "scope": i[5],
                "description": i[6],
                "active": i[7],
                "stats": i[8],
                "ports": i[9],
                "untagged_ports": i[10],
                "active_ports": i[11],
            }
            vlans.append(i)
        return vlans

    def test_vlan_create_number(self):
        self.coneceted_sw.vlan_create(
            "10",
            "local",
            "",
            "",
            "",
            "",
            "",
            "",
            "Nejlepsi vlan na svete",
            False,
            False,
            "",
            "",
            "",
        )
        vlans = self.parse_vlan_show(self.coneceted_sw.vlan_show())
        found = False
        for vlan in vlans:
            if vlan.get("id") is not None and vlan.get("id") == 10:
                found = True
                self.assertEqual(vlan.get("description"), "Nejlepsi vlan na svete")
        self.assertEqual(found, True)

    def test_vlan_create_range(self):
        out = self.connected_sw.vlan_create(
            id_or_range="11-42,43-44,56", scope="local", description="pepa vlan"
        )
        vlans = self.parse_vlan_show(self.coneceted_sw.vlan_show())
        counter = 0
        for vlan in vlans:
            if vlan.get("id") is not None and ((vlan.get("id") >= 11 and vlan.get("id") <= 44) or vlan.get("id") == 56):
                counter += 1
                self.assertEqual(vlan.get("description"), "pepa vlan")
        self.assertEqual(counter, 35)
    
    def test_vlan_modify(self):
        self.connected_sw.vlan_create(id_or_range="111", scope="local", description="pepa vlan")
        self.coneceted_sw.vlan_modify(id="111", description="pepova vlan")
        vlans = self.parse_vlan_show(self.coneceted_sw.vlan_show())
        for vlan in vlans:
            if vlan.get("id") is not None and vlan.get("id") == "111":
                self.assertEqual(vlan.get("description"), "pepova vlan")
    
    def test_vlan_delete(self):
        self.connected_sw.vlan_create(id_or_range="112", scope="local", description="pepa vlan")
        self.coneceted_sw.vlan_delete(id_or_range="112")
        vlans = self.parse_vlan_show(self.coneceted_sw.vlan_show())
        found = False
        for vlan in vlans:
            if vlan.get("id") is not None and vlan.get("id") == "112":
                found = True
        self.assertEqual(found, False)


if __name__ == "__main__":
    unittest.main()