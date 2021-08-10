import paramiko
from loguru import logger
from typing import Any, Tuple, List

import re
# from switch_in_fabric import Switch_in_Fabric
from logger_decorator import logger_wraps

logger.remove()
logger.add('fabric.log', level="TRACE")

#from switch_info import Switch_info
#from vlan import Vlans


class Fabric():
    def __init__(
        self,
        hostname: str,
        username: str,
        password: str,
        port: int = 22,
        timeout: int = 60,
        keepalive: int = 60,
    ) -> None:
        """Created object that iminiadly connect to that switch and find all switch in fabric

        :param hostname: hostname that we connect
        :param username:
        :param password: password to switch
        :param port: port, defaults to 22
        :param timeout: timeout, defaults to 60
        :param keepalive: keepalive, defaults to 60
        """
        logger.success("Object was creted success.")

        self.__connection = None
        self.__fabric_devices = None
        self.__sw_to_change = None

        self.__hostname = hostname
        self.open_connection(username, password, port, timeout, keepalive)
        self.__fabric_devices = self.get_parsed_fabric_node_show()

    def change_configured_device(self, devices: list = None, all: bool = False) -> None:
        if all == True:
            self.get_parsed_fabric_node_show()
            # for sure refresh nodes
            self.__sw_to_change = self.__fabric_devices
        if not devices == None:
            self.__sw_to_change = devices

    @logger_wraps()
    def open_connection(
        self,
        username: str,
        password: str,
        port: int = 22,
        timeout: int = 60,
        keepalive: int = 60,
    ) -> None:
        """Opens a SSH connection"""
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
    def parse_line(self, line_to_parse: str) -> str:
        """Parse line of code from "fabric node show" output

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
        """Download and parse all nodes that are in same fabric.  
        """
        stdin, stdout, stderr = self.send_command(
            "fabric-node-show no-show-headers")
        fabric_node = []
        # print("stdout" + stdout.read()
        line = ""
        for i in stdout:
            line += i
            if (i == "\n"):
                fabric_node.append(self.parse_line(line))
                line = ""
        return fabric_node

    @logger_wraps()
    def send_command(self, command: str,  perfix_with_sw: bool = True) -> Tuple[str, str, str]:
        """Generic function for sending command to switch

        :param command: Command that user want to send
        """
        perfix = ""
        for i in self.__sw_to_change:

            perfix += i
            if not self.__sw_to_change[-1]:
                perfix += ","

        if perfix_with_sw:
            stdin, stdout, stderr = self.__connection.exec_command(
                f"switch {perfix} {command}")

        else:
            stdin, stdout, stderr = self.__connection.exec_command(command)
        logger.info(f"Command {command} was send.")

        stdout_str = str(stdout.read())
        stderr_str = str(stderr.read())
        try:
            stdin_str = str(stdin.read())
        except:
            print("")
            stdin_str = ""

        if not stderr_str == "":
            logger.error(f"Command was send. stderr {stderr_str}")
        return stdin_str, stdout_str, stderr_str

    @logger_wraps()
    def fabric_info(self) -> str:
        """Retruns info from comamnd fabric-info """
        stdin, stdout, stderr = self.send_command("fabric-info")
        return stdout

    @logger_wraps()
    def fabric_node_show(self) -> str:
        """output from command fabric-node-show"""
        stdin, stdout, stderr = self.send_command("fabric-node-show")
        return stdout

    @property
    def fabric_nodes(self) -> List[str]:
        """Nodes thaht are associated with this fabric"""
        return self.__fabric_devices
    # TODO: nezapomenou uvést do dokumentace jak se jmenuje ten getter

    def __del__(self):
        self.__connection.close()
        print("removing obj")

    def port_show(self):
        stdin, stdout, stderr = self.send_command("port-show")
        return stdout

    def port_config_modify(self):
        pass

    def port_phy_show(self):
        stdin, stdout, stderr = self.send_command("port-phy-show")
        return stdout

    def software_show(self):
        stdin, stdout, stderr = self.send_command("software-show")
        return stdout
