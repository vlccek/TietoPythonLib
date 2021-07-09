# Concept
## Getting info about switch
```py
switch01 = Switch(name="Switch01", iphost="1.1.1.1")
switch01.password = input('Enter password from ' + switch.get_name())
switch.ssh_connect()

infoSW01 = switch.get_info() # returns <<switchInfo>>
print(infoSW01)
```

## Usage of auto connect
```py
switch01 = Switch(name="Switch01", iphost="1.1.1.1", autoconnect=True)
switch01.password = input('Enter password from ' + switch.get_name())
# Automatically connect if possible

infoSW01 = switch.get_info() # returns <<switchInfo>>
print(infoSW01)
```

## Run an (unknown) command on switch
```py
switch01 = Switch(name="Pepa", iphost="1.1.1.0")  
switch01.run_command(command="switch-get-config", params=[]) # possible output or error will be visible on console

```
## VLANS
```py
switch01 = Switch(name="Vlaďa", iphost="1.1.1.1")
switch01.password = input(" password of {switch.getName()}")
switch.sshconnect()

vlan10 = {
    "name":"Vidláci",
    "number" : 10,
    "ports" : ["eth0"]
}

vlans = Vlans()


#more vlans like:
vlans_dict = [
{
    "name":"Vidláci",
    "number" : 10,
    "ports" : ["eth0"]
},
{
    "name":"vidlačky",
    "number" : 11,
    "ports" : ["eth11"]
}
]
for i in vlans_dict:
    vlans.add(i)

vlans.add(vlan10)
# or
vlans.add(name="Luďek", number=110, ports=["eth10"])

switch01.vlansappend(vlans)
# just append if exist let it bee

switch01.vlansreplace(vlans)
# force delete all exits vlans and replace them by vlans in var vlans
switch.showVlans()
# show table of vlans
switch(vlan)
```