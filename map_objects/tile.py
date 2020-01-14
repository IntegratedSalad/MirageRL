from random import choice as rand_choice

class Tile:

    def __init__(self, blocked, type_of, block_sight=None):
        self.blocked = blocked
        self.type_of = type_of

        if block_sight is None:
            block_sight = blocked

        self.block_sight = block_sight

        if type(type_of.get('char')) is list: # it gets called 1215029 times
            char = rand_choice(type_of.get('char'))

        else:
            char = type_of.get('char') 
          
        color = type_of.get('color')

        self.char = char
        self.color = color
