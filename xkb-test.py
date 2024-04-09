from xkbcommon import xkb

ctx = xkb.Context()
keymap = ctx.keymap_new_from_names(layout="no")  # TODO: make this changeable somehow

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
        base_key = ""
        for level in range(0, levels + 1):
            # print(level, keymap.mod_get_name(level))
            """
            All modifier names:
            0 modifier_map Shift { <LFSH>, <RTSH> };
            1 modifier_map Lock { <CAPS> };
            2 modifier_map Control { <LCTL>, <RCTL> };
            3 modifier_map Mod1 { <LALT>, <ALT>, <META> };
            4 modifier_map Mod2 { <NMLK> };
            5 modifier_map Mod3 { <LVL5> };
            6 modifier_map Mod4 { <LWIN>, <RWIN>, <SUPR>, <HYPR> };
            7 modifier_map Mod5 { <LVL3> };

            From my testing, the `level` means:
            0 nothing
            1 shift
            2 altgr
            3 shift + altgr
            (which does not correspond to the modifiers for some reason)
            """

            level_syms = keymap.key_get_syms_by_level(key, 1, level)
            if len(level_syms) == 0:  # There is nothing on this level
                continue
            key_result = xkb.keysym_to_string(level_syms[0])  # Only one per level
            if level == 0:  # Save the base key to be used later
                base_key = key_result
            if key_result is None:  # The key does not output a character
                continue
            if level > 3:  # Some weird modifier combination
                continue

            modifiers = level_mapping.get(level, "")
            print(base_key, modifiers, key_result)
            symbols[key_result] = (base_key, modifiers)
    except xkb.XKBInvalidKeycode:
        # Iter *should* return only valid, but still returns some invalid...
        pass

print(symbols)
