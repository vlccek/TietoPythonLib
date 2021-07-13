from typing import List, Dict, Any, Optional
from vlan import Vlans
import re
from ipaddress import IPv4Network, IPv6Network



teststr = """
switch-name:               119-NRU02-spine-01
mgmt-ip:                   21.119.28.11/19
mgmt-ip-assignment:        static
mgmt-ip6:                  fe80::491:2aff:fe26:ffaf/64
mgmt-ip6-assignment:       autoconf
mgmt-link-state:           up
mgmt-link-speed:           1g
in-band-ip:                169.254.119.11/24
in-band-ip6:               fe80::640e:94ff:fe4f:1c24/64
in-band-ip6-assign:        autoconf
gateway-ip:                21.119.31.254
dns-ip:                    21.255.254.45
dns-secondary-ip:          21.255.254.46
domain-name:               domain.com
ntp-server:                21.255.254.13
ntp-secondary-server:      21.255.254.14
timezone:                  Europe/Stockholm
date:                      2021-07-09,13:13:39
hostid:                    285212751
location-id:               4
enable-host-ports:         yes
motd:                      LINUX TRACK - 6.1.0 HF4
banner:                    LINUX TRACK - 6.1.0 HF4
mgmt-lag:                  active-standby
mgmt-lacp-mode:            off
ntp:                       on
"""

class Switch:
    def __init__(self, vlans: Vlans = Vlans()) -> None:
        self.vlans = vlans
    
    def parse_switch_setup_show(self, info_to_parse: str):
        pattern = "(.[^\:]*)\:\ *(.*)"
        parsed_info = re.findall(pattern, info_to_parse)
        new_dictionary = dict()
        ip4field = ["mgmt-ip", "in-band-ip","gateway-ip","dns-ip", "dns-secondary-ip", "ntp-server", "ntp-secondary-server"]
        ip6field = ["mgmt-ip6", "in-band-ip6"]
        for i in parsed_info:
            new_dictionary[i[0]] = i[1]
            if(i[0] in ip4field): 
                new_dictionary[i[0]] = i[1] # convert string to ipv4 object
            if(i[0] in ip6field):
                new_dictionary[i[0]] = i[1] # convert string to ipv6 object
        return new_dictionary   
 
 # https://docs.python.org/3/library/ipaddress.html#ipaddress.ip_interface


n  = Switch()
print(n.parse_switch_setup_show(info_to_parse=teststr))