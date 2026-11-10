import os
import tempfile
import unittest
import xml.etree.ElementTree as ET
import zipfile

from retarget_group_animations import NS, main, retarget_slide


def slide_xml(proxies):
    shapes = "".join(
        f'<p:sp><p:nvSpPr><p:cNvPr id="{sid}" name="{name}"/><p:cNvSpPr/><p:nvPr/></p:nvSpPr><p:spPr/></p:sp>'
        for name, sid in proxies
    )
    targets = "".join(
        f'<p:animMotion path="M 0 1 L 0 0 E"><p:cBhvr><p:cTn id="{30 + i}" dur="500"/>'
        f'<p:tgtEl><p:spTgt spid="{sid}"/></p:tgtEl></p:cBhvr></p:animMotion>'
        for i, (_, sid) in enumerate(proxies)
    )
    builds = "".join(f'<p:bldP spid="{sid}" grpId="0" build="p"/>' for _, sid in proxies)
    return f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<p:sld xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main"
       xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main">
  <p:cSld><p:spTree>
    <p:grpSp><p:nvGrpSpPr><p:cNvPr id="10" name="#s3-content"/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr><p:grpSpPr/></p:grpSp>
    {shapes}
  </p:spTree></p:cSld>
  <p:timing><p:tnLst><p:par><p:cTn id="1"><p:childTnLst><p:par><p:cTn id="2" start="indefinite">
    <p:childTnLst>{targets}</p:childTnLst>
  </p:cTn></p:par></p:childTnLst></p:cTn></p:par></p:tnLst>
  <p:bldLst>{builds}</p:bldLst></p:timing>
</p:sld>'''.encode()


class RetargetTest(unittest.TestCase):
    def test_target_moves_to_group_and_proxy_is_removed(self):
        out = retarget_slide(slide_xml([("#s3-proxy-content", "20")]))
        root = ET.fromstring(out)
        names = [n.get("name") for n in root.findall(".//p:cNvPr", NS)]
        self.assertIn("#s3-content", names)
        self.assertNotIn("#s3-proxy-content", names)
        self.assertEqual([t.get("spid") for t in root.findall(".//p:spTgt", NS)], ["10"])
        self.assertEqual([b.get("spid") for b in root.findall(".//p:bldP", NS)], ["10"])

    def test_two_proxies_for_one_group_keep_one_build_entry(self):
        out = retarget_slide(slide_xml([("#s3-proxy-content", "20"), ("#s3-proxy-content", "21")]))
        root = ET.fromstring(out)
        self.assertEqual([t.get("spid") for t in root.findall(".//p:spTgt", NS)], ["10", "10"])
        self.assertEqual([b.get("spid") for b in root.findall(".//p:bldP", NS)], ["10"])

    def test_missing_group_is_an_error(self):
        with self.assertRaises(ValueError):
            retarget_slide(slide_xml([("#s3-proxy-sidebar-bg", "20")]))

    def test_namespace_used_by_ignorable_survives(self):
        xml = slide_xml([("#s3-proxy-content", "20")]).replace(
            b'xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"',
            b'xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" '
            b'xmlns:mc="http://schemas.openxmlformats.org/markup-compatibility/2006" '
            b'xmlns:p14="http://schemas.microsoft.com/office/powerpoint/2010/main" '
            b'mc:Ignorable="p14"',
        )
        out = retarget_slide(xml)
        self.assertIn(b'xmlns:p14=', out)
        self.assertIn(b'mc:Ignorable="p14"', out)

    def test_main_rewrites_slide_and_keeps_other_entries(self):
        with tempfile.TemporaryDirectory() as d:
            path = os.path.join(d, "deck.pptx")
            with zipfile.ZipFile(path, "w") as z:
                z.writestr("ppt/slides/slide1.xml", slide_xml([("#s3-proxy-content", "20")]))
                z.writestr("keep.txt", b"keep")
            main(path)
            with zipfile.ZipFile(path) as z:
                self.assertEqual(z.read("keep.txt"), b"keep")
                self.assertNotIn(b"#s3-proxy-content", z.read("ppt/slides/slide1.xml"))


if __name__ == "__main__":
    unittest.main()
