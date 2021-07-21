from typing import List, Dict, Any, Optional
from vlan import Vlans
from switch_info import Switch_info
import re
import paramiko
from loguru import logger
import sys

from socket import error as socket_error
from socket import gaierror as socket_gaierror

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
            "ports": parse_ports(i[9]),
            "untagged_ports": parse_ports(i[10]),
            "active_ports": parse_ports(i[11]),
        }
        new_vlan_obj.add_by_dict(new_vlan)

    return new_vlan_obj


def parse_interval(interval_to_parse: str):
    resolut = re.match('^(\d+)\-(\d+)$', interval_to_parse)
    if not resolut:
        return []

    tmp = []

    for i in range(int(resolut.group(1)), int(resolut.group(2))+1):
        tmp.append(i)

    return tmp


def parse_ports(ports_to_parse: str):
    splited = ports_to_parse.split(',')
    output = []
    for i in splited:
        if not '-' in i:
            output.append(int(i))
        else:
            output += parse_interval(i)

    return sorted(output)


"""
TODO
- user name a password
- přidat connected
- metoda na převod z range na array

"""


class Switch:
    def __init__(self, username: str, password: str, management_ip: str = "", management_ipv6: str = "", port: int = 22, timeout: int = 60, keepalive: int = 60) -> None:
        """
        self.__vlans = Vlans()
        
        self.__switch_name = ""
        self.__management_ipv4 = management_ip
        self.__inband_ipv4 = ""
        self.__gateway_ipv4 = ""
        self.__dns_ipv4 = ""
        self.__dns_secondary_ipv4 = ""
        self.__ntp_server_ipv4 = ""
        self.__ntp_secondary""""""_ipv4 = ""
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
        """
        self.__info = Switch_info()
        self.__logger = logger.add(sys.stdout, format="{time} {level} {message}", filter="my_module", level="INFO")

        self.__port = port
        self.__timeout = timeout
        self.__keepalive = keepalive
        self.__username = username
        self.__password = password

        self.__changed = False
        self.__connected = False
        self.__connection = None

        if management_ip == "" and management_ipv6 == "":
            raise Exception("ip not provided")
        elif management_ipv6 == "":
            self.hostname = management_ip
        else:
            self.hostname = management_ipv6

        logger.debug("That's it, beautiful and simple logging!")
        self.open()

    def open(self):
        """Opens a SSH connection"""
        return
        """
        self.__connection = paramiko.SSHClient()
        self.__connection.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            self.__connection.connect(hostname=self.__management_ipv4,
                                      username=self.__username,
                                      password=self.__password,
                                      timeout=self.__timeout,
                                      port=self.__port)
            self.__connection.get_transport().set_keepalive(self.__keepalive)
            self.__connected = True
        except paramiko.ssh_exception.AuthenticationException:
            raise Exception("Unable to open connection with {hostname}: invalid credentials!".format(
                hostname=self._hostname))
        except socket_error as sockerr:
            raise Exception("Cannot open connection: {skterr}. Wrong port?".format(
                skterr=sockerr.message))
        except socket_gaierror as sockgai:
            raise Exception("Cannot open connection: {gaierr}. \
                Wrong hostname?".format(gaierr=sockgai.message))
        return self.__connection
    """

    def run_command(self, commands: List[str]):
        # TODO
        pass

    def commit(self):
        """Send changes made in Switch object to switch"""
        if not self.__changed:
            return
        # TODO
        pass

"""     def from_dict_to_attributes(self, parsed: Dict):
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
        pass """

    @property
    def connection(self):
        """Connection getter"""
        return self.__connection

    # @property
    # def vlans(self):
    #     """Vlan getter"""
    #     return self.__vlans

    # @property
    # def management_ipv4(self):
    #     """Management IPv4 getter"""
    #     return self.__management_ipv4

    # @property
    # def inband_ipv4(self):
    #     """Inband IPv4 getter"""
    #     return self.__inband_ipv4

    # @property
    # def gateway_ipv4(self):
    #     """Gateway IPv4 getter"""
    #     return self.__gateway_ipv4

    # @property
    # def dns_ipv4(self):
    #     """DNS IPv4 getter"""
    #     return self.__dns_ipv4

    # @property
    # def dns_secondary_ipv4(self):
    #     """DNS Secondary IPv4 getter"""
    #     return self.__dns_secondary_ipv4

    # @property
    # def ntp_server(self):
    #     """NTP Server IPv4 getter"""
    #     return self.__ntp_server_ipv4

    # @property
    # def ntp_secondary_server(self):
    #     """NTP Secondary server IPv4 getter

    #     """
    #     return self.__ntp_secondary_ipv4

    # @property
    # def management_ipv6(self):
    #     """Management IPv6 getter

    #     """
    #     return self.__management_ipv6

    # @property
    # def inband_ipv6(self):
    #     """Inband IPv6 getter

    #     """
    #     return self.__inband_ipv6

    @property
    def port(self):
        """Port getter
        """
        return self.__port

    @property
    def timeout(self):
        """Timeout getter
        """
        return self.__timeout

    @property
    def keepalive(self):
        """Keepalive getter
        """
        return self.__keepalive

    @property
    def username(self):
        """Username getter
        """
        return self.__username

    # @property
    # def software(self):
    #     """Software version getter
    #     """
    #     return self.__software

    @property
    def connected(self):
        """Connected getter
        """
        return self.__connected

    # @vlans.setter
    # def vlans(self, vlans: Vlans = Vlans()):
    #     """Vlan setter

    #     : param vlans: Vlans object. Empty Vlans object by default.
    #     """
    #     self.__vlans = vlans

    """
    @management_ipv4.setter
    def management_ipv4(self, ip:str):
        self.__management_ipv4 = ip
    """

    # @inband_ipv4.setter
    # def inband_ipv4(self, ip: str) -> None:
    #     """Inband IPv4 setter

    #     :param ip: IPv4 address in str type
    #     """
    #     self.__inband_ipv4 = ip

    # @gateway_ipv4.setter
    # def gateway_ipv4(self, ip: str) -> None:
    #     """Gateway IPv4 setter

    #     :param ip: IPv4 address in str type
    #     """
    #     self.__gateway_ipv4 = ip

    # @dns_ipv4.setter
    # def dns_ipv4(self, ip: str) -> None:
    #     """DNS IPv4 setter

    #     :param ip: IPv4 address in str type
    #     """
    #     self.__dns_ipv4 = ip

    # @dns_secondary_ipv4.setter
    # def dns_secondary_ipv4(self, ip: str) -> None:
    #     """DNS Secondary IPv4 setter

    #     :param ip: IPv4 address in str type
    #     """
    #     self.__dns_secondary_ipv4 = ip

    # @ntp_server.setter
    # def ntp_server(self, ip: str) -> None:
    #     """NTP Server IPv4 setter

    #     :param ip: IPv4 address in str type
    #     """
    #     self.__ntp_server_ipv4 = ip

    # @ntp_secondary_server.setter
    # def ntp_secondary_server(self, ip: str) -> None:
    #     """NTP Secondary server IPv4 setter

    #     :param ip: IPv4 address in str type
    #     """
    #     self.__ntp_secondary_ipv4 = ip

    """
    @management_ipv6.setter
    def management_ipv6(self, ip6: str):
        Management IPv6 setter
        self.__management_ipv6= ip6
    """

    # @inband_ipv6.setter
    # def inband_ipv6(self, ip6: str) -> None:
    #     """Inband IPv6 setter

    #     :param ip: IPv6 address in str type
    #     """
    #     self.__inband_ipv6 = ip6

    @port.setter
    def port(self, port_number: int) -> None:
        """Port setter

        :param port_number: Port number in int type
        """
        self.__port = port_number

    @timeout.setter
    def timeout(self, timeout_seconds: int) -> None:
        """Setter of timeout interval in seconds

        :param timeout_seconds: Interval of timeout in seconds
        """
        self.__timeout = timeout_seconds

    @keepalive.setter
    def keepalive(self, keepalive_seconds: int) -> None:
        """Setter of keepalive interval in seconds

        :param keepalive_seconds: Interval of keepalive in seconds
        """
        self.__keepalive = keepalive_seconds

    @username.setter
    def username(self, user_name: str) -> None:
        """Username setter

        :param user_name: Username in str type
        """
        self.__username = user_name

    @property
    def password(self):
        return self.__password

    @password.setter
    def password(self, password: str) -> None:
        """Password setter

        :param password: Password in str type in plaintext
        """
        self.__password = password

    # @software.setter
    # def software(self, version: str) -> None:
    #     """Software version setter

    #     :param version: Version of software on switch in str type
    #     """
    #     self.__software = version
