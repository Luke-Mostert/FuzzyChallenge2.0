import random

import Fuzzy_Inference_System
from Fuzzy_Inference_System import Fuzzy_Rule_Set
from Fuzzy_Rule_Set import Fuzzy_Rules
from Fuzzy_Inference_System import Fuzzy_Variables
from Fuzzy_Variables import Fuzzy_Set

reward = 0
newReward = 0
reward2 = 0
newReward2 = 0
iteration = 0


def OutputVector(InferenceSystem):
    #ruleset = InferenceSystem.ruleset
    ParamVector = []

    for i in InferenceSystem:
        for j in range(len(i.ruleset.rules)):
            ParamVector.append(i.ruleset.rules[j].output)
    return ParamVector

def ModifyVector(oldVec):
    randParam = random.randint(0, 30)
    uVec = [0] * 31
    tempVec = oldVec
    uVec[randParam] = 1
    tempVec[randParam] += 0.01

    return tempVec, uVec

def CalculateNewParams(oldVec, uVec):
    tempVec = [0] * 31
    for x in range(31):
        #0.0005
        #0.00001
        #0.001 works
        tempVec[x] = oldVec[x] + ((0.001 * ( newReward - reward)) * uVec[x])
    return tempVec