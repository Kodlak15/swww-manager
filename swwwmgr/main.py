#!/usr/bin/env python3 

import os
import sys
import argparse
import subprocess
import yaml
from pathlib import Path

CONFIG_PATH = Path.home().joinpath(".config", "swwwmgr", "config.yaml")
STATE_PATH = Path.home().joinpath(".local", "state", "swwwmgr", "state.yaml")

def setup_config():
    if not os.path.exists(CONFIG_PATH.parent):
        os.makedirs(CONFIG_PATH.parent)

    # Generate the default configuration file if one does not already exist
    if not os.path.exists(CONFIG_PATH):
        config = {
            "pywal": False,
            "transition": {
                "angle": "180",
                "duration": "0.5",
                "position": "0.7,0.9",
                "step": "180",
                "type": "wipe",
            },
        }

        with open(CONFIG_PATH, "w") as f:
            yaml.dump(config, f)

def setup_state():
    # Create the config and state directories if they do not exist
    print(STATE_PATH.parent)
    if not os.path.exists(STATE_PATH.parent):
        os.makedirs(STATE_PATH.parent)

    if not os.path.exists(STATE_PATH):
        state = {
            "directory": str(CONFIG_PATH.parent),
            "index": 0,
        }

        with open(STATE_PATH, "w") as f:
            yaml.dump(state, f)

def set_wallpaper(image: str, config: dict, state: dict):
    # Use swww to change the wallpaper
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
    ])

    # If using pywal, run pywal using the new image to generate colors
    if config["pywal"]:
        try:
            subprocess.run(["wal", "-i", image, "-n"])
        except FileNotFoundError:
            print("Could not find pywal, are you sure you have it installed?", file=sys.stderr)

    # Update the configuration
    directory = os.path.dirname(image)
    fname = os.path.basename(image)
    state["directory"] = os.path.dirname(image)
    state["index"] = os.listdir(directory).index(fname)
    with open(STATE_PATH, "w") as f:
        yaml.dump(state, f)

def set_directory(directory: str, config: dict, state: dict):
    images = os.listdir(directory)
    image = os.path.join(directory, images[0])
    set_wallpaper(image, config, state)

def next_image(config: dict, state: dict):
    images = os.listdir(state["directory"])
    image = os.path.join(
        state["directory"], 
        images[(state["index"] + 1) % len(images)]
    )
    set_wallpaper(image, config, state)

def prev_image(config: dict, state: dict):
    images = os.listdir(state["directory"])
    image = os.path.join(
        state["directory"], 
        images[(state["index"] - 1) % len(images)]
    )
    set_wallpaper(image, config, state)

def get_config() -> dict:
    with open(CONFIG_PATH, "r") as f:
        return yaml.safe_load(f)

def get_state() -> dict:
    with open(STATE_PATH, "r") as f:
        return yaml.safe_load(f)

def main():
    # Set up the configuration and state directories
    setup_config()
    setup_state()

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
    parser.add_argument(
        "-d",
        "--directory", 
        action="store",
        help="set a new active image directory",
        metavar="",
        required=False,
    )
    parser.add_argument(
        "-n",
        "--next", 
        action="store_true",
        help="set the wallpaper as the next image in the current active directory",
        required=False,
    )
    parser.add_argument(
        "-p",
        "--prev", 
        action="store_true",
        help="set the wallpaper as the previous image in the current active directory",
        required=False,
    )
    args = parser.parse_args()

    # Get the configuration
    config = get_config()
    state = get_state()

    # If no arguments are passed, print the help message and exit
    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)

    if args.image:
        set_wallpaper(args.image, config, state) 
    elif args.directory:
        set_directory(args.directory, config, state) 
    elif args.next:
        next_image(config, state)
    elif args.prev:
        prev_image(config, state)

if __name__ == "__main__":
    main()
