keyboard_scancodes_extended = {
    "a": {"scancode": 30},
    "A": {"scancode": 30, "modifiers": ["SHIFT"]},
    "b": {"scancode": 48},
    "B": {"scancode": 48, "modifiers": ["SHIFT"]},
    "c": {"scancode": 46},
    "C": {"scancode": 46, "modifiers": ["SHIFT"]},
    "d": {"scancode": 32},
    "D": {"scancode": 32, "modifiers": ["SHIFT"]},
    "e": {"scancode": 18},
    "E": {"scancode": 18, "modifiers": ["SHIFT"]},
    "f": {"scancode": 33},
    "F": {"scancode": 33, "modifiers": ["SHIFT"]},
    "g": {"scancode": 34},
    "G": {"scancode": 34, "modifiers": ["SHIFT"]},
    "h": {"scancode": 35},
    "H": {"scancode": 35, "modifiers": ["SHIFT"]},
    "i": {"scancode": 23},
    "I": {"scancode": 23, "modifiers": ["SHIFT"]},
    "j": {"scancode": 36},
    "J": {"scancode": 36, "modifiers": ["SHIFT"]},
    "k": {"scancode": 37},
    "K": {"scancode": 37, "modifiers": ["SHIFT"]},
    "l": {"scancode": 38},
    "L": {"scancode": 38, "modifiers": ["SHIFT"]},
    "m": {"scancode": 50},
    "M": {"scancode": 50, "modifiers": ["SHIFT"]},
    "n": {"scancode": 49},
    "N": {"scancode": 49, "modifiers": ["SHIFT"]},
    "o": {"scancode": 24},
    "O": {"scancode": 24, "modifiers": ["SHIFT"]},
    "p": {"scancode": 25},
    "P": {"scancode": 25, "modifiers": ["SHIFT"]},
    "q": {"scancode": 16},
    "Q": {"scancode": 16, "modifiers": ["SHIFT"]},
    "r": {"scancode": 19},
    "R": {"scancode": 19, "modifiers": ["SHIFT"]},
    "s": {"scancode": 31},
    "S": {"scancode": 31, "modifiers": ["SHIFT"]},
    "t": {"scancode": 20},
    "T": {"scancode": 20, "modifiers": ["SHIFT"]},
    "u": {"scancode": 22},
    "U": {"scancode": 22, "modifiers": ["SHIFT"]},
    "v": {"scancode": 47},
    "V": {"scancode": 47, "modifiers": ["SHIFT"]},
    "w": {"scancode": 17},
    "W": {"scancode": 17, "modifiers": ["SHIFT"]},
    "x": {"scancode": 45},
    "X": {"scancode": 45, "modifiers": ["SHIFT"]},
    "y": {"scancode": 44},
    "Y": {"scancode": 44, "modifiers": ["SHIFT"]},
    "z": {"scancode": 21},
    "Z": {"scancode": 21, "modifiers": ["SHIFT"]},
    "1": {"scancode": 2},
    "!": {"scancode": 2, "modifiers": ["SHIFT"]},
    "2": {"scancode": 3},
    "\"": {"scancode": 3, "modifiers": ["SHIFT"]},
    "3": {"scancode": 4},
    "§": {"scancode": 4, "modifiers": ["SHIFT"]},
    "4": {"scancode": 5},
    "$": {"scancode": 5, "modifiers": ["SHIFT"]},
    "5": {"scancode": 6},
    "%": {"scancode": 6, "modifiers": ["SHIFT"]},
    "6": {"scancode": 7},
    "&": {"scancode": 7, "modifiers": ["SHIFT"]},
    "7": {"scancode": 8},
    "/": {"scancode": 8, "modifiers": ["SHIFT"]},
    "8": {"scancode": 9},
    "(": {"scancode": 9, "modifiers": ["SHIFT"]},
    "9": {"scancode": 10},
    ")": {"scancode": 10, "modifiers": ["SHIFT"]},
    "0": {"scancode": 11},
    "=": {"scancode": 11, "modifiers": ["SHIFT"]},
    "-": {"scancode": 53},
    "_": {"scancode": 53, "modifiers": ["SHIFT"]},
    " ": {"scancode": 57},
    ".": {"scancode": 52},
    ":": {"scancode": 52, "modifiers": ["SHIFT"]},
    "@": {"scancode": 16, "modifiers": ["ALTGR"]}
}


def string_to_scancodes_with_release(string, scancodes):
    result = []
    for char in string:
        entry = scancodes.get(char, None)
        if entry:
            # Wenn Modifikatoren vorhanden sind, füge sie zuerst hinzu
            if "modifiers" in entry:
                for modifier in entry["modifiers"]:
                    if modifier == "SHIFT":
                        result.append({"scancode": "2A"})  # SHIFT drücken
                    elif modifier == "ALTGR":
                        result.append({"scancode": "38"})  # ALTGR drücken

            # Haupttaste drücken
            scancode = hex(entry["scancode"])[2:].zfill(2).upper()
            result.append({"scancode": scancode})

            # Haupttaste loslassen
            release_scancode = hex(entry["scancode"] + 128)[2:].zfill(2).upper()
            result.append({"scancode": release_scancode})

            # Modifikatoren in umgekehrter Reihenfolge loslassen
            if "modifiers" in entry:
                for modifier in reversed(entry["modifiers"]):
                    if modifier == "SHIFT":
                        result.append({"scancode": "AA"})  # SHIFT loslassen
                    elif modifier == "ALTGR":
                        result.append({"scancode": "B8"})  # ALTGR loslassen
        else:
            result.append({"char": char, "error": "Not found"})

    return result


# Hilfsfunktion zum Formatieren der Ausgabe
def format_scancode_sequence(scancode_list):
    formatted = []
    for item in scancode_list:
        if "error" in item:
            formatted.append(f"Fehler: {item['char']} nicht gefunden")
        else:
            formatted.append(item["scancode"])
    return " ".join(formatted)


# Beispielverwendung
def test_translation():
    test_strings = [
        "Hello@",  # Test mit ALTGR
        "Test!",  # Test mit SHIFT
        "abc",  # Test ohne Modifikatoren
        "https://www.hs-wismar.de/"
    ]

    for test_string in test_strings:
        print(f"\nTest String: {test_string}")
        translation = string_to_scancodes_with_release(test_string, keyboard_scancodes_extended)
        print(f"Scancodes: {format_scancode_sequence(translation)}")


test_translation()
