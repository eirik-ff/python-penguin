from movement import *
from math import sqrt, atan2, pi

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
    w_range = you['weaponRange']
    new_d = "right"
    action = PASS

    # enemy x and y coord
    ex = enemy['x']
    ey = enemy['y']

    dx = ex - x
    dy = ey - y
    print("x y ex ey", x, y, ex, ey)

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

    elif d_val == 1:
        if new_d_val == 0:
            action = ROTATE_RIGHT
        elif new_d_val == 2:
            action = ROTATE_LEFT

    elif d_val == 2:
        if new_d_val == 1:
            action = ROTATE_RIGHT
        elif new_d_val == 3:
            action = ROTATE_LEFT

    elif d_val == 3:
        if new_d_val == 0:
            action = ROTATE_RIGHT
        elif new_d_val == 2:
            action = ROTATE_LEFT

    else:
        dist = new_d_val - d_val
        if dist > 0:
            action = ROTATE_LEFT
        elif dist < 0:
            action = ROTATE_RIGHT


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
        d = sqrt( (x - bonus['x'])**2 + (y - bonus['y'])**2 )
        if d < m:
            m = d
            m_bonus = bonus

    return m_bonus['x'], m_bonus['y']