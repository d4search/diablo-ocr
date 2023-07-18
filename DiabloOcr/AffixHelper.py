import json
import os
import time

def singleton(class_):
    instances = {}

    def wrapper(*args, **kwargs):
        if class_ not in instances:
            instances[class_] = class_(*args, **kwargs)
        return instances[class_]

    return wrapper

@singleton
class AffixHelper:
    affixes = []
    item_types = []
    item_names = []

    def __init__(self):
        self.load_affixes()
        self.load_item_types()
        self.load_item_names()

    def load_affixes(self):
        with open(os.path.join(os.path.dirname(__file__), "data", "affixes.json"), encoding="utf-8") as file:
            data = json.load(file)
            self.affixes = data
    
    def load_item_types(self):
        with open(os.path.join(os.path.dirname(__file__), "data", "itemTypes.json"), encoding="utf-8") as file:
            data = json.load(file)
            self.item_types = data['itemTypes']

    def load_item_names(self):
        with open(os.path.join(os.path.dirname(__file__), "data", "itemNames.json"), encoding="utf-8") as file:
            data = json.load(file)
            self.item_names = data

    def find_closest_affix(self, query):
        closest_affix = None
        closest_distance = float('inf')

        for affix in self.affixes:
            distance = self.levenshtein_distance(affix, query)
            
            if distance < closest_distance:
                closest_affix = affix
                closest_distance = distance

        return closest_affix
    
    def find_closet_item_name(self, item_type, query: str):
        # Split the query into prefix and suffix
        parts = query.strip().split(' ')
        if len(parts) < 2:
            return ' '.join(parts)
        if len(parts) == 3:
            prefix = ' '.join(parts[0:2])
            suffix = parts[2]
        else:
            prefix = parts[0]
            suffix = parts[1]

        item_category = self.item_type_to_category(item_type)
        item_names_prefix = self.item_names['Prefix']['All'] 
        item_names_suffix = self.item_names['Suffix']['All']
        try:
            # Get the list of item names for the given item type
            item_names_prefix += self.item_names['Prefix'][item_category]
        except:
            pass

        try:
            item_names_suffix += self.item_names['Suffix'][item_category]
        except:
            pass

        closest_prefix = min(item_names_prefix, key=lambda name: self.levenshtein_distance(name, prefix))
        closest_suffix = min(item_names_suffix, key=lambda name: self.levenshtein_distance(name, suffix))

        return closest_prefix + ' ' + closest_suffix
    

    def item_type_to_category(self, item_type):
        if 'Sword' in item_type or 'Axe' in item_type:
            return 'SwingBlade'
        if 'Mace' in item_type:
            return 'SwingBlunt'
        if 'Totem' in item_type:
            return 'Offhand_Druid'
        if 'Chest Armor' in item_type:
            return 'Chest'
        if 'Pants' in item_type:
            return 'Leg'
        
        return item_type

    
    def find_closest_item_type(self, query):
        closest_item_type = ''
        closest_distance = float('inf')

        for item_type in self.item_types:
            distance = self.levenshtein_distance(item_type, query)
            
            if distance < closest_distance:
                closest_item_type = item_type
                closest_distance = distance

        return closest_item_type
    
    def levenshtein_distance(self, s1, s2):
        m, n = len(s1), len(s2)

        dp = [[0] * (n + 1) for _ in range(m + 1)]

        for i in range(m + 1):
            dp[i][0] = i
        for j in range(n + 1):
            dp[0][j] = j

        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if s1[i - 1] == s2[j - 1]:
                    dp[i][j] = dp[i - 1][j - 1]
                else:
                    dp[i][j] = min(dp[i - 1][j], dp[i][j - 1], dp[i - 1][j - 1]) + 1

        return dp[m][n]
