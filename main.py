#!/usr/bin/env python3 

import os
import sys
import argparse
import subprocess

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

def set_wallpaper(image: str):
    subprocess.run(["swww", "img", image])

if __name__ == "__main__":
    # Set up the necessary directories
    setup()

    # Command line arguments
    parser = argparse.ArgumentParser(
        prog="swww_manager",
        description="Command line utilities for managing wallpaper with swww (https://github.com/LGFae/swww)",
    )
    parser.add_argument(
        "-i",
        "--image", 
        action="store",
        help="set wallpaper as the image at the provided path",
        metavar="",
        required=False,
    )
    args = parser.parse_args()
