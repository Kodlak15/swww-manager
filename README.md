# swww-manager

This is a rudimentary script that I use to manage my desktop wallpaper with swww (https://github.com/LGFae/swww). The script uses a configuration file at \$HOME/.config/swwwmgr/config.yaml to set up the transition style for swww, and a state file at \$HOME/.local/state/swwwmgr/state.yaml to keep track of images. A home manager module is included for nix users.

## Usage

```
# Set the image directory to the one at the specified path
swwwmgr -d /path/to/images
# Set the wallpaper as the next image in the current image directory
swwwmgr -n
# Set the wallpaper as the previous image in the current image directory
swwwmgr -p
# Set the wallpaper as a random image in the current image directory
swwwmgr -r
```
