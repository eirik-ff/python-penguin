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
    theta = atan2(dx, -dy) + pi/2
    if (theta > pi): theta -= pi
    print("x y ex ey theta: ", x, y, ex, ey, theta)

    if -pi / 4 <= theta <= pi / 4:
        new_d = "left"
        print("new dir left")
    elif pi / 4 <= theta <= 3 * pi / 4:
        new_d = "bottom"
        print("new dir bottom")
    elif -3 * pi / 4 <= theta <= -pi / 4:
        new_d = "top"
        print("new dir top")
    else:  # pi / 4 <= theta <= pi or -pi <= theta <= -3 * pi / 4:
        new_d = "right"
        print("new dir right")


    d_val = DIR_VALUE[d]
    new_d_val = DIR_VALUE[new_d]

    dist = new_d_val - d_val
    if d_val == 0 and new_d == 3:
        action = ROTATE_RIGHT
    elif d_val == 3 and new_d == 0:
        action = ROTATE_LEFT
    elif dist > 0:
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