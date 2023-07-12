import json

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