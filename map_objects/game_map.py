from map_objects.gen_map import generate_map_list
from map_objects.tile import Tile

class GameMap:

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.map = self.initialize_map()

    def initialize_map(self):

        map = [[Tile(False) for y in range(self.width)] for x in range(self.height)]
        #tiles = generate_map_list()

        #for x in range(0, self.width):
        #    for y in range(0, self.height):
        #        if tiles[x][y] == '#':
        #            map[x][y].block_sight = True

        map[30][22].blocked = True
        map[30][22].block_sight = True

        return map

    def is_blocked(self, x, y):
        if self.map[x][y].blocked:
            return True

        return False