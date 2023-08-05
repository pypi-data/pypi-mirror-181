from enum import Enum
from ipaddress import IPv4Address, IPv6Address
from typing import List, Union

IPAddr = Union[IPv4Address, IPv6Address]
IPAddrList = List[IPAddr]


class MRTTypes(Enum):
    RIBS = 1
    UPDATES = 2
