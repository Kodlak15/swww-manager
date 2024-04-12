#!/usr/bin/env python

from setuptools import setup 
  
setup( 
    name="swwwmgr", 
    version='v0.1.0-alpha', 
    description="Command line utility script for managing wallpaper with swww (https://github.com/LGFae/swww)", 
    author='Cody Stanley', 
    author_email="stanlcod15@protonmail.com", 
    packages=["swwwmgr"], 
    install_requires=[ 
        "pyyaml"
    ], 
) 
