#!/usr/bin/env python3

import argparse
import os
import random
import subprocess
import sys
from pathlib import Path

import yaml

CONFIG_PATH = Path.home().joinpath(".config", "swwwmgr", "config.yaml")
STATE_PATH = Path.home().joinpath(".local", "state", "swwwmgr", "state.yaml")


def setup_config() -> None:
    if not os.path.exists(CONFIG_PATH.parent):
        os.makedirs(CONFIG_PATH.parent)
    # Generate the default configuration file if one does not already exist
    if not os.path.exists(CONFIG_PATH):
        config = {
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


def setup_state() -> None:
    # Create the config and state directories if they do not exist
    if not os.path.exists(STATE_PATH.parent):
        os.makedirs(STATE_PATH.parent)
    if not os.path.exists(STATE_PATH):
        state = {
            "directory": str(CONFIG_PATH.parent),
            "index": 0,
        }
        with open(STATE_PATH, "w") as f:
            yaml.dump(state, f)


def set_wallpaper(image: str, config: dict, state: dict) -> None:
    # Use swww to change the wallpaper
    subprocess.run(
        [
            "swww",
            "img",
            image,
            "--transition-type",
            config["transition"]["type"],
            "--transition-pos",
            config["transition"]["position"],
            "--transition-step",
            str(config["transition"]["step"]),
            "--transition-duration",
            str(config["transition"]["duration"]),
            "--transition-angle",
            str(config["transition"]["angle"]),
        ]
    )

    # Update the configuration
    directory = os.path.dirname(image)
    fname = os.path.basename(image)
    state["directory"] = os.path.dirname(image)
    state["index"] = os.listdir(directory).index(fname)
    with open(STATE_PATH, "w") as f:
        yaml.dump(state, f)


def set_directory(directory: str, config: dict, state: dict) -> None:
    images = os.listdir(directory)
    image = os.path.join(directory, images[0])
    set_wallpaper(image, config, state)


def next_image(config: dict, state: dict) -> None:
    images = os.listdir(state["directory"])
    image = os.path.join(state["directory"], images[(state["index"] + 1) % len(images)])
    set_wallpaper(image, config, state)


def prev_image(config: dict, state: dict) -> None:
    images = os.listdir(state["directory"])
    image = os.path.join(state["directory"], images[(state["index"] - 1) % len(images)])
    set_wallpaper(image, config, state)


def random_image(config: dict, state: dict) -> None:
    images = os.listdir(state["directory"])
    image = os.path.join(state["directory"], images[random.randint(0, len(images))])
    set_wallpaper(image, config, state)


def get_config() -> dict:
    with open(CONFIG_PATH, "r") as f:
        return yaml.safe_load(f)


def get_state() -> dict:
    with open(STATE_PATH, "r") as f:
        return yaml.safe_load(f)


def get_args() -> argparse.Namespace:
    """
    Parse and return command line arguments
    """
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
    parser.add_argument(
        "-r",
        "--random",
        action="store_true",
        help="set the wallpaper as a random image in the current active directory",
        required=False,
    )

    # If no arguments are passed, print the help message and exit
    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)

    return parser.parse_args()


def main():
    args = get_args()
    # Set up the configuration and state directories
    setup_config()
    setup_state()
    # Get the configuration
    config = get_config()
    state = get_state()
    if args.image:
        set_wallpaper(args.image, config, state)
    elif args.directory:
        set_directory(args.directory, config, state)
    elif args.random:
        random_image(config, state)
    elif args.next:
        next_image(config, state)
    elif args.prev:
        prev_image(config, state)


if __name__ == "__main__":
    main()
