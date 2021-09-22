import os
from settings import password, username, hostname, port
import unittest
import sys
import re

print(hostname)
print(username)
print(password)
print(port)

sys.path.append("../")
from fabric import Fabric



class TestShowCommands(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.connected_sw = Fabric(hostname, username, password, port)

    def test_fabric_info(self):
        text = self.connected_sw.fabric_info()

        self.assertIsInstance(text, str)
        self.assertNotEqual(text, "")

    def test_fabric_node_show(self):
        text = self.connected_sw.fabric_node_show()

        self.assertIsInstance(text, str)
        self.assertNotEqual(text, "")

    def test_node_show(self):
        text = self.connected_sw.node_show()

        self.assertIsInstance(text, str)
        self.assertNotEqual(text, "")

    def test_port_show(self):
        text = self.connected_sw.node_show()

        self.assertIsInstance(text, str)
        self.assertNotEqual(text, "")

    def test_port_phy_show(self):
        text = self.connected_sw.node_show()

        self.assertIsInstance(text, str)
        self.assertNotEqual(text, "")

    def test_port_software_show(self):
        text = self.connected_sw.node_show()

        self.assertIsInstance(text, str)
        self.assertNotEqual(text, "")

    def test_switch_config_show(self):
        text = self.connected_sw.node_show()

        self.assertIsInstance(text, str)
        self.assertNotEqual(text, "")

    def test_switch_setup_show(self):
        text = self.connected_sw.node_show()

        self.assertIsInstance(text, str)
        self.assertNotEqual(text, "")

    def test_switch_setup_show(self):
        text = self.connected_sw.node_show()

        self.assertIsInstance(text, str)
        self.assertNotEqual(text, "")

    def test_vlan_show(self):
        text = self.connected_sw.node_show()

        self.assertIsInstance(text, str)
        self.assertNotEqual(text, "")


class TestVlanCommands(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.connected_sw = Fabric(hostname, username, password, port)

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
            vlans.append(new_vlan)
        return vlans

    def test_vlan_create_number(self):
        why = self.connected_sw.vlan_create(
            "10",
            "local",
            "",
            "",
            "",
            "",
            "",
            "",
            "Nejlepsi_vlan_na_svete",
            False,
            False,
            "",
            "",
            "",
        )
        #print(why)
        vlans = self.parse_vlan_show(self.connected_sw.vlan_show())
        #print("Create number vlans:\n" + str(vlans))
        found = False
        for vlan in vlans:
            #print(vlan.get("id"))
            if vlan.get("id") is not None and vlan.get("id") == "10":
                found = True
                self.assertEqual(vlan.get("description"), "Nejlepsi_vlan_na_svete")
        self.assertEqual(found, True)

    def test_vlan_create_range(self):
        out = self.connected_sw.vlan_create(
            id_or_range="11-42,43-44,56", scope="local", description="pepa_vlan"
        )
        vlans = self.parse_vlan_show(self.connected_sw.vlan_show())
        #print("Create range vlans:\n" + str(vlans))
        counter = 0
        for vlan in vlans:
            if vlan.get("id") is not None and ((int(vlan.get("id")) >= 11 and int(vlan.get("id")) <= 44) or int(vlan.get("id")) == 56):
                counter += 1
                self.assertEqual(vlan.get("description"), "pepa_vlan")
        self.assertEqual(counter, 35)
    
    def test_vlan_modify(self):
        self.connected_sw.vlan_create(id_or_range="111", scope="local", description="pepa_vlan")
        self.connected_sw.vlan_modify(id="111", description="pepova_vlan")
        vlans = self.parse_vlan_show(self.connected_sw.vlan_show())
        #print("Vlan modify:\n" + str(vlans))
        for vlan in vlans:
            if vlan.get("id") is not None and vlan.get("id") == "111":
                self.assertEqual(vlan.get("description"), "pepova_vlan")
    
    def test_vlan_delete(self):
        self.connected_sw.vlan_create(id_or_range="112", scope="local", description="pepa_vlan")
        self.connected_sw.vlan_delete(id_or_range="112")
        vlans = self.parse_vlan_show(self.connected_sw.vlan_show())
        #print("Vlan delete:\n" + str(vlans))
        found = False
        for vlan in vlans:
            if vlan.get("id") is not None and vlan.get("id") == "112":
                found = True
        self.assertEqual(found, False)

class TestPorts(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.connected_sw = Fabric(hostname, username, password, port)
    def parse_port_show(self, info_to_parse: str):
        pattern = "([a-zA-Z0-9_.-]+)\s+(\d+)\s+([0-9.]+)\s+([0-9,.]*)\s+([0-9:a-zA-Z]*)\s+(\d*)\s+([a-zA-Z0-9_.-]*)\s+([a-zA-Z0-9-._,]+)\s+([a-zA-Z0-9-._,]+)\s+([a-zA-Z0-9-._,]*)"
        # https://regexr.com/65m42
        match = re.findall(pattern, info_to_parse)
        ports = []
        for i in match:
            new_port = {
                "switch": i[1],
                "port": i[2],
                "bezel-port": i[3],
                "ip": i[4],
                "mac": i[5],
                "vlan": i[6],
                "hostname": i[7],
                "status": i[8],
                "config": i[9],
                "trunk": i[10]
            }
            ports.append(new_port)
        return ports
    
    def test_port_vlan_add(self):
        self.connected_sw.vlan_create(id_or_range="59", scope="local")
        self.connected_sw.port_vlan_add("1", vlans="59")
        
    




if __name__ == "__main__":
    unittest.main()
