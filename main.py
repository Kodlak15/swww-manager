#!/usr/bin/env python3 

import os
import sys
import argparse
import subprocess
import yaml

def setup():
    if not os.path.exists("config.yaml"):
        config = {
            "directory": ".",
            "index": 16,
            "pywal": True,
            "transition": {
                "angle": "180",
                "duration": "0.5",
                "position": "0.7,0.9",
                "step": "180",
                "type": "wipe",
            },
        }

        with open("config.yaml", "w") as f:
            yaml.dump(config, f)

def set_wallpaper(image: str, config: dict):
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
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    # If using pywal, run pywal using the new image to generate colors
    if config["pywal"]:
        subprocess.run(["wal", "-i", image, "-n"])

    # Update the configuration
    directory = os.path.dirname(image)
    fname = os.path.basename(image)
    config["directory"] = os.path.dirname(image)
    config["index"] = os.listdir(directory).index(fname)
    with open("config.yaml", "w") as f:
        yaml.dump(config, f)

def set_directory(directory: str, config: dict):
    images = os.listdir(directory)
    image = os.path.join(directory, images[0])
    set_wallpaper(image, config)

def next_image(config: dict):
    images = os.listdir(config["directory"])
    image = os.path.join(config["directory"], images[(config["index"] + 1) % len(images)])
    set_wallpaper(image, config)

def prev_image(config: dict):
    images = os.listdir(config["directory"])
    image = os.path.join(config["directory"], images[(config["index"] - 1) % len(images)])
    set_wallpaper(image, config)

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
        # metavar="",
        required=False,
    )
    parser.add_argument(
        "-p",
        "--prev", 
        action="store_true",
        help="set the wallpaper as the previous image in the current active directory",
        # metavar="",
        required=False,
    )
    args = parser.parse_args()

    # Get the configuration
    config = get_config()

    # If no arguments are passed, print the help message and exit
    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)

    if args.image:
        set_wallpaper(args.image, config) 
    elif args.directory:
        set_directory(args.directory, config) 
    elif args.next:
        next_image(config)
    elif args.prev:
        prev_image(config)

