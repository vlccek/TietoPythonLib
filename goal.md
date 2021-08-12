# Concept
## Creating Fabric object
```py
fabric01 = Fabric(hostname="Best-Fabric", username="pepa", password="pejcpa123")

```

## Run an (unknown) command on switch
```py
fabric01 = Fabric(hostname="Best-Fabric", username="pepa", password="pejcpa123")
fabric01.send_command(command="switch-get-config") # possible output or error will be returned

```


# Legacy
## VLANS
```py
switch01 = Switch(name="Vlaďa", iphost="1.1.1.1")
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