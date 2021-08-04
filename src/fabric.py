import paramiko
from loguru import logger

#from switch_info import Switch_info
#from vlan import Vlans

import re

class Fabric:
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
        self.__connection = None
        self.__fabric_devices = None

        self.__hostname = hostname
        self.open_connection(username,password,port,timeout,keepalive)
        self.__fabric_devices = self.get_parsed_fabric_node_show()

    

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
    
    
    def get_parsed_fabric_node_show(self)->list:
        """Download and parse all nodes that are in same fabric.  
        """
        stdin, stdout, stderr = self.send_command("fabric-node-show")
        fabric_node = []

        for line in stdout:
            fabric_node.append(self.parse_line(line))
        
        return fabric_node
        

    def parse_line(self, line_to_parse:str) -> str:
        """Parse line of code from "fabric node show" output

        :param line_to_parse: line to parse
        """
        pattern = "([a-zA-Z0-9\-\/\_\.]+)\ +([a-zA-Z0-9\-\/\_\.]+)\ +([a-zA-Z0-9\-\/\_\.]+)\ +([a-zA-Z0-9\-\/\_\.]+)\ +([a-zA-Z0-9\-\/\_\.]+)\ +([a-zA-Z0-9\-\/\_\.]+)\ +([a-zA-Z0-9\-\/\_\.]+)\ +([a-zA-Z0-9\-\/\_\.]+)\ +([a-zA-Z0-9\-\/\_\.]+)\ +([a-zA-Z0-9\-\/\_\.]+)\ +"

        parsed_re = re.match(pattern, line_to_parse)
        return parsed_re.group(0)

    def send_command(self, command:str):
        stdin, stdout, stderr = self.__connection.exec_command(command)
        logger.info(f"Command was send. stdout {stdout.read()} ")
        logger.trace(f"Command was send. stdout {stdout.read()} ")
        if not stdout == "":
            logger.error(f"Command was send. stderr {stderr.read()}")
        return stdin, stdout, stderr


    @property
    def fabric_nodes(self):
        """Nodes thaht are associated with this fabric"""
        return self.__fabric_devices
    
    
    
    # Todo: nezapomenou uvést do dokumentace jak se jmenuje ten getter

