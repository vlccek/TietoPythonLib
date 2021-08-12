import sys
from typing import List

import paramiko
from loguru import logger

from switch_info import Switch_info
from vlan import Vlans

import copy
import tabulate


class Switch:
    def __init__(
        self,
        username: str,
        password: str,
        host: str,
        port: int = 22,
        timeout: int = 60,
        keepalive: int = 60,
    ) -> None:
        logger.add(
            sys.stdout, colorize=True, format="{time} {level} {message}", level=0
        )
        logger.debug("Logger up")

        logger.info("Pepa")

        self.__info = Switch_info()
        self.__otherConnected = []
        pepa.info.dns_ipv4 = ""
        self.__old_info = Switch_info()
        logger.debug("Succes add Vlans nad switch info private variables")

        self.__port = port
        self.__timeout = timeout
        self.__keepalive = keepalive
        self.__username = username
        self.__password = password
        logger.debug("Succes set connection parametrs")

        self.__changed = False
        self.__connected = False
        self.__connection = None
        self.__host = host

        logger.success("Object Crete succesfull opening connection with switch.")
        self.open()
        # tady budu načítat informace o sw
        self.load_switch_setup()
        self.load_vlan_show()
        self.__old_info = copy.deepcopy(self.__info)

    @logger.catch
    def open(self):
        """Opens a SSH connection"""
        self.__connection = paramiko.SSHClient()
        self.__connection.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.__connection.connect(
            hostname=self.__host,
            username=self.__username,
            password=self.__password,
            timeout=self.__timeout,
            port=self.__port,
        )
        self.__connection.get_transport().set_keepalive(self.__keepalive)
        self.__connected = True
        logger.success("Connection SUCCESS")
        return self.__connection

    def run_command(self, command: str):
        stdin, stdout, stderr = self.__connection.exec_command(command)
        return stdin, stdout, stderr

    def load_switch_setup(self):
        logger.trace("Starting loading switch setup")
        stdin, stdout, stderr = self.run_command("switch-setup-show")
        comandoutput = ""

        for line in stdout:
            comandoutput += line

        parseddict = self.__info.parse_switch_setup_show(comandoutput)
        self.__info.from_dict_to_attributes(parseddict)
        logger.success("Loading switch setup SUCCESS")

    def load_vlan_show(self):
        logger.trace("Starting colecting vlan info")
        stdin, stdout, stderr = self.run_command("switch-setup-show")
        comandoutput = ""

        for line in stdout:
            comandoutput += line

        self.info.vlans.parse_vlan_show(comandoutput)
        logger.success("Loadinf switch vlans SUCCESS")

    def commit(self):
        """Send changes made in Switch object to switch"""
        # self.__info.
        # TODO
        pass

    def __repr__(self) -> str:
        output = f"""Switch name: {self.info.__switch_name}
Connection information:
host (connected by): {self.__host}
port: {self.__port}
timeout: {self.__timeout}"""
        pass

    @property
    def info(self):
        return self.__info

    @property
    def old_info(self):
        return self.__old_info

    @property
    def port(self):
        """Port getter"""
        logger.trace("Getting port")
        return self.__port

    @property
    def timeout(self):
        """Timeout getter"""
        logger.trace("Getting timeout")
        return self.__timeout

    @property
    def keepalive(self):
        """Keepalive getter"""
        logger.trace("Getting keepalive")
        return self.__keepalive

    @property
    def username(self):
        """Username getter"""
        logger.trace("Getting username")
        return self.__username

    @property
    def connected(self):
        """Connected getter"""
        logger.trace("Getting connecetion")
        return self.__connected

    @port.setter
    def port(self, port_number: int) -> None:
        """Port setter

        :param port_number: Port number in int type
        """
        logger.info(f"Changing port from {self.__port} to {port_number}")
        self.__port = port_number
        logger.success("Port changed")

    # @timeout.setter
    # def timeout(self, timeout_seconds: int) -> None:
    #     """Setter of timeout interval in seconds

    #     :param timeout_seconds: Interval of timeout in seconds
    #     """
    #     self.__timeout = timeout_seconds
    #     logger.success("")

    # @keepalive.setter
    # def keepalive(self, keepalive_seconds: int) -> None:
    #     """Setter of keepalive interval in seconds

    #     :param keepalive_seconds: Interval of keepalive in seconds
    #     """
    #     self.__keepalive = keepalive_seconds
    #     logger.success("")

    # @username.setter
    # def username(self, user_name: str) -> None:
    #     """Username setter

    #     :param user_name: Username in str type
    #     """
    #     self.__username = user_name
    #     logger.success("")

    # @password.setter
    # def password(self, password: str) -> None:
    #     """Password setter

    #     :param password: Password in str type in plaintext
    #     """
    #     self.__password = password

    @staticmethod
    def comapare_2_switch_info(new: Switch_info, old: Switch_info):
        """compare 2 switch info a return dict"""
        diff = []
        if not new.vlans == old.vlans:
            tmp = diff_vlans(new.vlans, old.vlans)
            diff.append({"vlans": tmp})
        if not new.inband_ipv4 == old.inband_ipv4:
            diff.append("inband_ipv4")
        """
        if new.gateway_ipv6 == old.gateway_ipv6:
            diff.append("gateway_ipv4")
        """
        if not new.dns_ipv4 == old.dns_ipv4:
            diff.append("dns_ipv4")
        if not new.dns_secondary_ipv4 == old.dns_secondary_ipv4:
            diff.append("dns_secondary_ipv4")
        if not new.ntp_server == old.ntp_server:
            diff.append("ntp_server")
        if not new.ntp_secondary_server == old.ntp_secondary_server:
            diff.append("ntp_secondary_server")
        if not new.software == old.software:
            diff.append("software")
        if not new.domain_name == old.domain_name:
            diff.append("domain_name")
        if not new.time_zone == old.time_zone:
            diff.append("time_zone")
        if not new.hostid == old.hostid:
            diff.append("hostid")
        if not new.location_id == old.location_id:
            diff.append("location_id")
        if not new.motd == old.motd:
            diff.append("motd")
        if not new.banner == old.banner:
            diff.append("banner")
        if not new.mgmt_lag == old.mgmt_lag:
            diff.append("mgmt_lag")
        if not new.mgmt_lacp_mode == old.mgmt_lacp_mode:
            diff.append("mgmt_lacp_mode")
        if not new.ntp == old.ntp:
            diff.append("ntp")
        return diff


def diff_vlans(new: Vlans, old: Vlans) -> dict:
    """generrate diff between self and second

    :param second: new vlans
    """
    logger.trace("Running diff vlans function")
    old_vlans = old.vlan_array
    new_vlans = new.vlan_array

    ids_new = [i["id"] for i in new_vlans]
    ids_old = [i["id"] for i in old_vlans]
    diff = {"new_vlans": [], "edited_vlans": {}, "removed_vlans": []}
    diff["new_vlans"] = list(set(ids_new) - set(ids_old))
    diff["removed_vlans"] = list(set(ids_old) - set(ids_new))
    changed_or_original = set(set(ids_new) & set(ids_old))

    for i in range(len(old_vlans)):
        # procházím od 0 až po počet slovníku v old_vlans
        if old_vlans[i]["id"] in changed_or_original:
            # pokud je id právě zkoumáného slovníku v changed_or_original
            diff["edited_vlans"][old_vlans[i]["id"]] = list()
            # přídá se místo pro právě kontrolvaný slovník v diff
            # 'edited_vlans': {104: []}
            for key in list(set(old_vlans[i].keys()) - {"id"}):
                # projdou se všechny klíče od i-tého vlanu (bez id)
                if not old_vlans[i].get(key) == new_vlans[i].get(key):
                    # pokud nejsou hodnoty klíčů stejné tak se zapíše jako edited :D
                    diff["edited_vlans"][old_vlans[i]["id"]].append(key)
                    # jak jednoduché

    # ezzzy funguje :)
    logger.success("Comparing complete. More info in info trace log.")
    logger.trace("Dict with changes: \n {}".format(diff))
    return diff
