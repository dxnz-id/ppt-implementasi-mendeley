import re
import sys
import zipfile
import xml.etree.ElementTree as ET
from collections import Counter

P = "http://schemas.openxmlformats.org/presentationml/2006/main"
P14 = "http://schemas.microsoft.com/office/powerpoint/2010/main"
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


def _spec(index):
    """Exact (target name, path, duration, accel, decel) in effect order."""
    content = f"#s{index}-content"
    if index in (1, 2, 14, 16):
        return [(content, HIN, 420, 20, 70)]
    if index in (3, 15):
        return [
            (f"#s{index}-sidebar-bg", SIN, 400, 20, 70),
            (f"#s{index}-sidebar-fg", SIN, 400, 20, 70),
            (f"#s{index}-rail-pill", SIN, 400, 20, 70),
            (content, VIN, 500, 20, 70),
        ]
    if index in (5, 8, 13):
        return [
            (content, VIN, 500, 20, 70),
            (f"#s{index}-rail-pill", PDOWN, 500, 30, 50),
        ]
    return [(content, VIN, 500, 20, 70)]


def _num(value):
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def _ease(value):
    """XML stores easing in 1/1000 percent: 20000 is 20%."""
    number = _num(value)
    return None if number is None else number / 1000


def _effects(top, bad, index, ids):
    effects = []
    groups = top.findall("p:cTn/p:childTnLst/p:par", NS) if top is not None else []
    if not groups:
        bad.append(f"slide {index}: tidak punya motion path")
    for group in groups:
        ctn = next((c for c in group.iter(f"{{{P}}}cTn") if c.get("presetID")), None)
        if ctn is None:
            bad.append(f"slide {index}: grup animasi tanpa efek path")
            continue
        if ctn.get("presetID") != "26" or ctn.get("presetClass") != "path":
            bad.append(
                f"slide {index}: efek bukan path animation "
                f"(presetID={ctn.get('presetID')}, presetClass={ctn.get('presetClass')})"
            )
        child = ctn.find("p:childTnLst", NS)
        moves = child.findall("p:animMotion", NS) if child is not None else []
        other = [e.tag for e in child if e.tag != f"{{{P}}}animMotion"] if child is not None else []
        if len(moves) != 1 or other:
            bad.append(f"slide {index}: satu efek path harus tepat satu p:animMotion")
            if not moves:
                continue
        motion = moves[0]
        if motion.get("pathEditMode") != "relative":
            bad.append(
                f"slide {index}: pathEditMode={motion.get('pathEditMode')}, seharusnya relative"
            )
        target = motion.find(".//p:spTgt", NS)
        spid = target.get("spid") if target is not None else None
        if spid is None or spid not in ids:
            bad.append(f"slide {index}: target animasi spid={spid} tidak ada")
        duration = motion.find("p:cBhvr/p:cTn", NS)
        effects.append(
            {
                "spid": spid,
                "name": ids.get(spid, spid),
                "path": motion.get("path"),
                "dur": duration.get("dur") if duration is not None else None,
                "accel": ctn.get("accel"),
                "decel": ctn.get("decel"),
                "trigger": ctn.get("nodeType"),
            }
        )
    return effects


def _transition_errors(index, root):
    bad = []
    transition = root.find("p:transition", NS)
    if index == 1:
        if transition is not None:
            bad.append("slide 1: tidak boleh punya transisi")
        return bad
    if transition is None:
        return [f"slide {index}: transisi push-left-400 tidak ada"]
    push = transition.find("p:push", NS)
    if push is None or push.get("dir") != "l":
        bad.append(f"slide {index}: transisi bukan push kiri")
    if transition.get(f"{{{P14}}}dur") != "400":
        bad.append(
            f"slide {index}: durasi transisi "
            f"{transition.get(f'{{{P14}}}dur')}, seharusnya 400"
        )
    if transition.get("advTm") is not None:
        bad.append(f"slide {index}: transisi auto-advance, seharusnya klik")
    if transition.get("advClick") in ("0", "false"):
        bad.append(f"slide {index}: klik maju dimatikan")
    extra = [c.tag for c in transition if c.tag != f"{{{P}}}push"]
    if extra:
        bad.append(f"slide {index}: transisi punya efek tambahan")
    return bad


def check_slide(index, root):
    bad = []
    ids = {e.get("id"): e.get("name") for e in root.findall(".//p:cNvPr", NS)}
    groups = {
        e.get("name"): e.get("id")
        for e in root.findall(".//p:grpSp/p:nvGrpSpPr/p:cNvPr", NS)
    }
    names = set(ids.values())
    if any("-proxy-" in (n or "") for n in names):
        bad.append(f"slide {index}: proxy masih ada")
    required = ["content"] + (["sidebar-bg", "sidebar-fg"] if index in (3, 13, 15) else [])
    for tag in required:
        if f"#s{index}-{tag}" not in groups:
            bad.append(f"slide {index}: group #s{index}-{tag} tidak ada")

    bad.extend(_transition_errors(index, root))

    for tag in ("animEffect", "anim", "animClr", "animScale", "animRot", "set", "cmd"):
        if root.findall(f".//p:{tag}", NS):
            bad.append(f"slide {index}: ada efek {tag} selain motion path")

    timing = root.find("p:timing", NS)
    if timing is None:
        bad.append(f"slide {index}: tidak punya timing")
        return bad
    mains = [
        c for c in timing.findall(".//p:cTn", NS) if c.get("nodeType") == "mainSeq"
    ]
    if not mains:
        bad.append(f"slide {index}: mainSeq tidak ada")
        return bad
    if len(mains) != 1:
        bad.append(f"slide {index}: mainSeq {len(mains)}, seharusnya 1")
    main = mains[0]

    tops = main.findall("p:childTnLst/p:par", NS)
    if len(tops) != 1:
        bad.append(f"slide {index}: mainSeq punya {len(tops)} grup klik, seharusnya 1")
    top = tops[0] if tops else None
    if top is not None:
        start = top.find("p:cTn", NS)
        conds = start.findall("p:stCondLst/p:cond", NS) if start is not None else []
        if len(conds) != 1 or conds[0].get("delay") != "0" or conds[0].get("evt"):
            bad.append(f"slide {index}: sequence tidak mulai otomatis (delay 0)")

    clicked = any(
        "click" in (c.get("nodeType") or "").lower()
        or "click" in (c.get("evt") or "").lower()
        for c in timing.findall(".//p:cTn", NS) + timing.findall(".//p:cond", NS)
    )
    if clicked:
        bad.append(f"slide {index}: ada trigger klik; slide harus mulai otomatis")

    effects = _effects(top, bad, index, ids)
    motions = len(timing.findall(".//p:animMotion", NS))
    if motions != len(effects):
        bad.append(f"slide {index}: jumlah animMotion {motions}, terdeteksi {len(effects)}")

    want = _spec(index)
    expected = {name: (name, path, dur, accel, decel) for name, path, dur, accel, decel in want}
    actual = [e["name"] for e in effects]
    counts = Counter(actual)
    for name, count in counts.items():
        if count > 1:
            bad.append(f"slide {index}: animasi {name} muncul {count} kali")
    for name, *_ in want:
        if name not in counts:
            bad.append(f"slide {index}: animasi {name} tidak ada")
    for name in counts:
        if name not in expected:
            bad.append(f"slide {index}: animasi tambahan pada {name}")
    wanted_order = [name for name, *_ in want]
    if Counter(actual) == Counter(wanted_order) and actual != wanted_order:
        bad.append(f"slide {index}: urutan animasi {actual}, seharusnya {wanted_order}")

    for pos, effect in enumerate(effects):
        target = expected.get(effect["name"])
        if target:
            _, path, dur, accel, decel = target
            if effect["path"] != path:
                bad.append(
                    f"slide {index}: {effect['name']} path {effect['path']}, seharusnya {path}"
                )
            if _num(effect["dur"]) != dur:
                bad.append(
                    f"slide {index}: {effect['name']} durasi {effect['dur']} ms, seharusnya {dur} ms"
                )
            ease_in, ease_out = _ease(effect["accel"]), _ease(effect["decel"])
            if ease_in != accel or ease_out != decel:
                easing = (
                    f"{ease_in:g}/{ease_out:g}"
                    if ease_in is not None and ease_out is not None
                    else f"{effect['accel']}/{effect['decel']}"
                )
                bad.append(
                    f"slide {index}: {effect['name']} easing {easing}, seharusnya {accel}/{decel}"
                )
        if pos == 0:
            if effect["trigger"] != "afterEffect":
                bad.append(
                    f"slide {index}: efek pertama harus afterEffect (start otomatis), "
                    f"bukan {effect['trigger'] or 'tanpa nodeType'}"
                )
        elif effect["trigger"] != "withEffect":
            bad.append(
                f"slide {index}: {effect['name']} harus withEffect, "
                f"bukan {effect['trigger'] or 'tanpa nodeType'}"
            )

    builds = [b.get("spid") for b in timing.findall("p:bldLst/p:bldP", NS)]
    targets = [e["spid"] for e in effects]
    if Counter(builds) != Counter(targets):
        bad.append(f"slide {index}: bldLst {builds} tidak cocok dengan target animasi {targets}")

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
    print(f"{len(roots)} slide: satu klik, transisi, easing, arah, dan urutan animasi valid")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else "deck.pptx"))
