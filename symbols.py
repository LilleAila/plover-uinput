from xkbcommon import xkb


# layout can be "no", "us", "gb", "fr" or any other xkb layout
def generate_symbols(layout="no"):
    ctx = xkb.Context()
    keymap = ctx.keymap_new_from_names(layout=layout)

    # Modifier names from xkb, converted to strings
    level_mapping = {
        0: "",
        1: "shift",
        2: "altgr",
        3: "shift altgr",
    }

    symbols = {}

    for key in iter(keymap):
        try:
            # Levels are different outputs from the same key with modifiers pressed
            levels = keymap.num_levels_for_key(key, 1)
            if levels == 0:  # Key has no output
                continue

            # === Base key symbol ===
            base_key_syms = keymap.key_get_syms_by_level(key, 1, 0)
            if len(base_key_syms) == 0:  # There are no symbols for this key
                continue
            base_key = xkb.keysym_to_string(base_key_syms[0])
            if base_key is None:
                continue
            symbols[base_key] = (base_key, "")
            # === Base key symbol ===

            # === Key variations ===
            if levels < 2:  # There are no variations (Check maybe not needed)
                continue
            for level in range(1, levels + 1):  # Ignoring the first (base) one
                level_key_syms = keymap.key_get_syms_by_level(key, 1, level)
                if len(level_key_syms) == 0:
                    continue
                level_key = xkb.keysym_to_string(level_key_syms[0])
                if level_key is None:
                    continue
                modifiers = level_mapping.get(level, "")
                symbols[level_key] = (base_key, modifiers)
            # === Key variations ===
        except xkb.XKBInvalidKeycode:
            # Iter *should* return only valid, but still returns some invalid...
            pass

    return symbols
