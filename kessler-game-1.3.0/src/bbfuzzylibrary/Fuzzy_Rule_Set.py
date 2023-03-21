import numpy as np
import matplotlib.pyplot as plt
import Fuzzy_Rules
import re

class FuzzyRuleSet:
    def __init__(self, rules=[]):
        self.rules = rules

    def AddRule(self, toAdd):
        self.rules.append(toAdd)

    def UpdateOutput(self, newOutput):
        for i in range(len(self.rules)):
            self.rules[i].output = newOutput[i]
            self.rules[i].rule = re.sub("[+-]?\d+\.\d+", str(newOutput[i]), self.rules[i].rule)


    def PrintRules(self):
        for i in range(len(self.rules)):
            self.rules[i].PrintRule()
