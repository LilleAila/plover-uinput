from evdev import UInput, ecodes as e, util
from time import sleep


mods = {
    "shift": e.KEY_LEFTSHIFT,
    "ctrl": e.KEY_LEFTCTRL,
    "alt": e.KEY_LEFTALT,
    "altgr": e.KEY_RIGHTALT,
    "super": e.KEY_LEFTMETA,
}


class Chord:
    def __init__(self, char, modifiers=""):
        self.char = char
        self.mods = (
            [mods[mod] for mod in modifiers.split(" ")] if len(modifiers) > 0 else []
        )

    def display(self):
        return f"Char: {ecodes.KEY[self.char]}, Mods: " + ", ".join(
            [ecodes.KEY[i] for i in self.mods]
        )

    # should probably be outside of the class
    def type(self, ui):
        for mod in self.mods:
            ui.write(e.EV_KEY, mod, 1)
        ui.write(e.EV_KEY, self.char, 1)
        ui.write(e.EV_KEY, self.char, 0)
        for mod in self.mods:
            ui.write(e.EV_KEY, mod, 0)
        sleep(0.001)


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
    "A": Chord(e.KEY_A, "shift"),
    "B": Chord(e.KEY_B, "shift"),
    "C": Chord(e.KEY_C, "shift"),
    "D": Chord(e.KEY_D, "shift"),
    "E": Chord(e.KEY_E, "shift"),
    "F": Chord(e.KEY_F, "shift"),
    "G": Chord(e.KEY_G, "shift"),
    "H": Chord(e.KEY_H, "shift"),
    "I": Chord(e.KEY_I, "shift"),
    "J": Chord(e.KEY_J, "shift"),
    "K": Chord(e.KEY_K, "shift"),
    "L": Chord(e.KEY_L, "shift"),
    "M": Chord(e.KEY_M, "shift"),
    "N": Chord(e.KEY_N, "shift"),
    "O": Chord(e.KEY_O, "shift"),
    "P": Chord(e.KEY_P, "shift"),
    "Q": Chord(e.KEY_Q, "shift"),
    "R": Chord(e.KEY_R, "shift"),
    "S": Chord(e.KEY_S, "shift"),
    "T": Chord(e.KEY_T, "shift"),
    "U": Chord(e.KEY_U, "shift"),
    "V": Chord(e.KEY_V, "shift"),
    "W": Chord(e.KEY_W, "shift"),
    "X": Chord(e.KEY_X, "shift"),
    "Y": Chord(e.KEY_Y, "shift"),
    "Z": Chord(e.KEY_Z, "shift"),
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
    "\b": Chord(e.KEY_BACKSPACE),
    "!": Chord(e.KEY_1, "shift"),
    "[": Chord(e.KEY_8, "altgr"),  # Problem because different kb layouts
}

print(keys["e"])


def type_string(ui, string):
    chords = [keys[i] for i in list(string)]
    for chord in chords:
        chord.type(ui)
    ui.syn()


res = util.find_ecodes_by_regex(r"KEY_.*")
ui = UInput(res)

type_string(ui, "Hello, World!")

ui.close()
