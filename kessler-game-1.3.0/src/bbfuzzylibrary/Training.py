import Fuzzy_Inference_System
from Fuzzy_Inference_System import Fuzzy_Rule_Set
from Fuzzy_Rule_Set import Fuzzy_Rules
from Fuzzy_Inference_System import Fuzzy_Variables
from Fuzzy_Variables import Fuzzy_Set

reward = 0

def OutputVector(InferenceSystem):
    #ruleset = InferenceSystem.ruleset
    ParamVector = []

    for i in InferenceSystem:
        for j in range(len(i.ruleset.rules)):
            ParamVector.append(i.ruleset.rules[j].output)
    return ParamVector
