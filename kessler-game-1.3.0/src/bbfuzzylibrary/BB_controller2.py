# -*- coding: utf-8 -*-
# Copyright © 2022 Thales. All Rights Reserved.
# NOTICE: This file is subject to the license agreement defined in file 'LICENSE', which is part of
# this source code package.
import kesslergame.kessler_game
from kesslergame import KesslerController
from typing import Dict, Tuple
from bbfuzzylibrary import Fuzzy_Create_FIS, Training, Fuzzy_Rules
import math
import numpy as np
from bbfuzzylibrary import Training

asteroidFIS2 = Fuzzy_Create_FIS.CreateAsteroidFIS("asteroidrules3000.txt")
actionFIS2 = Fuzzy_Create_FIS.CreateActionFIS("actionrules3000.txt")

class BBController2(KesslerController):

    def actions(self, ship_state: Dict, game_state: Dict) -> Tuple[float, float, bool]:
        """
        Method processed each time step by this controller.
        """
        thrust = 0
        retDict = self.DecideAction(ship_state, game_state)
        #print(retDict)
        #oVector = Training.OutputVector([asteroidFIS, actionFIS])

        if retDict["action"] == 0:
            thrust = 0
            if math.isclose(retDict["targetRot"], ship_state['heading'], abs_tol=3):
                fire = True
            else:
                fire = False
        else:
            fire = False
            if math.isclose(retDict["targetRot"], ship_state['heading'], abs_tol=5):
                thrust = retDict["thrust"]
            else:
                thrust = 0

        return thrust, retDict["turn_rate"], fire

    @property
    def name(self) -> str:
        return "BBController"

    def FindShootingRotation(self, ship_state, asteroid):
        shipPos = ship_state['position']
        shipRot = ship_state['heading']
        # increase the pos by timestep * velocity

        # timestep = how long takes projectile to get there dist/speed
        asteroidPos = asteroid['position']

        asteroidVel = asteroid['velocity']
        shipAsteroidDis = self.FindDist(shipPos, asteroidPos)
        timeStep = shipAsteroidDis / 800

        newXPos = asteroidPos[0] + (timeStep * asteroidVel[0])
        newYPos = asteroidPos[1] + (timeStep * asteroidVel[1])

        xDis = newXPos - shipPos[0]
        yDis = newYPos - shipPos[1]

        return self.FindRotation(ship_state, (xDis, yDis))

    def FindRotation(self, ship_state, tarPosition):

        xDis = tarPosition[0]
        yDis = tarPosition[1]
        shipRot = ship_state['heading']

        dot = (xDis * 1) + (yDis * 0)
        length = math.sqrt((xDis * xDis) + (yDis * yDis))
        cross = ((xDis * 0) - (yDis * 1))
        targetRot = math.acos(dot / (length * 1)) * (180/math.pi)
        #what is this for, fixes incorrect rotation but breaks targeting
        if cross < 0:
            targetRot = 360 - targetRot

        targetRot = 360 - targetRot

        if targetRot - shipRot < 0:
            if targetRot - shipRot < -5:
                return[-120, targetRot]
            else:
                return[-70, targetRot]
        else:
            if targetRot - shipRot > 5:
                return [120, targetRot]
            else:
                return [70, targetRot]

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

    def FindDist(self, shipPos, asteroidPos) -> float:
        x = (shipPos[0] - asteroidPos[0]) * (shipPos[0] - asteroidPos[0])
        y = (shipPos[1] - asteroidPos[1]) * (shipPos[1] - asteroidPos[1])
        return math.sqrt(x + y)

    def FindHighestThreat(self, ship_state, asteroid):
        asteroidDict = {
            "speed": 0,
            "position": 0,
            "angle": 0,
        }

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
        threat = asteroidFIS2.TSKEval(asteroidDict)
        if asteroid['size'] == 4:
            threat += .1
        elif asteroid['size'] == 3:
            threat += .075
        elif asteroid['size'] == 2:
            threat += .05
        else:
            threat += .025
        return threat

    def Avoidance(self, ship, asteroid):
        asteroidPos = asteroid['position']
        asteroidVel = asteroid['velocity']
        shipPos = ship['position']

        perpVecX = asteroidVel[0]
        perpVecY = asteroidVel[1]
        #Greater than zero means left side
        if ((asteroidPos[0]) * (shipPos[1]) - (asteroidPos[1]) * (shipPos[0])) > 0:
            if(asteroidPos[0] <= shipPos[0] and asteroidPos[1] >= shipPos[1]):
                perpVecX *= -1
            elif(asteroidPos[0] >= shipPos[0] and asteroidPos[1] <= shipPos[1]):
                perpVecX *= -1
            elif(asteroidPos[0] <= shipPos[0] and asteroidPos[1] <= shipPos[1]):
                perpVecX *= -1
            elif(asteroidPos[0] >= shipPos[0] and asteroidPos[1] >= shipPos[1]):
                perpVecX *= -1
        # Greater than zero means go right
        else:
            if(asteroidPos[0] < shipPos[0] and asteroidPos[1] > shipPos[1]):
                perpVecY *= -1
            elif(asteroidPos[0] > shipPos[0] and asteroidPos[1] < shipPos[1]):
                perpVecY *= -1
            elif(asteroidPos[0] > shipPos[0] and asteroidPos[1] > shipPos[1]):
                perpVecY *= -1
            elif(asteroidPos[0] < shipPos[0] and asteroidPos[1] < shipPos[1]):
                perpVecY *= -1


        xTemp = perpVecX
        perpVecX = perpVecY
        perpVecY = xTemp

        #print(str(asteroid["position"]) + " VEL " + str(asteroid["velocity"]) + " PERP " + str((perpVecX, perpVecY)))

        turn_rate, targetRot = self.FindRotation(ship, (perpVecX, perpVecY))
        return turn_rate, targetRot, 120

    def Shooting(self, ship, asteroid):
        turn_rate, targetRot = self.FindShootingRotation(ship, asteroid)
        return turn_rate, targetRot

    def DecideAction(self, ship_state, game_state):
        actionDict = {
            "position": 0,
            "threat": 0,
        }
        highestShoot = game_state['asteroids'][0]
        highestAvoid = game_state['asteroids'][0]
        secondary = game_state['asteroids'][0]
        highestThreat = -1
        highestAvoidThreat = -1
        closestDist = 10000

        for asteroid in game_state['asteroids']:
            dist = self.FindDist(ship_state['position'], asteroid['position'])
            if dist < closestDist:
                closestDist = dist
                secondary = asteroid
            threat = 0
            if dist < 300:
                threat = self.FindHighestThreat(ship_state, asteroid)
                if threat > highestThreat:
                    highestShoot = asteroid
                    highestThreat = threat
            else:
                threat = 0.2
            actionDict["position"] = dist
            actionDict["threat"] = threat

            avoidThreat = actionFIS2.TSKEval(actionDict)
            if avoidThreat > highestAvoidThreat:
                highestAvoid = asteroid
                highestAvoidThreat = avoidThreat


        if highestThreat == -1:
            highestShoot = secondary

        retDict = {
            "action": 0,
            "targetRot": 0,
            "turn_rate": 0,
            "thrust": 0
        }
#highestAvoidThreat > 0.5
        if highestAvoidThreat > 0.5:
            turn_rate, targetRot, thrust = self.Avoidance(ship_state, highestAvoid)
            retDict["action"] = 1
            retDict["targetRot"] = targetRot
            retDict["turn_rate"] = turn_rate
            retDict["thrust"] = thrust
        else:
            turn_rate, targetRot = self.Shooting(ship_state, highestAvoid)
            retDict["action"] = 0
            retDict["targetRot"] = targetRot
            retDict["turn_rate"] = turn_rate

        return retDict
