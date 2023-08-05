"""Get stats from HAProxy Stick Tables on a Route Views collector.

(HAProxy runs on each collector to enable telnet access)
"""
import logging
import operator
import sys
from typing import List, Optional

import configargparse
import humanize
import tabulate
import uologging

import routeviews.exec
import routeviews.haproxy
import routeviews.influx
import routeviews.parse

logger = logging.getLogger(__name__)
trace = uologging.trace(logger, capture_args=False)

HAPROXY_SOCKET = 'unix-connect:/var/run/haproxy.sock'
DEFAULT_TABLE = 'st-rate-limit'  # st: Stick Table (in HAProxy lingo)


@trace
def main(args):
    # echo "show pools" | sudo socat stdio unix-connect:/var/run/haproxy.sock
    # Prepare command
    haproxy_command = f"show table {args.table}"
    socat_command = f'socat stdio {args.socket}'
    if args.sudo:
        socat_command = f'sudo {socat_command}'
    # Run command
    command = [f'echo "{haproxy_command}" | {socat_command}']
    result = routeviews.exec.run(command, shell=True)
    logger.debug(f'Raw command and output: {command} {result}')
    haproxy_stats = parse_raw_output(result,  # type: ignore
                                     args.min_connection_count,
                                     args.sort)
    if args.influxdb:
        for stat in haproxy_stats:
            print(generate_influxdb_line(stat, f'haproxy-{args.table}'))
    else:
        # TODO Sort by args.sort
        # print_table(sorted(haproxy_stats, key=args.sort))
        print_table(haproxy_stats)


def parse_raw_output(console_output: str,
                     min_connections: int = 0,
                     sort_key: Optional[str] = None) -> List[routeviews.haproxy.HAProxyTableStat]:
    haproxy_stats_data = routeviews.parse.template_parse(
        console_output, 'haproxy_show_table')
    haproxy_stats = routeviews.haproxy.parse_table_stats(haproxy_stats_data)
    if min_connections:
        haproxy_stats = list(filter(
            lambda stat: stat.conn_cnt >= min_connections,
            haproxy_stats
        ))
    if sort_key:
        haproxy_stats = sorted(
            haproxy_stats, key=operator.attrgetter(sort_key))
    return haproxy_stats


def print_table(results: List[routeviews.haproxy.HAProxyTableStat]):
    header = [
        'Key', 'Current Conn.', 'Total Conn.', 'Data In Rate', 'Date Out Rate',
    ]
    data = [
        tuple([
            stat.key, stat.conn_cur, stat.conn_cnt,
            humanize.naturalsize(stat.bytes_in_rate),
            humanize.naturalsize(stat.bytes_out_rate),
        ])
        for stat in results
    ]
    print(tabulate.tabulate(data, headers=header))


def generate_influxdb_line(table_stat: routeviews.haproxy.HAProxyTableStat,
                           measurement='haproxy_table_stats'):
    """Generate a InfluxDB Line Protocol line.

    Args:
        table_stat (routeviews.haproxy.HAProxyTableStat): The data that we
        want to record.
        measurement (str, optional): Name of measurement in InfluxDB. 
        Defaults to 'haproxy_table_stats'.

    Returns:
        str: Single long string containing the vals we want to track.
    """
    return routeviews.influx.measurement_line(
        name=measurement,
        fields={
            'bin_rate': table_stat.bytes_in_rate,
            'bout_rate': table_stat.bytes_out_rate,
            'conn_cnt': table_stat.conn_cnt,
            'conn_cur': table_stat.conn_cur,
        },
        tags={
            'key': str(table_stat.key),
            'type': table_stat.type,
        },
    )


def parse_args(argv):
    parser = configargparse.ArgumentParser(
        description=__doc__, 
        formatter_class=configargparse.ArgumentDefaultsHelpFormatter)
    uologging.add_verbosity_flag(parser)
    parser.add_argument(
        '--influxdb',
        action='store_true',
        help='Produce a measurement as InfluxDB Line Protocol.'
    )
    parser.add_argument(
        '--socket',
        help='What is the path of the HAProxy socket?',
        default=HAPROXY_SOCKET,
    )
    parser.add_argument(
        '--table',
        help='What table to look at?',
        default=DEFAULT_TABLE,
    )
    parser.add_argument(
        '--sudo', '-b',  # '-b' is shorthand borrowed from Ansible CLI tool
        action='store_true',
        help='Use `sudo` when running underlying command.'
    )
    parser.add_argument(
        '--min-conn-cnt',
        dest='min_connection_count',
        type=int,
        default=0,
        help='Omit records that have fewer than this many total connections.',
    )
    parser.add_argument(
        '--sort',
        choices=routeviews.parse.load_template('haproxy_show_table').header,
        default='conn_cnt',
        help='Which column to sort by?',
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
