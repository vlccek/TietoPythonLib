# Jak si představuju že to bude fungovat
## chci si vypsat info o SW
```py
switch01 = Switch(name="Switch01", iphost="1.1.1.1")
switch01.password = input(Zadejte heslo od {switch.getName()})
switch.sshconnect()

infoSW01 = switch.getInfo() # vrací objekt typu switchInfo
print(infoSW01)
```

## Využítí auto connect
```py
switch01 = Switch(name="Switch01", iphost="1.1.1.1", autoconnect=True)
switch01.password = input(Zadejte heslo od {switch.getName()})
# Automaticky se připojí pokud je možno

if(switch01.connected):
    infoSW01 = switch.getInfo() # vrací objekt typu switchInfo
    print(infoSW01)
```

