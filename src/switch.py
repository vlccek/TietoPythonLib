from typing import List, Dict, Any, Optional
from vlan import Vlans
import re
from ipaddress import IPv4Network, IPv6Network

# from tests.stringforparse import vlan_show, switch_setup_show


def parse_switch_setup_show(info_to_parse: str) -> dict:
    """parse output of command switch setup show

    :param info_to_parse: string format info
    :return: parsed information
    """
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


def parse_vlan_show(info_to_parse: str) -> Vlans:
    """Parse vlan show

    :param info_to_parse: string to parse
    """
    pattern = "(?P<Sw_name>[a-zA-Z0-9_.-]*)\s+(?P<vlan_id>\d+)\s+(?P<type>\w+)\s+(?P<auto_vxlan>yes|no)\s+(?P<replicators>\w+)\s+(?P<scope>\w+)\s+(?P<description>[a-zA-Z0-9_.-]*)\s+(?P<active>yes|no)\s+(?P<stats>yes|no)\s+(?P<ports>[0-9,-]*|none)\s+(?P<untagged_ports>[0-9,-]*|none)\s+(?P<active_ports>none|[0-9,-]*)"
    # https://regexr.com/61s1p
    new_vlan_obj = Vlans()
    match = re.findall(pattern, info_to_parse)
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
        self.__vlans = Vlans()
        self.__management_ipv4 = management_ip
        self.__inband_ipv4 = ""
        self.__gateway_ipv4 = ""
        self.__dns_ipv4 = ""
        self.__dns_secondary_ipv4 = ""
        self.__ntp_server_ipv4 = ""
        self.__ntp_secondary_ipv4 = ""
        self.__management_ipv6 = ""
        self.__inband_ipv6 = ""

    @property
    def vlans(self):
        """Vlan getter"""
        return self.__vlans

    @property
    def management_ipv4(self):
        """Management IPv4 getter"""
        return self.__management_ipv4

    @property
    def inband_ipv4(self):
        """Inband IPv4 getter"""
        return self.__inband_ipv4

    @property
    def gateway_ipv4(self):
        """Gateway IPv4 getter"""
        return self.__gateway_ipv4

    @property
    def dns_ipv4(self):
        """DNS IPv4 getter"""
        return self.__dns_ipv4

    @property
    def dns_secondary_ipv4(self):
        """DNS Secondary IPv4 getter"""
        return self.__dns_secondary_ipv4

    @property
    def ntp_server(self):
        """NTP Server IPv4 getter"""
        return self.__ntp_server_ipv4

    @property
    def ntp_secondary_server(self):
        """NTP Secondary server IPv4 getter
        
        """
        return self.__ntp_secondary_ipv4

    @property
    def management_ipv6(self):
        """Management IPv6 getter
        
        """
        return self.___management_ipv6

    @property
    def inband_ipv6(self):
        """Inband IPv6 getter
        
        """
        return self.__inband_ipv6

    @vlans.setter
    def vlans(self, vlans: Vlans = Vlans()):
        """Vlan setter

        :param vlans: Vlans object. Empty Vlans object by default.
        """
        self.__vlans = vlans

    """
    @management_ipv4.setter
    def management_ipv4(self, ip:str):
        self.__management_ipv4 = ip
    """

    @inband_ipv4.setter
    def inband_ipv4(self, ip: str):
        """Inband IPv4 setter
        
        :param ip: IPv4 address in str type
        """
        self.__inband_ipv4 = ip

    @gateway_ipv4.setter
    def gateway_ipv4(self, ip: str):
        """Gateway IPv4 setter
        
        :param ip: IPv4 address in str type
        """
        self.__gateway_ipv4 = ip

    @dns_ipv4.setter
    def dns_ipv4(self, ip: str):
        """DNS IPv4 setter
        
        :param ip: IPv4 address in str type
        """
        self.__dns_ipv4 = ip

    @dns_secondary_ipv4.setter
    def dns_secondary_ipv4(self, ip: str):
        """DNS Secondary IPv4 setter
        
        :param ip: IPv4 address in str type
        """
        self.__dns_secondary_ipv4 = ip

    @ntp_server.setter
    def ntp_server(self, ip: str):
        """NTP Server IPv4 setter
        
        :param ip: IPv4 address in str type
        """
        self.__ntp_server_ipv4 = ip

    @ntp_secondary_server.setter
    def ntp_secondary_server(self, ip: str):
        """NTP Secondary server IPv4 setter
        
        :param ip: IPv4 address in str type
        """
        self.__ntp_secondary_ipv4 = ip

    """
    @management_ipv6.setter
    def management_ipv6(self, ip6: str):
        Management IPv6 setter
        self.__management_ipv6= ip6
    """

    @inband_ipv6.setter
    def inband_ipv6(self, ip6: str):
        """Inband IPv6 setter
        
        :param ip: IPv6 address in str type
        """
        self.__inband_ipv6 = ip6
