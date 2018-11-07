from __future__ import print_function
from movement import *
import math
from eirik import *
from martin import *
import sys
from pprint import pprint


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

        writeToFile(body, BODY_FILENAME)
    except KeyError:
        return False
    except:
        print("enemyNearby failed...")
        print(sys.exc_info())

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
    state = readFromFile(STATE_FILENAME)
    action = PASS
    #action = moveTowardsCenterOfMap(body)
    #action = moveTowardsPoint(body, body["enemies"][0]["x"], body["enemies"][0]["y"])
    bx, by = closestPowerup(body)
    hx, hy = findClosestHeart(body)

    if not lowerHealthThanEnemy(body):
        state = readFromFile(STATE_FILENAME)
        state["safeHeartHarvest"] = False
        writeToFile(state, STATE_FILENAME)

    if bx == -1:
        action = moveTowardsCenterOfMap(body)
        print("Moving to center of map")
    else:
        print("Moving towards closest powerup @ ", bx, by)
        action = moveTowardsPoint(body, bx, by)

        if lowerHealthThanEnemy(body) and hx != -1:
            action = moveTowardsPoint(body, hx, hy)
            print("Moving towards nearest heart @ ", hx, hy)

    prev_body = readFromFile(BODY_FILENAME)
    state = readFromFile(STATE_FILENAME)
    if len(state) == 0:  # emptyd dict
        state["safeHeartHarvest"] = False

    if state["safeHeartHarvest"] = True:
        action = moveTowardsPoint(body, hx, hy)


    if enemyNearby(body):       #battle formation                        
        if not winningTheBattle(body):                        #lavere enn fiendens
            print("Not winning battle")          
            state["safeHeartHarvest"] = True
            writeToFile(state, STATE_FILENAME)
            
            #sx, sy = safeHeartHarvest(body)
            #action = moveTowardsPoint(body, sx, sy)        Denne flyttes utenfor if statement
            
        

        elif shootIfPossible(body):
            print("Shooting")
            action = SHOOT
        else:
            print("Looking at enemy")
            action = lookAtEnemy(body)

    elif enemyNearby(prev_body) and state["safeHeartHarvest"]==False:
        hunt_x, hunt_y = huntingPoint(prev_body)
        print("Enemy nearby prev body")
        radius = 2
        if not(hunt_x - radius <= body['you']['x'] <= hunt_x + radius and \
                hunt_y - radius <= body['you']['y'] <= hunt_y + radius):
            action = huntEnemy(body)
    
    return action


def safeHeartHarvest(body):
    goodX, goodY = safePlace(body)
    hearts = [b for b in body["bonusTiles"] if b['type'] == 'strength' and not(heart["x"] in goodX and heart["y"] in goodY)]
    if len(hearts) == 0:
        return -1, -1
    you = body['you']
    x = you['x']
    y = you['y']

    m = 1000000
    m_heart = heart    
    for heart in hearts:
        d = sqrt((x - heart['x'])**2 + (y - heart['y'])**2)
        if d < m:
            m = d
            m_heart = heart

    return m_heart["x"], m_heart["y"]

def safePlace(body):
    goodX = [] 
    goodY = []
    #returnerer liste med lovlige x og y posisjoner (se 2. linje i safeHeartHarvest)  
    
    for i in range(): pass
          
    return goodX, goodY


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

