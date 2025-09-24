import random

def roll_dice():
    my_dice = random.randint(1, 100)

    if my_dice <= 33:
        color = 0xff0000
    elif my_dice <= 66:
        color = 0xffff00
    else:
        color = 0x00ff00
    
    return {'dice':my_dice, 'color':color}