import pytesseract
import re
import json
from PIL import ImageOps
from PIL import ImageEnhance
from AffixHelper import AffixHelper

class DiabloItemParser:
    def __init__(self, text=None):
        self.text = text
        if self.text:
            self.text_section1, self.text_section2, self.text_section3 = self.split_string_sections(self.text)

    def parse(self, text=None):
        if text:
            self.text = text
            self.text_section1, self.text_section2, self.text_section3 = self.split_string_sections(self.text)
        affix_helper = AffixHelper()

        item_name = self.extract_name()
        item_power = self.extract_power()
        item_power_type = self.extract_power_type()
        item_type = affix_helper.find_closest_item_type(self.extract_type())
        dps = self.extract_dps()
        armor = self.extract_armor()
        affixes = self.extract_affixes()

        if item_type in ["Pants", "Boots", "Amulet"]:
            implict_affixes_count = 1
        elif item_type in ["Ring"]:
            implict_affixes_count = 2
        elif dps != 0:
            implict_affixes_count = 1
        else:
            implict_affixes_count = 0

        for i, affix in enumerate(affixes):
            found_affix = affix_helper.find_closest_affix(affix)
            affix_value = self.extract_affix_value(affix)
            affixes[i] = [found_affix['name'], affix_value]

        implicit_affixes = affixes[0:implict_affixes_count]
        affixes = affixes[implict_affixes_count:]

        socket_count = self.extract_socket_count()
        required_level = self.extract_level_requirement()
        item_class_requirement = self.extract_class_requirement()

        diablo_item = DiabloItem(
            name=item_name,
            power=item_power,
            power_type=item_power_type,
            type=item_type,
            dps=dps,
            armor=armor,
            implicit_affixes=implicit_affixes,
            affixes=affixes,
            socket_count=socket_count,
            required_level=required_level,
            class_requirement=item_class_requirement,
            raw_text = [self.text, self.text_section1, self.text_section2, self.text_section3]
        )
        
        return diablo_item


    def split_string_sections(self, text):
        # Pattern to match the end of the first section
        pattern_section1 = r"\d+\s+Armor|Attacks per Second"

        # Pattern to match the end of the second section
        pattern_section2 = r"Properties lost"

        # Pattern to match the start of the third section
        pattern_section3 = r"Requires Level"

        # Pattern to match when first section fails (amulet, ring)
        pattern_section4 = r"Item Power"

        # Find the end index of the first section
        match_section1 = re.search(pattern_section1, text)
        end_index_section1 = match_section1.end() if match_section1 else None

        if end_index_section1 == None:
            match_section1 = re.search(pattern_section4, text)
            end_index_section1 = match_section1.end() if match_section1 else None 

        # Find the end index of the second section
        match_section2 = re.search(pattern_section2, text)
        end_index_section2 = match_section2.end() if match_section2 else None

        if end_index_section2 == None:
            match_section2 = re.search(pattern_section3, text)
            end_index_section2 = match_section2.start() if match_section2 else None            

        # Find the start index of the third section
        match_section3 = re.search(pattern_section3, text)
        start_index_section3 = match_section3.start() if match_section3 else None

        # Extract the three sections based on the found indices
        section1 = text[:end_index_section1].strip() if end_index_section1 else ''
        section2 = text[end_index_section1:end_index_section2].strip() if end_index_section2 else ''
        section3 = text[start_index_section3:].strip() if start_index_section3 else ''

        return section1, section2, section3

    def extract_affixes_old(self, dps, armor):
        #pattern = r'Lucky Hit(.+)|While Injured(.+)|[^\s]\+*\d+\.*\d*%*.*\s*\W*\[\d+\.*\d*\s*((=|-)\s*\d+\.*\d*)?(\)|\]|1)%*(?:\W*\(*\d*\.\d*%*\))?'
        pattern = r'Lucky Hit(.+)\s(.+)|While Injured(.+)\s(.+)|\+?\d+\.?\d?\%?.+\s.+'
        matches = re.finditer(pattern, self.text_section2, re.MULTILINE)
        affixes = []

        def replace_percentage(string):
            result = re.sub(r'(?<=\d)\d\%', ']%', string)
            return result

        def remove_after_first(text):
            index = text.find(']%')
            offset = 1
            if index == -1:
                index = text.find(']')
                offset = 0
            if index != -1:
                text = text[:index+1+offset]
            return text

        for _, match in enumerate(matches, start=1):
            cleaner_affix = replace_percentage(match.group().replace('\n', ' ').replace('  ', ' ').replace('=', '-').replace(' |', ''))
            affix = re.sub(r'\s*\(\+*\d+\.\d+%\)$', '', cleaner_affix)
            affixes.append(remove_after_first(affix))

        return affixes

    def extract_affix_value(self, text):
        pattern = r'\d+(\.\d+)?'  # Regular expression pattern to match a number
        match = re.search(pattern, text)
        if match:
            return float(match.group())  # Convert the matched string to a float
        else:
            return 0  # Return None if no number is found
    
    def extract_affixes(self):
        lines = self.text_section2.split("\n")

        formatted_lines = []

        for line in lines:
            if not line:
                continue  # Skip empty lines
            elif re.search(r'^(\ +)?\S\ +(\+\d|\d+\.\d+\% \w)', line):
                start = re.search(r'(\+\d|\d+\.\d+\% \w)', line).start()
                formatted_lines.append(line[start:].strip())
            elif re.search(r'^(\ +)?(\+\d|\d+\.\d+\% \w)', line):
                formatted_lines.append(line.strip())
            elif re.search(r'\s?While', line):
                formatted_lines.append(line.strip())
            elif re.search(r'\s?Evade', line):
                formatted_lines.append(line.strip())
            elif re.search(r'\s?Lucky Hit', line):
                formatted_lines.append(line.strip())
            elif re.search(r'\s?Properties', line):
                break
            elif formatted_lines:
                formatted_lines[-1] = formatted_lines[-1] + " " + line
                # formatted_lines.append(line.strip())

        for i, line in enumerate(formatted_lines):
            index = line.find(' [')
            if index == -1:
                index = line.find(' +[')
            if index == -1:
                continue
            formatted_lines[i] = line[:index].strip()

        return formatted_lines

    def extract_name(self):
        item_name = re.search(r'^([A-Z]+)\s([A-Z]+)', re.sub(r'[^A-Z\s]', '', self.text_section1.replace('e', 'O')), re.MULTILINE)
        try:
            if item_name:
                item_name = item_name.group(0)
                return item_name.title()
        except:
            pass

        return ''

    def extract_power_type(self):
        if 'Ancestral Rare' in self.text_section1:
            return 'Ancestral'
        elif 'Sacred Rare' in self.text_section1:
            return 'Sacred'
        else:
            return 'Rare'

    def extract_type(self):
        try:
            item_type = re.findall(r'(?:Ancestral|Sacred)*( *Rare )(((([A-Za-z]|\-|\s)*))+)', self.text_section1)
            if item_type:
                item_type = item_type[0][1]
                return item_type.strip().replace('\n', ' ')
        except:
            pass

        return ''

    def extract_power(self):
        try:
            pattern = r'\d+(?: Item Power)'
            item_power = re.search(pattern, self.text_section1, re.MULTILINE)
            if item_power:
                item_power = item_power.group(0)
                return int(item_power.replace(' Item Power', ''))
        except:
            pass
        return 0

    def extract_dps(self):
        try:
            pattern = r'\d+(?: Damage Per Second)'
            dps = re.search(pattern, self.text_section1.replace(',', ''), re.MULTILINE)
            if dps:
                dps = dps.group(0)
                return int(dps.replace(' Damage Per Second', ''))
        
        except:
            pass
        return 0

    def extract_armor(self):
        try:
            pattern = r'\d+(?: Armor)'
            armor = re.search(pattern, self.text_section1.replace(',', ''), re.MULTILINE)
            if armor:
                armor = armor.group(0)
                return int(armor.replace(' Armor', ''))
        except:
            pass
        return 0

    def extract_level_requirement(self):
        try:
            pattern = r'(?:Requires Level )\d+'
            match = re.findall(pattern, self.text_section3, re.MULTILINE)

            return int(match[0].replace('Requires Level ', ''))
        except:
            pass

    def extract_socket_count(self):
        socket_count = self.text_section2.count('Empty Socket')
        return socket_count

    def extract_class_requirement(self):
        if 'Barbarian' in self.text_section3:
            return 'Barbarian'
        elif 'Druid' in self.text_section3:
            return 'Druid'
        elif 'Sorcerer' in self.text_section3:
            return 'Sorcerer'
        elif 'Rogue' in self.text_section3:
            return 'Rogue'
        elif 'Necromancer' in self.text_section3:
            return 'Necromancer'
        else:
            return 'No Class Requirement'


class DiabloItem:
    def __init__(self, name, power, power_type, type, dps, armor, implicit_affixes, affixes, socket_count, required_level, class_requirement, raw_text):
        self.name = name
        self.power = power
        self.power_type = power_type
        self.type = type
        self.dps = dps
        self.armor = armor
        self.implicit_affixes = implicit_affixes
        self.affixes = affixes
        self.socket_count = socket_count
        self.required_level = required_level
        self.class_requirement = class_requirement
        self.raw_text = raw_text

    def __str__(self):
        implicit_affixes = '\n'.join(self.implicit_affixes) if self.implicit_affixes else ''
        affixes = '\n'.join(self.affixes)
        dps_or_armor = f'\n{self.armor} Armor' if self.armor else f'\n{self.dps} Damage Per Second' if self.dps else ''
        newline_before_implicit_affixes = '\n' if implicit_affixes else ''
        socket_text = f'{self.socket_count} Empty Sockets\n' if self.socket_count else ''
        class_requirement = f'\n{self.class_requirement}' if self.class_requirement != 'No Class Requirement' else ''
        return f"{self.name}\n{self.power} {self.power_type} {self.type}{dps_or_armor}{newline_before_implicit_affixes}{implicit_affixes}\n{affixes}\n{socket_text}Requires Level {self.required_level}{class_requirement}"
    
    def to_object(self):
        return {
            'name': self.name,
            'power': self.power,
            'powerType': self.power_type,
            'type': self.type,
            'dps': self.dps,
            'armor': self.armor,
            'implicitAffixes': self.implicit_affixes,
            'affixes': self.affixes,
            'socketCount': self.socket_count,
            'requiredLevel': self.required_level,
            'classRequirement': self.class_requirement,
            'rawText': self.raw_text
        }

    def to_json(self):
        return json.dumps(self.to_object())


class DiabloImageReader:
    @staticmethod
    def optimize_image_for_tesseract(image):
        # Resize the image if needed (optional)
        max_size = 3000
        if max(image.size) > max_size:
            image.thumbnail((max_size, max_size))

        # Convert to grayscale
        image = image.convert('L')
        
        # Apply image enhancement
        enhancer = ImageEnhance.Contrast(image)
        image = enhancer.enhance(2.0)


        image = ImageOps.invert(image)
        image = image.point(lambda pixel: 0 if pixel < 128 else 255 if pixel > 200 else 0)
       
        return image

    @staticmethod
    def perform_ocr(image):
        image = DiabloImageReader.optimize_image_for_tesseract(image)
        ocr_text = pytesseract.image_to_string(image)
        return DiabloImageReader.replace_special_characters(ocr_text)

    @staticmethod
    def replace_special_characters(text):
        pattern = r'[^0-9a-zA-Z\+\[\]\(\)%\. \n-]+'
        return re.sub(pattern, '', text.replace('®', 'O').replace('@', 'O').replace('£', 'E').replace('(', '[').replace(')', ']'))