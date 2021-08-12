import re


class Vnet:
    def __init__(self, id, name, scope, vlan_type):
        self.__id = id
        pass


r = """Netvisor OS Command Line Interface 6.1
Connected to Switch 102-NRU02-spine-01; nvOS Identifier:0x11000044; Ver: 6.1.0-6010018207
LINUX TRACK - 6.1.0 HF1

name               fab-name                                    mgmt-ip         in-band-ip        in-band-vlan-type fab-tid cluster-tid out-port version          state  firmware-upgrade device-state 
------------------ ------------------------------------------- --------------- ----------------- ----------------- ------- ----------- -------- ---------------- ------ ---------------- ------------ 
102-NRU02-spine-01 fabric_a6da4ba2-2e55-4f70-8dd6-b754a549e7fd 21.102.28.11/19 169.254.102.11/24 public            39      6                    6.1.0-6010018207 online not-required     ok           
102-NRU02-spine-02 fabric_a6da4ba2-2e55-4f70-8dd6-b754a549e7fd 21.102.28.21/19 169.254.102.21/24 public            39      6           272      6.1.0-6010018207 online not-required     ok           
102-NRU02-leaf-02  fabric_a6da4ba2-2e55-4f70-8dd6-b754a549e7fd 21.102.28.41/19 169.254.102.41/24 public            39      4           274      6.1.0-6010018207 online not-required     ok           
102-NRU02-leaf-01  fabric_a6da4ba2-2e55-4f70-8dd6-b754a549e7fd 21.102.28.31/19 169.254.102.31/24 public            39      4           274      6.1.0-6010018207 online not-required     ok           
102-NRU02-leaf-03  fabric_a6da4ba2-2e55-4f70-8dd6-b754a549e7fd 21.102.28.51/19 169.254.102.51/24 public            39      4           274      6.1.0-6010018207 online not-required     ok           
102-NRU02-leaf-04  fabric_a6da4ba2-2e55-4f70-8dd6-b754a549e7fd 21.102.28.61/19 169.254.102.61/24 public            39      4           274      6.1.0-6010018207 online not-required     ok           
"""
tsplited = r.splitlines()


def parse_line(line_to_parse: str) -> str:
    """Parse line of code from "fabric node show" output

    :param line_to_parse: line to parse
    """
    pattern = "([a-zA-Z0-9\-\/\_\.]+)\ +([a-zA-Z0-9\-\/\_\.]+)\ +([a-zA-Z0-9\-\/\_\.]+)\ +([a-zA-Z0-9\-\/\_\.]+)\ +([a-zA-Z0-9\-\/\_\.]+)\ +([a-zA-Z0-9\-\/\_\.]+)\ +([a-zA-Z0-9\-\/\_\.]+)\ +([a-zA-Z0-9\-\/\_\.]+)\ +([a-zA-Z0-9\-\/\_\.]+)\ +([a-zA-Z0-9\-\/\_\.]+)\ +"

    parsed_re = re.match(pattern, line_to_parse)
    if parsed_re != None:
        return parsed_re.group(1)
    else:
        return ""


for i in tsplited:
    # print(i)
    print(parse_line(line_to_parse=i))
