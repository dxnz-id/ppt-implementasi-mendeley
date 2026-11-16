import re
import sys
import zipfile
import xml.etree.ElementTree as ET

P = "http://schemas.openxmlformats.org/presentationml/2006/main"
NS = {"p": P}
ANIM_TAGS = ("anim", "animMotion", "animEffect", "animClr", "animScale", "animRot", "set", "cmd")


def parse(path):
    with zipfile.ZipFile(path) as z:
        names = sorted(
            (n for n in z.namelist() if re.fullmatch(r"ppt/slides/slide\d+\.xml", n)),
            key=lambda n: int(re.search(r"(\d+)", n).group(1)),
        )
        return [ET.fromstring(z.read(n)) for n in names]


def check_slide(index, root):
    bad = []
    if root.find("p:timing", NS) is not None:
        bad.append(f"slide {index}: masih punya timing animasi")
    for tag in ANIM_TAGS:
        if root.findall(f".//p:{tag}", NS):
            bad.append(f"slide {index}: masih ada efek {tag}")
    return bad


def main(path="deck.pptx"):
    roots = parse(path)
    bad = []
    if len(roots) != 16:
        bad.append(f"jumlah slide {len(roots)}, seharusnya 16")
    for i, root in enumerate(roots, 1):
        bad.extend(check_slide(i, root))
    if bad:
        print("\n".join(bad))
        return 1
    print(f"{len(roots)} slide: tidak ada animasi")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else "deck.pptx"))
