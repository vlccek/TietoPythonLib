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





class Switch:
    def __init__(self, username: str, password: str, host:str, port: int = 22, timeout: int = 60, keepalive: int = 60) -> None:
        logger.add(sys.stdout,colorize=True, format="{time} {level} {message}", level=0)
        logger.remove(0)
        logger.debug("Logger up")

        logger.info("Pepa")

        self.__vlans = Vlans()
        self.__info = Switch_info()
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

    @logger.catch
    def open(self):
        """Opens a SSH connection"""         
        self.__connection = paramiko.SSHClient()
        self.__connection.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.__connection.connect(hostname=self.__host,
                                    username=self.__username,
                                    password=self.__password,
                                    timeout=self.__timeout,
                                    port=self.__port)
        self.__connection.get_transport().set_keepalive(self.__keepalive)
        self.__connected = True
        logger.success("Connection SUCCESS")
        return self.__connection

        
    

    def run_command(self, commands: List[str]):
        # TODO
        pass

    def commit(self):
        """Send changes made in Switch object to switch"""
        if not self.__changed:
            return
        # TODO
        pass

    @property
    def port(self):
        """Port getter
        """
        logger.trace("Getting port")
        return self.__port

    @property
    def timeout(self):
        """Timeout getter
        """
        logger.trace("Getting timeout")
        return self.__timeout

    @property
    def keepalive(self):
        """Keepalive getter
        """
        logger.trace("Getting keepalive")
        return self.__keepalive

    @property
    def username(self):
        """Username getter
        """
        logger.trace("Getting username")
        return self.__username


    @property
    def connected(self):
        """Connected getter
        """
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