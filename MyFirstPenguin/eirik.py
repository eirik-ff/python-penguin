from __future__ import print_function
from movement import *
from utilities import *
from martin import *
from math import sqrt
import json


BODY_FILENAME = "body.json"
STATE_FILENAME = "state.json"


def lookAtEnemy(body):
    """
    skal snu seg mot fienden
    """
    DIR_VALUE = {
        "right": 0,
        "top": 1,
        "left": 2,
        "bottom": 3
    }

    you = body['you']
    enemy = body['enemies'][0]

    # my x and y coord
    x = you['x']
    y = you['y']
    d = you['direction']
    new_d = "right"
    action = PASS

    # enemy x and y coord
    ex = enemy['x']
    ey = enemy['y']

    dx = ex - x
    dy = ey - y
    print("x y ex ey d", x, y, ex, ey, sqrt(dx**2 + dy**2))

    if ey < y:  # enemy above
        if abs(dx) > abs(dy):
            if dx > 0:
                new_d = "right"
            elif dx < 0:
                new_d = "left"
        elif abs(dy) >= abs(dx):
            new_d = "top"

    elif ey > y:  # enemy below
        if abs(dx) > abs(dy):
            if dx > 0:
                new_d = "right"
            elif dx < 0:
                new_d = "left"
        elif abs(dy) >= abs(dx):
            new_d = "bottom"

    else:  # enemy same height
        if ex < x:
            new_d = "left"
        elif ex > x:
            new_d = "right"

    print("new dir", new_d)


    d_val = DIR_VALUE[d]
    new_d_val = DIR_VALUE[new_d]


    if d_val == 0:
        if new_d_val == 1:
            action = ROTATE_LEFT
        elif new_d_val == 3:
            action = ROTATE_RIGHT
        elif new_d_val == 2:
            if ey < y:
                action = ROTATE_LEFT
            elif ey > y:
                action = ROTATE_RIGHT

    elif d_val == 1:
        if new_d_val == 0:
            action = ROTATE_RIGHT
        elif new_d_val == 2:
            action = ROTATE_LEFT
        elif new_d_val == 3:
            if ex > x:
                action = ROTATE_RIGHT
            elif ex < x:
                action = ROTATE_LEFT

    elif d_val == 2:
        if new_d_val == 1:
            action = ROTATE_RIGHT
        elif new_d_val == 3:
            action = ROTATE_LEFT
        elif new_d_val == 0:
            if ey < y:
                action = ROTATE_RIGHT
            elif ey > y:
                action = ROTATE_LEFT

    elif d_val == 3:
        if new_d_val == 0:
            action = ROTATE_LEFT
        elif new_d_val == 2:
            action = ROTATE_RIGHT
        elif new_d_val == 1:
            if ex > x:
                action = ROTATE_RIGHT
            elif ex < x:
                action = ROTATE_LEFT
    else:
        print("Looking at enemy: else????????")

    print("Looking at enemy")
    return action


def closestPowerup(body):
    """
    gives x, y for closest powerup
    """
    bonus_list = body["bonusTiles"]
    if len(bonus_list) == 0:
        return -1, -1

    you = body['you']
    x = you['x']
    y = you['y']

    m = 1000000
    m_bonus = bonus_list[0]
    for bonus in bonus_list:
        d = sqrt((x - bonus['x'])**2 + (y - bonus['y'])**2)
        if d < m:
            m = d
            m_bonus = bonus

    print("Closest powerup:", m_bonus['type'], "@", m_bonus['x'], m_bonus['y'], "dist=", m)
    return m_bonus['x'], m_bonus['y']


def enemyFacingYou(body):
    you = body['you']
    enemy = body['enemies'][0]

    x = you['x']
    y = you['y']

    ex = enemy['x']
    ey = enemy['y']
    ed = enemy['direction']

    if ed == "top" and y < ey:  # vi er over, fiende ser opp
        return True
    elif ed == "bottom" and y > ey:  # vi er under, fiende ser ned
        return True
    elif ed == "left" and x < ex:  # vi er til venstre, fiende ser mot venstre
        return True
    elif ed == "right" and x > ex:  # vi er til hoyre, fiende ser mot hoyre
        return True

    return False


def winningTheBattle(body):
    weaponDamage = body['you']['weaponDamage']
    eWeaponDamage = body['enemies'][0]['weaponDamage']

    if enemyFacingYou(body) and lowerHealthThanEnemy(body) and \
        weaponDamage <= eWeaponDamage:
        return False
    print("winningBattle() is running")
    return True


def readFromFile(filename):
    try:
        f = open(filename, "r")
        state = f.read()
        state = json.read(state)
        f.close()
    except:
        print("Couldn't open file or something???")
        state = {}

    return state


def writeToFile(state, filename):
    """
    state must be dict
    """
    try:
        f = open(filename, "w")
        f.write(json.dump(state))
        f.close()

        print("Wrote to file")
        return True
    except:
        return False


def huntEnemy(body):
    """
    guess that enemy is moving three blocks in direction from last seen position
    """
    GUESS = 3
    action = PASS

    max_x = body['mapWidth']
    max_y = body['mapHeight']    
    
    you = body['you']
    x = you['x']
    y = you['y']

    prev_body = readFromFile(BODY_FILENAME)
    enemy = prev_body['enemies'][0]
    ex = enemy['x']
    ey = enemy['y']    
    ed = enemy['direction']
    
    if ed == "right":
        new_x = ex + GUESS
        new_y = ey

        if new_x >= max_x:
            new_x = max_x - 1
    elif ed == "top":
        new_x = ex
        new_y = ey - GUESS

        if new_y < 0:
            new_y = 0
    elif ed == "left":
        new_x = ex - GUESS
        new_y = ey

        if new_x < 0:
            new_x = 0
    elif ed == "bottom":
        new_x = ex
        new_y = ey + GUESS  

        if new_y >= max_y:
            new_y = max_y - 1      

    print("Hunting towards", new_x, new_y)
    action = moveTowardsPoint(body, new_x, new_y)
    return action