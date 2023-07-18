import json
import os
import re

class AttributeDescriptionsReader:
    def __init__(self):
        self.file_path = os.path.dirname(__file__) +  "/data/AttributeDescriptions.stl.json"

    def read_attributes(self):
        with open(self.file_path, "r") as file:
            data = json.load(file)
            ar_strings = data["arStrings"]
            attribute_objects = []

            for string in ar_strings:
                sz_text = string["szText"]
                name = sz_text
                precision = "*100|1%|" in name.replace(' ', '')
                clean_name = re.sub(r'{[/]?c[_:]?(label|[A-F0-9]+)?}', '', name)

                if re.match(r'^\(.+ Only\)$', name):
                    continue

                attribute = {
                    "name": name,
                    "cleanName": clean_name,
                    "precision": precision
                }

                attribute_objects.append(attribute)

            return attribute_objects

    def save_to_json(self, attribute_objects):
        output = {"attributes": attribute_objects}
        with open("Attributes.json", "w") as file:
            json.dump(output, file, indent=4)

class RareNameStringsReader:
    def __init__(self):
        self.directory = os.path.dirname(__file__) + "/data/"
        self.file_pattern = "RareNameStrings_{}{}"

    def read_files(self):
        data_structure = {'Prefix': {}, 'Suffix': {}}
        item_types = set()
        matching_files = []

        for i in ["Prefix", "Suffix"]:
            for x in ["_Armor", "_Weapon", ""]:
                file_name = self.file_pattern.format(i, x)
                files = os.listdir(self.directory)
                for file in files:
                    if file.startswith(file_name) and file not in matching_files:
                        item_type = file.replace(file_name + '_', '').replace('.stl.json', '')
                        if item_type == file_name:
                            item_type = 'All'
                        
                        matching_files.append(file)

                        if os.path.isfile(self.directory + file):
                            with open(self.directory + file, "r") as file:
                                data = json.load(file)
                                ar_strings = data["arStrings"]

                                for string in ar_strings:
                                    sz_text = string["szText"]
                                    if item_type not in data_structure[i]:
                                        data_structure[i][item_type] = []

                                    if sz_text not in data_structure[i][item_type]:
                                        data_structure[i][item_type].append(sz_text)

        return data_structure
    
    def save_to_json(self, name_object):
        with open("Names.json", "w") as file:
            json.dump(name_object, file, indent=4)

# Example usage
reader = RareNameStringsReader()
data_structure = reader.read_files()
reader.save_to_json(data_structure)

# Example usage
reader = AttributeDescriptionsReader()
attributes = reader.read_attributes()
reader.save_to_json(attributes)
