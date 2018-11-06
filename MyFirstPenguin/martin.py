from movement import *

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
        return True
    elif direction == "left" and enX - myPosX < 0 and enY == myPosY:
        return True
    elif direction == "down" and enY - myPosY > 0 and enX == myPosX:
        return True
    elif direction == "top" and enY - myPosY < 0 and enX == myPosX:
        return True
    else:
        return False

