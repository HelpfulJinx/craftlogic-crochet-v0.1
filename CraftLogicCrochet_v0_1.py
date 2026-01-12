"""
CraftLogic: Crochet — v0.1 (CLI prototype)

A small command-line prototype for a future mobile app concept:
- Mode 1 (demo): "Recreate from photo" (currently mocked as a granny-square workflow)
- Mode 2: Blanket Builder (size + border + rough yardage estimate)

Navigation (within modes):
- Type 'b' to go back
- Type 'q' to quit
"""

from __future__ import annotations

import math


# ----------------------------
# Configuration
# ----------------------------

pattern_style = "beginner"  # "beginner" or "advanced"
DEFAULT_UNIT = "in"         # industry standard (inches)

SIZE_PRESETS = {
    "baby":  (30, 36),
    "throw": (50, 60),
    "twin":  (66, 90),
    "queen": (90, 100),
}


# ----------------------------
# Input / navigation helpers
# ----------------------------

def prompt(text: str) -> str:
    """
    Universal input handler.

    Returns:
      '__BACK__' if user types 'b'
      '__QUIT__' if user types 'q'
      otherwise the raw (stripped) input
    """
    ans = input(text).strip()
    low = ans.lower()
    if low == "b":
        return "__BACK__"
    if low == "q":
        return "__QUIT__"
    return ans


# ----------------------------
# Text style helpers
# ----------------------------

def word(term: str) -> str:
    beginner_map = {"DC": "double crochet", "CH": "chain", "SK": "skip", "ST": "stitch"}
    advanced_map = {"DC": "dc", "CH": "ch", "SK": "sk", "ST": "st"}
    return (beginner_map if pattern_style == "beginner" else advanced_map).get(term, term.lower())


# ----------------------------
# Units + size input
# ----------------------------

def to_inches(value: float, unit: str) -> float:
    if unit == "in":
        return value
    if unit == "ft":
        return value * 12
    if unit == "cm":
        return value / 2.54
    if unit == "m":
        return (value * 100) / 2.54
    raise ValueError("Unsupported unit")


def choose_unit():
    print("\nDefault unit is inches (industry standard).")
    print("Type 'b' to go back or 'q' to quit.\n")

    while True:
        raw = prompt("Do you want to change the unit for CUSTOM dimensions? (y/n): ")

        if raw == "__BACK__":
            return "back"
        if raw == "__QUIT__":
            return "quit"

        change = raw.strip().lower()
        if change == "n":
            return DEFAULT_UNIT
        if change == "y":
            break

        print("Please type 'y' or 'n' (or 'b' to go back, 'q' to quit).\n")

    while True:
        raw = prompt("Choose unit (in / ft / cm / m): ")

        if raw == "__BACK__":
            return "back"
        if raw == "__QUIT__":
            return "quit"

        unit = raw.strip().lower()
        if unit in ("in", "ft", "cm", "m"):
            return unit

        print("Please type: in, ft, cm, or m (or 'b' to go back, 'q' to quit).\n")


def parse_dimensions(text: str):
    t = text.lower().strip()
    for sep in ["by", "x", ","]:
        t = t.replace(sep, " ")
    parts = [p for p in t.split() if p]

    if len(parts) != 2:
        return None

    try:
        w = float(parts[0])
        h = float(parts[1])
    except ValueError:
        return None

    if w <= 0 or h <= 0:
        return None

    return w, h


def ask_size_or_custom(unit_for_custom: str):
    print("\nChoose a size preset OR type custom dimensions:")
    print("Presets: baby / throw / twin / queen")
    print('Custom examples: "52x68" or "4x5" (uses your selected unit for custom)')
    print("Type 'b' to go back or 'q' to quit.\n")

    while True:
        raw = prompt("Enter size: ")

        if raw == "__BACK__":
            return "back"
        if raw == "__QUIT__":
            return "quit"

        entry = raw.strip().lower()

        # Preset
        if entry in SIZE_PRESETS:
            w, h = SIZE_PRESETS[entry]
            return float(w), float(h), f"preset ({entry})"

        # Custom dimensions
        dims = parse_dimensions(entry)
        if dims:
            w, h = dims
            w_in = to_inches(w, unit_for_custom)
            h_in = to_inches(h, unit_for_custom)
            return w_in, h_in, f"custom ({unit_for_custom})"

        print('Try "throw" or dimensions like "52x68" (or b/q).\n')


# ----------------------------
# Border selection + geometry
# ----------------------------

def ask_border():
    print("\nBORDER")
    print("------")
    print("Choose a border style:")
    print("  0 = none")
    print("  1 = simple (straight)")
    print("  2 = scallop / shell (rounded)")
    print("  3 = picot (tiny points)")
    print("  4 = ribbed / textured (more yarn)")
    print("  5 = other / custom (describe it)")
    print("Type 'b' to go back or 'q' to quit.\n")

    style_map = {
        "0": ("none",    0.0, 1.00),
        "1": ("simple",  2.0, 1.00),
        "2": ("scallop", 2.5, 1.12),
        "3": ("picot",   1.5, 1.05),
        "4": ("ribbed",  2.5, 1.15),
        "5": ("custom",  2.0, 1.10),
    }

    while True:
        raw = prompt("Choose 0 / 1 / 2 / 3 / 4 / 5: ")

        if raw == "__BACK__":
            return "back"
        if raw == "__QUIT__":
            return "quit"

        choice = raw.strip().lower()
        if choice in style_map:
            break

        print("Please type 0, 1, 2, 3, 4, or 5 (or b/q).\n")

    border_type, default_border_in, yardage_factor = style_map[choice]

    if border_type == "none":
        return {"type": "none", "border_in": 0.0, "yardage_factor": 1.00, "description": ""}

    description = ""
    if border_type == "custom":
        raw = prompt("Describe your border (short): ")

        if raw == "__BACK__":
            return "back"
        if raw == "__QUIT__":
            return "quit"

        description = raw.strip()

    while True:
        raw = prompt(f"Border width in inches (press Enter for {default_border_in:g}): ")

        if raw == "__BACK__":
            return "back"
        if raw == "__QUIT__":
            return "quit"

        custom = raw.strip()
        if custom == "":
            border_in = default_border_in
            break

        try:
            border_in = float(custom)
            if border_in <= 0:
                raise ValueError
            break
        except ValueError:
            print("Please enter a positive number, e.g. 2 or 3.5 (or b/q).\n")

    return {
        "type": border_type,
        "border_in": border_in,
        "yardage_factor": yardage_factor,
        "description": description,
    }


def ask_border_included():
    print("\nFINISHED SIZE QUESTION")
    print("----------------------")
    print("Does your FINISHED size include the border?")
    print("  1 = Yes (the size you entered includes the border)")
    print("  2 = No  (the border will add to the size you entered)")
    print("Type 'b' to go back or 'q' to quit.\n")

    while True:
        raw = prompt("Choose 1 or 2: ")

        if raw == "__BACK__":
            return "back"
        if raw == "__QUIT__":
            return "quit"

        choice = raw.strip()
        if choice == "1":
            return True
        if choice == "2":
            return False

        print("Please type 1 or 2 (or b/q).\n")


def compute_body_size(width_in: float, height_in: float, border: dict, finished_includes_border: bool):
    """
    Returns (body_width_in, body_height_in) or None if border makes body impossible.
    """
    if (not finished_includes_border) or border["type"] == "none":
        return width_in, height_in

    b = border.get("border_in", 0.0)
    body_w = width_in - (2 * b)
    body_h = height_in - (2 * b)

    if body_w <= 0 or body_h <= 0:
        return None

    return body_w, body_h


# ----------------------------
# Yardage + materials
# ----------------------------

def estimate_yardage_range(width_in: float, height_in: float, border: dict, finished_includes_border: bool):
    """
    Rough v1 estimate based on area.
    Uses the include-border choice to decide whether border adds outside the body.
    """
    border_in = border.get("border_in", 0.0)
    factor = border.get("yardage_factor", 1.0)

    if border.get("type") == "none" or border_in <= 0:
        effective_area = width_in * height_in
    else:
        if finished_includes_border:
            body = compute_body_size(width_in, height_in, border, True)
            if body is None:
                return "n/a (border too large)"
            body_w, body_h = body

            finished_area = width_in * height_in
            body_area = body_w * body_h
            border_area = max(finished_area - body_area, 0)
        else:
            body_w, body_h = width_in, height_in
            body_area = body_w * body_h

            finished_w = body_w + 2 * border_in
            finished_h = body_h + 2 * border_in
            finished_area = finished_w * finished_h
            border_area = max(finished_area - body_area, 0)

        effective_area = body_area + (border_area * 0.7 * factor)

    low = int(round((effective_area * 0.35) / 50) * 50)
    high = int(round((effective_area * 0.55) / 50) * 50)
    return f"{max(low,200)}–{max(high,300)} yd"


def print_materials(width_in: float, height_in: float, border: dict, finished_includes_border: bool):
    print("\nMATERIALS")
    print("---------")
    print(f"Finished size entered: {width_in:g} × {height_in:g} in")

    if border["type"] == "none":
        print("Border: none")
        print("Finished size includes border: n/a")
    else:
        line = f"Border: {border['type']} ({border['border_in']:g} in)"
        if border["type"] == "custom" and border.get("description"):
            line += f" — {border['description']}"
        print(line)
        print("Finished size includes border:", "yes" if finished_includes_border else "no")

    body = compute_body_size(width_in, height_in, border, finished_includes_border)
    if body is None:
        print("Body size: n/a (border too large)")
        yardage = "n/a"
    else:
        body_w, body_h = body
        print(f"Body size: {body_w:g} × {body_h:g} in")
        yardage = estimate_yardage_range(width_in, height_in, border, finished_includes_border)

    print(f"Estimated yardage (v1): {yardage}")
    print("Yarn: Worsted weight (#4)")
    print("Hook: 5.0 mm")
    print("Notions: scissors, tapestry needle")
    print("Optional: stitch markers, measuring tape\n")


# ----------------------------
# Confirmation
# ----------------------------

def confirm_selection(unit: str, width_in: float, height_in: float, border: dict, finished_includes_border: bool):
    print("\nCONFIRM SELECTION")
    print("-----------------")
    print(f"Units for custom input: {unit}")
    print(f"Finished size entered: {width_in:g} × {height_in:g} in")

    if border["type"] == "none":
        print("Border: none")
        print("Finished size includes border: n/a")
        body_w, body_h = width_in, height_in
    else:
        line = f"Border: {border['type']} ({border['border_in']:g} in)"
        if border["type"] == "custom" and border.get("description"):
            line += f" — {border['description']}"
        print(line)
        print("Finished size includes border:", "yes" if finished_includes_border else "no")

        body = compute_body_size(width_in, height_in, border, finished_includes_border)
        if body is None:
            print("\n⚠️ That border is too large for the finished size you entered.")
            print("Try a smaller border width or a larger blanket size.\n")
            return False

        body_w, body_h = body

    print(f"Body size (main stitch area): {body_w:g} × {body_h:g} in")
    print("Type 'b' to go back or 'q' to quit.\n")

    while True:
        raw = prompt("Continue? (y/n): ")

        if raw == "__BACK__":
            return "back"
        if raw == "__QUIT__":
            return "quit"

        answer = raw.strip().lower()
        if answer == "y":
            return True
        if answer == "n":
            return False

        print("Please type 'y' or 'n' (or b/q).\n")


# ----------------------------
# Mode A: Recreate from photo (demo for now)
# ----------------------------

def ask_target_square_size_in():
    print("\nGRANNY SQUARE SIZE")
    print("------------------")
    print("Enter square size in inches (e.g., 6, 8, 10)")
    print("Type 'b' to go back or 'q' to quit.\n")

    while True:
        raw = prompt("Size: ")

        if raw == "__BACK__":
            return "back"
        if raw == "__QUIT__":
            return "quit"

        entry = raw.strip()
        try:
            size_in = float(entry)
            if size_in <= 0:
                raise ValueError
            return size_in
        except ValueError:
            print("Please enter a positive number (or b/q).\n")


def estimate_granny_rounds(target_in: float):
    """
    Very rough v1 estimate: classic granny squares grow ~1 inch per round
    after the first couple rounds with worsted yarn.
    We'll clamp to minimum 2 rounds.
    """
    if target_in <= 2:
        return 2
    rounds = int(round(target_in))  # 6 in -> ~6 rounds (rough)
    return max(rounds, 2)


def ask_blanket_size_for_project(unit_for_custom: str):
    print("\nPROJECT: BLANKET SIZE")
    print("---------------------")
    print("Choose the blanket size you want to make with granny squares.")
    print("Presets: baby / throw / twin / queen")
    print('Or type custom dimensions like "50x60" or "4x5" (uses your selected unit)')
    print()
    return ask_size_or_custom(unit_for_custom)  # returns (w_in, h_in, label)


def estimate_square_layout(blanket_w_in: float, blanket_h_in: float, square_in: float):
    """
    Simple v1 grid layout. Ignores join gap. We'll add join allowance later.
    """
    across = max(1, math.ceil(blanket_w_in / square_in))
    down = max(1, math.ceil(blanket_h_in / square_in))
    total = across * down

    est_w = across * square_in
    est_h = down * square_in
    return across, down, total, est_w, est_h


def print_granny_blanket_plan(
    blanket_w_in: float,
    blanket_h_in: float,
    blanket_label: str,
    square_in: float,
    border: dict,
    finished_includes_border: bool,
):
    print("\nPROJECT PLAN: Granny-Square Blanket")
    print("----------------------------------")
    print(f"Blanket size entered: {blanket_w_in:g} × {blanket_h_in:g} in ({blanket_label})")
    print(f"Square size target: ~{square_in:g} in across")

    body = compute_body_size(blanket_w_in, blanket_h_in, border, finished_includes_border)
    if body is None:
        print("⚠️ Border is too large for this blanket size. Try a smaller border or larger size.\n")
        return

    body_w, body_h = body
    print(f"Body size used for square layout: {body_w:g} × {body_h:g} in")

    across, down, total, est_w, est_h = estimate_square_layout(body_w, body_h, square_in)

    print(f"Estimated layout: {across} squares across × {down} squares down = {total} squares")
    print(f"Estimated assembled body size (before joins/border tweaks): ~{est_w:g} × {est_h:g} in")

    if border["type"] == "none":
        print("Border: none\n")
    else:
        line = f"Border: {border['type']} ({border['border_in']:g} in)"
        if border["type"] == "custom" and border.get("description"):
            line += f" — {border['description']}"
        print(line)
        print("Finished size includes border:", "yes" if finished_includes_border else "no")
        print()

    print("Note: This estimate does not include joining gap or blocking.")
    print("      Next upgrade: ask join method and add a join allowance.\n")


def generate_granny_square(style: str, target_size_in: float):
    rounds_est = estimate_granny_rounds(target_size_in)

    print("\nPATTERN: Classic Granny Square")
    print("-----------------------------")
    print(f"Target size: ~{target_size_in:g} in across (estimate: ~{rounds_est} rounds)")

    if style == "beginner":
        print("Materials: Worsted weight (#4) yarn, 5.0 mm hook, scissors, tapestry needle.")
        print("Note: Size is approximate—everyone’s tension is different. Measure as you go.\n")

        print("Round 1:")
        print("  1) Make a magic ring (or chain 4 and slip stitch to form a ring).")
        print("  2) Chain 3 (counts as first double crochet).")
        print("  3) Work 2 double crochet into the ring. Chain 2.")
        print("  4) Work 3 double crochet into the ring. Chain 2.")
        print("  5) Repeat Step 4 two more times (4 clusters total).")
        print("  6) Slip stitch to the top of the starting chain 3 to close.\n")

        print("Round 2:")
        print("  1) Slip stitch into the next corner (chain-2) space.")
        print("  2) In the corner space: chain 3, 2 double crochet, chain 2, 3 double crochet.")
        print("  3) In each remaining corner space: (3 double crochet, chain 2, 3 double crochet).")
        print("  4) Slip stitch to close.\n")

        print("Round 3 and beyond:")
        print("  - Corners: (3 double crochet, chain 2, 3 double crochet)")
        print("  - Sides: 3 double crochet in each space between corner clusters")
        print(f"  - Repeat rounds until your square measures about {target_size_in:g} inches across.")
        print("  - Fasten off and weave in ends.\n")
    else:
        print("Materials: Worsted (#4), 5.0 mm hook.\n")
        print(f"Work until square measures ~{target_size_in:g} in across.\n")
        print("R1: MR, ch 3 (counts as dc), 2 dc, ch 2, *(3 dc, ch 2) 3x, sl st.")
        print("R2: sl st to corner sp, ch 3, 2 dc, ch 2, 3 dc in same sp;")
        print("    *(3 dc, ch 2, 3 dc) in each corner sp; sl st.")
        print("R3+: corners (3 dc, ch 2, 3 dc); sides 3 dc in each sp between clusters.")
        print("FO. Weave in ends.\n")


def run_recreate_from_photo_demo():
    print("\n(Type 'b' at any prompt to go back, 'q' to quit)")
    print("\nRECREATE FROM PHOTO (demo)")
    print("--------------------------")
    print("Pretending the user uploaded a photo...")

    detected_pattern = "granny_square"
    confidence = 0.86
    print(f"Detected: {detected_pattern} (confidence {confidence:.2f})")

    if detected_pattern != "granny_square":
        print("Sorry — this pattern type isn’t supported yet.\n")
        _ = prompt("Press Enter to return to the main menu (or q to quit): ")
        return "quit" if _ == "__QUIT__" else "back"

    square_in = ask_target_square_size_in()
    if square_in in ("back", "quit"):
        return square_in

    unit_for_custom = choose_unit()
    if unit_for_custom in ("back", "quit"):
        return unit_for_custom

    blanket = ask_blanket_size_for_project(unit_for_custom)
    if blanket in ("back", "quit"):
        return blanket
    blanket_w_in, blanket_h_in, blanket_label = blanket

    border = ask_border()
    if border in ("back", "quit"):
        return border

    finished_includes_border = True
    if border["type"] != "none":
        finished_includes_border = ask_border_included()
        if finished_includes_border in ("back", "quit"):
            return finished_includes_border

    generate_granny_square(pattern_style, square_in)
    print_granny_blanket_plan(
        blanket_w_in, blanket_h_in, blanket_label,
        square_in, border, finished_includes_border
    )

    _ = prompt("Press Enter to return to the main menu (or q to quit): ")
    return "quit" if _ == "__QUIT__" else "back"


# ----------------------------
# Mode B: Blanket Builder
# ----------------------------

def print_demo_pattern():
    print("PATTERN (demo)")
    print("--------------")
    for row in range(1, 7):
        if row % 2:
            if pattern_style == "beginner":
                print(f"Row {row}: {word('DC')} in stitches across")
            else:
                print(f"Row {row}: {word('DC')} in sts across")
        else:
            print(f"Row {row}: {word('DC')} in spaces across")
    print()


def run_blanket_builder():
    print("\n(Type 'b' at any prompt to go back, 'q' to quit)")

    unit_for_custom = choose_unit()
    if unit_for_custom in ("back", "quit"):
        return unit_for_custom

    while True:
        result = ask_size_or_custom(unit_for_custom)
        if result in ("back", "quit"):
            return result
        width_in, height_in, size_mode = result

        border = ask_border()
        if border in ("back", "quit"):
            return border

        finished_includes_border = True
        if border["type"] != "none":
            finished_includes_border = ask_border_included()
            if finished_includes_border in ("back", "quit"):
                return finished_includes_border

        ok = confirm_selection(unit_for_custom, width_in, height_in, border, finished_includes_border)
        if ok == "back":
            continue
        if ok == "quit":
            return "quit"
        if ok is True:
            break

        # ok == False means “no, try again”
        print("\nOkay — let’s try again.\n")

    print(f"\nSelected: {size_mode}")
    print_materials(width_in, height_in, border, finished_includes_border)
    print_demo_pattern()

    _ = prompt("Press Enter to return to the main menu (or q to quit): ")
    return "quit" if _ == "__QUIT__" else "back"


# ----------------------------
# Program entry
# ----------------------------

def main():
    print("CraftLogic: Crochet")
    print("-------------------")
    print("Style:", pattern_style)

    while True:
        print("\nMAIN MENU")
        print("---------")
        print("  1 = Recreate from photo")
        print("  2 = Blanket Builder")
        print("  q = Quit")
        print("  (Tip: you can type 'b' inside modes to return here)")

        choice = input("Choose 1, 2, or q: ").strip().lower()
        if choice == "":
            continue

        if choice == "q":
            print("\nGoodbye!")
            break

        if choice == "1":
            result = run_recreate_from_photo_demo()
            if result == "quit":
                print("\nGoodbye!")
                break
            continue

        if choice == "2":
            result = run_blanket_builder()
            if result == "quit":
                print("\nGoodbye!")
                break
            continue

        print("Please type 1, 2, or q.\n")


if __name__ == "__main__":
    main()
