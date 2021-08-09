import random
import unittest

import vlan

"""TODO
chybí dopasat testy s nepovedenými vlany (slovníky
testy na mazání"""

vlan1_res = {
    "id": 1,
    "type": "private",
    "auto-vxlan": False,
    "replicators": "",
    "scope": "local",
    "description": "",
    "active": False,
    "stats": False,
    "ports": [],
    "untagged_ports": [],
    "active_ports": [],
    "vxlan": None,
    "vxlanmodule": "",
}

vlan2_res = {
    "id": 2,
    "type": "public",
    "auto-vxlan": False,
    "replicators": "",
    "scope": "local",
    "description": "test2",
    "active": True,
    "stats": True,
    "ports": [243, 244, 245, 666],
    "untagged_ports": [243, 244, 245],
    "active_ports": [666],
    "vxlan": None,
    "vxlanmodule": "",
}

vlan1_cor = {"id": 2, "type": "public", "ports": [23, 24], "active_ports": [23, 54]}

vlan1_incor = {"id": -1, "stats": True, "active": True, "ports": "42"}


class Test_vlans_add(unittest.TestCase):
    def test_vlan_add_by_dict(self):
        """test adding multiple vlans by dictinary"""
        listofvlans = [vlan1_res, vlan2_res]

        vlan_exp = vlan.Vlans()
        vlan_exp.add_by_dict(vlan1_res)
        vlan_exp.add_by_dict(vlan2_res)

        self.assertEqual(vlan_exp.__vlans__, listofvlans)

    def test_vlan_add_failure_dict(self):
        """Test if you cant add vlan with same id."""
        vlan_exp = vlan.Vlans()
        vlan_exp.add_by_dict(vlan1_res)
        with self.assertRaises(Exception):
            self.assertRaises(vlan_exp.add_by_dict(vlan1_res))

    def test_vlan_add_only_id(self):
        """Add new vlan to fresh object from vlan class with minimal arguments (just id) and control if object is ok"""
        vlan100 = {"id": 100}
        vlan_exp = vlan.Vlans()
        vlan_exp.add_by_dict(vlan100)

        vlan_example = {
            "id": 100,
            "type": "private",
            "auto-vxlan": False,
            "replicators": "",
            "scope": "local",
            "description": "",
            "active": False,
            "stats": False,
            "ports": [],
            "untagged_ports": [],
            "active_ports": [],
            "vxlan": None,
            "vxlanmodule": "",
        }

        self.assertEqual(vlan_exp.__vlans__, [vlan_example])

    def test_vlan_add_by_params(self):
        vlan_test1 = vlan.Vlans()
        vlan_test1.__vlans__ = [vlan1_res, vlan2_res]
        vlans1 = vlan.Vlans()
        vlans1.add_by_params(1)
        vlans1.add_by_params(
            2,
            type="public",
            auto_vxlan=False,
            description="test2",
            stats=True,
            active=True,
            untagged_ports=[243, 244, 245],
            active_ports=[666],
            ports=[243, 244, 245, 666],
        )
        self.assertEqual(vlans1.__vlans__, vlan_test1.__vlans__)


class Test_vlans_delete(unittest.TestCase):
    def test_basic_del(self):
        testedvlan = vlan.Vlans()
        testedvlan.add_by_params(112)
        testedvlan.add_by_params(123)
        testedvlan.add_by_params(10)
        testedvlan.add_by_params(100)
        testedvlan.delete(10)
        vlan_example = {
            "id": 100,
            "type": "private",
            "auto-vxlan": False,
            "replicators": "",
            "scope": "local",
            "description": "",
            "active": False,
            "stats": False,
            "ports": [],
            "untagged_ports": [],
            "active_ports": [],
            "vxlan": None,
            "vxlanmodule": "",
        }
        correctvlan = vlan.Vlans()

        for i in [100, 112, 123]:
            correctvlan.add_by_params(i)
        self.assertEqual(testedvlan.__vlans__, correctvlan.__vlans__)

    def test_all_del(self):
        testedvlan = vlan.Vlans()
        testedvlan.add_by_params(112)
        testedvlan.add_by_params(123)
        testedvlan.add_by_params(10)
        testedvlan.add_by_params(100)
        testedvlan.delete(10)
        testedvlan.delete(112)
        testedvlan.delete(100)
        testedvlan.delete(123)
        correctvlan = vlan.Vlans()

        self.assertEqual(testedvlan.__vlans__, correctvlan.__vlans__)

    def test_delete_not_exist(self):
        testedvlan = vlan.Vlans()
        testedvlan.add_by_params(112)

        with self.assertRaises(Exception):
            self.assertRaises(testedvlan.delete(10))


class Test_vlans_performace(unittest.TestCase):
    @unittest.skip("Takes too long, comment this if you want to run this test.")
    def test_port_performance(self):
        ports_ex = random.sample(range(1, 120000), 100000)
        active_ports_ex = random.sample(ports_ex, 300)
        untagged_ports_ex = random.sample(ports_ex, 10000)
        vlans1 = vlan.Vlans()
        vlans1.add_by_params(
            20,
            ports=ports_ex,
            active_ports=active_ports_ex,
            untagged_ports=untagged_ports_ex,
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
