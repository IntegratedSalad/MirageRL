from map_objects.gen_map import generate_map_list
from map_objects.tile import Tile
from map_objects.tile_types import *

class GameMap:

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self._map = self.initialize_map()

    def initialize_map(self):

        _map = [[Tile(False, type_of=nothing) for y in range(self.width)] for x in range(self.height)]

        for y in range(0, self.width):
            for x in range(0, self.height):

                # create_sand 
                _map[x][y] = Tile(False, type_of=sand)


        return _map

    def is_blocked(self, x, y):
        if self._map[x][y].blocked:
            return True

        return False