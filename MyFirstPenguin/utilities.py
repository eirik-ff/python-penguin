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
    try:
        temp = body["enemies"][0]["x"]      #If the position exists, then the enemy is in vision
        return True
    except:
        return False


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

    if enemyNearby(body):       #battle formation
        if shootIfPossible(body):
            plannedAction = SHOOT
        else:
            plannedAction = lookAtEnemy(body)

    elif plannedAction == ADVANCE and wallInFrontOfPenguin(body):
        plannedAction = SHOOT

    return plannedAction


def moveTowardsCenterOfMap(body):
    centerPointX = math.floor(body["mapWidth"] / 2)
    centerPointY = math.floor(body["mapHeight"] / 2)
    return moveTowardsPoint(body, centerPointX, centerPointY)


def chooseAction(body):
    action = PASS
    #action = moveTowardsCenterOfMap(body)
    #action = moveTowardsPoint(body, body["enemies"][0]["x"], body["enemies"][0]["y"])
    bx, by = closestPowerup(body)
    hx, hy = findClosestHeart(body)
    if bx == -1 or hx == -1:
        action = moveTowardsCenterOfMap(body)
    else:
        action = moveTowardsPoint(body, bx, by)
        
        if lowerHealthThanEnemy(body):
            action = moveTowardsPoint(body, hx, hy)
    return action


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