import json
import sys


def rect(props):
    x, y = float(props["x"].removesuffix("cm")), float(props["y"].removesuffix("cm"))
    return x, y, x + float(props["width"].removesuffix("cm")), y + float(props["height"].removesuffix("cm"))


def overlaps(a, b):
    return a[0] < b[2] and b[0] < a[2] and a[1] < b[3] and b[1] < a[3]


def main():
    slides = {}
    for op in json.load(open("ops.json")):
        if op["type"] in ("picture", "shape"):
            slides.setdefault(op["parent"], []).append(op)

    bad = 0
    for parent, ops in slides.items():
        arrows = [op for op in ops if op["type"] == "picture" and op["props"].get("alt") == "Panah"]
        cards = [op for op in ops if op["type"] == "shape" and op["props"].get("name") == "kartu"]
        for arrow in arrows:
            for card in cards:
                if overlaps(rect(arrow["props"]), rect(card["props"])):
                    bad += 1
                    print(f"{parent}: panah {rect(arrow['props'])} menabrak kartu {rect(card['props'])}")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
