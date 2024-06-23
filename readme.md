# Plover output plugin for linux using uinput
This plugin directly emulates the keyboard using uinput, which is present on most linux distributions. This means that it will work on X11, wayland and even in the tty.

## Setup
Add your user to the `input` group, and install this `udev` rule:
```
KERNEL=="uinput", GROUP="input", MODE="0660", OPTIONS+="static_node=uinput"
```
Set the `PLOVER_UINPUT_LAYOUT` environment variable to your two-letter `xkb` keyboard layout, for example `us`, `no` or `fr`. This is not necessary if you're using a US keyboard.

## Issues
### Unicode characters
If you want to use unicode characters, either `iBus` or `fcitx5` has to be installed. You might have to increase the key press delay in plover if some characters do not output properly.

### Other issues
If you encounter any other problems, feel free to open an issue, pull request or send a message on discord (`lilleaila`)! Before asking for help, please check if the plugin is enabled in the settings.

## Inspired by:
- [halbGefressen/plover-output-dotool](https://github.com/halbGefressen/plover-output-dotool)
- [svenkeidel/plover-wtype-output](https://github.com/svenkeidel/plover-wtype-output/tree/main)

# TODO
- [ ] Implement keyboard capture
- [ ] Make it easier to install udev rules
- [ ] Add a github action for publishing to PyPi
