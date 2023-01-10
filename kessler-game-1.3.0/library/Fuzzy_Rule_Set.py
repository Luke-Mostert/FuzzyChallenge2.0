import numpy as np
import matplotlib.pyplot as plt
import Fuzzy_Rules


class FuzzyRuleSet:
    def __init__(self, rules=[]):
        self.rules = rules

    def AddRule(self, toAdd):
        self.rules.append(toAdd)

    def PrintRules(self):
        for i in range(len(self.rules)):
            self.rules[i].PrintRule()
