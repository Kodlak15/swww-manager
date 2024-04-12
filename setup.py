#!/usr/bin/env python

from setuptools import setup, find_packages
  
setup( 
    name="swwwmgr", 
    version="v0.1.0-alpha", 
    description="Command line utility script for managing wallpaper with swww (https://github.com/LGFae/swww)", 
    packages=find_packages(), 
    entry_points={
        "console-scripts": ["swwwmgr = swwwmgr.main:main"],
    },
    install_requires=[ 
        "pyyaml"
    ], 
    include_package_data=True,
) 
