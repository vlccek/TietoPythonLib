from loguru import logger

from vlan import Vlans


def parse_switch_setup_show(info_to_parse: str) -> dict:
    """parse output of command switch setup show

    :param info_to_parse: string format info
    :return: parsed information
    """
    pattern = "(.[^\:]*)\:\ *(.*)"
    logger.trace("Parsing switch-setup-show")
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
    logger.success("Parsed successfully")
    return new_dictionary


def parse_vlan_show(info_to_parse: str) -> Vlans:
    """Parse vlan show

    :param info_to_parse: string to parse
    """
    pattern = "(?P<Sw_name>[a-zA-Z0-9_.-]*)\s+(?P<vlan_id>\d+)\s+(?P<type>\w+)\s+(?P<auto_vxlan>yes|no)\s+(?P<replicators>\w+)\s+(?P<scope>\w+)\s+(?P<description>[a-zA-Z0-9_.-]*)\s+(?P<active>yes|no)\s+(?P<stats>yes|no)\s+(?P<ports>[0-9,-]*|none)\s+(?P<untagged_ports>[0-9,-]*|none)\s+(?P<active_ports>none|[0-9,-]*)"
    # https://regexr.com/61s1p
    logger.trace("Parsing vlan-show")
    new_vlan_obj = Vlans()
    logger.debug("Vlan object created successfully")
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
    logger.success("Parsed successfully")
    return new_vlan_obj


def parse_interval(interval_to_parse: str):
    logger.trace("Parsing number interval")
    resolut = re.match('^(\d+)\-(\d+)$', interval_to_parse)
    if not resolut:
        return []

    tmp = []

    for i in range(int(resolut.group(1)), int(resolut.group(2)) + 1):
        tmp.append(i)
    logger.success("Parsed successfully")
    return tmp


def parse_ports(ports_to_parse: str):
    logger.trace("Parsing ports")
    splited = ports_to_parse.split(',')
    output = []
    for i in splited:
        if not '-' in i:
            output.append(int(i))
        else:
            output += parse_interval(i)
    logger.success("Parsed successfully")
    return sorted(output)
