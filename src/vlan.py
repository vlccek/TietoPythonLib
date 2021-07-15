import tabulate
from typing import List, Dict, Any, Optional


class Vlans:
    def __init__(self):
        """Stored vlans, example of vlan_dict
        """
        self.__vlans__ = []

    def __id_checker(self, id: Any) -> int:
        """Check if id is already in use and if it's of correct type. If not, Exception is raised.

        :param id: Is being checked for correctness
        """
        if type(id) is not int:
            raise Exception("ID must be int")
        if id < 0:
            raise Exception("ID cannot be negative")
        for i in self.__vlans__:
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

    def __vxlan_checker__(self, vxlan: Optional[Any]) -> Optional[int]:
        """Checks if vxlan is in correct format/type and if it is non-negative number. If not, it returns None.

        :param vxlan: Controlled variable. 
        """
        if vxlan is None or type(vxlan) is not int or vxlan < 0:
            return None
        return vxlan

    def __type_checker__(self, vlan_type: Any) -> str:
        if (
            type(vlan_type) is not str
            or vlan_type == "private"
            or vlan_type != "public"
        ):
            return "private"
        return "public"

    def __replicators_check__(self, replicators: Optional[Any]) -> Optional[str]:
        if type(replicators) is not str:
            return None
        return replicators

    def __bool_check__(self, boolean: Any):
        if type(boolean) is not bool:
            return False
        return boolean

    def add_by_dict(self, vlan_dict: Dict) -> None:
        """add vlan by dict
        !warnings!: the only mandatory key is <<id>> (when <<id>> key is missing or is invalid, exception is raised)
                    every unknown key will be ignored
                    if any key is missing it will be replaced by an empty class of the required data type
                    if any key will be in wrong format it will replace by an empty class of the required data type
        Correct_format=
        {
        "id": 1,
        "type": "private",
        "auto-vxlan": False,
        "replicators": None,
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


        :params vlan_dict: atributes of vlan in dict"""
        new_vlan = {
            "id": self.__id_checker(vlan_dict.get("id", 0)),
            "type": self.__type_checker__(vlan_dict.get("type")),
            "auto-vxlan": self.__bool_check__(vlan_dict.get("auto-vxlan")),
            "replicators": self.__replicators_check__(vlan_dict.get("replicators")),
            "scope": self.__text_checker(vlan_dict.get("scope", "local")),
            "description": self.__text_checker(vlan_dict.get("description", "")),
            "active": self.__bool_check__(vlan_dict.get("active")),
            "stats": self.__bool_check__(vlan_dict.get("stats")),
            "ports": self.__port_checker(vlan_dict.get("ports", [])),
            "untagged_ports": self.__special_port_checker(
                vlan_dict.get("untagged_ports", []), vlan_dict.get("ports", [])
            ),
            "active_ports": self.__special_port_checker(
                vlan_dict.get("active_ports", []), vlan_dict.get("ports", [])
            ),
            "vxlan": self.__vxlan_checker__(vlan_dict.get("vxlan")),
            "vxlanmodule": self.__text_checker(vlan_dict.get("vxlanmodule", "")),
        }
        self.__vlans__.append(new_vlan)
        self.__vlans__ = sorted(self.__vlans__, key=lambda k: k["id"])

    def add_by_params(
        self,
        id: int,
        type: str = "private",
        auto_vxlan: bool = False,
        replicators: Optional[str] = None,
        scope: str = "local",
        description: str = "",
        active: bool = False,
        stats: bool = False,
        ports: List[int] = [],
        untagged_ports: List[int] = [],
        active_ports: List[int] = [],
        vxlan: Optional[int] = None,
        vxlanmodule: str = ""
    ) -> None:
        """Add vlan by parametrs

        :param id: id of new creted vlan
        :param type: type of vlan, defaults to "private"
        :param auto_vxlan:  defaults to False
        :param replicators:  defaults to None
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
            "type": self.__type_checker__(type),
            "auto-vxlan": self.__bool_check__(auto_vxlan),
            "replicators": self.__replicators_check__(replicators),
            "scope": self.__text_checker(scope),
            "description": self.__text_checker(description),
            "active": self.__bool_check__(active),
            "stats": self.__bool_check__(stats),
            "ports": self.__port_checker(ports),
            "untagged_ports": self.__special_port_checker(untagged_ports, ports),
            "active_ports": self.__special_port_checker(active_ports, ports),
            "vxlan": self.__vxlan_checker__(vxlan),
            "vxlanmodule": self.__text_checker(vxlanmodule),
        }
        self.__vlans__.append(new_vlan)
        self.__vlans__ = sorted(self.__vlans__, key=lambda k: k["id"])

    def __repr__(self) -> str:
        if self.__vlans__ == []:
            return ""
        header = self.__vlans__[0].keys()
        rows = [x.values() for x in self.__vlans__]
        return tabulate.tabulate(rows, header)

    def delete(self, id: int) -> None:
        """delere vlan by id

        :param id: id of vlan that should be delete
        :raises Exception: Not existing vlan
        """
        deleted = False
        for i in range(0, len(self.__vlans__)):
            if self.__vlans__[i]["id"] == id:
                delete_idx = i
                self.__vlans__[delete_idx], self.__vlans__[len(self.__vlans__) - 1] = (
                    self.__vlans__[len(self.__vlans__) - 1],
                    self.__vlans__[delete_idx],
                )
                self.__vlans__.pop()
                self.__vlans__ = sorted(self.__vlans__, key=lambda k: k["id"])
                deleted = True
                break
        if not deleted:
            raise Exception("Vlan with such ID isn't in this object")


"""template variable
"""
example_vlan = {
    "id": 1,
    "type": "private",
    "auto-vxlan": False,
    "replicators": None,
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
