"""TODO single line describing tool.

TODO any additional discussion goes here...
"""
import logging
import sys

import configargparse
import uologging

logger = logging.getLogger(__name__)
trace = uologging.trace(logger, capture_args=False)


@trace
def main(args):
    # TODO Write main logic to implement your tool!
    print('Hello, World!')
    if args.detailed:
        print('''
        This "template" tool exist solely as an example.
        Developers can copy/paste this template script to
        get started adding a tool to this package!

        > Don't forget `console_scripts` in "setup.py"!
        >
        > See "docs/add-tools.md" for full details.''')


def parse_args(argv):
    parser = configargparse.ArgumentParser(
        description=__doc__, 
        formatter_class=configargparse.ArgumentDefaultsHelpFormatter)
    uologging.add_verbosity_flag(parser)

    # TODO Add arguments as needed
    #   Also, do any post-processing required before returning the args.
    #   Ex. convert strings to objects.
    parser.add_argument(
        '--detailed',
        '-d',
        action='store_true',
        help='Output some more info about this tool.'
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
