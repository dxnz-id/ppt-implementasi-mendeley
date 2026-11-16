import unittest
import xml.etree.ElementTree as ET

from check_no_anim import check_slide


def slide_xml(timing=""):
    return f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<p:sld xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main">
  <p:cSld><p:spTree/></p:cSld>{timing}
</p:sld>"""


class CheckNoAnimTest(unittest.TestCase):
    def errors(self, xml):
        return check_slide(1, ET.fromstring(xml))

    def test_static_slide_passes(self):
        self.assertEqual(self.errors(slide_xml()), [])

    def test_timing_fails(self):
        errors = self.errors(slide_xml("<p:timing/>"))
        self.assertTrue(any("timing" in error for error in errors), errors)

    def test_animation_effect_fails(self):
        errors = self.errors(slide_xml("<p:timing><p:animMotion/></p:timing>"))
        self.assertTrue(any("animMotion" in error for error in errors), errors)


if __name__ == "__main__":
    unittest.main()
