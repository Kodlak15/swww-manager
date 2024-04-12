# swww-manager (alpha)
This is a simple utility script for managing wallpaper with swww (https://github.com/LGFae/swww). In case you are unfamiliar with swww, it is an animated wallpaper daemon for wayland. Check out the provided GitHub link to learn more about swww. This project allows you to preconfigure the behavior of swww and easily switch through images in a given directory.

### What can I do with this?
- Set the wallpaper to any image on your system (also updates the active image directory in config.yaml)
```
main.py --image /path/to/directory/image.jpg
```
- Set the active image directory and set the wallpaper to the first image inside that directory (as of now the directory must only contain images for this to work properly)
```
main.py --directory /path/to/directory
```
- Set the wallpaper to the next image in the active image directory
```
main.py --next
```
- Set the wallpaper to the previous image in the active image directory
```
main.py --prev
```
- Set custom configuration options (such as animations) inside config.yaml
