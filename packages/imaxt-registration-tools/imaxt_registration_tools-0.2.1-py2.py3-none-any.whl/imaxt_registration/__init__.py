import sys
from argparse import ArgumentParser, Namespace
from typing import List
from pathlib import Path


from .axio2stpt import axio2stpt

__version__ = "0.2.1"
__author__ = "E.A. Gonzales Solares"


def parse_args(input: List[str]) -> Namespace:

    parent_parser = ArgumentParser(add_help=False)

    main_parser = ArgumentParser(description="IMAXT Registration")
    main_parser.add_argument(
        "-V", "--version", action="version", version="%(prog)s (" + __version__ + ")"
    )

    subparsers = main_parser.add_subparsers(help="commands", dest="command")

    # axio2stpt
    a2s_parser = subparsers.add_parser("axio2stpt", parents=[parent_parser])
    a2s_parser.add_argument(
        "--stpt", required=True, type=Path, help="Full path to STPT dataset"
    )
    a2s_parser.add_argument(
        "--axio", required=True, type=Path, help="Full path to AXIO dataset"
    )
    a2s_parser.add_argument(
        "--output",
        required=True,
        type=Path,
        help="Destination of output correspondence table (csv, parquet, npy, pkl)",
    )
    a2s_parser.add_argument(
        "--pdf",
        required=True,
        type=Path,
        help="Destination of outout PDF quality control file",
    )
    a2s_parser.add_argument(
        "--verbose", action="store_true", default=False, help="Verbose output"
    )
    a2s_parser.add_argument(
        "--nprocs",
        required=False,
        type=int,
        default=6,
        help="Number of processes to run in parallel (default 6)",
    )
    a2s_parser.add_argument(
        "--sections",
        required=False,
        type=str,
        default=None,
        help="Comma separated list of AXIO sections to do (default is all)",
    )
    a2s_parser.add_argument(
        "--nblobs",
        required=False,
        type=int,
        default=None,
        help="Maximum number of blobs for mask detection (default 1)",
    )
    a2s_parser.add_argument(
        "--blobsize",
        required=False,
        type=float,
        default=None,
        help="Relative blob size for mask detection (default 0.01)",
    )
    a2s_parser.set_defaults(func=axio2stpt)

    args = main_parser.parse_args(input)
    return args


def main():
    """Main entry point for owl.

    Invoke the command line help with::

    """
    args = parse_args(sys.argv[1:])

    if hasattr(args, "func"):
        args.func(args)
