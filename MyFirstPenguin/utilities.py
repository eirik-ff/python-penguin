from __future__ import print_function
from movement import *
import math
from eirik import *
from martin import *


def doesCellContainWall(walls, x, y):
    for wall in walls:
        if wall["x"] == x and wall["y"] == y:
            return True
    return False


def wallInFrontOfPenguin(body):
    xValueToCheckForWall = body["you"]["x"]
    yValueToCheckForWall = body["you"]["y"]
    bodyDirection = body["you"]["direction"]

    if bodyDirection == "top":
        yValueToCheckForWall -= 1
    elif bodyDirection == "bottom":
        yValueToCheckForWall += 1
    elif bodyDirection == "left":
        xValueToCheckForWall -= 1
    elif bodyDirection == "right":
        xValueToCheckForWall += 1
    return doesCellContainWall(body["walls"], xValueToCheckForWall, yValueToCheckForWall)


def enemyNearby(body):
    retval = False
    try:
        temp = body["enemies"][0]["x"]      #If the position exists, then the enemy is in vision
        print("Enemy nearby")
        retval = True
    except:
        print("enemyNearby failed....")

    return retval


def moveTowardsPoint(body, pointX, pointY):
    penguinPositionX = body["you"]["x"]
    penguinPositionY = body["you"]["y"]
    plannedAction = PASS
    bodyDirection = body["you"]["direction"]

    if penguinPositionX < pointX:
        plannedAction = MOVE_RIGHT[bodyDirection]
    elif penguinPositionX > pointX:
        plannedAction = MOVE_LEFT[bodyDirection]
    elif penguinPositionY < pointY:
        plannedAction = MOVE_DOWN[bodyDirection]
    elif penguinPositionY > pointY:
        plannedAction = MOVE_UP[bodyDirection]

    if plannedAction == ADVANCE and wallInFrontOfPenguin(body):
        plannedAction = SHOOT

    return plannedAction


def moveTowardsCenterOfMap(body):
    centerPointX = math.floor(body["mapWidth"] / 2)
    centerPointY = math.floor(body["mapHeight"] / 2)
    return moveTowardsPoint(body, centerPointX, centerPointY)

"""
flytt combatmode ned i choose action
"""
def chooseAction(body):
    action = PASS
    #action = moveTowardsCenterOfMap(body)
    #action = moveTowardsPoint(body, body["enemies"][0]["x"], body["enemies"][0]["y"])
    bx, by = closestPowerup(body)
    hx, hy = findClosestHeart(body)

    if bx == -1:
        action = moveTowardsCenterOfMap(body)
        print("Moving to center of map")
    else:
        print("Moving towards closest powerup @ ", bx, by)
        action = moveTowardsPoint(body, bx, by)

        if lowerHealthThanEnemy(body) and hx != -1:
            action = moveTowardsPoint(body, hx, hy)
            print("Moving towards nearest heart @ ", hx, hy)


    if enemyNearby(body):       #battle formation
        writeToFile(body, STATE_FILE)
        if not winningTheBattle(body):                        #lavere enn fiendens
            print("Not winning battle")
            #action=safeHeartHarvest(body)           #returner en action eller retreat hvis ingen hjerter mulig
            state = readFromFile(STATE_FILENAME)
            state["safeHeartHarvest"] = True
            writeToFile(state, STATE_FILENAME)

            action = RETREAT
        elif shootIfPossible(body):
            print("Shooting")
            action = SHOOT
        else:
            print("Looking at enemy")
            action = lookAtEnemy(body)
    
    return action


def safeHeartHarvest(body):
    return RETREAT


def distanceToEnemyXandY(body, myPosX, myPosY, enPosX, enPosY):
    distX = myPosX - enPosX
    distY = myPosY - enPosY
    return distX, distY


def smallestDistanceToEnemy(body, myPosX, myPosY, enPosX, enPosY):
    distX, distY = distanceToEnemyXandY(body, myPosX, myPosY, enPosX, enPosY)
    if abs(distX) < abs(distY):
        return distX
    else:
        return distY


def distanceBetweenPoints(x1, y1, x2, y2):
    return ( (x1 - x2)**2 + (y1 - y2)**2 )**(1/2)

