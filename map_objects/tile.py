from random import choice as rand_choice

class Tile:

    def __init__(self, blocked, type_of, block_sight=None):
        self.blocked = blocked

        if block_sight is None:
            block_sight = blocked

        self.block_sight = block_sight

        if type(type_of.get('char')) is list:
            char = rand_choice(type_of.get('char'))
        else:
            char = type_of.get('char') 
          
        color = type_of.get('color')

        self.char = char
        self.color = color
