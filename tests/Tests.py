from io import BytesIO
import os
import unittest
from PIL import Image
import cv2
from DiabloOcr.DiabloImageReader import DiabloImageReader
from DiabloOcr.DiabloItemParser import DiabloItemParser

class DiabloItemParserIntegrationTest(unittest.TestCase):
    maxDiff = None
    
    def setUp(self):
        self.parser = DiabloItemParser()
        self.fixture_folder = os.path.join(os.path.dirname(__file__), "fixtures")

    def test_parse_test1(self):
        image_path = os.path.join(self.fixture_folder, "test1.png")
        image = cv2.imread(image_path)
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
                ["[VALUE]% Poison Resistance", 24.5]
            ],
            "affixes": [
                ["+[VALUE]% Vulnerable Damage", 23.5],
                ["+[VALUE]% Critical Strike Chance", 3.4],
                ["+[VALUE]% Damage to Stunned Enemies", 19.0],
                ["[VALUE]% Resource Generation", 10.5]
            ],
            "socketCount": 0,
            "requiredLevel": 80,
            "classRequirement": "No Class Requirement",
            "rawText": ""
        }

        item = self.parser.parse(ocr_result)
        print(ocr_result)
        item.raw_text = ''
        self.assertEqual(item.to_object(), expected_result)

    def test_parse_test2(self):
        image_path = os.path.join(self.fixture_folder, "test2.png")
        image = cv2.imread(image_path)
        ocr_result = DiabloImageReader.perform_ocr(image)
        expected_result = {
            "name": "Vicious Omen",
            "power": 764,
            "powerType": "Ancestral",
            "type": "Amulet",
            "dps": 0,
            "armor": 0,
            "implicitAffixes": [
                ['[VALUE]% Resistance to All Elements', 18.1]
            ],
            "affixes": [
                ['+[VALUE] Ranks of the Evulsion Passive', 2.0],
                ['+[VALUE]% Healing Received', 14.0],
                ['+[VALUE]% Damage', 8.0],
                ['[VALUE]% Damage Reduction', 5.5]
            ],
            "socketCount": 0,
            "requiredLevel": 83,
            "classRequirement": "No Class Requirement",
            "rawText": ""
        }

        item = self.parser.parse(ocr_result)
        print(ocr_result)
        item.raw_text = ''
        self.assertEqual(item.to_object(), expected_result)
    
    def test_parse_test3(self):
        image_path = os.path.join(self.fixture_folder, "test3.jpg")
        image = cv2.imread(image_path)
        ocr_result = DiabloImageReader.perform_ocr(image)
        expected_result = {
            "name": "Cleave Impact",
            "power": 765,
            "powerType": "Ancestral",
            "type": "Sword",
            "dps": 1001,
            "armor": 0,
            "implicitAffixes": [
                ["+[VALUE]% Critical Strike Damage", 17.5]
            ],
            "affixes": [
                ['+[VALUE]% Core Skill Damage', 13.0],
                ['+[VALUE]% Vulnerable Damage', 20.5],
                ['+[VALUE]% Critical Strike Damage', 16.0],
                ['+[VALUE]% Overpower Damage', 37.5]
            ],
            "socketCount": 0,
            "requiredLevel": 77,
            "classRequirement": "No Class Requirement",
            "rawText": ""
        }

        item = self.parser.parse(ocr_result)
        item.raw_text = ''
        self.assertEqual(item.to_object(), expected_result)

    def test_parse_test4(self):
        image_path = os.path.join(self.fixture_folder, "test4.png")
        image = cv2.imread(image_path)
        ocr_result = DiabloImageReader.perform_ocr(image)
        expected_result = {
            "name": "Doom Aim",
            "power": 790,
            "powerType": "Ancestral",
            "type": "Sword",
            "dps": 1104,
            "armor": 0,
            "implicitAffixes": [
                ["+[VALUE]% Critical Strike Damage", 17.5],
            ],
            "affixes": [
                ["+[VALUE] Strength", 57],
                ["+[VALUE]% Damage to Crowd Controlled Enemies", 9.5],
                ['+[VALUE]% Critical Strike Damage', 19.5],
                ['+[VALUE]% Vulnerable Damage', 22.5],
            ],
            "socketCount": 1,
            "requiredLevel": 89,
            "classRequirement": "No Class Requirement",
            "rawText": ""
        }

        item = self.parser.parse(ocr_result)
        print(ocr_result)
        item.raw_text = ''
        self.assertEqual(item.to_object(), expected_result)

    def test_parse_test5(self):
        image_path = os.path.join(self.fixture_folder, "test5.png")
        image = cv2.imread(image_path)
        ocr_result = DiabloImageReader.perform_ocr(image)
        expected_result = {
            "name": "Doom Gash",
            "power": 734,
            "powerType": "Ancestral",
            "type": "Sword",
            "dps": 886,
            "armor": 0,
            "implicitAffixes": [
                ["+[VALUE]% Critical Strike Damage", 17.5],
            ],
            "affixes": [
                ['+[VALUE]% Critical Strike Damage', 16.0],
                ['+[VALUE]% Core Skill Damage', 17.5],
                ['+[VALUE]% Damage to Injured Enemies', 30.0],
                ['+[VALUE] All Stats', 26.0]
            ],
            "socketCount": 0,
            "requiredLevel": 98,
            "classRequirement": "No Class Requirement",
            "rawText": ""
        }

        item = self.parser.parse(ocr_result)
        item.raw_text = ''
        self.assertEqual(item.to_object(), expected_result)

    def test_parse_test6(self):
        image_path = os.path.join(self.fixture_folder, "test6.png")
        image = cv2.imread(image_path)
        ocr_result = DiabloImageReader.perform_ocr(image)
        expected_result = {
            "name": "High Council's Tormentor",
            "power": 773,
            "powerType": "Ancestral",
            "type": "Staff",
            "dps": 2066,
            "armor": 0,
            "implicitAffixes": [
                ['+[VALUE]% Damage to Crowd Controlled Enemies', 35.0]
            ],
            "affixes": [
                ['+[VALUE]% Ultimate Skill Damage', 35.0],
                ['+[VALUE]% Core Skill Damage', 26.0],
                ['+[VALUE] Willpower', 102.0],
                ['+[VALUE]% Vulnerable Damage', 46.0]
            ],
            "socketCount": 0,
            "requiredLevel": 91,
            "classRequirement": "No Class Requirement",
            "rawText": ""
        }

        print(ocr_result)

        item = self.parser.parse(ocr_result)
        item.raw_text = ''
        self.assertEqual(item.to_object(), expected_result)

    def test_parse_test7(self):
        image_path = os.path.join(self.fixture_folder, "test7.png")
        image = cv2.imread(image_path)
        ocr_result = DiabloImageReader.perform_ocr(image)
        expected_result = {
            "name": "Radiance Eye",
            "power": 776,
            "powerType": "Ancestral",
            "type": "Ring",
            "dps": 0,
            "armor": 0,
            "implicitAffixes": [
                ['[VALUE]% Lightning Resistance', 24.8],
                ['[VALUE]% Shadow Resistance', 24.8]
            ],
            "affixes": [
                ['+[VALUE]% Critical Strike Chance', 5.0],
                ['+[VALUE]% Critical Strike Damage with Werewolf Skills', 16.0],
                ['+[VALUE]% Critical Strike Damage', 20.0],
                ['+[VALUE] Maximum Life', 408.0],
            ],
            "socketCount": 1,
            "requiredLevel": 100,
            "classRequirement": "No Class Requirement",
            "rawText": ""
        }

        item = self.parser.parse(ocr_result)
        item.raw_text = ''
        self.assertEqual(item.to_object(), expected_result)

    def test_parse_test8(self):
        image_path = os.path.join(self.fixture_folder, "test8.png")
        image = cv2.imread(image_path)
        ocr_result = DiabloImageReader.perform_ocr(image)
        expected_result = {
            "name": "Doom Orders",
            "power": 763,
            "powerType": "Ancestral",
            "type": "Two-Handed Scythe",
            "dps": 1986,
            "armor": 0,
            "implicitAffixes": [
                ['+[VALUE] Life On Kill', 167.0]
            ],
            "affixes": [
                ['+[VALUE] All Stats', 44.0],
                ['+[VALUE]% Core Skill Damage', 37.0],
                ['+[VALUE]% Vulnerable Damage', 43.0],
                ['+[VALUE] Intelligence', 126.0]
            ],
            "socketCount": 0,
            "requiredLevel": 87,
            "classRequirement": "Necromancer",
            "rawText": ""
        }

        item = self.parser.parse(ocr_result)
        # print(item)
        item.raw_text = ''
        self.assertEqual(item.to_object(), expected_result)

    def test_parse_test9(self):
        image_path = os.path.join(self.fixture_folder, "test9.png")
        image = cv2.imread(image_path)
        ocr_result = DiabloImageReader.perform_ocr(image)
        expected_result = {
            "name": "Fiend Armor",
            "power": 784,
            "powerType": "Ancestral",
            "type": "Pants",
            "dps": 0,
            "armor": 784,
            "implicitAffixes": [
                ['While Injured, Your Potion Also Restores [VALUE]% Resource', 20.0]
            ],
            "affixes": [
                ['+[VALUE]% Damage for 4 Seconds After Dodging an Attack', 13.0], 
                ['[VALUE]% Damage Reduction while Injured', 25.5],
                ['[VALUE]% Damage Reduction from Close Enemies', 10.0], 
                ['[VALUE]% Damage Reduction', 6.1]
            ],
            "socketCount": 2,
            "requiredLevel": 86,
            "classRequirement": "No Class Requirement",
            "rawText": ""
        }

        print(ocr_result)

        item = self.parser.parse(ocr_result)
        print(item.to_object())
        item.raw_text = ''
        self.assertEqual(item.to_object(), expected_result)

    def test_parse_test10(self):
        image_path = os.path.join(self.fixture_folder, "test10.png")
        image = cv2.imread(image_path)
        ocr_result = DiabloImageReader.perform_ocr(image)
        expected_result = {
            "name": "Armageddon Chain",
            "power": 788,
            "powerType": "Ancestral",
            "type": "Amulet",
            "dps": 0,
            "armor": 0,
            "implicitAffixes": [
                ['[VALUE]% Resistance to All Elements', 18.5],
            ],
            "affixes": [
                ['[VALUE]% Energy Cost Reduction', 11.0],
                ['+[VALUE]% Movement Speed', 12.5],
                ['+[VALUE]% Crowd Control Duration', 8.5],
                ['+[VALUE] Ranks of the Impetus Passive', 2.0]
            ],
            "socketCount": 1,
            "requiredLevel": 92,
            "classRequirement": "No Class Requirement",
            "rawText": ""
        }

        print(ocr_result)

        item = self.parser.parse(ocr_result)
        item.raw_text = ''
        self.assertEqual(item.to_object(), expected_result)

    def test_parse_test11(self):
        image_path = os.path.join(self.fixture_folder, "test11.png")
        image = cv2.imread(image_path)
        ocr_result = DiabloImageReader.perform_ocr(image)
        expected_result = {
            "name": "Doom Orders",
            "power": 763,
            "powerType": "Ancestral",
            "type": "Two-Handed Scythe",
            "dps": 1986,
            "armor": 0,
            "implicitAffixes": [
                ["+[VALUE]% Critical Strike Damage", 17.5],
            ],
            "affixes": [
                ['+[VALUE]% Critical Strike Damage', 16.0],
                ['+[VALUE]% Core Skill Damage', 17.5],
                ['+[VALUE]% Damage to Injured Enemies', 30.0],
                ['+[VALUE] All Stats', 26.0]
            ],
            "socketCount": 0,
            "requiredLevel": 87,
            "classRequirement": "Necromancer",
            "rawText": ""
        }

        print(ocr_result)

        item = self.parser.parse(ocr_result)
        item.raw_text = ''
        self.assertEqual(item.to_object(), expected_result)

    def test_parse_test12(self):
        image_path = os.path.join(self.fixture_folder, "test12.png")
        image = cv2.imread(image_path)
        ocr_result = DiabloImageReader.perform_ocr(image)
        expected_result = {
            "name": "Doom Orders",
            "power": 763,
            "powerType": "Ancestral",
            "type": "Two-Handed Scythe",
            "dps": 1986,
            "armor": 0,
            "implicitAffixes": [
                ["+[VALUE]% Critical Strike Damage", 17.5],
            ],
            "affixes": [
                ['+[VALUE]% Critical Strike Damage', 16.0],
                ['+[VALUE]% Core Skill Damage', 17.5],
                ['+[VALUE]% Damage to Injured Enemies', 30.0],
                ['+[VALUE] All Stats', 26.0]
            ],
            "socketCount": 0,
            "requiredLevel": 87,
            "classRequirement": "Necromancer",
            "rawText": ""
        }

        print(ocr_result)

        item = self.parser.parse(ocr_result)
        item.raw_text = ''
        self.assertEqual(item.to_object(), expected_result)

    def test_parse_test13(self):
        image_path = os.path.join(self.fixture_folder, "test13.png")
        image = cv2.imread(image_path)
        ocr_result = DiabloImageReader.perform_ocr(image)
        expected_result = {
            "name": "Doom Orders",
            "power": 763,
            "powerType": "Ancestral",
            "type": "Two-Handed Scythe",
            "dps": 1986,
            "armor": 0,
            "implicitAffixes": [
                ["+[VALUE]% Critical Strike Damage", 17.5],
            ],
            "affixes": [
                ['+[VALUE]% Critical Strike Damage', 16.0],
                ['+[VALUE]% Core Skill Damage', 17.5],
                ['+[VALUE]% Damage to Injured Enemies', 30.0],
                ['+[VALUE] All Stats', 26.0]
            ],
            "socketCount": 0,
            "requiredLevel": 87,
            "classRequirement": "Necromancer",
            "rawText": ""
        }

        print(ocr_result)

        item = self.parser.parse(ocr_result)
        item.raw_text = ''
        self.assertEqual(item.to_object(), expected_result)

    def test_parse_test14(self):
        image_path = os.path.join(self.fixture_folder, "test14.jpg")
        image = cv2.imread(image_path)
        ocr_result = DiabloImageReader.perform_ocr(image)
        expected_result = {
            "name": "Doom Orders",
            "power": 763,
            "powerType": "Ancestral",
            "type": "Two-Handed Scythe",
            "dps": 1986,
            "armor": 0,
            "implicitAffixes": [
                ["+[VALUE]% Critical Strike Damage", 17.5],
            ],
            "affixes": [
                ['+[VALUE]% Critical Strike Damage', 16.0],
                ['+[VALUE]% Core Skill Damage', 17.5],
                ['+[VALUE]% Damage to Injured Enemies', 30.0],
                ['+[VALUE] All Stats', 26.0]
            ],
            "socketCount": 0,
            "requiredLevel": 87,
            "classRequirement": "Necromancer",
            "rawText": ""
        }

        print(ocr_result)

        item = self.parser.parse(ocr_result)
        item.raw_text = ''
        self.assertEqual(item.to_object(), expected_result)

    def test_parse_test15(self):
        image_path = os.path.join(self.fixture_folder, "test15.png")
        image = cv2.imread(image_path)
        ocr_result = DiabloImageReader.perform_ocr(image)
        expected_result = {
            "name": "Doom Orders",
            "power": 763,
            "powerType": "Ancestral",
            "type": "Two-Handed Scythe",
            "dps": 1986,
            "armor": 0,
            "implicitAffixes": [
                ["+[VALUE]% Critical Strike Damage", 17.5],
            ],
            "affixes": [
            ],
            "socketCount": 0,
            "requiredLevel": 87,
            "classRequirement": "Necromancer",
            "rawText": ""
        }

        print(ocr_result)

        item = self.parser.parse(ocr_result)
        item.raw_text = ''
        self.assertEqual(item.to_object(), expected_result)

    def test_parse_test16(self):
        image_path = os.path.join(self.fixture_folder, "test16.jpg")
        image = cv2.imread(image_path)
        ocr_result = DiabloImageReader.perform_ocr(image)
        expected_result = {
            "name": "Doom Orders",
            "power": 763,
            "powerType": "Ancestral",
            "type": "Two-Handed Scythe",
            "dps": 1986,
            "armor": 0,
            "implicitAffixes": [
                ["+[VALUE]% Critical Strike Damage", 17.5],
            ],
            "affixes": [
                ['+[VALUE]% Critical Strike Damage', 16.0],
                ['+[VALUE]% Core Skill Damage', 17.5],
                ['+[VALUE]% Damage to Injured Enemies', 30.0],
                ['+[VALUE] All Stats', 26.0]
            ],
            "socketCount": 0,
            "requiredLevel": 87,
            "classRequirement": "Necromancer",
            "rawText": ""
        }

        print(ocr_result)

        item = self.parser.parse(ocr_result)
        item.raw_text = ''
        self.assertEqual(item.to_object(), expected_result)

    def test_parse_test17(self):
        image_path = os.path.join(self.fixture_folder, "test17.png")
        image = cv2.imread(image_path)
        ocr_result = DiabloImageReader.perform_ocr(image)
        expected_result = {
            "name": "Doom Orders",
            "power": 763,
            "powerType": "Ancestral",
            "type": "Two-Handed Scythe",
            "dps": 1986,
            "armor": 0,
            "implicitAffixes": [
                ["+[VALUE]% Critical Strike Damage", 17.5],
            ],
            "affixes": [
                ['+[VALUE]% Critical Strike Damage', 16.0],
                ['+[VALUE]% Core Skill Damage', 17.5],
                ['+[VALUE]% Damage to Injured Enemies', 30.0],
                ['+[VALUE] All Stats', 26.0]
            ],
            "socketCount": 0,
            "requiredLevel": 87,
            "classRequirement": "Necromancer",
            "rawText": ""
        }

        print(ocr_result)

        item = self.parser.parse(ocr_result)
        item.raw_text = ''
        self.assertEqual(item.to_object(), expected_result)

    def test_parse_test18(self):
        image_path = os.path.join(self.fixture_folder, "test18.png")
        image = cv2.imread(image_path)
        ocr_result = DiabloImageReader.perform_ocr(image)
        expected_result = {
            "name": "Doom Orders",
            "power": 763,
            "powerType": "Ancestral",
            "type": "Two-Handed Scythe",
            "dps": 1986,
            "armor": 0,
            "implicitAffixes": [
                ["+[VALUE]% Critical Strike Damage", 17.5],
            ],
            "affixes": [
                ['+[VALUE]% Critical Strike Damage', 16.0],
                ['+[VALUE]% Core Skill Damage', 17.5],
                ['+[VALUE]% Damage to Injured Enemies', 30.0],
                ['+[VALUE] All Stats', 26.0]
            ],
            "socketCount": 0,
            "requiredLevel": 87,
            "classRequirement": "Necromancer",
            "rawText": ""
        }

        print(ocr_result)

        item = self.parser.parse(ocr_result)
        item.raw_text = ''
        self.assertEqual(item.to_object(), expected_result)

if __name__ == "__main__":
    unittest.main()