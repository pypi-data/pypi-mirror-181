import dataclasses
from typing import List, Optional

from routeviews import exceptions, parse, typez


@dataclasses.dataclass(frozen=True)
class Router:
    """Represent a PeeringDB "Peering Exchange Point".

    Exmaple raw data:
        | id          | 34335                |
        | ix_id       | 3                    |
        | name        | Equinix Dallas       |
        | ixlan_id    | 3                    |
        | notes       |                      |
        | speed       | 10000                |
        | asn         | 14832                |
        | ipaddr4     | 206.223.118.132      |
        | ipaddr6     |                      |
        | is_rs_peer  | False                |
        | operational | True                 |
        | created     | 2017-04-24T18:32:54Z |
        | updated     | 2017-04-24T18:32:54Z |
        | status      | ok                   |
    """
    id: Optional[int] = None
    ix_id: Optional[int] = None
    name: Optional[str] = None
    ixlan_id: Optional[int] = None
    notes: Optional[str] = None
    speed: Optional[int] = None
    asn: Optional[int] = None
    ip4addr: Optional[typez.IPAddr] = None
    ip6addr: Optional[typez.IPAddr] = None
    is_rs_peer: Optional[bool] = None
    operational: bool = True
    status: Optional[str] = None

    @property
    def ipaddrs(self) -> typez.IPAddrList:
        """Return all IP Addresses associated with this Router.

        Returns:
            types.IPAddrList: List of 0-2 IP Address associated to this router.
        """
        ipaddrs = []
        if self.ip4addr:
            ipaddrs.append(self.ip4addr) 
        if self.ip6addr:
            ipaddrs.append(self.ip6addr)
        return ipaddrs

    def peerable_ipaddrs(self, other: 'Router') -> List['typez.IPAddr']:
        ipaddrs = []
        if self.ip4addr and other.ip4addr:
            ipaddrs.append(other.ip4addr)  
        if self.ip6addr and other.ip6addr:
            ipaddrs.append(other.ip6addr)
        return ipaddrs

    @staticmethod
    def _parse_ipaddr(ipaddr: str) -> Optional[typez.IPAddr]:
        try:
            return parse.IPAddr(ipaddr)
        except exceptions.ParseError:
            return None

    @classmethod
    def from_raw(cls, data):
        return cls(
            id=data['id'],
            ix_id=data['ix_id'],
            name=data['name'],
            ixlan_id=data['ixlan_id'],
            notes=data['notes'],
            speed=data['speed'],
            asn=data['asn'],
            ip4addr=cls._parse_ipaddr(data['ipaddr4']),
            ip6addr=cls._parse_ipaddr(data['ipaddr6']),
            is_rs_peer=data['is_rs_peer'],
            operational=data['operational'],
            status=data['status'],
        )
