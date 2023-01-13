import numpy as np
import matplotlib.pyplot as plt
import Fuzzy_Variables
import Fuzzy_Rule_Set


class FuzzyInferenceSystem:
    def __init__(self, ruleset, variables=[]):
        self.variables = variables
        self.ruleset = ruleset
        self.dictAntecedent = {}
        #creating dictionary where key is rule antecedent and value is index to membership function
        for i in range(len(ruleset.rules)):
            for j in range(len(ruleset.rules[i].antecedents)):
                self.dictAntecedent[ruleset.rules[i].antecedents[j]] = [0, 0]
        for i in range(len(self.variables)):
            for j in range(len(self.variables[i].sets)):
                for k in range(len(self.variables[i].sets[j].name)):
                    if self.variables[i].sets[j].name in self.dictAntecedent:
                        self.dictAntecedent[self.variables[i].sets[j].name] = [i, j]

    #make the input a dictionary
    def TSKEval(self, inputs={}):
        #Creating a 2D list where rows are equal to the number of inputs
        # Columns are equal to number of sets in variables to the power of antecedents in the rules.
        rows = len(inputs)
        cols = len(self.variables[0].sets) ** len(self.ruleset.rules[0].antecedents)
        numer = [ [0] * cols for _ in range(rows)]
        denom = [ [0] * cols for _ in range(rows)]
        #Check if the values are in range of the variables
        for b in range(len(inputs)):
            for a in range(len(self.variables)):
                if self.variables[a].name == list(inputs)[b]:
                    # Check that the x value is in the range of the variable
                    if self.variables[a].xMin > list(inputs.values())[b] or self.variables[a].xMax < list(inputs.values())[b]:
                        print("This value is out of range")
                        return -999999999
        #Loop for each rule
        for m in range(len(inputs)):
            for i in range(len(self.ruleset.rules)):
                for k in range(len(self.ruleset.rules[i].antecedents)):
                    #Searching for the matching membership function that goes with the current rule
                    #Won't need these loops bc dictionary
                    varsIndex = self.dictAntecedent[self.ruleset.rules[i].antecedents[k]][0]
                    setIndex = self.dictAntecedent[self.ruleset.rules[i].antecedents[k]][1]
                    currInput = list(inputs.values())[m]

                    # We only want to multiply by the rules output once so do it to the first iteration
                    if self.variables[varsIndex].name == list(inputs)[m]:
                        if m == 0:
                            numer[m][i] = self.variables[varsIndex].sets[setIndex].calcMembership(currInput) * self.ruleset.rules[i].output
                            #print(self.ruleset.rules[i].antecedents[k])
                        else:
                            numer[m][i] = self.variables[varsIndex].sets[setIndex].calcMembership(currInput)
                        denom[m][i] = self.variables[varsIndex].sets[setIndex].calcMembership(currInput)

        numerReturn = 0
        denomReturn = 0
        for i in range(cols):
            numerTemp = 1
            denomTemp = 1
            for j in range(rows):
                numerTemp *= numer[j][i]
                denomTemp *= denom[j][i]
            numerReturn += numerTemp
            denomReturn += denomTemp
        return numerReturn / denomReturn
