import unittest
import xml.etree.ElementTree as ET

from check_anim import HIN, check_slide

P14 = "http://schemas.microsoft.com/office/powerpoint/2010/main"


def transition_xml(direction="l", duration=400, attrs=""):
    return (
        f'<p:transition xmlns:p14="{P14}" p14:dur="{duration}"{attrs}>'
        f'<p:push dir="{direction}"/></p:transition>'
    )


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


def slide_xml(effects=None, extra_shapes="", extra_top="", build_ids=("100",),
              index=1, path=HIN, duration=420, transition=""):
    effects = (
        effect_group("100", "afterEffect", path=path, duration=duration)
        if effects is None else effects
    )
    builds = "".join(f'<p:bldP spid="{spid}" grpId="0"/>' for spid in build_ids)
    tops = f"""
      <p:par><p:cTn fill="hold"><p:stCondLst><p:cond delay="0"/></p:stCondLst>
        <p:childTnLst>{effects}</p:childTnLst>
      </p:cTn></p:par>{extra_top}"""
    return f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<p:sld xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main">
  <p:cSld><p:spTree>
    <p:grpSp><p:nvGrpSpPr><p:cNvPr id="100" name="#s{index}-content"/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr><p:grpSpPr/></p:grpSp>
    {extra_shapes}
  </p:spTree></p:cSld>{transition}
  <p:timing><p:tnLst><p:par><p:cTn id="1" nodeType="tmRoot"><p:childTnLst>
    <p:seq><p:cTn id="2" nodeType="mainSeq"><p:childTnLst>{tops}</p:childTnLst></p:cTn></p:seq>
  </p:childTnLst></p:cTn></p:par></p:tnLst>
  <p:bldLst>{builds}</p:bldLst></p:timing></p:sld>"""


class CheckAnimTest(unittest.TestCase):
    def errors(self, xml, index=1):
        return check_slide(index, ET.fromstring(xml))

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

    def test_valid_slide_2_push_transition_passes(self):
        xml = slide_xml(index=2, path=HIN, duration=420, transition=transition_xml())
        self.assertEqual(self.errors(xml, index=2), [])

    def test_missing_transition_on_slide_2_fails(self):
        xml = slide_xml(index=2, path=HIN, duration=420)
        errors = self.errors(xml, index=2)
        self.assertTrue(any("transisi" in e for e in errors), errors)

    def test_wrong_transition_direction_fails(self):
        xml = slide_xml(index=2, path=HIN, duration=420,
                        transition=transition_xml(direction="r"))
        errors = self.errors(xml, index=2)
        self.assertTrue(any("push kiri" in e for e in errors), errors)

    def test_wrong_transition_duration_fails(self):
        xml = slide_xml(index=2, path=HIN, duration=420,
                        transition=transition_xml(duration=500))
        errors = self.errors(xml, index=2)
        self.assertTrue(any("durasi transisi" in e for e in errors), errors)

    def test_auto_advance_transition_fails(self):
        xml = slide_xml(index=2, path=HIN, duration=420,
                        transition=transition_xml(attrs=' advTm="2000"'))
        errors = self.errors(xml, index=2)
        self.assertTrue(any("auto-advance" in e for e in errors), errors)

    def test_click_disabled_transition_fails(self):
        xml = slide_xml(index=2, path=HIN, duration=420,
                        transition=transition_xml(attrs=' advClick="0"'))
        errors = self.errors(xml, index=2)
        self.assertTrue(any("klik" in e for e in errors), errors)

    def test_transition_on_slide_1_fails(self):
        xml = slide_xml(transition=transition_xml())
        errors = self.errors(xml)
        self.assertTrue(any("slide 1" in e for e in errors), errors)


if __name__ == "__main__":
    unittest.main()
