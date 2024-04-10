from evdev import UInput, ecodes as e, util

# from symbols import generate_symbols
from time import sleep

from plover.oslayer.keyboardcontrol import KeyboardEmulation as OldKeyboardEmulation
from plover import log

# TODO: rewrite the entire thing like ̃~/devel/plover-output-dotool/plover_output_dotool/__init__.py
# Put all the methods needed into the KeyboardEmulation class, and use symbols.py to get symbols
# If keys has character then send_key key with no modifiers (the function should have a string input, that gets split into a list and read from the mods dictionary)
# Else if symbols has character then send_key base_key with modifiers from the symbols dictionary generated
# Else, do nothing because key is not defined

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


mods = {
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
    " ": e.KEY_SPACE,
    ".": e.KEY_DOT,
    ",": e.KEY_COMMA,
    "-": e.KEY_MINUS,
    "\b": e.KEY_BACKSPACE,
}


class Chord:
    def __init__(self, char, modifiers=""):
        self.char = char
        self.mods = (
            [mods[mod] for mod in modifiers.split(" ")] if len(modifiers) > 0 else []
        )


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

    def start(self):
        start()

    def cancel(self):
        pass

    def stop(self):
        self._ui.close()

    def set_key_press_delay(self, ms):
        if self._ms != ms:
            self._ms = ms
            self._delay = self._ms / 1000

    def _press_key(self, key, state):
        self._ui.write(e.EV_KEY, key, 1 if state else 0)

    def _send_key(self, key):
        self._press_key(key, True)
        self._press_key(key, False)

    def send_string(self, string):
        key_presses = [keys[i] for i in list(string)]
        for key in key_presses:
            self._send_key(key)
            sleep(self._delay)
        self._ui.syn()

    def send_backspaces(self, num):
        for i in range(num):
            self._send_key(keys["\b"])
            sleep(self._delay)
        self._ui.syn()

    def send_key_combination(self, combo_string):
        key_events = parse_key_combo(combo_string)

        for key, pressed in key_events:
            k = mods[key] if key in mods else keys[key]
            self._press_key(k, pressed)


class Main:
    def __init__(self, engine):
        self._engine = engine
        self._old_keyboard_emulation = None

    def start(self):
        if hasattr(self._engine, "_output"):
            pass
        else:
            assert self._old_keyboard_emulation is None
            self._old_keyboard_emulation = self._engine._keyboard_emulation
            assert isinstance(self._old_keyboard_emulation, OldKeyboardEmulation)
            self._engine._keyboard_emulation = KeyboardEmulation()

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
