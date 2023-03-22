# -*- coding: utf-8 -*-
# Copyright © 2022 Thales. All Rights Reserved.
# NOTICE: This file is subject to the license agreement defined in file 'LICENSE', which is part of
# this source code package.

import time

import BB_controller
from kesslergame import Scenario, KesslerGame, GraphicsType, TrainerEnvironment
from test_controller import TestController
from bbfuzzylibrary.BB_controller import BBController, actionFIS, asteroidFIS
from bbfuzzylibrary.BB_controller2 import BBController2, actionFIS2, asteroidFIS2
from bbfuzzylibrary import Training
from bbfuzzylibrary import Fuzzy_Rules

my_test_scenario = Scenario(name='Test Scenario',
                            num_asteroids=15,
                            ship_states=[
                                {'position': (400, 400), 'angle': 90, 'lives': 3, 'team': 1},
                                {'position': (400, 600), 'angle': 90, 'lives': 3, 'team': 2},
                            ],
                            map_size=(1000, 800),
                            time_limit=10,
                            ammo_limit_multiplier=0,
                            stop_if_no_ammo=False)


game_settings = {'perf_tracker': True,
                 'graphics_mode': GraphicsType.Tkinter,
                 'realtime_multiplier': 5}
game = KesslerGame(settings=game_settings)  # Use this to visualize the game scenario
#game = TrainerEnvironment(settings=game_settings)  # Use this for max-speed, no-graphics simulation

for x in range(1501):
    pre = time.perf_counter()
    score, perf_data = game.run(scenario=my_test_scenario, controllers = [BBController(), BBController2()])
    Training.iteration += 1

    thetaVector = Training.OutputVector([asteroidFIS, actionFIS])
    copyTVector = thetaVector.copy()

    nVector, uVec = Training.ModifyVector(copyTVector)

    #print("nVec" + str(len(nVector)))
    #print("uVec" + str(len(uVec)))

    asteroidFIS.ruleset.UpdateOutput(nVector[0:27])
    actionFIS.ruleset.UpdateOutput(nVector[27:32])

    pre = time.perf_counter()
    score, perf_data = game.run(scenario=my_test_scenario, controllers = [BBController(), BBController2()])
    #print(thetaVector)
    if Training.reward < Training.reward2:
        Training.reward -= 15
    elif Training.reward > Training.reward2:
        Training.reward += 15
    if Training.newReward < Training.newReward2:
        Training.newReward -= 15
    elif Training.newReward > Training.newReward2:
        Training.newReward += 15

    newVec = Training.CalculateNewParams(thetaVector, uVec)

    asteroidFIS.ruleset.UpdateOutput(newVec[0:27])
    actionFIS.ruleset.UpdateOutput(newVec[27:32])

    #print("oVec" + str(thetaVector))
    #print("tVec" + str(temp))
    #print("nVec" + str(newVec))
    #print(Training.reward)
    #print(Training.newReward)
    if x % 500 == 0:
        asteroidFIS2.ruleset.UpdateOutput(newVec[0:27])
        actionFIS2.ruleset.UpdateOutput(newVec[27:32])
    if x % 50 == 0:
        print("EPOCH: " + str(x))
        print(str(Training.reward))
        print(str(Training.newReward))
        print("second agent")
        print(str(Training.reward2))
        print(str(Training.newReward2))
        Fuzzy_Rules.FuzzyRuleExport("actionrules" + str(x) + ".txt", actionFIS.ruleset)
        Fuzzy_Rules.FuzzyRuleExport("asteroidrules" + str(x) + ".txt", asteroidFIS.ruleset)

    Training.iteration = 0
    Training.reward = 0
    Training.newReward = 0
    Training.reward2 = 0
    Training.newReward2 = 0


#print('Scenario eval time: '+str(time.perf_counter()-pre))
#print(score.stop_reason)
#print('Asteroids hit: ' + str([team.asteroids_hit for team in score.teams]))
#print('Deaths: ' + str([team.deaths for team in score.teams]))
#print('Accuracy: ' + str([team.accuracy for team in score.teams]))
#print('Mean eval time: ' + str([team.mean_eval_time for team in score.teams]))

