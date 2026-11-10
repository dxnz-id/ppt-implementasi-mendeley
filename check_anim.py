import re
import sys
import zipfile
import xml.etree.ElementTree as ET

P = "http://schemas.openxmlformats.org/presentationml/2006/main"
NS = {"p": P}
HIN, HOUT = "M 1 0 L 0 0 E", "M 0 0 L -1 0 E"
VIN, VOUT = "M 0 1 L 0 0 E", "M 0 0 L 0 -1 E"
SIN, SOUT = "M -0.12 0 L 0 0 E", "M 0 0 L -0.12 0 E"
PDOWN = "M 0 -0.1522 L 0 0 E"


def parse(path):
    with zipfile.ZipFile(path) as z:
        names = sorted(
            (n for n in z.namelist() if re.fullmatch(r"ppt/slides/slide\d+\.xml", n)),
            key=lambda n: int(re.search(r"(\d+)", n).group(1)),
        )
        return [ET.fromstring(z.read(n)) for n in names]


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

        motions = []
        for m in root.findall(".//p:animMotion", NS):
            tgt = m.find(".//p:spTgt", NS)
            if tgt is not None:
                motions.append((tgt.get("spid"), m.get("path", "")))
        if not motions:
            bad.append(f"slide {i}: tidak punya motion path")
        for spid, _ in motions:
            if spid not in ids:
                bad.append(f"slide {i}: target animasi spid={spid} tidak ada")
        if root.findall(".//p:animEffect", NS) or root.findall(".//p:anim", NS):
            bad.append(f"slide {i}: ada efek selain motion path")

        def paths(name):
            gid = groups.get(name)
            return [p for sid, p in motions if sid == gid]

        content = paths(f"#s{i}-content")
        if i == 1:
            want = [HOUT]
        elif i in (2, 14):
            want = [HIN, HOUT]
        elif i == 16:
            want = [HIN]
        else:
            want = [VIN, VOUT]
        for p in want:
            if p not in content:
                bad.append(f"slide {i}: content tidak punya {p}")
        if i in (3, 15):
            for tag in ("sidebar-bg", "sidebar-fg"):
                if SIN not in paths(f"#s{i}-{tag}"):
                    bad.append(f"slide {i}: {tag} tidak masuk dari kiri")
        if i in (13, 15):
            for tag in ("sidebar-bg", "sidebar-fg"):
                if SOUT not in paths(f"#s{i}-{tag}"):
                    bad.append(f"slide {i}: {tag} tidak keluar ke kiri")

        pid = next((sid for sid, n in ids.items() if n == f"#s{i}-rail-pill"), None)
        pill = [p for sid, p in motions if sid == pid]
        if i in (3, 15) and SIN not in pill:
            bad.append(f"slide {i}: pill tidak masuk dari kiri")
        if i in (13, 15) and SOUT not in pill:
            bad.append(f"slide {i}: pill tidak keluar ke kiri")
        if i in (5, 8, 13) and PDOWN not in pill:
            bad.append(f"slide {i}: pill tidak bergeser turun")

    if bad:
        print("\n".join(bad))
        return 1
    print(f"{len(roots)} slide: motion path, group, dan urutan target valid")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else "deck.pptx"))
