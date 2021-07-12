from typing import List, Dict, Any, Optional
from vlan import Vlans


class Switch:
    def __init__(self, vlans: Vlans = Vlans()) -> None:
        self.vlans = vlans
