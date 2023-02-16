import random

import numpy as np


class FuzzyRules:
    def __init__(self, rule):
        self.rule = rule


class MamdaniFuzzyRules(FuzzyRules):
    def __init__(self, rule):
        super().__init__(self, rule)


class TSKFuzzyRules(FuzzyRules):
    def __init__(self, rule):
        self.rule = rule
        self.output = 1
        self.variableName = []
        self.antecedents = []
        self.SplitRule()

    def PrintRule(self):
        print("The rule is: " + self.rule + "\n")
        print("With an output value of: " + str(self.output) + "\n")
        print("It belongs to the variable: " + str(self.variableName) + "\n")
        print("These are the antecedents: ", end="")
        for i in range(len(self.antecedents)):
            if i == len(self.antecedents) - 1:
                print(str(self.antecedents[i]) + ".")
            else:
                print(str(self.antecedents[i]) + ", ", end="")

    def SplitRule(self):
        temp = self.rule.split()
        self.variableName = []
        for i in range(len(temp)):
            if temp[i] == "If" or temp[i] == "if" or temp[i] == "and" or temp[i] == "or":
                self.variableName.append(temp[i + 1])
                i += 1
            elif temp[i] == "is":
                self.antecedents.append(temp[i + 1])
                i += 1
            elif temp[i] == "then":
                self.output = float(temp[i + 1])
                i += 1


def ImportFile(fileName):
    ruleset = []
    with open("../rulesets/" + fileName) as f:
        lines = f.read().splitlines()
    for i in range(len(lines)):
        ruleset.append(TSKFuzzyRules(lines[i]))
    return ruleset

#class FuzzyRuleExport:

    #def __init__(self):
        #pass


def GetKey(dict, n=0):
    if n < 0:
        n += len(dict)
    for i, key in enumerate(dict.keys()):
        if i == n:
            return key


def CreateRule(ruleDict):
    firstAntecedent = GetKey(ruleDict, 0)
    secondAntecedent = GetKey(ruleDict, 1)
    thirdAntecedent = GetKey(ruleDict, 2)
    file = open("../rulesets/rules.txt", "w")
    for i in range(3):
        for j in range(3):
            for k in range(3):
                    file.write("If " + firstAntecedent + " is " + ruleDict[firstAntecedent][i]
                               + " and " + secondAntecedent + " is " + ruleDict[secondAntecedent][j]
                               + " and " + thirdAntecedent + " is " + ruleDict[thirdAntecedent][k] + " then .\n")

