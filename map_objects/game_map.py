import tcod
import enum
from map_objects.tile import Tile
from components.fighter import Fighter
from components.ai import BasicMonster
from random import randint
from entity import Entity
from map_objects.tile_types import *
from constants import *

class MapElevation(enum.Enum):

    ELEV_ABOVE = enum.auto()
    ELEV_BELOW = enum.auto()


class GameMap:

    def __init__(self, width, height):
        self.width = width # of chunk
        self.height = height # of chunk
        self.elevation = MapElevation.ELEV_ABOVE
        self.chunk = self.initialize_chunk() # an area of gameplay
        self.world = [] # an array of chunks with data, that is offloaded when player moves into another chunk

    def initialize_chunk(self):

        if self.elevation == MapElevation.ELEV_ABOVE:

            chunk = [[Tile(False, type_of=nothing) for y in range(self.height)] for x in range(self.width)]
            # possibility of necessity to change that

            for y in range(1, self.height):
                for x in range(1, self.width):

                    # create_sand 
                    chunk[x][y] = Tile(False, type_of=sand) # it is a ground, but water or anything can be an object!

             # create random objects etc...

        else:
            pass
        

        return chunk

    def place_entities(self, entities):

        self.place_enemies(entities)
        # place objects etc.

    def is_blocked(self, x, y):
        if self.chunk[x][y].blocked:
            return True

        return False

    def save_chunk(self):
        pass

    def place_enemies(self, entities):

        enemies_num = randint(0, MAX_MONSTERS_PER_CHUNK)

        for mon in range(enemies_num):

            x = randint(1, self.width - 1)
            y = randint(1, self.height - 1)

            if not any([entity for entity in entities if entity.x == x and entity.y == y]):
                monster_ai = BasicMonster()
                if randint(0, 100) < 50:
                    monster_fighter_component = Fighter(3, 1, 2)
                    monster = Entity(x, y, 'a', tcod.darker_red, 'red ant', blocks=True, fighter=monster_fighter_component, ai=monster_ai)

                else:
                    monster_fighter_component = Fighter(3, 1, 4)
                    monster = Entity(x, y, 's', tcod.dark_yellow, 'scorpion', blocks=True, fighter=monster_fighter_component, ai=monster_ai)

            entities.append(monster)

        

class NpGameMap(tcod.map.Map):

    def __init__(self, width, height, order="C"): # if walkable - set to random
        super().__init__(width, height, order)

    # maybe two np.arrays? One with symbols, and one with data
