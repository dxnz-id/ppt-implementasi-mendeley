import re
import sys
import zipfile
import xml.etree.ElementTree as ET

P = "http://schemas.openxmlformats.org/presentationml/2006/main"
NS = {"p": P}
HIN = "M 1 0 L -0.015 0 L 0 0 E"
VIN = "M 0 1 L 0 -0.015 L 0 0 E"
SIN = "M -0.12 0 L 0.003 0 L 0 0 E"
PDOWN = "M 0 -0.1522 L 0 0.004 L 0 0 E"


def parse(path):
    with zipfile.ZipFile(path) as z:
        names = sorted(
            (n for n in z.namelist() if re.fullmatch(r"ppt/slides/slide\d+\.xml", n)),
            key=lambda n: int(re.search(r"(\d+)", n).group(1)),
        )
        return [ET.fromstring(z.read(n)) for n in names]


def motions(root):
    """Return (spid, path, effect cTn) for every animated shape."""
    found = []
    for ctn in root.findall(".//p:cTn", NS):
        if not ctn.get("presetID"):
            continue
        for motion in ctn.findall(".//p:animMotion", NS):
            target = motion.find(".//p:spTgt", NS)
            if target is not None:
                found.append((target.get("spid"), motion.get("path", ""), ctn))
    return found


def main(path="deck.pptx"):
    roots = parse(path)
    bad = []
    if len(roots) != 16:
        bad.append(f"jumlah slide {len(roots)}, seharusnya 16")
    for i, root in enumerate(roots, 1):
        ids = {e.get("id"): e.get("name") for e in root.findall(".//p:cNvPr", NS)}
        groups = {e.get("name"): e.get("id") for e in root.findall(".//p:grpSp/p:nvGrpSpPr/p:cNvPr", NS)}
        names = set(ids.values())
        if any("-proxy-" in (n or "") for n in names):
            bad.append(f"slide {i}: proxy masih ada")
        if f"#s{i}-content" not in groups:
            bad.append(f"slide {i}: group #s{i}-content tidak ada")
        if i in (3, 13, 15):
            for tag in ("sidebar-bg", "sidebar-fg"):
                if f"#s{i}-{tag}" not in groups:
                    bad.append(f"slide {i}: group #s{i}-{tag} tidak ada")

        fx = motions(root)
        if not fx:
            bad.append(f"slide {i}: tidak punya motion path")
        for spid, _, ctn in fx:
            if spid not in ids:
                bad.append(f"slide {i}: target animasi spid={spid} tidak ada")
            if ctn.get("nodeType") == "clickEffect":
                bad.append(f"slide {i}: masih ada efek klik; satu slide harus satu klik")
            for attr in ("accel", "decel"):
                value = ctn.get(attr)
                if not value or int(value) <= 0:
                    bad.append(f"slide {i}: {ids.get(spid, spid)} tidak punya {attr}")

        if root.findall(".//p:animEffect", NS) or root.findall(".//p:anim", NS):
            bad.append(f"slide {i}: ada efek selain motion path")

        def paths(name):
            gid = groups.get(name)
            return [(p, ctn) for sid, p, ctn in fx if sid == gid]

        content = paths(f"#s{i}-content")
        want = HIN if i in (1, 2, 14, 16) else VIN
        if not any(p == want for p, _ in content):
            bad.append(f"slide {i}: content tidak punya {want}")
        if i in (3, 15):
            for tag in ("sidebar-bg", "sidebar-fg"):
                if not any(p == SIN for p, _ in paths(f"#s{i}-{tag}")):
                    bad.append(f"slide {i}: {tag} tidak masuk dari kiri")
        if i in (3, 15):
            if not any(p == VIN and ctn.get("nodeType") == "withEffect" for p, ctn in content):
                bad.append(f"slide {i}: content tidak masuk bersama sidebar")

        pid = next((sid for sid, n in ids.items() if n == f"#s{i}-rail-pill"), None)
        pill = [(p, ctn) for sid, p, ctn in fx if sid == pid]
        if i in (3, 15) and not any(p == SIN for p, _ in pill):
            bad.append(f"slide {i}: pill tidak masuk dari kiri")
        if i in (5, 8, 13):
            if not any(p == PDOWN for p, _ in pill):
                bad.append(f"slide {i}: pill tidak bergeser turun")
            if not any(p == PDOWN and ctn.get("nodeType") == "withEffect" for p, ctn in pill):
                bad.append(f"slide {i}: pill bergeser setelah konten, bukan bersamanya")

    if bad:
        print("\n".join(bad))
        return 1
    print(f"{len(roots)} slide: satu klik, easing, arah, dan urutan animasi valid")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else "deck.pptx"))
