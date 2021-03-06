
## Creating Fabric object
```py
fabric01 = Fabric(hostname="Best-Fabric", username="pepa", password="pejcpa123")

```

## Run an unknown command on the switch by the library 
```py
fabric01 = Fabric(hostname="Best-Fabric", username="pepa", password="pejcpa123")
fabric01.send_command(command="switch-get-config") # possible output or error will be returned

```

## List of supported commands
```
fabric-info
fabric-node-show
node-show
port-show
port-config-modify
port-phy-show
port-vlan-add
vlan-show
vlan-create
software-show
switch-config-show
```

## Planned commands
```
fabric-{create, info, show, join, unjoin, modify, stats-show, node-show, ....} 
lldp-show 
node-{info, show, ...} 
port-{show, config-modify, stats-show, phy-show, vlan-add, xcvr-show, ...} 
vlan-{show, modify, delete, create, port-add, ...} 
running-config-show 
software-show 
switch-{config-show, export, setup-show, local, ...} 
```

## Script showcase
```py
pepa = Fabric(hostname="Best-Fabric", username="pepa", password="pejcpa123")
pepa.vlan_show()
pepa.vlan_create(id="43", scope="local")
pepa.vlan_show()

pepa.send_command("vlan-show format switch,id,ports")

pepa.send_command_with_prefix(command="vlan-show format id,ports", switches="switch-01")
```

## Log downloading
```py
from download import download
download(hostname="Best-Fabric", username="pepa", password="pejcpa123")
```

## Tests showcase
```py
class TestVlanShow(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.connected_sw = Fabric(hostname, username, password, port)
    def test_vlan_create_range(self):
        out = self.connected_sw.vlan_create(
            id_or_range="11-42,43-44,56", scope="local", description="pepa_vlan"
        )
        vlans = self.parse_vlan_show(self.connected_sw.vlan_show())
        #print("Create range vlans:\n" + str(vlans))
        counter = 0
        for vlan in vlans:
            if vlan.get("id") is not None and ((int(vlan.get("id")) >= 11 and \
                int(vlan.get("id")) <= 44) or int(vlan.get("id")) == 56):
                counter += 1
                self.assertEqual(vlan.get("description"), "pepa_vlan")
        self.assertEqual(counter, 35)
```

## Diags downloading
```py
from diags import download_diags
# downloads diags from switch in settings.py to current location
download_diags() 
```


# Legacy
## VLANS
```py
switch01 = Switch(name="Vla??a", iphost="1.1.1.1")
switch01.password = input('Enter password from ' + switch.get_name())
switch.ssh_connect()

vlan10 = {
    "id": 10,
    "type": "private",
    "auto-vxlan": False,
    "replicators": None,
    "scope": "local",
    "description": "pepa",
    "active": True,
    "stats": True,
    "ports": [457, 621],
    "untagged_ports": [457],
    "active_ports": [621],
    "vxlan": None,
    "vxlanmodule": ""
}

vlans = Vlans()


#more vlans like:
vlans_list = [
{
    "id": 10,
    "type": "private",
    "auto-vxlan": False,
    "replicators": None,
    "scope": "local",
    "description": "pepa",
    "active": True,
    "stats": True,
    "ports": [457, 621],
    "untagged_ports": [457],
    "active_ports": [621],
    "vxlan": None,
    "vxlanmodule": ""
},
{
    "id": 11,
    "type": "public",
    "scope": "cluster",
    "description": "vidlak",
    "active": True,
    "stats": True,
    "ports": [460, 635],
    "untagged_ports": [635],
    "active_ports": [460]
}
]
for i in vlans_dict:
    vlans.add_by_dict(i)

vlans.add_by_dict(vlan10)
# or
vlans.add_by_params(id=42, description="Gerwant", type="public", scope="cluster", ports=[7, 21, 42, 99], untagged_ports=[7, 99], active_ports=[21, 42]) 
# the only mandatory parameter is <<id>>

switch01.vlans_append(vlans)
# just append if exist let it be

switch01.vlans_replace(vlans)
# force delete all exists vlans and replace them by vlans in var vlans
switch.get_vlans()
# obj. type Vlans()

switch(vlan)
```