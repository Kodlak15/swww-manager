#!/usr/bin/env python3 

import os
import sys
import argparse
import subprocess
import yaml

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

def set_wallpaper(image: str, config: dict):
    subprocess.run([
        "swww", 
        "img", 
        image,
        "--transition-type",
        config["transition"]["type"],
        "--transition-pos",
        config["transition"]["position"],
        "--transition-step",
        config["transition"]["step"],
        "--transition-duration",
        config["transition"]["duration"],
        "--transition-angle",
        config["transition"]["angle"],
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    if config["pywal"]:
        subprocess.run(["wal", "-i", image, "-n"])

    directory = os.path.dirname(image)
    fname = os.path.basename(image)
    if os.path.dirname(image) != config["directory"]:
        config["directory"] = os.path.dirname(image)
        config["index"] = os.listdir(directory).index(fname)
        with open("config.yaml", "w") as f:
            yaml.dump(config, f)

def get_config():
    with open("config.yaml", "r") as f:
        return yaml.safe_load(f)

if __name__ == "__main__":
    # Set up the necessary directories
    setup()

    # Command line arguments
    parser = argparse.ArgumentParser(
        prog="swww_manager",
        description="Command line utility script for managing wallpaper with swww (https://github.com/LGFae/swww)",
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

    # Get the configuration
    config = get_config()

    # If no arguments are passed, print the help message and exit
    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)

    # Testing
    set_wallpaper(args.image, config)
