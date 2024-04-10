from evdev import UInput, ecodes as e, util
from symbols import generate_symbols
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
    "a": Chord(e.KEY_A),
    "b": Chord(e.KEY_B),
    "c": Chord(e.KEY_C),
    "d": Chord(e.KEY_D),
    "e": Chord(e.KEY_E),
    "f": Chord(e.KEY_F),
    "g": Chord(e.KEY_G),
    "h": Chord(e.KEY_H),
    "i": Chord(e.KEY_I),
    "j": Chord(e.KEY_J),
    "k": Chord(e.KEY_K),
    "l": Chord(e.KEY_L),
    "m": Chord(e.KEY_M),
    "n": Chord(e.KEY_N),
    "o": Chord(e.KEY_O),
    "p": Chord(e.KEY_P),
    "q": Chord(e.KEY_Q),
    "r": Chord(e.KEY_R),
    "s": Chord(e.KEY_S),
    "t": Chord(e.KEY_T),
    "u": Chord(e.KEY_U),
    "v": Chord(e.KEY_V),
    "w": Chord(e.KEY_W),
    "x": Chord(e.KEY_X),
    "y": Chord(e.KEY_Y),
    "z": Chord(e.KEY_Z),
    # Uppercase
    "A": Chord(e.KEY_A, "shift_l"),
    "B": Chord(e.KEY_B, "shift_l"),
    "C": Chord(e.KEY_C, "shift_l"),
    "D": Chord(e.KEY_D, "shift_l"),
    "E": Chord(e.KEY_E, "shift_l"),
    "F": Chord(e.KEY_F, "shift_l"),
    "G": Chord(e.KEY_G, "shift_l"),
    "H": Chord(e.KEY_H, "shift_l"),
    "I": Chord(e.KEY_I, "shift_l"),
    "J": Chord(e.KEY_J, "shift_l"),
    "K": Chord(e.KEY_K, "shift_l"),
    "L": Chord(e.KEY_L, "shift_l"),
    "M": Chord(e.KEY_M, "shift_l"),
    "N": Chord(e.KEY_N, "shift_l"),
    "O": Chord(e.KEY_O, "shift_l"),
    "P": Chord(e.KEY_P, "shift_l"),
    "Q": Chord(e.KEY_Q, "shift_l"),
    "R": Chord(e.KEY_R, "shift_l"),
    "S": Chord(e.KEY_S, "shift_l"),
    "T": Chord(e.KEY_T, "shift_l"),
    "U": Chord(e.KEY_U, "shift_l"),
    "V": Chord(e.KEY_V, "shift_l"),
    "W": Chord(e.KEY_W, "shift_l"),
    "X": Chord(e.KEY_X, "shift_l"),
    "Y": Chord(e.KEY_Y, "shift_l"),
    "Z": Chord(e.KEY_Z, "shift_l"),
    # Numbers
    "1": Chord(e.KEY_1),
    "2": Chord(e.KEY_2),
    "3": Chord(e.KEY_3),
    "4": Chord(e.KEY_4),
    "5": Chord(e.KEY_5),
    "6": Chord(e.KEY_6),
    "7": Chord(e.KEY_7),
    "8": Chord(e.KEY_8),
    "9": Chord(e.KEY_9),
    "0": Chord(e.KEY_0),
    # Symbols
    " ": Chord(e.KEY_SPACE),
    ".": Chord(e.KEY_DOT),
    ",": Chord(e.KEY_COMMA),
    "-": Chord(e.KEY_MINUS),
    "\b": Chord(e.KEY_BACKSPACE),
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

    def set_key_press_delay(self, ms):
        if self._ms != ms:
            self._ms = ms
            self._delay = self._ms / 1000

    def _press_key(self, key, state):
        self._ui.write(e.EV_KEY, key, 1 if state else 0)

    def _send_key(self, key):
        self._press_key(key, True)
        self._press_key(key, False)

    def _send_chord(self, key):
        for mod in key.mods:
            self._ui.write(e.EV_KEY, mod, 1)
        self._send_key(key.char)
        for mod in key.mods:
            self._ui.write(e.EV_KEY, mod, 0)

    def send_string(self, string):
        chords = [keys[i] for i in list(string)]
        for chord in chords:
            self._send_chord(chord)
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
        else:
            assert self._old_keyboard_emulation is not None
            self._engine._keyboard_emulation = self._old_keyboard_emulation
            self._engine._keyboard_emulation.stop()
            self._old_keyboard_emulation = None
