import logging
import os
from dataclasses import dataclass
from typing import Dict, List, Optional

from routeviews import ansible, const, exceptions, peeringdb, typez

logger = logging.getLogger(__name__)

def load(ansible_inventory_directory: str):
    return Inventory.load(ansible_inventory_directory)

@dataclass
class Inventory:
    collector_configs: List['ansible.CollectorConfig']

    def get_multihop_collector(self, multihop_index: str):
        def match(collector_config: 'ansible.CollectorConfig'):
            return f'route-views{multihop_index}.routeviews.org' == collector_config.hostname

        try:
            return next(filter(match, self.collector_configs))
        except StopIteration:
            raise LookupError(f'Unable to find Multihop collector with index "{multihop_index}" in Ansible Inventory.')

    def get_collector_by_hostname(self, hostname: str) -> 'ansible.CollectorConfig':
        def match(collector_config: 'ansible.CollectorConfig'):
            return hostname == collector_config.hostname

        try:
            return next(filter(match, self.collector_configs))
        except StopIteration:
            raise LookupError(f'Unable to find "{hostname}" in Ansible Inventory.')

    def get_collector_by_address(self, ipaddr: typez.IPAddr) -> 'ansible.CollectorConfig':
        def match(collector_config: 'ansible.CollectorConfig'):
            try:
                return ipaddr in collector_config.peerable_ipaddrs
            except exceptions.ParseError:
                return False

        try:
            return next(filter(match, self.collector_configs))
        except StopIteration:
            raise LookupError(f'Unable to find "{ipaddr}" in Ansible Inventory.')

    def peer_requests(self, requests: List[peeringdb.PeerRequest], bgp_options: Optional[List[str]] = None):
        """Add many peer requests to this Inventory in memory.

        > NOTE: Filesystem is not updated until a future call to 'save'.

        Args:
            requests (peeringdb.PeerRequest): The requests to be added.
        """
        from functools import partial
        add_peer_request = partial(self.peer_request, bgp_options=bgp_options)
        return list(map(add_peer_request, requests))

    def peer_request(self, request: peeringdb.PeerRequest, bgp_options: Optional[List[str]] = None):
        """Add a peer request to this Inventory in memory.

        > NOTE: Filesystem is not updated until a future call to 'save'.

        Args:
            request (peeringdb.PeerRequest): The request to be added.
        """
        try:
            collector = self.get_collector_by_address(request.my_address)
        except LookupError:
            logger.warning(f'Skipping peer request -- cannot find collector with address: {request.my_address}')
            return
        if collector.is_peered_with(request.your_address):
            logger.info(f'Skipping peer request that already exist: {request.your_address}')
            return
        return collector.add_neighbor(
            asn=request.your_network.asn,
            address=request.your_address,
            description=request.your_network.name,
            options=bgp_options,
        )

    def effected_hosts(self) -> str:
        """Hosts' interfaces that MAY be effected when "save" is called.

        This method WILL print ALL interface addresses for each collector.

        Returns:
            str: Markdown doc containing lists of interfaces per host.
        """
        messages = []
        for collector in self.collector_configs:
            if collector.diff():
                messages.append(f'\n### {collector.hostname}\n')
                for addr in collector.peerable_ipaddrs:
                    if isinstance(addr, typez.IPv6Address):
                        messages.append(f'- IPv6: {addr}')
                    elif isinstance(addr, typez.IPv4Address):
                        messages.append(f'- IPv4: {addr}')
        messages = filter(lambda message: message.strip() != '', messages)
        final_message = '\n'.join(messages)
        return final_message

    def diff(self) -> str:
        """Show changes that will be applied when "save" is called.

        Returns:
            str: Pretty diff output.
        """
        diffs = []
        for collector in self.collector_configs:
            if not collector.diff():
                continue
            diffs.append(f'\n+++ { collector.filepath }\n{ collector.diff() }\n')
        diffs = filter(lambda message: message.strip() != '', diffs)
        final_message = ''.join(diffs)
        return final_message

    @classmethod
    def load(cls, inventory_path: str) -> 'Inventory':
        """Parses all existing YAML config files relating to different collectors.

        Args:
            inventory_path (str): Path to Ansible Inventory.

        Returns:
            Inventory: The inventory loaded into memory.
        """
        return Inventory(
            collector_configs=Inventory.load_collector_configs(inventory_path),
        )

    def save(self):
        """Save all changes back to the Inventory on the filesystem.
        """
        list(map(ansible.CollectorConfig.save, self.collector_configs))

    @staticmethod
    def load_collector_configs(inventory_path) -> List[ansible.CollectorConfig]:
        configs = []
        host_vars_dir = os.path.join(inventory_path, 'host_vars')
        for config_filename in os.listdir(host_vars_dir):
            if not config_filename.startswith(const.ANSIBLE_HOSTVAR_COLLECTOR_FILENAME_PREFIX):
                continue
            config_path = os.path.join(host_vars_dir, config_filename)
            configs.append(ansible.CollectorConfig.load(config_path))
        return configs

    def potential_peer_requests(self, asn: int) -> List[peeringdb.PeerRequest]:
        routeviews_network = peeringdb.get_routeviews_info()
        requestor_network = peeringdb.get_network_info(asn)
        return routeviews_network.potential_peerings_with_network(requestor_network)
