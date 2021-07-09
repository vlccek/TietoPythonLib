from typing import List, Dict, Any, Optional


class Vlans:
    __vlan_example__ = {
        "id": 0,
        "description": "",
        "interface": [],
        "scope": "",
        "ports": [],
        "Untagedports": [],
        "Activeports": [],
        "vxlan": 0,
        "vxlanmodule": ""
    }

    def __init__(self):
        """
        Stored vlans, example of vlan_dict
        """
        self.__vlans__ = []

    def __id_checker__(self, id: int) -> int:
        for i in self.__vlans__:
            if not (i.get("id") != id and id > 0):
                raise Exception("ID invalid or already in list")
        return id

    def __text_checker__(self, text: Any) -> str:
        if type(text) is str:
            return text
        return ""

    def __port_checker__(self, ports: Any) -> List[int]:
        if type(ports) is not list:
            return []
        real_ports = []
        for port in ports:
            if type(port) is int and port >= 0:
                real_ports.append(port)
        return real_ports

    def __vxlan_checker__(self, vxlan: Optional[Any]) -> Optional[int]:
        if vxlan is None or type(vxlan) is not int or vxlan < 0:
            return None
        return vxlan

    def __type_checker__(self, vlan_type: Any) -> str:
        if type(vlan_type) is not str or vlan_type == "private" \
                                        or vlan_type != "public":
            return "private"
        return "public"

    def check_vlan_dict(self, vlan_dict: Dict) -> Dict:
        new_vlan = {
            "id": self.__id_checker__(vlan_dict.get("id", 0)),
            "description": self.__text_checker__(vlan_dict.get("description", "")),
            "type": self.__type_checker__(vlan_dict.get("type")),
            "scope": self.__text_checker__(vlan_dict.get("scope", "local")),
            "ports": self.__port_checker__(vlan_dict.get("ports", [])),
            "untagged_ports": self.__port_checker__(vlan_dict.get("untagged_ports", [])),
            "active_ports": self.__port_checker__(vlan_dict.get("active_ports", [])),
            "vxlan": self.__vxlan_checker__(vlan_dict.get("vxlan")),
            "vxlanmodule": self.__text_checker__(vlan_dict.get("vxlanmodule", ""))
        }
        return new_vlan

    def add_by_dict(self, vlan_dict: Dict) -> None:
        new_vlan = self.check_vlan_dict(vlan_dict)
        self.__vlans__.append(new_vlan)

    def add_by_params(self, id: int, description: str = "", type: str = "private",
                      scope: str = "local", ports: List[int] = [],
                      untagged_ports: List[int] = [], active_ports: List[int] = [],
                      vxlan: Optional[int] = None, vxlanmodule: str = "") -> None:
        new_vlan = {
            "id": self.__id_checker__(id),
            "description": self.__text_checker__(description),
            "type": self.__type_checker__(type),
            "scope": self.__text_checker__(scope),
            "ports": self.__port_checker__(ports),
            "untagged_ports": self.__port_checker__(untagged_ports),
            "active_ports": self.__port_checker__(active_ports),
            "vxlan": self.__vxlan_checker__(vxlan),
            "vxlanmodule": self.__text_checker__(vxlanmodule)
        }
        self.__vlans__.append(new_vlan)
