# TietoPythonLib

## Vlans
 - for adding vlans to switch you can use class `Vlans`. 
 - you can create vlan in vlans by method `add_by_params()` or `add_by_dict()`
 - Class `Vlans` can be also displayed as table by simply printing it
 - You can also delete vlan from `Vlans` class by method `delete()`
 - Methods `delete()`, `add_by_params()` and `add_by_dict()` also sorts vlans in `Vlans` object by their `id` after addition/deletion 

### add_by_params() method
```py

example_vlans = Vlans()
example_vlans.add_by_params(id=10) # add vlan with id 10 and default values to `example_vlans`

# other arguments are optional :) like
example_vlans.add_by_params(2, type="public", auto_vxlan=False, description="test2", stats=True, active=True, untagged_ports=[243, 244, 245], active_ports=[666], ports=[243, 244, 245, 666])

"""
print(example_vlans): produce table of used vlans
  id  type     auto-vxlan    replicators    scope    description    active    stats    ports                 untagged_ports    active_ports    vxlan    vxlanmodu
----  -------  ------------  -------------  -------  -------------  --------  -------  --------------------  ----------------  --------------  -------  ---------
  10  private  False                        local                   False     False    []                    []                []
  20  public   False                        local    test2          True      True     [243, 244, 245, 666]  [243, 244, 245]   [666]
"""
```

### add_by_dict() method
```py 
example_vlans = Vlans()
vlan_template = {
        "id": 1,
        "type": "private",
        "auto-vxlan": False,
        "replicators": None,
        "scope": "local",
        "description": "", 
        "active": False, 
        "stats": False, 
        "ports": [], 
        "untagged_ports": [], 
        "active_ports": [], 
        "vxlan": None, 
        "vxlanmodule": "" 
    }
example_vlans.add_by_dict(vlan_template)

"""
print(example_vlans): produce table of used vlans
  id  type     auto-vxlan    replicators    scope    description    active    stats    ports                 untagged_ports    active_ports    vxlan    vxlanmodu
----  -------  ------------  -------------  -------  -------------  --------  -------  --------------------  ----------------  --------------  -------  ---------
  1   private  False                        local                   False     False    []                    []                []
"""

```

### delete() method
```py
example_vlans = Vlans()
example_vlans.add_by_params(id=42)
example_vlans.add_by_params(id=31)
example_vlans.add_by_params(id=128)
example_vlans.add_by_params(id=4)
example_vlans.delete(id=42) # deletes vlan with id 42 and sorts the rest of them by id

# before delete
"""
print(example_vlans): produce table of used vlans
  id  type     auto-vxlan    replicators    scope    description    active    stats    ports                 untagged_ports    active_ports    vxlan    vxlanmodu
----  -------  ------------  -------------  -------  -------------  --------  -------  --------------------  ----------------  --------------  -------  ---------
  42  private  False                        local                   False     False    []                    []                []
  31  private  False                        local                   False     False    []                    []                []
  128 private  False                        local                   False     False    []                    []                []
  4   private  False                        local                   False     False    []                    []                []
"""

# after delete
"""
print(example_vlans): produce table of used vlans
  id  type     auto-vxlan    replicators    scope    description    active    stats    ports                 untagged_ports    active_ports    vxlan    vxlanmodu
----  -------  ------------  -------------  -------  -------------  --------  -------  --------------------  ----------------  --------------  -------  ---------
  4   private  False                        local                   False     False    []                    []                []
  31  private  False                        local                   False     False    []                    []                []
  128 private  False                        local                   False     False    []                    []                []
"""

try:
    example_vlans.delete(id=67) # if vlan with such id doesn't exist, exception raises
except:
    print("Vlan with such ID doesn't exist")
```







