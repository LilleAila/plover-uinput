from evdev import util, ecodes

res = util.find_ecodes_by_regex(r"KEY_.*")
keys = [ecodes.KEY[key] for key in res[1]]
print(keys)
