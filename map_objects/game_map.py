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

class ChunkProperty(enum.Enum):

    NONE = enum.auto()
    DIRECTION = enum.auto()
    START = enum.auto()
    END = enum.auto

class Chunk:


    """
    Class that represents one area of gameplay.

    """

    def __init__(self):
        self.property = ChunkProperty.NONE
        self.has_player = False
        self.objects = []
        self.tiles = []


    def offload(self, obj_list, tiles):

        """
        Notice that sand is not offloaded, so every time player returns to chunk, the chunk gets random sand tiles.
        It is to make a game slightly harder - plaer will not be able to memorize map by looking at sand.
    
        """

        self.objects = [obj for obj in obj_list]
        self.tiles = [tile for tile in tiles if tile.type_of not in [sand, nothing]]

    def __str__(self):
        return f"\t\t+Chunk type+\n PROPERTY: {self.property} \n HAS_PLAYER: {self.has_player} \
                                 \n OBJECTS: {self.objects} \n TILES: {self.tiles} \n \t\t    ++"


class GameWorld:

    """
    Accessing chunks is done via self.world list.

    """


    def __init__(self):
        self.world = [[Chunk() for y in range(0, WORLD_HEIGHT)] for x in range(0, WORLD_WIDTH)]
        self.player_pos_x_in_world = int(WORLD_WIDTH / 2) + randint(-3, 4)
        self.player_pos_y_in_world = int(WORLD_HEIGHT / 2) + randint(-3, 3)
        self.world[self.player_pos_x_in_world][self.player_pos_y_in_world].property = ChunkProperty.START
    

    def update_position(self, dx, dy):
        self.world[player_pos_x_in_world][player_pos_y_in_world].has_player = False
        self.player_pos_x_in_world += dx
        self.player_pos_y_in_world += dy
        self.world[player_pos_x_in_world + dx][player_pos_y_in_world + dy].has_player = True


    def get_current_chunk(self):

        for i in range(0, WORLD_HEIGHT):
            for j in range(0, WORLD_WIDTH):
                if self.world[i][j].has_player:
                    return self.world[i][j]

        print("Couldn't find player")
        exit(-1)


    def is_new_chunk(self, world_x, world_y):

        if self.world[world_x][world_y].objects == [] and self.word[world_x][world_y] == []:
            return True

        return False


class GameMap:

    """
    Current map.

    """

    def __init__(self, width, height):
        self.width = width # of chunk
        self.height = height # of chunk
        self.elevation = MapElevation.ELEV_ABOVE
        self.current_chunk = None#self.initialize_chunk() # an area of gameplay
        self.entities = []

    def initialize_chunk(self):

        chunk = [[Tile(False, type_of=nothing) for y in range(self.height)] for x in range(self.width)]

        for y in range(1, self.height):
            for x in range(1, self.width):

                # create_sand 
                chunk[x][y] = Tile(False, type_of=sand) # it is a ground, but water or anything can be an object!

         # create random objects etc...

        self.current_chunk = chunk

    def restore_chunk(self, chunk):

        chunk = [[Tile(False, type_of=nothing) for y in range(self.height)] for x in range(self.width)]

        map_objects = chunk.objects.extend(tiles)

        for y in range(1, self.height):
            for x in range(1, self.width):


                chunk[x][y] = Tile(False, type_of=sand)

                for obj in map_objects:
                    pass


    def place_entities(self, entities):

        self.place_enemies(entities)
        # place objects etc.

    def is_blocked(self, x, y):
        if self.current_chunk[x][y].blocked:
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

