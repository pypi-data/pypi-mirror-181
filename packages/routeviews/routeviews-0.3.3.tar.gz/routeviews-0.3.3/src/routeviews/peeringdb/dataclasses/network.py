import logging
from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional

import routeviews.peeringdb
import routeviews.peeringdb.parse

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class Network:
    """Represent a PeeringDB Network (Autonomous System).

    Exmaple raw data:
        | id                           | 13284                                                                                                                                                                                                                                                                                          |
        | org_id                       | 16837                                                                                                                                                                                                                                                                                          |
        | name                         | NETWORKUSA                                                                                                                                                                                                                                                                                     |
        | aka                          |                                                                                                                                                                                                                                                                                                |
        | name_long                    |                                                                                                                                                                                                                                                                                                |
        | website                      | http://www.networkusa.com                                                                                                                                                                                                                                                                      |
        | asn                          | 14832                                                                                                                                                                                                                                                                                          |
        | looking_glass                |                                                                                                                                                                                                                                                                                                |
        | route_server                 |                                                                                                                                                                                                                                                                                                |
        | irr_as_set                   |                                                                                                                                                                                                                                                                                                |
        | info_type                    | NSP                                                                                                                                                                                                                                                                                            |
        | info_prefixes4               | 43                                                                                                                                                                                                                                                                                             |
        | info_prefixes6               | 0                                                                                                                                                                                                                                                                                              |
        | info_traffic                 | 10-20Gbps                                                                                                                                                                                                                                                                                      |
        | info_ratio                   | Balanced                                                                                                                                                                                                                                                                                       |
        | info_scope                   | Regional                                                                                                                                                                                                                                                                                       |
        | info_unicast                 | True                                                                                                                                                                                                                                                                                           |
        | info_multicast               | False                                                                                                                                                                                                                                                                                          |
        | info_ipv6                    | False                                                                                                                                                                                                                                                                                          |
        | info_never_via_route_servers | False                                                                                                                                                                                                                                                                                          |
        | ix_count                     | 1                                                                                                                                                                                                                                                                                              |
        | fac_count                    | 0                                                                                                                                                                                                                                                                                              |
        | notes                        |                                                                                                                                                                                                                                                                                                |
        | netixlan_updated             | 2017-04-24T18:32:54Z                                                                                                                                                                                                                                                                           |
        | netfac_updated               |                                                                                                                                                                                                                                                                                                |
        | poc_updated                  |                                                                                                                                                                                                                                                                                                |
        | policy_url                   |                                                                                                                                                                                                                                                                                                |
        | policy_general               | Open                                                                                                                                                                                                                                                                                           |
        | policy_locations             | Not Required                                                                                                                                                                                                                                                                                   |
        | policy_ratio                 | False                                                                                                                                                                                                                                                                                          |
        | policy_contracts             | Not Required                                                                                                                                                                                                                                                                                   |
        | netfac_set                   | []                                                                                                                                                                                                                                                                                             |
        | netixlan_set                 | [{'id': 34335, 'ix_id': 3, 'name': 'Equinix Dallas', 
            'ixlan_id': 3, 'notes': '', 'speed': 10000, 'asn': 14832, 'ipaddr4': 
            '206.223.118.132', 'ipaddr6': None, 'is_rs_peer': False, 'operational': True, 
            'created': '2017-04-24T18:32:54Z', 'updated': '2017-04-24T18:32:54Z', 'status': 'ok'}] |
        | poc_set                      | []                                                                                                                                                                                                                                                                                             |
        | allow_ixp_update             | False                                                                                                                                                                                                                                                                                          |
        | status_dashboard             |                                                                                                                                                                                                                                                                                                |
        | created                      | 2017-04-21T21:12:01Z                                                                                                                                                                                                                                                                           |
        | updated                      | 2017-04-24T18:30:20Z                                                                                                                                                                                                                                                                           |
        | status                       | ok                                                                                                                                                                                                                                                                                             |
    """
    id: Optional[int] = None
    asn: Optional[int] = None
    name: Optional[str] = None
    name_long: Optional[str] = None
    aka: Optional[str] = None
    info_type: Optional[str] = None
    notes: Optional[str] = None
    org_id: Optional[int] = None
    policy_general: Optional[str] = None
    last_updated: Optional[datetime] = None
    website: Optional[str] = None
    contacts: Optional[List['routeviews.peeringdb.Contact']] = field(
        default_factory=list)
    routers: Optional[List['routeviews.peeringdb.Router']] = field(
        default_factory=list)

    @property
    def technician_email(self) -> str:
        """Get the email address that most likely corresponds to this network's 'operators'.

        Returns:
            str: The email address.
        """
        contacts_with_email = list(filter(
            lambda contact: contact.email is not None, self.contacts))
        contacts_with_email.sort(
            key=routeviews.peeringdb.Contact.technical_prowess)
        return list(contacts_with_email)[0].email

    @classmethod
    def from_raw(cls, data):
        asn = data['asn']
        name = data['name']
        try:
            contacts = routeviews.peeringdb.parse.Contacts(
                data['poc_set'])
        except IndexError:
            contacts = []
            logger.info(
                f"No contact info in PeeringDB for {name} (ASN {asn}).")
        return cls(
            asn=asn,
            name=name,
            contacts=contacts,
            last_updated=routeviews.peeringdb.parse.DateTime(
                data['updated']),
            id=data['id'],
            name_long=data['name_long'],
            aka=data['aka'],
            info_type=data['info_type'],
            notes=data['notes'],
            org_id=data['org_id'],
            policy_general=data['policy_general'],
            website=data['website'],
            routers=routeviews.peeringdb.parse.Routers(
                data['netixlan_set'])
        )

    def potential_peerings_with_network(self, other_network: 'Network') -> List['routeviews.peeringdb.PeerRequest']:
        """Get a list of possible PeerRequests that other_network might like to perform.

        > Does not check for existing peering connections.
        """
        def potential_peerings_with_router(other_router: 'routeviews.peeringdb.Router') -> List['routeviews.peeringdb.PeerRequest']:
            peer_requests = []
            for my_router in self.routers:
                if not other_router.operational or not my_router.operational:
                    continue  # If either are non-operational, skip!
                if other_router.ix_id == my_router.ix_id:
                    if other_router.ip4addr and my_router.ip4addr:
                        peer_requests.append(
                            routeviews.peeringdb.PeerRequest(
                                my_address=my_router.ip4addr,
                                my_network=self,
                                your_address=other_router.ip4addr,
                                your_network=other_network,
                                exchange=my_router.name,
                            ))
                    if other_router.ip6addr and my_router.ip6addr:
                        peer_requests.append(
                            routeviews.peeringdb.PeerRequest(
                                my_address=my_router.ip6addr,
                                my_network=self,
                                your_address=other_router.ip6addr,
                                your_network=other_network,
                                exchange=my_router.name,
                            ))
            return peer_requests

        potential_peerings = []
        for peer_requests in list(map(potential_peerings_with_router, other_network.routers)):
            potential_peerings.extend(peer_requests)
        return list(filter(None, potential_peerings))
