import tcod
import enum
from map_objects.tile import Tile
from components.fighter import Fighter
from components.ai import BasicMonster
from random import randint, choice
from entity import Entity
from map_objects.tile_types import *
from constants import *

# Move GameWorld to different file.

class MapElevation(enum.Enum):

    ELEV_ABOVE = enum.auto()
    ELEV_BELOW = enum.auto()

class ChunkProperty(enum.Enum):

    NONE = enum.auto()
    HAS_DIRECTION = enum.auto()
    START = enum.auto()
    END = enum.auto()

class Chunk:


    """
    Class that represents one area of gameplay.

    """

    def __init__(self):
        self.property = ChunkProperty.NONE
        self.has_player = False
        self.objects = []
        self.tiles = [[Tile(False, type_of=nothing) for y in range(MAP_HEIGHT)] for x in range(MAP_WIDTH)]


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
        self.gate_place = []
        self.create_village()
        self.place_glyphs()

        for x in range(0, WORLD_WIDTH):
            for y in range(0, WORLD_HEIGHT):
                if self.world[x][y].property == ChunkProperty.END:
                    print(f"END CHUNK: {x}, {y}")
    

    def update_position(self, dx, dy, teleport=False):
        self.world[self.player_pos_x_in_world][self.player_pos_y_in_world].has_player = False

        if not teleport:
            self.player_pos_x_in_world += dx
            self.player_pos_y_in_world += dy
            self.world[self.player_pos_x_in_world][self.player_pos_y_in_world].has_player = True
        else:
            pass


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


    def create_village(self, size=2):

        """
        Chooses an endgame area position.

        """

        border =  randint(0, 3) # clockwise, 0 is top.


        #set those x and y.

        if border == 0:
            start_x = randint(0, WORLD_WIDTH - size)
            for _ in range(size):
                self.world[start_x][0].property = ChunkProperty.END

                self.gate_place.append((start_x, 0))

                start_x += 1

        if border == 1:
            start_y = randint(0, WORLD_HEIGHT - size)
            for _ in range(size):
                self.world[WORLD_WIDTH - 1][start_y].property = ChunkProperty.END

                self.gate_place.append((WORLD_WIDTH - 1, start_y))

                start_y += 1

        if border == 2:
            start_x = randint(0, WORLD_WIDTH - size)
            for _ in range(size):
                self.world[start_x][WORLD_HEIGHT - 1].property = ChunkProperty.END

                self.gate_place.append((start_x, WORLD_HEIGHT - 1))

                start_x += 1

        if border == 3:
            start_y = randint(0, WORLD_HEIGHT - size)
            for _ in range(size):
                self.world[0][start_y].property = ChunkProperty.END

                self.gate_place.append((0, start_y))

                start_y += 1
        

    def place_glyphs(self):

        gate_coordinates = choice(self.gate_place)

        for glyph in range(GLYPHS_NUM):

            # find random place on map
            # place the right glyph.

            rand_map_place_x = randint(1, WORLD_WIDTH - 1)
            rand_map_place_y = randint(1, WORLD_HEIGHT - 1)
            rand_chunk_place_x = randint(0, MAP_WIDTH - 1)
            rand_chunk_place_y = randint(0, MAP_HEIGHT - 1)

            print(f"GLYPH_POS: {rand_map_place_x}, {rand_map_place_y}")
            print(f"GLYPH POS ON CHUNK: {rand_chunk_place_x}, {rand_chunk_place_y}")

            difference_x, difference_y = (gate_coordinates[0] - rand_map_place_x, gate_coordinates[1] - rand_map_place_y)

            if difference_x < -2 and difference_y < 0: # glyph is further on x and y axis than gate. It will point to the LEFT.
                self.world[rand_map_place_x][rand_map_place_y].tiles[rand_chunk_place_x][rand_chunk_place_y] = Tile(False, type_of=arrow_left)


            elif difference_x >= -1 and difference_y < 0:
                self.world[rand_map_place_x][rand_map_place_y].tiles[rand_chunk_place_x][rand_chunk_place_y] = Tile(False, type_of=arrow_up)


            elif difference_x > -2 and difference_y > 0:
                self.world[rand_map_place_x][rand_map_place_y].tiles[rand_chunk_place_x][rand_chunk_place_y] = Tile(False, type_of=arrow_right)


            elif difference_x >= -1 and difference_y > 0:
                self.world[rand_map_place_x][rand_map_place_y].tiles[rand_chunk_place_x][rand_chunk_place_y] = Tile(False, type_of=arrow_down)


            # Should work

            self.world[rand_map_place_x][rand_map_place_y].property = ChunkProperty.HAS_DIRECTION





class GameMap:

    """
    Current map.

    """

    def __init__(self, width, height):
        self.width = width # of chunk
        self.height = height # of chunk
        self.elevation = MapElevation.ELEV_ABOVE
        self.current_chunk = None # an area of gameplay
        self.entities = []

    def initialize_chunk(self, chunk): # chunk = world.world[map_x][map_y]

        for y in range(1, self.height):
            for x in range(1, self.width):

                # create_sand 

                # add rendering order - if I pick something up, beneath that item will by type_of == nothing.

                if chunk.tiles[x][y].type_of == nothing:
                    chunk.tiles[x][y] = Tile(False, type_of=sand) # it is a ground, but water or anything can be an object!

                # load tiles

         # create random objects etc...

        self.current_chunk = chunk

    def restore_chunk(self, chunk):

        #map_objects = chunk.objects.extend(tiles)

        for y in range(1, self.height):
            for x in range(1, self.width):


                chunk[x][y] = Tile(False, type_of=sand)

                for obj in map_objects:
                    pass


    def place_entities(self, entities):

        self.place_enemies(entities)
        # place objects etc.

    def is_blocked(self, x, y):
        if self.current_chunk.tiles[x][y].blocked:
            return True

        return False

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
