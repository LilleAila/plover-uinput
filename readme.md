# Plover output plugin for linux using uinput

## Setup
Add your user to the `input` group, and add this `udev` rule:
```
KERNEL=="uinput", GROUP="input", MODE="0660", OPTIONS+="static_node=uinput"
```
