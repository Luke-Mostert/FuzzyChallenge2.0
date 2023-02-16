# -*- coding: utf-8 -*-
# Copyright © 2022 Thales. All Rights Reserved.
# NOTICE: This file is subject to the license agreement defined in file 'LICENSE', which is part of
# this source code package.

from kesslergame import KesslerController
from typing import Dict, Tuple
from bbfuzzylibrary import Fuzzy_Create_FIS
import math
import numpy as np

asteroidFIS = Fuzzy_Create_FIS.CreateAsteroidFIS("asteroidrules.txt")

class BBController(KesslerController):

    def actions(self, ship_state: Dict, game_state: Dict) -> Tuple[float, float, bool]:
        """
        Method processed each time step by this controller.
        """
        thrust = 0
        turn_rate, targetRot = self.FindRotation(ship_state, game_state)
        if math.isclose(targetRot, ship_state['heading'], abs_tol=3):
            fire = True
            #trying to fix stutter
            turn_rate = 0
        else:
            fire = False

        return thrust, turn_rate, fire

    @property
    def name(self) -> str:
        return "BBController"

    def FindRotation(self, ship_state, game_state) -> (int, float):
        asteroid = self.FindHighestThreat(ship_state, game_state)
        shipPos = ship_state['position']
        shipRot = ship_state['heading']
        asteroidPos = asteroid['position']
        xDis = asteroidPos[0] - shipPos[0]
        yDis = asteroidPos[1] - shipPos[1]

        dot = (xDis * 1) + (yDis * 0)
        length = math.sqrt((xDis * xDis) + (yDis * yDis))
        cross = ((xDis * 0) - (yDis * 1))
        targetRot = math.acos(dot / (length * 1)) * (180/math.pi)
        #what is this for, fixes incorrect rotation but breaks targeting
        if cross < 0:
            targetRot = 360 - targetRot

        targetRot = 360 - targetRot

        #print(str(targetRot) + " TEST " + str(ship_state['heading']) + "TI" + str(shipPos) + " TESTY " + str(asteroidPos))

        if targetRot - shipRot < 0:
            return [-180, targetRot]
        else:
            return [180, targetRot]

    def FindClosestAsteroid(self, ship_state, game_state):
        closest = game_state['asteroids'][0]
        closestDist = 10000

        for asteroid in game_state['asteroids']:
            dist = self.FindDist(ship_state['position'], asteroid['position'])
            if dist < closestDist:
                #print(str(dist) + " " + str(closestDist))
                closest = asteroid
                closestDist = dist
                #print(str(dist) + " " + str(closestDist))

        return closest

    def FindDist(self,shipPos, asteroidPos) -> float:
        x = (shipPos[0] - asteroidPos[0]) * (shipPos[0] - asteroidPos[0])
        y = (shipPos[1] - asteroidPos[1]) * (shipPos[1] - asteroidPos[1])
        return math.sqrt(x + y)

    def FindHighestThreat(self, ship_state, game_state):
        highest = game_state['asteroids'][0]
        highestThreat = -1
        asteroidDict = {
            "speed": 0,
            "position": 0,
            "angle": 0,
        }

        for asteroid in game_state['asteroids']:
            dist = self.FindDist(ship_state['position'], asteroid['position'])
            speed = math.sqrt(asteroid['velocity'][0] * asteroid['velocity'][0] + asteroid['velocity'][1] * asteroid['velocity'][1])
            coordsx = ship_state['position'][0] - asteroid['position'][0]
            coordsy = ship_state['position'][1] - asteroid['position'][1]
            coords = [coordsx, coordsy]
            magcoords = math.sqrt(coords[0] * coords[0] + coords[1] * coords[1])
            #need to change the asteroids velo into its speed
            asteroidDict["speed"] = speed
            asteroidDict["position"] = dist
            #need to find angle somehow shipcoords - asteroidcoords
            asteroidDict["angle"] = math.acos(np.dot(asteroid['velocity'], coords)/(speed * magcoords)) * (180/math.pi)
            print(math.acos(np.dot(asteroid['velocity'], coords)/(speed * magcoords)) * (180/math.pi))
            threat = asteroidFIS.TSKEval(asteroidDict)
            if asteroid['size'] == 4:
                threat += .1
            elif asteroid['size'] == 3:
                threat += .075
            elif asteroid['size'] == 2:
                threat += .05
            else:
                threat += .025
            if(threat > highestThreat):
                highest = asteroid
                highestThreat = threat

        return highest
