from switch import parse_vlan_show
from typing import List, Dict, Any, Optional
from vlan import Vlans


class Switch_info:
    def __init__(self) -> None:
        self.__vlans = Vlans()
        self.__switch_name = ""
        self.__inband_ipv4 = ""
        self.__gateway_ipv4 = ""
        self.__dns_ipv4 = ""
        self.__dns_secondary_ipv4 = ""
        self.__ntp_server_ipv4 = ""
        self.__ntp_secondary_ipv4 = ""
        self.__inband_ipv6 = ""
        self.__software = ""
        self.__domain_name = ""
        self.__time_zone = ""
        self.__hostid = None  # int
        self.__location_id = None  # int
        self.__motd = ""
        self.__banner = ""
        self.__mgmt_lag = ""
        self.__mgmt_lacp_mode = ""
        self.__ntp = ""
    
    def from_dict_to_attributes(self, parsed: Dict):
        # self.__management_ipv4 = parsed.get("mgmt-ip", "")
        self.__inband_ipv4 = parsed.get("in-band-ip", "")
        self.__gateway_ipv4 = parsed.get("gateway-ip", "")
        self.__dns_ipv4 = parsed.get("dns-ip", "")
        self.__dns_secstdondary_ipv4 = parsed.get("dns-secondary-ip", "")
        self.__ntp_server_ipv4 = parsed.get("ntp-server", "")
        self.__ntp_secondary_ipv4 = parsed.get("ntp-secondary-server", "")
        # self.__management_ipv6 = parsed.get("mgmt-ip6", "")

        self.__switch_name = parsed.get("", "")
        self.__inband_ipv4 = parsed.get("", "")
        self.__gateway_ipv4 = parsed.get("", "")
        self.__dns_ipv4 = parsed.get("", "")
        self.__dns_secondary_ipv4 = parsed.get("", "")
        self.__ntp_server_ipv4 = parsed.get("", "")
        self.__ntp_secondary_ipv4 = parsed.get("", "")
        self.__inband_ipv6 = parsed.get("in-band-ip6", "")
        self.__software = parsed.get("", "")
        self.__domain_name = parsed.get("", "")
        self.__time_zone = parsed.get("", "")
        self.__hostid = parsed.get("", None)  # int
        self.__location_id = parsed.get("", None)  # int
        self.__motd = parsed.get("", "")
        self.__banner = parsed.get("", "")
        self.__mgmt_lag = parsed.get("", "")
        self.__mgmt_lacp_mode = parsed.get("", "")
        self.__ntp = parsed.get("", "")
    
    def load_info(self):
        pass

    def download_info(self):
        pass

    @property
    def connection(self):
        """Connection getter"""
        return self.__connection

    @property
    def vlans(self):
        """Vlan getter"""
        return self.__vlans
    
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
    def inband_ipv6(self):
        """Inband IPv6 getter

        """
        return self.__inband_ipv6

    @property
    def software(self):
        """Software version getter
        """
        return self.__software
    
    @vlans.setter
    def vlans(self, vlans: Vlans = Vlans()):
        """Vlan setter

        : param vlans: Vlans object. Empty Vlans object by default.
        """
        self.__vlans = vlans
    
    @inband_ipv4.setter
    def inband_ipv4(self, ip: str) -> None:
        """Inband IPv4 setter

        :param ip: IPv4 address in str type
        """
        self.__inband_ipv4 = ip

    @gateway_ipv4.setter
    def gateway_ipv4(self, ip: str) -> None:
        """Gateway IPv4 setter

        :param ip: IPv4 address in str type
        """
        self.__gateway_ipv4 = ip

    @dns_ipv4.setter
    def dns_ipv4(self, ip: str) -> None:
        """DNS IPv4 setter

        :param ip: IPv4 address in str type
        """
        self.__dns_ipv4 = ip

    @dns_secondary_ipv4.setter
    def dns_secondary_ipv4(self, ip: str) -> None:
        """DNS Secondary IPv4 setter

        :param ip: IPv4 address in str type
        """
        self.__dns_secondary_ipv4 = ip

    @ntp_server.setter
    def ntp_server(self, ip: str) -> None:
        """NTP Server IPv4 setter

        :param ip: IPv4 address in str type
        """
        self.__ntp_server_ipv4 = ip

    @ntp_secondary_server.setter
    def ntp_secondary_server(self, ip: str) -> None:
        """NTP Secondary server IPv4 setter

        :param ip: IPv4 address in str type
        """
        self.__ntp_secondary_ipv4 = ip
    
    @inband_ipv6.setter
    def inband_ipv6(self, ip6: str) -> None:
        """Inband IPv6 setter

        :param ip: IPv6 address in str type
        """
        self.__inband_ipv6 = ip6

    @software.setter
    def software(self, version: str) -> None:
        """Software version setter

        :param version: Version of software on switch in str type
        """
        self.__software = version