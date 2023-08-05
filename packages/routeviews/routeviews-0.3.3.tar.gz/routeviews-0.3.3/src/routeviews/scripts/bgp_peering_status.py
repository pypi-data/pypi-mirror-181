"""Get info about BGP Peerings on a Route Views collector.
"""

import logging
import socket
import sys

import configargparse
import humanize
import tabulate
import uologging

from routeviews import exceptions, exec, influx
from routeviews.frr.bgp import BGPPeer, BGPSummary

logger = logging.getLogger(__name__)
trace = uologging.trace(logger, capture_args=False)


@trace
def main(args):
    bgp_summary = get_bgp_summary(args.sudo)
    if args.influxdb:
        print_influxdb(bgp_summary)
    elif args.detailed:
        print_detailed(bgp_summary)
    else:
        print_table(bgp_summary)


def get_bgp_summary(sudo=False) -> BGPSummary:
    command = ['vtysh', '-c', 'show bgp summary json']
    if sudo:
        command.insert(0, 'sudo')
    json_output = exec.run(command)
    try:
        return BGPSummary.from_json(json_output)
    except exceptions.EmptyError as e:
        print(e)
        print('''BGP summary appears empty... This may mean:
 * There aren't any BGP peers
 * FRR service is not working properly
 ''')
        exit()

def print_detailed(results: BGPSummary):
    print(f'Collector ASN: {results.my_asn}')
    print(f'Collector Router ID: {results.router_id}')
    for peer in results.peers:
        print(peer.pprint())


def print_table(results: BGPSummary):
    header = [
        'ASN', 'Peer Address', 'State', 'Prefixes', 'InQ', 'Uptime',
        'ConnsEst', 'ConnsDrop'
    ]
    data = [
        tuple([
            peer.asn, peer.ip_address, peer.state.name, peer.prefixes_received,
            peer.input_queue, humanize.naturaldelta(peer.uptime_seconds),
            peer.connections_established, peer.connections_dropped
        ])
        for peer in results.peers
    ]
    print(tabulate.tabulate(data, headers=header))


def print_influxdb(results: BGPSummary):
    hostname = socket.gethostname()
    for peer in results.peers:
        print(generate_influxdb_line(hostname, peer))


def generate_influxdb_line(hostname: str, peer: BGPPeer, measurement='bgp_status'):
    """Produce an influxdb line for sending to influxDB.

    Returns:
        str: Single long string containing the vals we want to track.
    """
    return influx.measurement_line(
        measurement,
        fields={
            'state': peer.state.name.lower(),
            'uptime_sec': peer.uptime_seconds,
            'prefixes_received': peer.prefixes_received,
            'established': peer.connections_established,
            'dropped': peer.connections_dropped,
            'in_q': peer.input_queue,
        },
        tags={
            'collector': hostname,
            'remote_as': str(peer.asn),
            'peer': str(peer.ip_address),
            'type': str(peer.type), 
        }
    )


def parse_args(argv):
    parser = configargparse.ArgumentParser(
        description=__doc__, 
        formatter_class=configargparse.ArgumentDefaultsHelpFormatter)
    uologging.add_verbosity_flag(parser)
    parser.add_argument(
        '--detailed',
        '-d',
        action='store_true',
        help='Output information in further detail.'
    )
    parser.add_argument(
        '--influxdb',
        action='store_true',
        help='Produce a measurement as InfluxDB Line Protocol.'
    )
    parser.add_argument(
        '--sudo', '-b',  # '-b' is shorthand borrowed from Ansible CLI tool
        action='store_true',
        help='Use `sudo` when running underlying command.'
    )
    args = parser.parse_args(argv[1:])
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
