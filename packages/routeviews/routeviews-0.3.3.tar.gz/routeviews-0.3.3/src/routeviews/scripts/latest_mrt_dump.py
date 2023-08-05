"""Get metrics about the latest MRT Dump files on a Route Views collector.

TODO: Consider feature to monitor all MRT files on archive.routeviews.org.
"""
import logging
import os
import socket
import sys

import configargparse
import uologging

import routeviews.influx
from routeviews.filesystem import FileMetrics, latest_file, list_dir
from routeviews.typez import MRTTypes

DEFAULT_MRT_PATH = '/mnt/storage/bgpdata/'
INFLUXDB_MEASUREMENT_RIB = 'latest_mrt_RIB'
INFLUXDB_MEASUREMENT_UPDATE = 'latest_mrt_update'

uologging.init_syslog()

logger = logging.getLogger(__name__)


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


def main(args):
    try:
        latest_RIB = FileMetrics(latest_MRT_file(
            MRTTypes.RIBS, args.path, args.zipped))
        latest_update = FileMetrics(latest_MRT_file(
            MRTTypes.UPDATES, args.path, args.zipped))
    except OSError as e:
        print(e)
        exit(1)
    if args.influxdb:
        print(generate_influxdb_line(latest_RIB, INFLUXDB_MEASUREMENT_RIB))
        print(generate_influxdb_line(latest_update, INFLUXDB_MEASUREMENT_UPDATE))
    elif args.simple:
        print(f'Latest RIB:    {latest_RIB.path}')
        print(f'Latest UPDATE: {latest_update.path}')
    else:
        print_detailed(latest_RIB, latest_update)


def print_detailed(latest_RIB: FileMetrics, latest_update: FileMetrics):
    import textwrap
    latest_RIB_stats = latest_RIB.pprint()
    print('Latest RIB:')
    print(textwrap.indent(latest_RIB_stats, '  '))
    latest_update_stats = latest_update.pprint()
    print('Latest update:')
    print(textwrap.indent(latest_update_stats, '  '))


def latest_MRT_file(mrt_type: MRTTypes, path=DEFAULT_MRT_PATH, bz2=False) -> str:
    """Gets the latest MRT file from a collector.

    Args:
        mrt_type: Choose which type of Route Views MRT file to lookup. RIB, 
        UPDATE path (str, optional): The path where Route Views MRT dumps 
        are stored. Defaults to DEFAULT_MRT_PATH.
        bz2: Only return latest MRT files that have .bz2 file extension.

    Returns:
        str: Path to the latest "mrt_type" file.
    """
    mrt_directories = list_dir(path, sort_key=os.path.getctime)
    for mrt_dir in mrt_directories:
        latest_mrt_dir = os.path.join(mrt_dir, mrt_type.name)
        try:
            return latest_file(latest_mrt_dir, '*.bz2' if bz2 else '*')
        except OSError:
            continue  # Try the next mrt_directory
    raise OSError(f'Unable to find any MRT Archive files at: "{path}"')


def generate_influxdb_line(latest: FileMetrics,
                           measurement=INFLUXDB_MEASUREMENT_RIB):
    """Generate a InfluxDB Line Protocol line.

    Args:
        latest (FileMetrics): Latest MRT RIB or update file. 
        measurement (str, optional): Name of measurement in InfluxDB. 
        Defaults to 'latest_mrt_RIB' (INFLUXDB_MEASUREMENT_RIB).

    Returns:
        str: Single long string containing metrics we want to track.
    """
    return routeviews.influx.measurement_line(
        measurement,
        tags={
            'file': latest.path,
            'zipped': latest.bz2,
        },
        fields={
            'age_sec': latest.age_in_seconds(),
            'size': latest.size,
        }
    )


def parse_args(argv):
    parser = configargparse.ArgumentParser(
        description=__doc__, 
        formatter_class=configargparse.ArgumentDefaultsHelpFormatter)
    uologging.add_verbosity_flag(parser)
    parser.add_argument(
        '--path', '-p',
        default=DEFAULT_MRT_PATH,
        help=f'Look for Route Views style MRT Archives at this path. Default: {DEFAULT_MRT_PATH}'
    )
    parser.add_argument(
        '--zipped',
        '-z',
        action='store_true',
        help='Only report files that have the .bz2 file extension.'
    )
    output_options = parser.add_mutually_exclusive_group()
    output_options.add_argument(
        '--influxdb',
        '-i',
        action='store_true',
        help='Produce a measurement as InfluxDB Line Protocol.'
    )
    output_options.add_argument(
        '--simple',
        '-s',
        action='store_true',
        help='Produce more detailed output, focused on being human readable.'
    )
    args = parser.parse_args(argv[1:])
    # Do any argument pre-processing. E.g. convert strings to objects.
    return args


if __name__ == '__main__':
    logger.warning(f'Invoked as script, not using entry point {__file__}')
    run_main()
