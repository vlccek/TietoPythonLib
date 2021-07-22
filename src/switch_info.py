from typing import List, Dict, Any, Optional
from vlan import Vlans
from loguru import logger
from help_function import dict_diff


class Switch_info:
    def __init__(self, management_ip: str = "", management_ipv6: str = "") -> None:
        logger.trace("Initializing Switch_info object")
        self.__vlans = Vlans()
        self.__switch_name = ""
        self.__management_ipv4 = management_ip
        self.__inband_ipv4 = ""
        self.__gateway_ipv4 = ""
        self.__dns_ipv4 = ""
        self.__dns_secondary_ipv4 = ""
        self.__ntp_server_ipv4 = ""
        self.__ntp_secondary_ipv4 = ""
        self.__management_ipv6 = management_ipv6
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
        logger.success("Switch_info object created successfully")

    def from_dict_to_attributes(self, parsed: Dict):
        logger.trace("Converting dictionary to attributes")
        # self.__management_ipv4 = parsed.get("mgmt-ip", "")
        self.__inband_ipv4 = parsed.get("in-band-ip", "")
        self.__gateway_ipv4 = parsed.get("gateway-ip", "")
        self.__dns_ipv4 = parsed.get("dns-ip", "")
        self.__dns_secstdondary_ipv4 = parsed.get("dns-secondary-ip", "")
        self.__ntp_server_ipv4 = parsed.get("ntp-server", "")
        self.__ntp_secondary_ipv4 = parsed.get("ntp-secondary-server", "")
        # self.__management_ipv6 = parsed.get("mgmt-ip6", "")

        self.__switch_name = parsed.get("switch-name", "")
        self.__inband_ipv4 = parsed.get("in-band-ip", "")
        self.__gateway_ipv4 = parsed.get("gateway-ip", "")
        self.__dns_ipv4 = parsed.get("in-band-ip6-assignment", "")
        self.__dns_secondary_ipv4 = parsed.get("dns-secondary-ip", "")
        self.__ntp_server_ipv4 = parsed.get("ntp-server", "")
        self.__ntp_secondary_ipv4 = parsed.get("ntp-secondary-server", "")
        self.__inband_ipv6 = parsed.get("in-band-ip6", "")
        self.__software = parsed.get(
            "", "")  # Neni hotovo nevím co to je pomoc pomoc pomoc :'(
        self.__domain_name = parsed.get("domain-name", "")
        self.__time_zone = parsed.get("timezone", "")
        self.__hostid = parsed.get("hostid", None)  # int
        self.__location_id = parsed.get("location-id", None)  # int
        self.__motd = parsed.get("motd", "")
        self.__banner = parsed.get("banner", "")
        self.__mgmt_lag = parsed.get("mgmt-lag", "")
        self.__mgmt_lacp_mode = parsed.get("mgmt-lacp-mode", "")
        self.__ntp = parsed.get("ntp", "")
        logger.success("Dictionary converted to attributes successfully")

    def load_info(self):
        pass

    def download_info(self):
        pass

    @property
    def vlans(self):
        """Vlan getter"""
        logger.trace("Getting vlans")
        return self.__vlans

    @property
    def inband_ipv4(self):
        """Inband IPv4 getter"""
        logger.trace("Getting inband IP")
        return self.__inband_ipv4

    @property
    def gateway_ipv4(self):
        """Gateway IPv4 getter"""
        logger.trace("Getting gateway IP")
        return self.__gateway_ipv4

    @property
    def dns_ipv4(self):
        """DNS IPv4 getter"""
        logger.trace("Getting Primary DNS IP")
        return self.__dns_ipv4

    @property
    def dns_secondary_ipv4(self):
        """DNS Secondary IPv4 getter"""
        logger.trace("Getting Secondary DNS IP")
        return self.__dns_secondary_ipv4

    @property
    def ntp_server(self):
        """NTP Server IPv4 getter"""
        logger.trace("Getting NTP server IP")
        return self.__ntp_server_ipv4

    @property
    def ntp_secondary_server(self):
        """NTP Secondary server IPv4 getter
        """
        logger.trace("Getting NTP secondary server IP")
        return self.__ntp_secondary_ipv4

    @property
    def inband_ipv6(self):
        """Inband IPv6 getter
        """
        logger.trace("Getting inband IPv6")
        return self.__inband_ipv6

    @property
    def software(self):
        """Software version getter
        """
        logger.trace("Getting software version")
        return self.__software

    @property
    def domain_name(self):
        """Domain name getter
        """
        logger.trace("Getting domain name")
        return self.__domain_name

    @property
    def time_zone(self):
        """Time zone getter
        """
        logger.trace("Getting time zone")
        return self.__time_zone

    @property
    def hostid(self):
        """HostID getter
        """
        logger.trace("Getting HostID")
        return self.__hostid

    @property
    def location_id(self):
        """LocationID getter
        """
        logger.trace("Getting LocationID")
        return self.__location_id

    @property
    def motd(self):
        """Motd getter
        """
        logger.trace("Getting motd")
        return self.__motd

    @property
    def banner(self):
        """Banner getter
        """
        logger.trace("Getting banner")
        return self.__banner

    @property
    def mgmt_lag(self):
        """Management lag getter
        """
        logger.trace("Getting Management lag")
        return self.__mgmt_lag

    @property
    def mgmt_lacp_mode(self):
        """Management lacp mode getter
        """
        logger.trace("Getting Management lacp mode")
        return self.__mgmt_lacp_mode

    @property
    def ntp(self):
        """Ntp getter
        """
        logger.trace("Getting ntp state")
        return self.__ntp

    @vlans.setter
    def vlans(self, vlans: Vlans = Vlans()):
        """Vlan setter

        : param vlans: Vlans object. Empty Vlans object by default.
        """
        logger.info(f"Changing vlans")
        self.__vlans = vlans
        logger.success("Vlans changed successfully")

    @inband_ipv4.setter
    def inband_ipv4(self, ip: str) -> None:
        """Inband IPv4 setter

        :param ip: IPv4 address in str type
        """
        self.__inband_ipv4 = ip
        logger.success("Inband IP changed successfully")

    @gateway_ipv4.setter
    def gateway_ipv4(self, ip: str) -> None:
        """Gateway IPv4 setter

        :param ip: IPv4 address in str type
        """
        self.__gateway_ipv4 = ip
        logger.success("Gateway IP changed successfully")

    @dns_ipv4.setter
    def dns_ipv4(self, ip: str) -> None:
        """DNS IPv4 setter

        :param ip: IPv4 address in str type
        """
        self.__dns_ipv4 = ip
        logger.success("DNS IP changed successfully")

    @dns_secondary_ipv4.setter
    def dns_secondary_ipv4(self, ip: str) -> None:
        """DNS Secondary IPv4 setter

        :param ip: IPv4 address in str type
        """
        self.__dns_secondary_ipv4 = ip
        logger.success("DNS Secondary IP changed successfully")

    @ntp_server.setter
    def ntp_server(self, ip: str) -> None:
        """NTP Server IPv4 setter

        :param ip: IPv4 address in str type
        """
        self.__ntp_server_ipv4 = ip
        logger.success("NTP server IP changed successfully")

    @ntp_secondary_server.setter
    def ntp_secondary_server(self, ip: str) -> None:
        """NTP Secondary server IPv4 setter

        :param ip: IPv4 address in str type
        """
        self.__ntp_secondary_ipv4 = ip
        logger.success("NTP secondary server IP changed successfully")

    @inband_ipv6.setter
    def inband_ipv6(self, ip6: str) -> None:
        """Inband IPv6 setter

        :param ip: IPv6 address in str type
        """
        self.__inband_ipv6 = ip6
        logger.success("Inband IPv6 changed successfully")

    # @software.setter
    # def software(self, version: str) -> None:
    #     """Software version setter

    #     :param version: Version """"""of software on switch in str type
    #     """
    #     self.__software = version

    @domain_name.setter
    def domain_name(self, name: str) -> None:
        """Domain name setter

        :param name: Desired domain name
        """
        self.__domain_name = name

    @time_zone.setter
    def time_zone(self, zone: str) -> None:
        """Time zone setter

        :param zone: Desired time zone
        """
        self.__time_zone = zone

    @hostid.setter
    def hostid(self, id: int):
        """HostID setter

        :param id: Desired HostID
        """
        self.__hostid = id

    @location_id.setter
    def location_id(self, id: int):
        """LocationID setter

        :param id: Desired LocationID
        """
        self.__location_id = id

    @motd.setter
    def motd(self, motd: str):
        """Motd setter

        :param motd: Desired motd
        """
        self.__motd = motd

    @banner.setter
    def banner(self, banner: str):
        """Banner setter

        :param banner: Desired banner
        """
        self.__banner = banner

    @mgmt_lag.setter
    def mgmt_lag(self, lag: str):
        """Management lag setter

        :param lag: Desired management lag
        """
        self.__mgmt_lag = lag

    @mgmt_lacp_mode.setter
    def mgmt_lacp_mode(self, lacp_mode: str):
        """Management lacp mode setter

        :param lacp_mode: Desired management lacp mode
        """
        self.__mgmt_lacp_mode = lacp_mode

    @ntp.setter
    def ntp(self, ntp: str):
        """Ntp setter

        :param ntp: Ntp state
        """
        self.__ntp = ntp

    def print_instance_attributes(self):
        for attribute, value in self.__dict__.items():
            print(attribute, '=', value)
