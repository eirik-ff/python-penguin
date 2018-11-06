from movement import *

def lookAtEnemy(body):
    """
    skal snu seg mot fienden
    hvis fienden er innenfor weapon range, skyt
    """
    you = body['you']
    enemy = body['enemies']

    # my x and y coord
    x = you['x']
    y = you['y']
    w_range = you['weaponRange']
    action = PASS

    # enemy x and y coord
    ex = enemy['x']
    ey = enemy['y']

    if ex >= x:  # fiende til høyre for deg
        pass