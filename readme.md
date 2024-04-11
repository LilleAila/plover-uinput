# Plover output plugin for linux using uinput

## Setup
Add your user to the `input` group, and add this `udev` rule:
```
KERNEL=="uinput", GROUP="input", MODE="0660", OPTIONS+="static_node=uinput"
```
Set the `PLOVER_UINPUT_LAYOUT` environment variable to your two-letter `xkb` keyboard layout, for example `us`, `no` or `fr`.

## Unicode characters
If you want to use unicode characters, `iBus` has to be installed.
