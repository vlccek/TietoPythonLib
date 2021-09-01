from datetime import time
from threading import local
from loguru import logger
import paramiko
import datetime


def download(
    hostname: str,
    username: str,
    password: str,
    name_of_log: str = f"""log-snapshot-{datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")}""",
    port: int = 22,
    timeout: int = 60,
    keepalive: int = 60,
):
    connection = open_connection(username, password, hostname, port, timeout, keepalive)

    connection.exec_command(
        f"tar -czcf {name_of_log} /var/adm /var/fm /nvOS/log /var/nvOS/ /var/svc/ /var/log/ --exclude='/var/nvOS/log/cores/*' --exclude='/var/nvOS/mirror/*'"
    )

    local_path = f"./{name_of_log}"
    remote_path = f"./{name_of_log}"

    sftp = connection.open_sftp()
    sftp.get(local_path, remote_path)
    sftp.close()
    connection.close()


def open_connection(
    self,
    username: str,
    password: str,
    hostname: str,
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
    __connection = paramiko.SSHClient()
    __connection.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    __connection.connect(
        hostname=hostname,
        username=username,
        password=password,
        timeout=timeout,
        port=port,
    )
    __connection.get_transport().set_keepalive(keepalive)
    __connected = True
    logger.success("Connection SUCCESS")
    return __connection
