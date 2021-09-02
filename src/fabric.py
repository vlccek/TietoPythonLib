from sys import stderr, stdout
from threading import local
import paramiko
from loguru import logger
from typing import Any, Tuple, List, Dict

import re

# from switch_in_fabric import Switch_in_Fabric
from logger_decorator import logger_wraps

logger.remove()
logger.add("fabric.log", level="TRACE")

# from switch_info import Switch_info
# from vlan import Vlans


class Fabric:
    """Created object that iminiadly connect to that switch and find all switch in fabric

    .. code::

        pepa = Fabric("pepa.cz", "root", "pa$$word123")


    :param hostname: hostname that we connect
    :param username: username of user that we connect
    :param password: password to switch
    :param port: port, defaults to 22
    :param timeout: timeout, defaults to 60
    :param keepalive: keepalive, defaults to 60
    """

    def __init__(
        self,
        hostname: str,
        username: str,
        password: str,
        port: int = 22,
        timeout: int = 60,
        keepalive: int = 60,
    ) -> None:

        logger.success("Object was creted success.")

        self.__connection = None
        self.__fabric_devices = None
        self.__sw_to_change = None
        self.__vlans = []

        self.__hostname = hostname
        self.open_connection(username, password, port, timeout, keepalive)
        self.__fabric_devices = self.get_parsed_fabric_node_show()
        self.__sw_to_change = self.__fabric_devices

    @logger_wraps()
    @logger.catch
    def open_connection(
        self,
        username: str,
        password: str,
        port: int = 22,
        timeout: int = 60,
        keepalive: int = 60,
    ) -> None:
        """Open ssh connection to switch

        Run on creation of object. No need to run manualy

        :param username: Username that are connected
        :param password: Password
        :param port: port of ssh, defaults to 22
        :param timeout: timeout, defaults to 60
        :param keepalive: keeplive, defaults to 60
        """
        self.__connection = paramiko.SSHClient()
        self.__connection.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.__connection.connect(
            hostname=self.__hostname,
            username=username,
            password=password,
            timeout=timeout,
            port=port,
        )
        self.__connection.get_transport().set_keepalive(keepalive)
        self.__connected = True
        logger.success("Connection SUCCESS")
        return self.__connection

    @logger_wraps()
    def update_vlans(self):
        """Update vlans from switch"""
        stdin, stdout, stderr = self.send_command("vlan-show no-show-headers")

        self.__vlans = self.parse_vlan_show(stdout)

    @logger_wraps()
    def parse_vlan_show(self, info_to_parse: str) -> List[Dict[str, str]]:
        """Parse output from vlan show"""
        pattern = "(?P<Sw_name>[a-zA-Z0-9_.-]*)\s+(?P<vlan_id>\d+)\s+(?P<type>\w+)\s+(?P<auto_vxlan>yes|no)\s+(?P<replicators>\w+)\s+(?P<scope>\w+)\s+(?P<description>[a-zA-Z0-9_.-]*)\s+(?P<active>yes|no)\s+(?P<stats>yes|no)\s+(?P<ports>[0-9,-]*|none)\s+(?P<untagged_ports>[0-9,-]*|none)\s+(?P<active_ports>none|[0-9,-]*)"
        # https://regexr.com/61s1p
        match = re.findall(pattern, info_to_parse)
        vlans = []
        for i in match:
            new_vlan = {
                "id": i[1],
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
            vlans.append(new_vlan)
        return vlans

    @logger_wraps()
    def parse_line_of_node_show(self, line_to_parse: str) -> str:
        """Parse line of code from "fabric node show" output

         Run on creation of object. No need to run manualy (for dowload fabric members)

        :param line_to_parse: line to parse
        """
        pattern = "([a-zA-Z0-9\-\/\_\.]+)\ +([a-zA-Z0-9\-\/\_\.]+)\ +([a-zA-Z0-9\-\/\_\.]+)\ +([a-zA-Z0-9\-\/\_\.]+)\ +([a-zA-Z0-9\-\/\_\.]+)\ +([a-zA-Z0-9\-\/\_\.]+)\ +([a-zA-Z0-9\-\/\_\.]+)\ +([a-zA-Z0-9\-\/\_\.]+)\ +([a-zA-Z0-9\-\/\_\.]+)\ +([a-zA-Z0-9\-\/\_\.]+)\ +"

        parsed_re = re.match(pattern, line_to_parse)
        if parsed_re != None:
            return parsed_re.group(1)
        else:
            return ""

    @logger_wraps()
    def get_parsed_fabric_node_show(self) -> List[str]:
        """Download and parse all nodes that are in same fabric."""
        stdin, stdout, stderr = self.__connection.exec_command(
            "fabric-node-show no-show-headers"
        )
        fabric_node = []
        # print("stdout" + stdout.read()
        for i in stdout:
            parsed = self.parse_line_of_node_show(i)
            if not parsed == "":
                fabric_node.append(parsed)
        return fabric_node

    @logger_wraps()
    def send_command_with_prefix(
        self, command: str, switches: str = ""
    ) -> Tuple[str, str, str]:
        """Run command with some kind of perfix before command example: "switch {sw01,sw02} <random command>"

        :param command: command what you want to run
        """
        print("Full command: \n" + command)
        if not switches:
            stdin, stout, stderr = self.send_command(command)
            print("Stdin:\n" + str(stdin))
            print("Stdout:\n" + str(stdout))
            print("Stderr:\n" + str(stderr))
        else:
            command = f"switch {switches} {command}"
            stdin, stout, stderr = self.send_command(command)
        # command = f"switch {self.__sw_to_change} {command}"

        return stdin, stout, stderr

    @logger_wraps()
    def send_command(self, command: str) -> Tuple[str, str, str]:
        """Generic function for sending command to switch
        To co dám na vstup tak se pustí (je mi jedno jestli se to pustí na všech nebo tak)

        :param command: Command that user want to send
        """
        stdin, stdout, stderr = self.__connection.exec_command(command)
        logger.info(f"Command {command} was send.")

        stdout_str = str(stdout.read())
        stderr_str = str(stderr.read())
        try:
            stdin_str = str(stdin.read())
        except:
            stdin_str = ""

        if not stderr_str == "":
            logger.error(f"Command was send. stderr {stderr_str}")
        return stdin_str, stdout_str, stderr_str

    @logger_wraps()
    def fabric_info(self) -> str:
        """Retruns info from comamnd `fabric-info`"""
        command = ""
        if format != "":
            command = f" format {format}"
        stdin, stdout, stderr = self.send_command("fabric-info")
        return stdout

    @logger_wraps()
    def fabric_node_show(self, format: str = "") -> str:
        """output from command `fabric-node-show`"""
        command = ""
        if format != "":
            command = f" format {format}"
        stdin, stdout, stderr = self.send_command("fabric-node-show")
        return stdout

    @logger_wraps()
    def node_show(self, format: str = "") -> str:
        """output from command `node-show`"""
        command = ""
        if format != "":
            command = f" format {format}"
        stdin, stdout, stderr = self.send_command("node-show")
        return stdout

    @property
    def fabric_nodes(self) -> List[str]:
        """Nodes thaht are associated with this fabric"""
        return self.__fabric_devices

    def __del__(self):
        self.__connection.close()
        logger.info(
            f"Disconecting from switch: {self.__hostname}. Object was destroyed."
        )
        print("Disconecting from switch: {self.__hostname}. Object was destroyed.")

    @logger_wraps()
    def port_show(self, format: str = "") -> str:
        """Cannot run with switch <...> port-show"""
        command = ""
        if format != "":
            command = f" format {format}"
        stdin, stdout, stderr = self.send_command("port-show")
        return stdout

    @logger_wraps()
    def port_config_modify(
        self,
        port_list: str,
        speed: str = "",
        egress_rate_limit: str = "",
        eth_mode: str = "",
        autoneg: bool = False,
        no_autoneg: bool = False,
        jumbo: bool = False,
        no_jumbo: bool = False,
        enable: bool = False,
        disable: bool = False,
        lacp_priority: str = "",
        reflect: bool = False,
        non_reflect: bool = False,
        edge_switch: bool = False,
        no_edge_switch: bool = False,
        pause: bool = False,
        no_pause: bool = False,
        description: str = "",
        loopback: bool = False,
        no_loopback: bool = False,
        vxlan_termination: bool = False,
        no_vxlan_termination: bool = False,
        mirror_only: bool = False,
        no_mirror_receive_only: bool = False,
        port_mac_address: bool = False,
        send_port: str = "",
        loop_vlans: str = "",
        routing: bool = False,
        no_routing: bool = False,
        defer_bringup: bool = False,
        no_defer_bringup: bool = False,
        host_enable: bool = False,
        host_disable: bool = False,
        crc_check_enable: bool = False,
        crc_check_disable: bool = False,
        dscp_map: str = "",
        local_switching: bool = False,
        no_local_switching: bool = False,
        allowed_tpid: bool = False,
        fabric_guard: bool = False,
        no_fabric_guard: bool = False,
        fec: bool = False,
        no_fec: bool = False,
        switches: str = "",
    ):
        """Ports config modify"""
        arguments = locals()

        command = ""
        for key, value in arguments.items():
            if key.startswith("__"):
                continue
            elif type(value) is str:
                if not value == "":
                    command += f""" {key.replace("_", "-")} {value}"""
            elif type(value) is bool:
                if value == True:
                    command += f""" {key.replace("_", "-")}"""

        stdin, stdout, stderr = self.send_command_with_prefix(
            "port-config-modify" + command, switches
        )
        return stdout

    @logger_wraps()
    def port_phy_show(self, switches: str = "", format: str = ""):
        """Run commnad `port-phy-show`

        :param switches: switches where should be show runs, defaults to ""
        :param format: column that should shows, defaults to ""
        :return: stdout of command
        """
        command = ""
        if format != "":
            command = f" format {format}"
        stdin, stdout, stderr = self.send_command_with_prefix(
            "port-phy-show" + command, switches
        )
        return stdout

    @logger_wraps()
    def software_show(self, switches: str = "", format: str = ""):
        """Run commnad `software-show`

        :param switches: switches where should be show runs, defaults to ""
        :param format: column that should shows, defaults to ""
        :return: stdout of command
        """
        command = ""
        if format != "":
            command = f" format {format}"
        stdin, stdout, stderr = self.send_command_with_prefix(
            "software-show" + command, switches
        )
        return stdout

    @logger_wraps()
    def switch_config_show(self, switches: str = "", format: str = ""):
        """Run commnad `switch-config-show`

        :param switches: switches where should be show runs, defaults to ""
        :param format: column that should shows, defaults to ""
        :return: stdout of command
        """
        command = ""
        if format != "":
            command = f" format {format}"
        stdin, stdout, stderr = self.send_command_with_prefix(
            "switch-config-show" + command, switches
        )
        return stdout

    @logger_wraps()
    def switch_setup_show(self, switches: str = "", format: str = ""):
        """Run commnad `switch-setup-show`

        :param switches: switches where should be show runs, defaults to ""
        :param format: column that should shows, defaults to ""
        :return: stdout of command
        """
        command = ""
        if format != "":
            command = f" format {format}"
        stdin, stdout, stderr = self.send_command_with_prefix(
            "switch-setup-show" + command, switches
        )
        return stdout

    @logger_wraps()
    def vlan_show(self, switches: str = "", format: str = ""):
        """Run commnad `vlans-show`

        :param switches: switches where should be show runs, defaults to ""
        :param format: column that should shows, defaults to ""
        :return: stdout of command
        """
        command = ""
        if format != "":
            command = f" format {format}"
        stdin, stdout, stderr = self.send_command_with_prefix(
            "vlan-show" + command, switches
        )
        return stdout

    @logger_wraps()
    def vlan_create(
        self,
        id_or_range: str,
        scope: str,
        vnet: str = "",
        vxlan: str = "",
        auto_vxlan: str = "",
        vxlan_mode: str = "",
        replicators: str = "",
        public_vlan: str = "",
        description: str = """""",
        stats: bool = False,
        no_stats: bool = False,
        ports: str = "",
        untagged_ports: str = "",
        switches: str = "",
    ) -> str:
        """Adds vlan by parametrs

        :param id: id of new creted vlan, mandatory parameter
        :param scope:  defaults to ""
        :param vnet: defaults to ""
        :param vxlan: defaults to ""
        :param auto_vxlan:  defaults to ""
        :param vxlan_mode: defaults to ""
        :param replicators:  defaults to ""
        :param public_vlan: defaults to ""
        :param description:  defaults to ""
        :param stats:  defaults to False
        :param no_stats: defaults to False
        :param ports: defaults to ""
        :param untagged_ports:  defaults to ""
        """

        arguments = locals()

        command = ""
        for key, value in arguments.items():
            if key.startswith("__") or key == "switches":
                continue
            elif type(value) is str:
                if key == "id_or_range":
                    if "," in value or "-" in value:
                        command += f" range {value}"
                    else:
                        command += f" id {value}"
                elif not value == "":
                    command += f""" {key.replace("_", "-")} {value}"""
            elif type(value) is bool:
                if value == True:
                    command += f""" {key.replace("_", "-")}"""
        print("command parametres:\n" + command)

        stdin, stdout, stderr = self.send_command_with_prefix(
            "vlan-create" + command, switches
        )
        self.update_vlans()
        return stdout

    @logger_wraps()
    def vlan_delete(self, id_or_range: str, switches: str = "") -> str:
        """Delete vlan

        :param id_or_range: id or range of vlans thath should be deleted
        :param switches: switches that should be run, defaults to ""
        :return: stdout
        """
        if "," in id_or_range or "-" in id_or_range:
            command = f" range {id_or_range}"
        else:
            command = f" id {id_or_range}"

        stdin, stdout, stderr = self.send_command_with_prefix(
            "vlan-delete" + command, switches
        )
        self.update_vlans()
        return stdout

    @logger_wraps()
    def vlan_port_add(
        self,
        id_or_range: str,
        switch: str,
        ports: str,
        untagged: bool = False,
        tagged: bool = False,
    ):
        """Add ports to vlan

        :param id_or_range: id of new creted vlan, mandatory parameter
        :param switch: switchs
        :param ports: ports, defaults to ""
        :param tagged: defaults to ""
        :param untagged:  defaults to ""
        """
        arguments = locals()

        command = ""
        for key, value in arguments.items():
            # if key.startswith("__") or key == "switches":
            #    continue
            if type(value) is str:
                if key == "id_or_range":
                    if "," in value or "-" in value:
                        command += f" range {value}"
                    else:
                        command += f" id {value}"
                elif not value == "":
                    command += f""" {key.replace("_", "-")} {value}"""
            elif type(value) is bool:
                if value == True:
                    command += f""" {key.replace("_", "-")}"""

        stdin, stdout, stderr = self.send_command_with_prefix("vlan-port-add" + command)
        self.update_vlans()
        return stdout

    @logger_wraps()
    def vlan_modify(
        self,
        id: str,
        description: str = "",
        vxlan: str = "",
        replicators: str = "",
        vnet: str = "",
        public_vlan: str = "",
    ) -> str:
        """modify vlan

        Example:

        .. code::

            pepa.vlan_modify(id="10", description="New text")

        :param id: id of vlan
        :param description: description
        :param vxlan: vxlan
        :param vnet: vnet
        :param public:vlan: public vlan
        """
        arguments = locals()

        command = ""
        counter = -1
        for key, value in arguments.items():
            # if key.startswith("__") or key == "switches":
            #    continue
            if type(value) is str:
                if key == "id" or not value == "":
                    command += f""" {key.replace("_", "-")} {value}"""
                    counter += 1

        if counter < 1 or counter > 4:
            raise Exception("Too many arguments or no arguments")
        stdin, stdout, stderr = self.send_command_with_prefix("vlan-modify" + command)
        self.update_vlans()
        return stdout
