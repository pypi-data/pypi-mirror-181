"""Add BGP peering(s) to Route Views Ansible inventory.
"""
import logging
import sys
from typing import List, Optional

import configargparse
import tabulate
import uologging

from routeviews import ansible, parse, peeringdb, typez

logger = logging.getLogger(__name__)
trace = uologging.trace(logger, capture_args=False)


def main(args):
    if args.peeringdb_username and args.peeringdb_password or args.peeringdb_key:
        peeringdb.Repository(args.peeringdb_username,
                             args.peeringdb_password, args.peeringdb_key)

    if args.show_options:
        if args.ipaddrs:
            logger.warning('IP Address (--ip) arg(s) ignored when showing options')
        run_show(args.asn)
        return

    inventory = ansible.load(args.inventory)
    if args.multihop_index:
        collector_addr = inventory.get_multihop_collector(args.multihop_index).first_peering_addr
        possible_peerings = multihop_peer_requests(collector_addr, args.asn, args.ipaddrs)
        inventory.peer_requests(
            possible_peerings, 
            bgp_options=['ebgp-multihop 255']
        )
    else:
        possible_peerings = ix_peer_requests(args.asn, args.ipaddrs)
        inventory.peer_requests(possible_peerings)
    if inventory.diff():
        print(f'''### Changes
{ inventory.diff() }
### Effected Hosts
{ inventory.effected_hosts() }
''')
        if args.dry_run:
            print("Note: Run again without '--dry-run' flag for these changes to apply.")
        else:
            inventory.save()
    else:
        print(f'''No changes made to Ansible Inventory by this request.
    Inventory: {args.inventory}''')


def run_show(asn):
    peer_requests = potential_ix_peer_requests(asn)

    def table_summary():
        my_network = peer_requests[0].my_network
        your_network = peer_requests[0].your_network
        return f'''Potential BGP Peerings for networks:

- {my_network.name} (ASN: {my_network.asn}), and 
- {your_network.name} (ASN: {your_network.asn}).'''

    def table():
        header = ['Exchange', 'RV Collector', 'Router']
        data = [
            tuple([req.exchange, req.my_address, req.your_address])
            for req in peer_requests
        ]
        return tabulate.tabulate(data, headers=header)

    print(f'\n{table_summary()}\n\n{table()}')


@trace
def ix_peer_requests(asn: int, ipaddrs: Optional[List[typez.IPAddr]] = None) -> List[peeringdb.PeerRequest]:
    """Get all potential peerings that match ipaddrs.

    Args:
        asn (int): The network to try and peer with.
        ipaddrs (Optional[List[types.IPAddr]], optional): Only return Peer 
        Request if it matches one of these IP Addresses. Defaults to None, 
        which means do NO filtering at all.

    Returns:
        List[peeringdb.PeerRequest]: List of potential peer requests.
    """
    possible_peer_requests = potential_ix_peer_requests(asn)
    if ipaddrs:
        possible_peer_requests = list(filter(
            lambda peer_req: peer_req.your_address in ipaddrs, possible_peer_requests))
    return possible_peer_requests


def potential_ix_peer_requests(asn: int) -> List[peeringdb.PeerRequest]:
    """Get all possible peerings for a network.

    Args:
        asn (int): The network to try and peer with.

    Returns:
        List[peeringdb.PeerRequest]: List of potential peer requests.
    """
    routeviews_network = peeringdb.get_routeviews_info()
    requestor_network = peeringdb.get_network_info(asn)
    return routeviews_network.potential_peerings_with_network(requestor_network)


def multihop_peer_requests(my_addr: typez.IPAddr,
                           asn: int,
                           ipaddrs: typez.IPAddrList
                           ) -> List[peeringdb.PeerRequest]:
    return [
        peeringdb.PeerRequest(
            my_network=peeringdb.get_routeviews_info(),
            my_address=my_addr,
            your_network=peeringdb.get_network_info(asn),
            your_address=ipaddr,
            exchange=None,
        )
        for ipaddr in ipaddrs
    ]


def parse_args(argv):
    parser = configargparse.ArgumentParser(
        description=__doc__, 
        formatter_class=configargparse.ArgumentDefaultsHelpFormatter)
    uologging.add_verbosity_flag(parser)
    parser.add_argument(
        '--asn', '-a',
        required=True,
        help="The ASN to peer with."
    )
    parser.add_argument(
        '--show-options', '-s',
        action='store_true',
        help='Show potential peering options in a pretty table.'
    )
    inventory_parser = parser.add_argument_group(title='Ansible Inventory (optional)')
    inventory_parser.add_argument(
        '--inventory',
        env_var='ROUTEVIEWS_INVENTORY',
        help='''Provide the path to the "inventory/" directory 
        of your local copy of the Route Views ansible repo: 
        https://github.com/routeviews/infra (private)
        '''
    )
    inventory_parser.add_argument(
        '--ip', '-i',
        action='append',
        dest='ipaddrs',
        help='''Specific IP address(es) to peer with. (If omitted, attempt to 
        peer with ALL compatible IP Addresses for ASN)'''
    )
    inventory_parser.add_argument(
        '--multihop-index', '-m',
        help='''Which collector should be used for BGP Multihop peering? 
        NOTE: Multihop collectors are named: 
        `route-views<MULTIHOP_INDEX>.routeviews.org`''',
    )
    inventory_parser.add_argument(
        '--dry-run',
        action='store_true',
        help="Do not make any changes to ansible inventory when running this script (for testing).",
    )

    peergindb_auth_parser = parser.add_argument_group(title='PeeringDB Auth (optional)')
    peergindb_auth_parser.add_argument(
        '-u', '--peeringdb-username',
        env_var='PEERINGDB_USERNAME',
        help='Username for your PeeringDB account. (If omitted, will use PeeringDB API anonymously)'
    )
    peergindb_auth_parser.add_argument(
        '-p', '--peeringdb-password',
        env_var='PEERINGDB_PASSWORD',
        help='Password for your PeeringDB account.'
    )
    peergindb_auth_parser.add_argument(
        '-k', '--peeringdb-key',
        env_var='PEERINGDB_KEY',
        help='API Key for your PeeringDB account.'
    )

    args = parser.parse_args(argv[1:])
    # Do any argument pre-processing. E.g. convert strings to objects.
    if args.ipaddrs:
        args.ipaddrs = parse.IPAddrList(args.ipaddrs)
    if args.multihop_index and not args.ipaddrs:
        parser.error('For multihop peerings, --ip ADDRESS must be specified.')
    if not args.inventory and not args.show_options:
        parser.error('Use --show-options, else provide an --inventory.')
    return args


def run_main():
    _main(sys.argv)


def _main(argv):
    """Parse args, set up logging, then call the inner 'main' function. 
    """
    package_name = __name__.split('.')[0]
    uologging.init_console(package_name)
    args = parse_args(argv)
    uologging.set_logging_verbosity(args.verbosity_flag, package_name)
    main(args)


if __name__ == '__main__':
    logger.warning(f'Invoked as script, not using entry point {__file__}')
    run_main()
