"""Get contact info for all active BGP peers on a Route Views collector.

By default only returns ESTABLISHED BGP peering sessions.

Email address selected based on `technical_prowess` method (:func:`~routeviews.peeringdb.dataclasses.contact.Contact.technical_prowess`).
"""
import logging
import socket
import sys
from functools import partial
from typing import List, Tuple

import configargparse
import requests.exceptions
import uologging
from netmiko import ConnectHandler

import routeviews.peeringdb
import routeviews.peeringdb.dataclasses.network
from routeviews import exec
from routeviews.frr.bgp import BGPNeighborState, BGPPeer, BGPSummary

logger = logging.getLogger(__name__)
trace = uologging.trace(logger, capture_args=False)


@trace
def main(args):
    SHOW_BGP_JSON = 'show bgp summary json'
    if args.collector:
        logging.info(f"Connecting to colllector (via netmiko): {args.collector}")
        try:
            connection = ConnectHandler(
                host=args.collector,
                device_type='cisco_ios_telnet',
                timeout=15,
            )
        except socket.gaierror:  # gaierror: Get Address Info error (aka DNS lookup error)
            raise NameError(f'DNS lookup failed for: {args.collector}')
        output = connection.send_command(SHOW_BGP_JSON)
    else:
        command = ['vtysh', '-c', SHOW_BGP_JSON]
        if args.sudo:
            command.insert(0, 'sudo')
        output = exec.run(command)
    bgp_summary = BGPSummary.from_json(output)

    # Get the email address for each peer ASN
    if args.established_only:
        emails = get_email_address_for_established_peers(
                bgp_summary.peers, args.peeringdb_auth)
    else:
        emails = get_email_address_for_peers(
                bgp_summary.peers, args.peeringdb_auth)

    print('; '.join(emails) + ';')


def get_email_address_for_established_peers(peers: List[BGPPeer], peeringdb_auth: Tuple[str] = None, parallelize: int = 32):
    def established_only(peer):
        return peer.state is BGPNeighborState.ESTABLISHED
    established_peers = filter(established_only, peers)
    return get_email_address_for_peers(list(established_peers), peeringdb_auth, parallelize)


# TODO Maybe simpler to take a list of ASNs instead of peers
def get_email_address_for_peers(peers: List[BGPPeer], peeringdb_auth: Tuple[str] = None, parallelize: int = 32):
    peers_asns = [peer.asn for peer in peers]
    if peeringdb_auth:
        get_emails_authenticated = partial(get_email_address, peeringdb_auth=peeringdb_auth)  # type: ignore
        result = map(get_emails_authenticated, peers_asns)
    else:
        result = map(get_email_address, peers_asns)
    return list(filter(None, result))


def get_email_address(asn, peeringdb_auth=None):
    """Get the email address of one ASN.

    Args:
        asn (int): The ASN to get the email address for.
        peeringdb_auth (Tuple[str], optional): PeeringDB credentials. Defaults to None.

    Returns:
        str: The ASN's email address.
    """
    try:
        network = routeviews.peeringdb.get_network_info(asn)
        if len(network.contacts) > 0:
            return network.technician_email
    except requests.exceptions.HTTPError:
        logger.warning(f'PeeringDB is missing ASN: {asn}')


    # TODO If PeeringDB failed, try RDAP
    # return routeviews.rdap.get_network_info(asn).email


def parse_args(argv):
    parser = configargparse.ArgumentParser(
        description=__doc__, 
        formatter_class=configargparse.ArgumentDefaultsHelpFormatter)
    uologging.add_verbosity_flag(parser)
    parser.add_argument(
        '-u', '--peeringdb-username', 
        env_var='PEERINGDB_USERNAME', 
        help='Username for your PeeringDB account.'
    )
    parser.add_argument(
        '-p', '--peeringdb-password', 
        env_var='PEERINGDB_PASSWORD', 
        help='Password for your PeeringDB account.'
    )
    parser.add_argument(
        '-c', '--collector', 
        help='The Route Views collector to get info about. If omitted, will use `vtysh -c "COMMAND"` on **localhost.**'
    )
    parser.add_argument(
        '--all-peers', '-a', 
        dest='established_only',
        action='store_false',
        help='Default only shows peers with healthy, "ESTABLISHED," BGP sessions.'
    )
    parser.add_argument(
        '--sudo', '-b',  # '-b' is shorthand borrowed from Ansible CLI tool
        action='store_true',
        help='Use `sudo` when running underlying command.'
    )
    args = parser.parse_args(argv[1:])
    # Process PeeringDB credentials into a custom "peeringdb_auth" tuple
    args.peeringdb_auth = None
    if args.peeringdb_username and args.peeringdb_password:
        args.peeringdb_auth = (args.peeringdb_username, args.peeringdb_password)
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
