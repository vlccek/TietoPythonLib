from typing import List, Dict, Any, Optional
from vlan import Vlans
import re
from ipaddress import IPv4Network, IPv6Network
from tests.stringforparse import vlan_show, switch_setup_show

def parse_switch_setup_show( info_to_parse: str):
    pattern = "(.[^\:]*)\:\ *(.*)"
    parsed_info = re.findall(pattern, info_to_parse)
    new_dictionary = dict()
    ip4field = [
        "mgmt-ip",  # managment ip
        "in-band-ip",  # nemám tušení mby vnitřní ip ale aby byl na sw NAT to se mi nepozdává
        "gateway-ip",  # gw
        "dns-ip",  # DNS
        "dns-secondary-ip",  # DNS2
        "ntp-server",
        "ntp-secondary-server",
    ]
    ip6field = ["mgmt-ip6", "in-band-ip6"]  # managment ip
    for i in parsed_info:
        new_dictionary[i[0]] = i[1]
        if i[0] in ip4field:
            new_dictionary[i[0]] = i[1]
        if i[0] in ip6field:
            new_dictionary[i[0]] = i[1]
    return new_dictionary

def parse_vlan_show( info_to_parse: str):
    pattern = "(?P<Sw_name>[a-zA-Z0-9_.-]*)\s+(?P<vlan_id>\d+)\s+(?P<type>\w+)\s+(?P<auto_vxlan>yes|no)\s+(?P<replicators>\w+)\s+(?P<scope>\w+)\s+(?P<description>[a-zA-Z0-9_.-]*)\s+(?P<active>yes|no)\s+(?P<stats>yes|no)\s+(?P<ports>[0-9,-]*|none)\s+(?P<untagged_ports>[0-9,-]*|none)\s+(?P<active_ports>none|[0-9,-]*)"
    # https://regexr.com/61s1p
    new_vlan_obj = Vlans()
    match = re.findall(pattern,info_to_parse)
    for i in match:
        new_vlan = {
        "id": int(i[1]),
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
        new_vlan_obj.add_by_dict(new_vlan) 
    
    return new_vlan_obj

class Switch:
    def __init__(self, management_ip: str, management_ipv6: str = "") -> None:
        self.__vlans__ = Vlans()
        self.__management_ipv4__ = management_ip
        self.__inband_ipv4__ = ""
        self.__gateway_ipv4__ = ""
        self.__dns_ipv4__ = ""
        self.__dns_secondary_ipv4__ = ""
        self.__ntp_server_ipv4__ = ""
        self.__ntp_secondary_ipv4__ = ""
        self.__management_ipv6__ = ""
        self.__inband_ipv6__ = ""

    @property
    def vlans(self):
        """Vlan getter"""
        return self.__vlans__
    
    @property
    def management_ipv4(self):
        """Management IPv4 getter"""
        return self.__management_ipv4__
    
    @property
    def inband_ipv4(self):
        """Inband IPv4 getter"""
        return self.__inband_ipv4__
    
    @property
    def gateway_ipv4(self):
        """Gateway IPv4 getter"""
        return self.__gateway_ipv4__

    @property
    def dns_ipv4(self):
        """DNS IPv4 getter"""
        return self.__dns_ipv4__
    
    @property
    def dns_secondary_ipv4(self):
        """DNS Secondary IPv4 getter"""
        return self.__dns_secondary_ipv4__

    @property
    def ntp_server(self):
        """NTP IPv4 getter"""
        return self.__ntp_server_ipv4__
    
    @property
    def ntp_secondary_server(self):
        """NTP IPv4 getter"""
        return self.__ntp_secondary_ipv4__

    @property
    def management_ipv6(self):
        """Management IPv6 getter"""
        return self.___management_ipv6__
    
    @property
    def inband_ipv6(self):
        """Inband IPv6 getter"""
        return self.__inband_ipv6__

    @vlans.setter
    def vlans(self, vlans: Vlans = Vlans()):
        self.__vlans__ = vlans
    
    """
    @management_ipv4.setter
    def management_ipv4(self, ip:str):
        self.__management_ipv4__ = ip
    """
    
    @inband_ipv4.setter
    def inband_ipv4(self, ip:str):
        self.__inband_ipv4__ = ip

    @gateway_ipv4.setter
    def gateway_ipv4(self, ip :str):
        self.__gateway_ipv4__ = ip

    @dns_ipv4.setter
    def dns_ipv4(self, ip:str):
        self.__dns_ipv4__ = ip

    @dns_secondary_ipv4.setter
    def dns_secondary_ipv4(self, ip:str):
        self.__dns_secondary_ipv4__ = ip
    
    @ntp_server.setter
    def ntp_server(self, ip:str):
        self.__ntp_server_ipv4__ = ip

    @ntp_secondary_server.setter
    def ntp_secondary_server(self, ip:str):
        self.__ntp_secondary_ipv4__ = ip
    
    @management_ipv6.setter
    def management_ipv6(self, ip6:str):
        self.__management_ipv6__ = ip6

    """
    @inband_ipv6.setter
    def inband_ipv6(self, ip6:str):
        self.__inband_ipv6__ = ip6
    """
        
