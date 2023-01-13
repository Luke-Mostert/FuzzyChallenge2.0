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
        xDis = abs(shipPos[0] - asteroidPos[0])
        yDis = abs(shipPos[1] - asteroidPos[1])
        targetRot = math.tan(yDis / xDis) * (180/math.pi)
        if shipRot - targetRot < 180:
            return [-50, targetRot]
        else:
            return [50, targetRot]

    def FindClosestAsteroid(self, ship_state, game_state):
        closest = game_state['asteroids'][0]
        closestDist = 10000000

        for asteroid in game_state['asteroids']:
            dist = self.FindDist(ship_state['position'], asteroid['position'])
            if dist < closestDist:
                closest = asteroid
                closestDist = dist

        return closest


    def FindDist(self,shipPos, asteroidPos) -> float:
        x = (shipPos[0] - asteroidPos[0]) * (shipPos[0] - asteroidPos[0])
        y = (shipPos[1] - asteroidPos[1]) * (shipPos[1] - asteroidPos[1])
        return math.sqrt(x + y)