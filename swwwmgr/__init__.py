#!/usr/bin/env python

from pathlib import Path
from shutil import copy
import os

CONFIG_PATH = Path.home().joinpath(".config", "swwwmgr", "config.yaml")

if not CONFIG_PATH.exists():
    dirname = Path(__file__).parent
    src = dirname.joinpath("config.yaml")

    if not CONFIG_PATH.parent.exists():
        os.makedirs(CONFIG_PATH.parent)

    copy(src, CONFIG_PATH)
