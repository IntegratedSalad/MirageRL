from map_objects.tile import Tile
from map_objects.tile_types import *
from tcod.map import Map

class GameMap:

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self._map = self.initialize_map()

    def initialize_map(self):

        _map = [[Tile(False, type_of=nothing) for y in range(self.height)] for x in range(self.width)]

        for y in range(1, self.height):
            for x in range(1, self.width):

                # create_sand 
                _map[x][y] = Tile(False, type_of=sand) # it is a ground, but water or anything can be an object!

                # create random objects etc...

        return _map

    def is_blocked(self, x, y):
        if self._map[x][y].blocked:
            return True

        return False

class NpGameMap(Map):

    def __init__(self, width, height, order="C"): # if walkable - set to random
        super().__init__(width, height, order)

    # maybe two np.arrays? One with symbols, and one with data
