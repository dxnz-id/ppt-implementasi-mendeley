import unittest
import xml.etree.ElementTree as ET

from check_anim import HIN, PDOWN, SIN, VIN, _spec, check_slide


def effect_group(
    spid,
    trigger="withEffect",
    path=HIN,
    duration=420,
    accel=20000,
    decel=70000,
    preset_id="26",
    preset_class="path",
    edit="relative",
):
    return f"""
      <p:par><p:cTn fill="hold"><p:stCondLst><p:cond delay="0"/></p:stCondLst>
        <p:childTnLst>
          <p:par><p:cTn presetID="{preset_id}" presetClass="{preset_class}"
              accel="{accel}" decel="{decel}" fill="hold" nodeType="{trigger}">
            <p:stCondLst><p:cond delay="0"/></p:stCondLst>
            <p:childTnLst>
              <p:animMotion path="{path}" pathEditMode="{edit}">
                <p:cBhvr><p:cTn dur="{duration}"/><p:tgtEl><p:spTgt spid="{spid}"/></p:tgtEl></p:cBhvr>
              </p:animMotion>
            </p:childTnLst>
          </p:cTn></p:par>
        </p:childTnLst>
      </p:cTn></p:par>"""


def click_group():
    return """
      <p:par><p:cTn nodeType="clickPar"><p:stCondLst>
        <p:cond evt="onClick" delay="0"><p:tgtEl><p:sldTgt/></p:tgtEl></p:cond>
      </p:stCondLst><p:childTnLst/></p:cTn></p:par>"""


def slide_xml(effects=None, extra_shapes="", extra_top="", build_ids=("100",)):
    effects = effect_group("100", "afterEffect") if effects is None else effects
    builds = "".join(f'<p:bldP spid="{spid}" grpId="0"/>' for spid in build_ids)
    tops = f"""
      <p:par><p:cTn fill="hold"><p:stCondLst><p:cond delay="0"/></p:stCondLst>
        <p:childTnLst>{effects}</p:childTnLst>
      </p:cTn></p:par>{extra_top}"""
    return f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<p:sld xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main">
  <p:cSld><p:spTree>
    <p:grpSp><p:nvGrpSpPr><p:cNvPr id="100" name="#s1-content"/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr><p:grpSpPr/></p:grpSp>
    {extra_shapes}
  </p:spTree></p:cSld>
  <p:timing><p:tnLst><p:par><p:cTn id="1" nodeType="tmRoot"><p:childTnLst>
    <p:seq><p:cTn id="2" nodeType="mainSeq"><p:childTnLst>{tops}</p:childTnLst></p:cTn></p:seq>
  </p:childTnLst></p:cTn></p:par></p:tnLst>
  <p:bldLst>{builds}</p:bldLst></p:timing>
</p:sld>"""


class CheckAnimTest(unittest.TestCase):
    def errors(self, xml):
        return check_slide(1, ET.fromstring(xml))

    def test_valid_slide_1_passes(self):
        self.assertEqual(self.errors(slide_xml()), [])

    def test_wrong_duration_fails(self):
        errors = self.errors(slide_xml(effect_group("100", "afterEffect", duration=500)))
        self.assertTrue(any("durasi" in error for error in errors), errors)

    def test_wrong_easing_fails(self):
        errors = self.errors(slide_xml(effect_group("100", "afterEffect", accel=10000)))
        self.assertTrue(any("easing" in error for error in errors), errors)

    def test_extra_animation_fails(self):
        extra = (
            '<p:sp><p:nvSpPr><p:cNvPr id="101" name="#s1-extra"/><p:cNvSpPr/>'
            "<p:nvPr/></p:nvSpPr><p:spPr/></p:sp>"
        )
        effects = effect_group("100", "afterEffect") + effect_group("101", "withEffect")
        errors = self.errors(
            slide_xml(effects, extra_shapes=extra, build_ids=("100", "101"))
        )
        self.assertTrue(any("tambahan" in error for error in errors), errors)

    def test_extra_click_group_fails(self):
        errors = self.errors(slide_xml(extra_top=click_group()))
        self.assertTrue(any("klik" in error.lower() for error in errors), errors)

    def test_slides_remapped_after_demo_removed(self):
        self.assertEqual(
            [(name, path) for name, path, *_ in _spec(12)],
            [("#s12-content", VIN), ("#s12-rail-pill", PDOWN)],
        )
        self.assertEqual(
            [(name, path) for name, path, *_ in _spec(13)],
            [("#s13-content", HIN)],
        )
        self.assertEqual(
            [(name, path) for name, path, *_ in _spec(14)],
            [
                ("#s14-sidebar-bg", SIN),
                ("#s14-sidebar-fg", SIN),
                ("#s14-rail-pill", SIN),
                ("#s14-content", VIN),
            ],
        )
        self.assertEqual(
            [(name, path) for name, path, *_ in _spec(15)],
            [("#s15-content", HIN)],
        )


if __name__ == "__main__":
    unittest.main()
