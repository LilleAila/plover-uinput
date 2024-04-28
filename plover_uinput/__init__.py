from evdev import UInput, ecodes as e, util

from .symbols import generate_symbols
from time import sleep

from plover.oslayer.keyboardcontrol import KeyboardEmulation as OldKeyboardEmulation
from plover import log
import os  # To read the layout variable

# If keys has character then send_key key with no modifiers (the function should have a string input, that gets split into a list and read from the mods dictionary)
# Else if symbols has character then send_key base_key with modifiers from the symbols dictionary generated
# Else, input unicode

# === Import or create `parse_key_combo` function ===
try:
    from plover.key_combo import parse_key_combo
except ImportError:
    log.warning("With new KeyCombo interface")
    from plover.key_combo import KeyCombo

    _key_combo = KeyCombo()

    def parse_key_combo(combo_string: str):
        return _key_combo.parse(combo_string)


# === Try importing `KeyboardEmulationBase` ===
have_output_plugin = False
try:
    from plover.oslayer import KeyboardEmulationBase

    have_output_plugin = True
except ImportError:
    pass


modifiers = {
    "alt_l": e.KEY_LEFTALT,
    "alt_r": e.KEY_RIGHTALT,
    "control_l": e.KEY_LEFTCTRL,
    "control_r": e.KEY_RIGHTCTRL,
    "shift_l": e.KEY_LEFTSHIFT,
    "shift_r": e.KEY_RIGHTSHIFT,
    "super_l": e.KEY_LEFTMETA,
    "super_r": e.KEY_RIGHTMETA,
}


keys = {
    # Lowercase
    "a": e.KEY_A,
    "b": e.KEY_B,
    "c": e.KEY_C,
    "d": e.KEY_D,
    "e": e.KEY_E,
    "f": e.KEY_F,
    "g": e.KEY_G,
    "h": e.KEY_H,
    "i": e.KEY_I,
    "j": e.KEY_J,
    "k": e.KEY_K,
    "l": e.KEY_L,
    "m": e.KEY_M,
    "n": e.KEY_N,
    "o": e.KEY_O,
    "p": e.KEY_P,
    "q": e.KEY_Q,
    "r": e.KEY_R,
    "s": e.KEY_S,
    "t": e.KEY_T,
    "u": e.KEY_U,
    "v": e.KEY_V,
    "w": e.KEY_W,
    "x": e.KEY_X,
    "y": e.KEY_Y,
    "z": e.KEY_Z,
    # Numbers
    "1": e.KEY_1,
    "2": e.KEY_2,
    "3": e.KEY_3,
    "4": e.KEY_4,
    "5": e.KEY_5,
    "6": e.KEY_6,
    "7": e.KEY_7,
    "8": e.KEY_8,
    "9": e.KEY_9,
    "0": e.KEY_0,
    # Symbols
    "-": e.KEY_MINUS,
    "=": e.KEY_EQUAL,
    " ": e.KEY_SPACE,
    "[": e.KEY_LEFTBRACE,
    "]": e.KEY_RIGHTBRACE,
    ";": e.KEY_SEMICOLON,
    "'": e.KEY_APOSTROPHE,
    "`": e.KEY_GRAVE,
    "\\": e.KEY_BACKSLASH,
    ".": e.KEY_DOT,
    ",": e.KEY_COMMA,
    "/": e.KEY_SLASH,
    "\b": e.KEY_BACKSPACE,
    "\n": e.KEY_ENTER,
    # Other keys (for send_key_combination())
    # https://github.com/openstenoproject/plover/blob/9b5a357f1fb57cb0a9a8596ae12cd1e84fcff6c4/plover/oslayer/osx/keyboardcontrol.py#L75
    # https://gist.github.com/jfortin42/68a1fcbf7738a1819eb4b2eef298f4f8
    "return": e.KEY_ENTER,
    "tab": e.KEY_TAB,
    "backspace": e.KEY_BACKSPACE,
    "delete": e.KEY_DELETE,
    "escape": e.KEY_ESC,
    "clear": e.KEY_CLEAR,
    # Navigation
    "up": e.KEY_UP,
    "down": e.KEY_DOWN,
    "left": e.KEY_LEFT,
    "right": e.KEY_RIGHT,
    "page_up": e.KEY_PAGEUP,
    "page_down": e.KEY_PAGEDOWN,
    # Function keys
    "fn": e.KEY_FN,
    "f1": e.KEY_F1,
    "f2": e.KEY_F2,
    "f3": e.KEY_F3,
    "f4": e.KEY_F4,
    "f5": e.KEY_F5,
    "f6": e.KEY_F6,
    "f7": e.KEY_F7,
    "f8": e.KEY_F8,
    "f9": e.KEY_F9,
    "f10": e.KEY_F10,
    "f11": e.KEY_F11,
    "f12": e.KEY_F12,
    "f13": e.KEY_F13,
    "f14": e.KEY_F14,
    "f15": e.KEY_F15,
    "f16": e.KEY_F16,
    "f17": e.KEY_F17,
    "f18": e.KEY_F18,
    "f19": e.KEY_F19,
    "f20": e.KEY_F20,
    "f21": e.KEY_F21,
    "f22": e.KEY_F22,
    "f23": e.KEY_F23,
    "f24": e.KEY_F24,
    # Numpad
    "kp_1": e.KEY_KP1,
    "kp_2": e.KEY_KP2,
    "kp_3": e.KEY_KP3,
    "kp_4": e.KEY_KP4,
    "kp_5": e.KEY_KP5,
    "kp_6": e.KEY_KP6,
    "kp_7": e.KEY_KP7,
    "kp_8": e.KEY_KP8,
    "kp_9": e.KEY_KP9,
    "kp_0": e.KEY_KP0,
    "kp_add": e.KEY_KPPLUS,
    "kp_decimal": e.KEY_KPDOT,
    "kp_delete": e.KEY_DELETE,  # There is no KPDELETE
    "kp_divide": e.KEY_KPSLASH,
    "kp_enter": e.KEY_KPENTER,
    "kp_equal": e.KEY_KPEQUAL,
    "kp_multiply": e.KEY_KPASTERISK,
    "kp_subtract": e.KEY_KPMINUS,
    # Media keys
    "AudioRaiseVolume": e.KEY_VOLUMEUP,
    "AudioLowerVolume": e.KEY_VOLUMEDOWN,
    "MonBrightnessUp": e.KEY_BRIGHTNESSUP,
    "MonBrightnessDown": e.KEY_BRIGHTNESSDOWN,
    "AudioMute": e.KEY_MUTE,
    "Num_Lock": e.KEY_NUMLOCK,
    "Eject": e.KEY_EJECTCD,
    "AudioPause": e.KEY_PAUSE,
    "AudioPlay": e.KEY_PLAY,
    "AudioNext": e.KEY_NEXT,  # Maybe VIDEO_NEXT or NEXTSONG
    "AudioRewind": e.KEY_REWIND,
    "KbdBrightnessUp": e.KEY_KBDILLUMUP,
    "KbdBrightnessDown": e.KEY_KBDILLUMDOWN,
}


class KeyboardEmulation(*([KeyboardEmulationBase] if have_output_plugin else [])):
    @classmethod
    def get_option_info(cls):
        return {}

    def __init__(self, params=None):
        if have_output_plugin:
            KeyboardEmulationBase.__init__(self, params)
        self._ms = 1
        self._delay = self._ms / 1000
        self._res = util.find_ecodes_by_regex(r"KEY_.*")
        self._ui = UInput(self._res)
        # Set the keyboard layout from an environment variable
        kb_env = "PLOVER_UINPUT_LAYOUT"
        kb_layout = os.environ[kb_env] if kb_env in os.environ else "us"
        self._set_layout(kb_layout)

    def start(self):
        start()

    def cancel(self):
        pass

    def stop(self):
        self._ui.close()

    def _set_layout(self, layout):
        log.info("Using keyboard layout " + layout + " for keyboard emulation.")
        symbols = generate_symbols(layout)
        # Remove unwanted symbols from the table
        # Includes symbols such as numpad-star - use unicode instead
        # There has to be a cleaner way to do this
        syms_to_remove = []
        for sym in symbols:
            (base, _) = symbols[sym]
            if base not in keys:
                syms_to_remove.append(sym)
        for sym in syms_to_remove:
            symbols.pop(sym)
        self._symbols = symbols

    def set_key_press_delay(self, ms):
        if self._ms != ms:
            self._ms = ms
            self._delay = self._ms / 1000

    def _press_key(self, key, state):
        self._ui.write(e.EV_KEY, key, 1 if state else 0)
        self._ui.syn()

    def _send_key(self, key):
        self._press_key(key, True)
        self._press_key(key, False)
        self._ui.syn()

    # Send unicode character (through iBus)
    def _send_unicode(self, hex):
        self._press_key(modifiers["control_l"], True)
        self._press_key(modifiers["shift_l"], False)
        sleep(self._delay)
        self._send_key(keys["u"])
        sleep(self._delay)
        self._press_key(modifiers["control_l"], False)
        self._press_key(modifiers["shift_l"], False)
        sleep(self._delay)
        self._send_string(hex)
        self._send_key(keys["\n"])

    def _send_char(self, char):
        # === Key can be sent with a key combination ===
        if char in self._symbols:
            (base, mods) = self._symbols[char]
            for mod in mods.split():
                self._press_key(modifiers[mods], True)
            sleep(self._delay)
            self._send_key(keys[base])
            for mod in mods.split():
                self._press_key(modifiers[mods], False)
            sleep(self._delay)
        # === Key can not be typed - send unicode symbol ===
        # It would be better if it was possible to modify the layout to a custom one
        # including all the needed symbols
        else:
            # Convert to hex and remove leading "0x"
            unicode_hex = hex(ord(char))[2:]
            self._send_unicode(unicode_hex)

        # === Delay before next ===
        sleep(self._delay)

    def send_string(self, string):
        # key_presses = [keys[i] for i in list(string)]
        # for key in key_presses:
        for key in list(string):
            self._send_char(key)

    def send_backspaces(self, num):
        for i in range(num):
            self._send_key(keys["\b"])
            sleep(self._delay)
            self._ui.syn()

    def send_key_combination(self, combo_string):
        key_events = parse_key_combo(combo_string)

        for key, pressed in key_events:
            k = modifiers[key] if key in modifiers else keys[key]
            self._press_key(k, pressed)


class Main:
    def __init__(self, engine):
        self._engine = engine
        self._old_keyboard_emulation = None

    # def _config_changed(self, config):
    #     print(config)

    def start(self):
        if hasattr(self._engine, "_output"):
            pass
        else:
            assert self._old_keyboard_emulation is None
            self._old_keyboard_emulation = self._engine._keyboard_emulation
            assert isinstance(self._old_keyboard_emulation, OldKeyboardEmulation)
            self._engine._keyboard_emulation = KeyboardEmulation()
            # self._engine.hook_connect("config_changed", self._config_changed)

    def stop(self):
        if hasattr(self._engine, "_output"):
            log.warning(
                "Stopping while Plover is running is unsupported - uninstall the plugin instead"
            )
            self._engine._keyboard_emulation.stop()
        else:
            assert self._old_keyboard_emulation is not None
            self._engine._keyboard_emulation.stop()
            self._engine._keyboard_emulation = self._old_keyboard_emulation
            self._old_keyboard_emulation = None
