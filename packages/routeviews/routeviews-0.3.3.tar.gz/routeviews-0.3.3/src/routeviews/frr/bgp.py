import ipaddress
import json
import logging
from dataclasses import dataclass
from enum import Enum
from typing import Dict, List, Optional

import humanize

from routeviews import exceptions, parse, typez

logger = logging.getLogger(__name__)


class BGPNeighborState(Enum):
    UNKNOWN = 0
    IDLE = 10
    CONNECT = 20
    ACTIVE = 30
    OPENSENT = 40
    OPENCONFIRM = 50
    ESTABLISHED = 60

    @classmethod
    def from_str(cls, raw_text: str):
        if raw_text.isnumeric() or raw_text.lower() == 'established':
            return cls.ESTABLISHED
        elif raw_text.lower() == 'connect':
            return cls.CONNECT
        elif raw_text.lower().startswith('idle'):
            return cls.IDLE
        elif raw_text.lower() == 'active':
            return cls.ACTIVE
        elif raw_text.lower() == 'openconfirm':
            return cls.OPENCONFIRM
        elif raw_text.lower() == 'opensent':
            return cls.OPENSENT
        else:
            raise exceptions.ParseError(
                f'Unable to parse BGP State from {raw_text}.')


@dataclass(frozen=True)
class BGPPeer:
    asn: int
    ip_address: typez.IPAddr
    state: BGPNeighborState
    prefixes_received: int
    uptime_seconds: float
    connections_established: int
    connections_dropped: int
    input_queue: int

    @property
    def type(self) -> Optional[str]:
        if isinstance(self.ip_address, ipaddress.IPv4Address):
            return 'ipv4'
        elif isinstance(self.ip_address, ipaddress.IPv6Address):
            return 'ipv4'
        else:
            return None

    def pprint(self):
        return f'''\
- Peer Address: {self.ip_address}
  ASN: {self.asn}
  Connections: {self.connections_established}
  State: {self.state.name}
  Uptime: {humanize.naturaldelta(self.uptime_seconds)}
  Prefix Count: {humanize.scientific(self.prefixes_received,precision=3)}
  Input Queue Size: {self.input_queue}
'''

    @classmethod
    def from_json(cls, peer_address: str, peer_info: Dict):

        def parse_uptime_seconds(raw_uptime: str) -> float:
            return float(raw_uptime) / 1000  # Convert from msec to seconds

        def _parse_prefixes_received(raw_text: str):
            try:
                return int(raw_text)
            except ValueError:
                return 0
        
        def parse_prefixes_received(peer_info: Dict):
            key_names = [
                'pfxRcd',
                'prefixReceivedCount'
            ]
            for key in key_names:
                try:
                    return _parse_prefixes_received(peer_info[key])
                except KeyError:
                    continue
            raise exceptions.ParseError(f'Unable to parse "Prefixes Received Count." JSON data for BGP Peer did not contain any of: {key_names}')

        return cls(
            ip_address=parse.IPAddr(peer_address),
            asn=peer_info['remoteAs'],
            state=BGPNeighborState.from_str(peer_info['state']),
            prefixes_received=parse_prefixes_received(peer_info),
            connections_established=int(peer_info['connectionsEstablished']),
            connections_dropped=int(peer_info['connectionsDropped']),
            input_queue=int(peer_info['inq']),
            uptime_seconds=parse_uptime_seconds(peer_info['peerUptimeMsec']),
        )


class BGPSummary:
    def __init__(self, ip_addr: typez.IPAddr, asn: int, peers: List[BGPPeer]):
        self.peers = peers
        self.router_id = ip_addr
        self.my_asn = int(asn)

    def __str__(self):
        return f"{[str(x) for x in self.peers]}"

    @classmethod
    def from_json(cls, raw_json: str) -> 'BGPSummary ':
        bgp_summary = json.loads(raw_json)
        if not bgp_summary:
            raise exceptions.EmptyError(
                f'Unable to parse BGPSummary from JSON data: {raw_json}')

        def parse_peers(bgp_summary: Dict) -> List[BGPPeer]:
            all_peers = dict()
            for router_instance in bgp_summary.values():
                all_peers.update(dict(router_instance['peers'].items()))
            return [
                BGPPeer.from_json(peer_address, peer_info)
                for peer_address, peer_info in all_peers.items()
            ]

        def extract_my(bgp_summary, key='routerId'):
            try:
                first_router_instance = list(bgp_summary.values())[0]
                return first_router_instance[key]
            except LookupError:
                logger.debug(f'Failed to find "{key}" in first item of: {bgp_summary}')
                raise exceptions.ParseError(
                    f'Unable to parse {key} of Router.')

        return cls(
            asn=int(extract_my(bgp_summary, 'as')),
            ip_addr=parse.IPAddr(extract_my(bgp_summary, 'routerId')),
            peers=parse_peers(bgp_summary),
        )
