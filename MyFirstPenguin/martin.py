from movement import *
from utilities import *
from math import sqrt

def shootIfPossible(body):
    
    you = body["you"]
    direction = you["direction"]
    myPosX = you["x"]
    myPosY = you["y"]
    enemy = body["enemies"][0]
    try:
        enX = enemy["x"]
        enY = enemy["y"]
    except:
        return False

    if direction == "right" and enX - myPosX > 0 and enY == myPosY:
        print("Shooting")
        return True
    elif direction == "left" and enX - myPosX < 0 and enY == myPosY:
        print("Shooting")
        return True
    elif direction == "bottom" and enY - myPosY > 0 and enX == myPosX:
        print("Shooting")
        return True
    elif direction == "top" and enY - myPosY < 0 and enX == myPosX:
        print("Shooting")
        return True
    else:
        return False


def lowerHealthThanEnemy(body):
    you = body["you"]
    enemy = body["enemies"][0]
    myHealth = int(you["strength"])

    return myHealth < int(enemy['strength'])


def findClosestHeart(body):
    hearts = [b for b in body["bonusTiles"] if b['type'] == 'strength']
    if len(hearts) == 0:
        return -1, -1

    you = body['you']
    x = you['x']
    y = you['y']

    m = 1000000
    m_heart = hearts[0]
    for heart in hearts:
        d = sqrt((x - heart['x'])**2 + (y - heart['y'])**2)
        if d < m:
            m = d
            m_heart = heart

    return m_heart['x'], m_heart['y']