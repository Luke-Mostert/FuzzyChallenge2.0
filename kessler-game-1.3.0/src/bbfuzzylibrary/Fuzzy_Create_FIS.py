import Fuzzy_Inference_System
from Fuzzy_Inference_System import Fuzzy_Rule_Set
from Fuzzy_Rule_Set import Fuzzy_Rules
from Fuzzy_Inference_System import Fuzzy_Variables
from Fuzzy_Variables import Fuzzy_Set



def CreateAsteroidFIS(filename):
    rules = Fuzzy_Rules.ImportFile(filename)
    asteroid_ruleset = Fuzzy_Rule_Set.FuzzyRuleSet(rules)
    # rule_set.PrintRules()

    # Creating memebership functions
    # speed
    speedFastSet = Fuzzy_Set.Triangle("fast", 142.5, 165, 165)
    # could swap to trapezoid since 2 - 3 size have different speed
    speedIntermediateSet = Fuzzy_Set.Triangle("intermediate", 120, 142.5, 165)
    speedSlowSet = Fuzzy_Set.Trapezoid("slow", 0, 0, 120, 142.5)

    # position
    positionFarSet = Fuzzy_Set.Trapezoid("far", 200, 300, 800, 800)
    positionMidrangeSet = Fuzzy_Set.Triangle("midrange", 100, 200, 300)
    positionCloseSet = Fuzzy_Set.Trapezoid("close", 0, 0, 100, 200)

    # angle
    # Why 181 not 180
    angleLargeSet = Fuzzy_Set.Triangle("large", 30, 38.5, 181)
    angleMediumSet = Fuzzy_Set.Triangle("medium", 22.5, 30, 38.5)
    angleSmallSet = Fuzzy_Set.Trapezoid("small", 0, 0, 22.5, 30)

    speedVar = Fuzzy_Variables.FuzzyVariables("speed", 0, 165, [speedFastSet, speedIntermediateSet, speedSlowSet])
    positionVar = Fuzzy_Variables.FuzzyVariables("position", 0, 800,
                                                 [positionFarSet, positionMidrangeSet, positionCloseSet])
    angleVar = Fuzzy_Variables.FuzzyVariables("angle", 0, 180, [angleLargeSet, angleMediumSet, angleSmallSet])

    asteroid_fis = Fuzzy_Inference_System.FuzzyInferenceSystem(asteroid_ruleset,
                                                               [speedVar, positionVar, angleVar])

    return asteroid_fis


def CreateActionFIS(filename):
    rules = Fuzzy_Rules.ImportFile(filename)
    threat_ruleset = Fuzzy_Rule_Set.FuzzyRuleSet(rules)
    # position
    positionFarSet = Fuzzy_Set.Trapezoid("far", 100, 200, 800, 1000)
    positionCloseSet = Fuzzy_Set.Trapezoid("close", 0, 0, 100, 200)

    #threat
    threatHighSet = Fuzzy_Set.Trapezoid("high", 0.8, 0.85, 1, 1)
    ThreatLowSet = Fuzzy_Set.Trapezoid("low", 0, 0, 0.8, 0.85)

    positionVar = Fuzzy_Variables.FuzzyVariables("position", 0, 800,
                                                 [positionFarSet, positionCloseSet])
    threatVar = Fuzzy_Variables.FuzzyVariables("threat", 0, 1,
                                                 [threatHighSet, ThreatLowSet])

    action_fis = Fuzzy_Inference_System.FuzzyInferenceSystem(threat_ruleset,
                                                               [positionVar, threatVar])
    return action_fis


