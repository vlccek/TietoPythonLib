from loguru import logger
import paramiko
import datetime
from download import open_connection
from tests import settings


def download_diags(
    self,
    hostname: str = settings.hostname,
    port: int = settings.port,
    timeout: int = 60,
    keepalive: int = 60,
) -> None:
    network = open_connection(
        "network-admin", settings.password, hostname, port, timeout, keepalive)

    network.exec_command(f"admin-sftp-modify enable")
    if "Diagnostics info saved." not in send_command_with_input(network, "save-diags"):
        print("Did not run save-diags properly")
        return
    logger.info(f"save-diags ran properly")
    if "Diagnostics exported to /sftp/export" not in send_command_with_input(network, "export-diags"):
        print("Did not run export-diags properly")
        return
    logger.info(f"export-diags ran properly")
    network.close()
    logger.info(f"Closed connection as network-admin")

    admin = open_connection("admin", settings.password,
                            hostname, port, timeout, keepalive)

    latest = 0
    latestfile = None

    sftp = admin.open_sftp()
    sftp.chdir('/sftp/export')
    for fileattr in sftp.listdir_attr():
        if fileattr.filename.startswith('core.nvOSd') and fileattr.st_mtime > latest:
            latest = fileattr.st_mtime
            latestfile = fileattr.filename

    if latestfile is not None:
        sftp.get(latestfile, latestfile)

    sftp.close()
    admin.close()


def send_command_with_input(connection, command):
    stdin, stdout, stderr = connection.exec_command(command, get_pty=True)
    stdin.write("/n")
    stdin.flush()
    stdin.write(settings.password + "/n")
    stdin.flush()
    return str(stdout.read())
