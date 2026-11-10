"""Pindahkan animasi proxy ke group dan buang proxy dari deck."""
import re
import sys
import zipfile
import os
import xml.etree.ElementTree as ET
from xml.sax.saxutils import quoteattr

P = "http://schemas.openxmlformats.org/presentationml/2006/main"
A = "http://schemas.openxmlformats.org/drawingml/2006/main"
NS = {"p": P, "a": A}
PROXY = "-proxy-"


def _decls(xml):
    return [
        (prefix, uri)
        for prefix, uri in re.findall(r'xmlns:([A-Za-z_][\w.-]*)="([^"]+)"', xml)
        if prefix != "xml"
    ]


def _register(xml):
    for prefix, uri in _decls(xml):
        ET.register_namespace(prefix, uri)


def _restore_ns(out, decls):
    text = out.decode("utf-8")
    start = text.find("<", text.find("?>") + 2 if "?>" in text else 0)
    end = text.find(">", start)
    add = [f" xmlns:{p}={quoteattr(u)}" for p, u in decls if f"xmlns:{p}=" not in text[start:end]]
    if add:
        text = text[:end] + "".join(add) + text[end:]
    return text.encode("utf-8")


def _name_id(el):
    nv = el.find("p:nvSpPr/p:cNvPr", NS)
    if nv is None:
        nv = el.find("p:nvGrpSpPr/p:cNvPr", NS)
    if nv is None:
        return None, None
    return nv.get("name"), nv.get("id")


def retarget_slide(xml):
    text = xml.decode("utf-8")
    _register(text)
    root = ET.fromstring(xml)
    tree = root.find("p:cSld/p:spTree", NS)
    if tree is None:
        return xml

    groups = {}
    proxies = []
    for el in list(tree):
        if el.tag not in (f"{{{P}}}sp", f"{{{P}}}grpSp"):
            continue
        name, sid = _name_id(el)
        if not name or not sid:
            continue
        if el.tag == f"{{{P}}}grpSp":
            groups[name] = sid
        if PROXY in name:
            proxies.append((el, name, sid))

    if not proxies:
        return xml

    for el, name, sid in proxies:
        target = groups.get(name.replace("-proxy", "", 1))
        if target is None:
            raise ValueError(f"{name}: group tujuan tidak ditemukan")
        for ref in root.iter(f"{{{P}}}spTgt"):
            if ref.get("spid") == sid:
                ref.set("spid", target)
        for ref in root.iter(f"{{{P}}}bldP"):
            if ref.get("spid") == sid:
                ref.set("spid", target)
        tree.remove(el)

    seen = set()
    builds = root.find("p:timing/p:bldLst", NS)
    if builds is not None:
        for bld in list(builds):
            if bld.tag != f"{{{P}}}bldP":
                continue
            sid = bld.get("spid")
            if sid in seen:
                builds.remove(bld)
            else:
                seen.add(sid)
        if not len(builds):
            root.find("p:timing", NS).remove(builds)

    return _restore_ns(ET.tostring(root, encoding="utf-8", xml_declaration=True), _decls(text))


def main(path):
    tmp = path + ".tmp"
    with zipfile.ZipFile(path) as zin, zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED) as zout:
        for item in zin.infolist():
            data = zin.read(item.filename)
            if re.fullmatch(r"ppt/slides/slide\d+\.xml", item.filename):
                data = retarget_slide(data)
            zout.writestr(item, data)
    os.replace(tmp, path)


if __name__ == "__main__":
    main(sys.argv[1])
