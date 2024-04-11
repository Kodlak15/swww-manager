#!/usr/bin/env python3 

import os
import sys
import argparse

def setup():
    # Get the home directory path from the HOME environment variable
    try:
        homedir = os.environ["HOME"]
    except KeyError:
        sys.exit("No HOME environment variable found...")

    # Create the directory where wallpaper state will be held ($HOME/.local/swww)
    statedir = os.path.join(homedir, ".local", "swww")
    if not os.path.exists(statedir):
        os.makedirs(statedir)

if __name__ == "__main__":
    # Set up the necessary directories
    setup()

    # Parse command line arguments
    parser = argparse.ArgumentParser(
        prog="swww_manager",
        description="Command line utilities for managing wallpaper with swww (https://github.com/LGFae/swww)",
    )
    parser.add_argument(
        "-i",
        "--image", 
        dest="image",
        action="store_const",
        const="image",
        help="set wallpaper as the image at the provided path",
    )
    args = parser.parse_args()

    # parser = argparse.ArgumentParser(description='Process some integers.')
    # parser.add_argument('integers', metavar='N', type=int, nargs='+',
    #                     help='an integer for the accumulator')
    # parser.add_argument('--sum', dest='accumulate', action='store_const',
    #                 const=sum, default=max,
    #                 help='sum the integers (default: find the max)')
    # args = parser.parse_args()
