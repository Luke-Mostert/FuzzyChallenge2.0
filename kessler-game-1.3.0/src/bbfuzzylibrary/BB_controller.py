# -*- coding: utf-8 -*-
# Copyright © 2022 Thales. All Rights Reserved.
# NOTICE: This file is subject to the license agreement defined in file 'LICENSE', which is part of
# this source code package.

from kesslergame import KesslerController
from typing import Dict, Tuple
import math

class BBController(KesslerController):

    def actions(self, ship_state: Dict, game_state: Dict) -> Tuple[float, float, bool]:
        """
        Method processed each time step by this controller.
        """
        thrust = 0
        turn_rate, targetRot = self.FindRotation(ship_state, game_state)
        if math.isclose(targetRot, ship_state['heading'], abs_tol=5):
            fire = True
        else:
            fire = False

        return thrust, turn_rate, fire

    @property
    def name(self) -> str:
        return "BBController"

    def FindRotation(self, ship_state, game_state) -> (int, float):
        asteroid = self.FindClosestAsteroid(ship_state, game_state)
        shipPos = ship_state['position']
        shipRot = ship_state['heading']
        asteroidPos = asteroid['position']
        xDis = asteroidPos[0] - shipPos[0]
        yDis = asteroidPos[1] - shipPos[1]
        denom = math.sqrt((xDis * xDis) + (yDis * yDis))

        dot = (xDis * 1) + (yDis * 0)
        length = math.sqrt((xDis * xDis) + (yDis * yDis))
        cross = ((xDis * 0) - (yDis * 1))
        targetRot = math.acos(dot / (length * 1)) * (180/math.pi)
        if cross < 0:
            targetRot = 360 - targetRot

        # + " shipangle:" + str(shipRot)+ " asteroidpos:" + str(asteroidPos) + " dot:" + str(dot) + " cross:" + str(cross) + " length:" + str(length) + " xDis:"  + str(xDis) + " yDis:"  + str(yDis))
        #targetRot = math.atan2((yDis / denom), (xDis / denom)) * (180/math.pi)
        #print(str(xDis) + " " + str(yDis) + " " + str(denom) + " " + str(targetRot))
        #print(str(targetRot) + " " + str(asteroidPos))        if targetRot > 180:
        targetRot = 360 - targetRot

        print(str(targetRot) + " TEST " + str(ship_state['heading']) + "TI" + str(shipPos) + " TESTY " + str(asteroidPos))



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