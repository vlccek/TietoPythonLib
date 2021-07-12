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
        if id < 0:
            raise Exception("ID cannot be negative")
        for i in self.__vlans__:
            if not (i.get("id") != id):
                raise Exception("ID is already in list")
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
    
    def __replicators_check__(self, replicators: Optional[Any]) -> Optional[str]:
        if type(replicators) is not str:
            return None
        return replicators
    
    def __bool_check__(self, boolean: Any):
        if type(boolean) is not bool:
            return False
        return boolean

    def add_by_dict(self, vlan_dict: Dict) -> None:
        new_vlan = {
            "id": self.__id_checker__(vlan_dict.get("id", 0)),
            "type": self.__type_checker__(vlan_dict.get("type")),
            "auto-vxlan": self.__bool_check__(vlan_dict.get("auto-vxlan")),
            "replicators": self.__replicators_check__(vlan_dict.get("replicators")),
            "scope": self.__text_checker__(vlan_dict.get("scope", "local")),
            "description": self.__text_checker__(vlan_dict.get("description", "")),
            "active": self.__bool_check__(vlan_dict.get("active")),
            "stats": self.__bool_check__(vlan_dict.get("stats")),
            "ports": self.__port_checker__(vlan_dict.get("ports", [])),
            "untagged_ports": self.__port_checker__(vlan_dict.get("untagged_ports", [])),
            "active_ports": self.__port_checker__(vlan_dict.get("active_ports", [])),
            "vxlan": self.__vxlan_checker__(vlan_dict.get("vxlan")),
            "vxlanmodule": self.__text_checker__(vlan_dict.get("vxlanmodule", ""))
        }
        self.__vlans__.append(new_vlan)

    def add_by_params(self, id: int, type: str = "private", auto_vxlan: bool = False, 
                      replicators: Optional[str] = None, scope: str = "local", 
                      description: str = "", active: bool = False, stats: bool = False,  
                      ports: List[int] = [], untagged_ports: List[int] = [], 
                      active_ports: List[int] = [], vxlan: Optional[int] = None, 
                      vxlanmodule: str = "") -> None:
        new_vlan = {
            "id": self.__id_checker__(id),
            "type": self.__type_checker__(type),
            "auto-vxlan": self.__bool_check__(auto_vxlan),
            "replicators": self.__replicators_check__(replicators),
            "scope": self.__text_checker__(scope),
            "description": self.__text_checker__(description),
            "active": self.__bool_check__(active),
            "stats": self.__bool_check__(stats),
            "ports": self.__port_checker__(ports),
            "untagged_ports": self.__port_checker__(untagged_ports),
            "active_ports": self.__port_checker__(active_ports),
            "vxlan": self.__vxlan_checker__(vxlan),
            "vxlanmodule": self.__text_checker__(vxlanmodule)
        }
        self.__vlans__.append(new_vlan)
