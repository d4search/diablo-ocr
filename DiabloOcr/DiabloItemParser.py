import re
from .AffixHelper import AffixHelper
from .DiabloItem import DiabloItem

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

        item_power = self.extract_power()
        item_power_type = self.extract_power_type()
        item_type = affix_helper.find_closest_item_type(self.extract_type())
        item_name = affix_helper.find_closet_item_name(item_type, self.extract_name())
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
            affix_value = self.extract_affix_value(affix)
            affix = affix.replace(str(affix_value), '[VALUE]')
            found_affix = affix_helper.find_closest_affix(affix)
            affixes[i] = [found_affix, affix_value]

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


    def extract_affix_value(self, text):
        pattern = r'\d+(\.\d+)?'  # Regular expression pattern to match a number
        match = re.search(pattern, text.replace('a 5% Chance', '').replace(' ', ''))
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
            if not formatted_lines and re.search(r'(\+\d|\d+\.\s?\d+\% ?\w)', line) or re.search(r'\ (\+\d|\d+\.\s?\d+\% ?\w)', line):
                start = re.search(r'(\+\d|\d+\.\s?\d+\% ?\w)', line).start()
                formatted_lines.append(line[start:].strip())
            #elif re.search(r'^(\ +)?(\+\d|\d+\.\s?\d+\% ?\w)', line):
            #    formatted_lines.append(line.strip())
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
        clean_line = re.sub(r'[^A-Za-z\s]|[^A-Za-z]{3,}', '', self.text_section1).strip()
        item_name = re.search(r'^([A-Za-z]+){2,}\s([A-Za-z]+){2,}(\n?\s+(?!Rare|Ancestral|Sacred)([A-Za-z]+){2,})?', clean_line, re.MULTILINE)
        try:
            if item_name:
                item_name = item_name.group(0)
                item_name = re.sub(r'\n+', ' ', item_name)
                return item_name.strip().title()
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