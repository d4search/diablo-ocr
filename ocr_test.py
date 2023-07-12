import unittest
from PIL import Image
from OCR import DiabloImageReader, DiabloItemParser

class DiabloItemParserIntegrationTest(unittest.TestCase):
    def setUp(self):
        self.parser = DiabloItemParser()
        self.fixture_folder = "fixtures/"

    def test_parse_test1(self):
        image_path = self.fixture_folder + "test1.png"
        image = Image.open(image_path)
        ocr_result = DiabloImageReader.perform_ocr(image)
        expected_result = {
            "name": "Cycle Vow",
            "power": 766,
            "powerType": "Ancestral",
            "type": "Ring",
            "dps": 0,
            "armor": 0,
            "implicitAffixes": [
                ["[VALUE]% Shadow Resistance", 24.5],

            ],
            "affixes": [
                ["+[VALUE]% Vulnerable Damage", 23.5],
                ["+[VALUE]% Critical Strike Chance", 3.4],
                ["+[VALUE]% Damage to Stun Enemies", 190.0],
                ["[VALUE]% Resource Generation", 10.5]
            ],
            "socketCount": 0,
            "requiredLevel": 80,
            "classRequirement": "No Class Requirement",
            "rawText": ""
        }

        print(ocr_result)

        item = self.parser.parse(ocr_result)
        item.raw_text = ''
        self.assertEqual(item.to_object(), expected_result)

if __name__ == "__main__":
    unittest.main()