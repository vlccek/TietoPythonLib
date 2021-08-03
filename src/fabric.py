import paramiko
from loguru import logger

from switch_info import Switch_info
from vlan import Vlans


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

        self.__hostname = hostname
        self.open_connection()

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
