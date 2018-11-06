from movement import *

def lookAtEnemy(body):
    """
    skal snu seg mot fienden
    hvis fienden er innenfor weapon range, skyt
    """
    DIR_VALUE = {
        "right": 0,
        "top": 1,
        "left": 2,
        "bottom": 3
    }

    you = body['you']
    enemy = body['enemies']

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

    if ex > x and ex < y and d != "right": # 1
        new_d = "right"
    elif ex > x and ex < y and d != "top": # 2
        new_d = "top"
    elif ex < x and ey < y and d != "top": # 3
        new_d = "top"
    elif ex < x and ey < y and d != "left": # 4
        new_d = "left"
    elif ex < x and ey > y and d != "left": # 5
        new_d = "left"
    elif ex < x and ey > y and d != "bottom": # 6
        new_d = "bottom"
    elif ex > x and ey > y and d != "bottom": # 7
        new_d = "bottom"
    elif ex > x and ey > y and d != "right": # 8
        new_d = "right"
    

    d_val = DIR_VALUE[d]
    new_d_val = DIR_VALUE[new_d]

    dist = d_val - new_d_val
    if dist > 0:
        action = ROTATE_LEFT
    elif dist < 0:
        action = ROTATE_RIGHT


    return action