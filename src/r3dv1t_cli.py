import os
import io
import sys
import json
import random
from pathlib import Path
import hashlib
import subprocess as sp
import argparse

import libr3dv1t
from libr3dv1t.central_config import dfcc


# ----------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------
def make_arkive(src_filename, out_filename, replicas):
    pass


# ----------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------
def extract_arkive(src_filename, out_filename):
    pass


# ----------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------
def run_command(args: argparse.Namespace):
    """ Run the command line interface based on the parsed arguments
    :param args: Namespace object containing the parsed arguments
    """

    if args.create:
        make_arkive(args.input, args.output, args.replicas)
    elif args.extract:
        extract_arkive(args.input, args.output)
    else:
        print(f"Invalid command line arguments. Use -h for help.")
        sys.exit(1)


# ----------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------
def check_args(args: argparse.Namespace):
    """ Check the command line arguments for validity. Exit if args are invalid.
    :param args: Namespace object containing the parsed arguments
    """

    replicas = args.replicas
    if replicas < 1:
        print(f"Invalid replication count: {replicas}. Must be >= 1")
        sys.exit(1)
    if replicas > 100:
        print(f"Replication count: {replicas} is too high. Must be <= 100")
        sys.exit(1)

    # --- Check if the input file exists
    if not os.path.isfile(args.input):
        print(f"Input file {args.input} does not exist.")
        sys.exit(1)

    # --- Check if the output file already exists
    if os.path.isfile(args.output):
        print(f"Output file {args.output} already exists. Please choose a different output filename.")
        sys.exit(1)

    # --- Check if the input and output files are the same
    if os.path.abspath(args.input) == os.path.abspath(args.output):
        print(f"Input and output files cannot be the same: {args.input}")
        sys.exit(1)

    # --- Check if the input file is a directory
    if os.path.isdir(args.input):
        print(f"Input file {args.input} is a directory. Please provide a filename.")
        sys.exit(1)

    # --- Check if the output file is a directory
    if os.path.isdir(args.output):
        print(f"Output file {args.output} is a directory. Please provide a filename for output.")
        sys.exit(1)


# ----------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------
def parse_args() -> argparse.Namespace:
    """ Parse command line arguments
    :return: Namespace object containing the parsed arguments
    """

    parser = argparse.ArgumentParser(description="r3dv1t command line interface")
    # parser.add_argument("-c", "--create", action="store_true", help="Create a new r3dv1t arkive")
    # parser.add_argument("-x", "--extract", action="store_true", help="Extract original files from a r3dv1t arkive")

    # Create a mutually exclusive group for -c and -x
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-c", "--create", action="store_true", help="Create a new r3dv1t arkive")
    group.add_argument("-x", "--extract", action="store_true", help="Extract original files from a r3dv1t arkive")

    parser.add_argument("-i", "--input", required=True, help="Input filename")
    parser.add_argument("-o", "--output", required=True, help="Output filename")
    parser.add_argument("-r",
                        "--replicas",
                        type=int,
                        default=dfcc.default_replicas,
                        help=f"Replication count. Default: {dfcc.default_replicas}")

    parser.add_argument("-v",
                        "--version",
                        action="version",
                        version=libr3dv1t.__version__,
                        help="Show program version and exit")

    args = parser.parse_args()
    return args


# ----------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------
def main():
    args = parse_args()
    check_args(args)
    run_command(args)


# ----------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------
if '__main__' == __name__:
    main()
