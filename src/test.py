from switch import Switch
import paramiko

pepa = Switch(
    username="admin", password="root", domain="sw-pepa.cz"
)  # auto dowload infmation about switch
pepa.info.vlans.add_by_params(id=10, ports=[10, 20, 30], active_ports=[10, 30])
pepa.info.dns_ipv4 = "192.168.19.1"
# ...

pepa.commit()  # Upload changes to connected switch


pepa.old_info.vlans.add_by_params(1015, description="nevim")
pepa.old_info.vlans.add_by_params(104)
pepa.old_info.vlans.add_by_params(1040)


pepa.info.vlans.add_by_params(10)
pepa.info.vlans.add_by_params(100)
pepa.info.vlans.add_by_params(1015)
pepa.info.vlans.add_by_params(104)
pepa.info.vlans.add_by_params(1040)

print(pepa.info.vlans)
print(pepa.old_info.vlans)
print(pepa.comapare_2_switch_info(pepa.info, pepa.old_info))


client = paramiko.SSHClient()
client.load_system_host_keys()
client.connect("ssh.example.com")
stdin, stdout, stderr = client.exec_command("ls -l")
