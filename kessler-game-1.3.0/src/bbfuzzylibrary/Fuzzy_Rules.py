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
                self.output = int(temp[i + 1])
                i += 1

