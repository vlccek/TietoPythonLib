from typing import List, Dict, Any, Optional

import tabulate
from loguru import logger


class Vlans:
    def __init__(self):
        """Stored vlans, example of vlan_dict"""
        self.__vlans = []

    def __id_checker(self, id: Any) -> int:
        """Check if id is already in use and if it's of correct type. If not, Exception is raised.

        :param id: Is being checked for correctness
        """
        if type(id) is not int:
            raise Exception("ID must be int")
        if id < 0:
            raise Exception("ID cannot be negative")
        for i in self.__vlans:
            if not (i.get("id") != id):
                raise Exception("ID is already in list")
        return id

    def __text_checker(self, text: Any) -> str:
        """Check if variable text is Str. If not, return empty string else return variable text

        :param text: variable that you want to check
        """
        if type(text) is str:
            return text
        return ""

    def __port_checker(self, ports: Any) -> List[int]:
        """Checks if port (ports of swtich) is in correct format and if not, then return empty list.

        :param ports: Controlled variable
        """
        if type(ports) is not list:
            return []
        real_ports = []
        for port in ports:
            if type(port) is int and port >= 0:
                real_ports.append(port)
        return real_ports

    def __special_port_checker(self, special_ports: Any, ports: Any) -> List[int]:
        """Same as __port_checker extended with check if ports in <<special_ports>> list are also in <<ports>> list. If not, that port isn't in result list.

        :param special_ports: Controlled variable. Should be list of ports, which should be tagged somehow.
        :param ports: Controlled variable. Should be list of all ports of vlan.
        """
        if type(ports) is not list or type(special_ports) is not list:
            return []
        real_ports = []
        for port in special_ports:
            if type(port) is int and port >= 0 and port in ports:
                real_ports.append(port)
        return real_ports

    def __vxlan_checker(self, vxlan: Optional[Any]) -> Optional[int]:
        """Checks if vxlan is in correct format/type and if it is non-negative number. If not, it returns None.

        :param vxlan: Controlled variable. Should be int and non-negative number, or None.
        """
        if vxlan is None or type(vxlan) is not int or vxlan < 0:
            return None
        return vxlan

    def __type_checker(self, vlan_type: Any) -> str:
        """Checks if <<vlan_type>> is of correct type and correct format. If not, default value ("private") is returned.

        :param vlan_type: Controlled variable.
        """
        if (
            type(vlan_type) is not str
            or vlan_type == "private"
            or vlan_type != "public"
        ):
            return "private"
        return "public"

    def __bool_check(self, boolean: Any):
        """Checks if <<boolean>> is of bool type. If not, default (False) is returned.

        :param boolean: Controlled variable
        """
        if type(boolean) is not bool:
            return False
        return boolean

    def add_by_dict(self, vlan_dict: Dict) -> None:
        """Adds vlan by dict
        !warnings!: the only mandatory key is <<id>> (when <<id>> key is missing or is invalid, exception is raised)
                    every unknown key will be ignored
                    if any key is missing it will be replaced by an empty class of the required data type
                    if any key will be in wrong format it will replace by an empty class of the required data type
        Correct_format=
        {
        "id": 1,
        "type": "private",
        "auto-vxlan": False,
        "replicators": "",
        "scope": "local",
        "description": "",
        "active": False,
        "stats": False,
        "ports": [],
        "untagged_ports": [],
        "active_ports": [],
        "vxlan": None,
        "vxlanmodule": "",
        }


        :params vlan_dict: Attributes of vlan in dict"""
        new_vlan = {
            "id": self.__id_checker(vlan_dict.get("id", 0)),
            "type": self.__type_checker(vlan_dict.get("type")),
            "auto-vxlan": self.__bool_check(vlan_dict.get("auto-vxlan")),
            "replicators": self.__text_checker(vlan_dict.get("replicators")),
            "scope": self.__text_checker(vlan_dict.get("scope", "local")),
            "description": self.__text_checker(vlan_dict.get("description", "")),
            "active": self.__bool_check(vlan_dict.get("active")),
            "stats": self.__bool_check(vlan_dict.get("stats")),
            "ports": self.__port_checker(vlan_dict.get("ports", [])),
            "untagged_ports": self.__special_port_checker(
                vlan_dict.get("untagged_ports", []), vlan_dict.get("ports", [])
            ),
            "active_ports": self.__special_port_checker(
                vlan_dict.get("active_ports", []), vlan_dict.get("ports", [])
            ),
            "vxlan": self.__vxlan_checker(vlan_dict.get("vxlan")),
            "vxlanmodule": self.__text_checker(vlan_dict.get("vxlanmodule", "")),
        }
        self.__vlans.append(new_vlan)
        self.__vlans = sorted(self.__vlans, key=lambda k: k["id"])

    def add_by_params(
        self,
        id: int,
        type: str = "private",
        auto_vxlan: bool = False,
        replicators: str = "",
        scope: str = "local",
        description: str = "",
        active: bool = False,
        stats: bool = False,
        ports: List[int] = [],
        untagged_ports: List[int] = [],
        active_ports: List[int] = [],
        vxlan: Optional[int] = None,
        vxlanmodule: str = "",
    ) -> None:
        """Adds vlan by parametrs

        :param id: id of new creted vlan, mandatory parameter
        :param type: type of vlan, defaults to "private"
        :param auto_vxlan:  defaults to False
        :param replicators:  defaults to ""
        :param scope:  defaults to "local"
        :param description:  defaults to ""
        :param active:  defaults to False
        :param stats:  defaults to False
        :param ports: defaults to []
        :param untagged_ports:  defaults to []
        :param active_ports:  defaults to []
        :param vxlan: defaults to None
        :param vxlanmodule: defaults to ""
        """
        new_vlan = {
            "id": self.__id_checker(id),
            "type": self.__type_checker(type),
            "auto-vxlan": self.__bool_check(auto_vxlan),
            "replicators": self.__text_checker(replicators),
            "scope": self.__text_checker(scope),
            "description": self.__text_checker(description),
            "active": self.__bool_check(active),
            "stats": self.__bool_check(stats),
            "ports": self.__port_checker(ports),
            "untagged_ports": self.__special_port_checker(untagged_ports, ports),
            "active_ports": self.__special_port_checker(active_ports, ports),
            "vxlan": self.__vxlan_checker(vxlan),
            "vxlanmodule": self.__text_checker(vxlanmodule),
        }
        self.__vlans.append(new_vlan)
        self.__vlans = sorted(self.__vlans, key=lambda k: k["id"])

    def __repr__(self) -> str:
        """Special method for formatting output of class <<Vlans>>"""
        if self.__vlans == []:
            return ""
        header = self.__vlans[0].keys()
        rows = [x.values() for x in self.__vlans]
        return tabulate.tabulate(rows, header)

    def delete(self, id: int) -> None:
        """Deletes vlan by <<id>>

        :param id: id of vlan that should be deleted
        :raises Exception: Not existing vlan
        """
        deleted = False
        for i in range(0, len(self.__vlans)):
            if self.__vlans[i]["id"] == id:
                delete_idx = i
                self.__vlans[delete_idx], self.__vlans[len(self.__vlans) - 1] = (
                    self.__vlans[len(self.__vlans) - 1],
                    self.__vlans[delete_idx],
                )
                self.__vlans.pop()
                self.__vlans = sorted(self.__vlans, key=lambda k: k["id"])
                deleted = True
                break
        if not deleted:
            raise Exception("Vlan with such ID isn't in this object")

    @property
    def vlan_array(self):
        return self.__vlans

    def parse_vlan_show(self, info_to_parse: str):
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
                "ports": self.parse_ports(i[9]),
                "untagged_ports": self.parse_ports(i[10]),
                "active_ports": self.parse_ports(i[11]),
            }
            new_vlan_obj.add_by_dict(new_vlan)
        logger.success("Parsed successfully")
        return new_vlan_obj

    def parse_interval(self, interval_to_parse: str):
        logger.trace("Parsing number interval")
        resolut = re.match("^(\d+)\-(\d+)$", interval_to_parse)
        if not resolut:
            return []

        tmp = []

        for i in range(int(resolut.group(1)), int(resolut.group(2)) + 1):
            tmp.append(i)
        logger.success("Parsed successfully")
        return tmp

    def parse_ports(self, ports_to_parse: str):
        logger.trace("Parsing ports")
        splited = ports_to_parse.split(",")
        output = []
        for i in splited:
            if not "-" in i:
                output.append(int(i))
            else:
                output += parse_interval(i)
        logger.success("Parsed successfully")
        return sorted(output)


"""template variable
"""
example_vlan = {
    "id": 1,
    "type": "private",
    "auto-vxlan": False,
    "replicators": "",
    "scope": "local",
    "description": "",
    "active": False,
    "stats": False,
    "ports": [],
    "untagged_ports": [],
    "active_ports": [],
    "vxlan": None,
    "vxlanmodule": "",
}
