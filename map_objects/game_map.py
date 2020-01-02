import tcod
import enum
import utils
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

    def __init__(self, pos):
        self.pos = pos
        self.property = ChunkProperty.NONE
        self.discovered = False
        self.objects = []
        self.tiles = [[Tile(False, type_of=sand) for y in range(MAP_HEIGHT)] for x in range(MAP_WIDTH)]

    def __str__(self):
        return f"\t\t+Chunk type+\n PROPERTY: {self.property} \n \
                                 \n OBJECTS: {self.objects} \n  \t\t DISCOVERED: {self.discovered} \n \t\t POS: {self.pos}"

    def __mem__(self):
        return f"{hex(id(self))}"




class GameWorld:

    """
    Handles chunks and world related features.
    Accessing chunks is done via self.world list.

    """


    def __init__(self):
        self.world_map = [[Tile(False, type_of=sand) for y in range(0, WORLD_HEIGHT * MAP_HEIGHT)] for x in range(0, WORLD_WIDTH * MAP_WIDTH)]
        # self.chunks = [[Chunk() for y in range(0, WORLD_HEIGHT)] for x in range(0, WORLD_WIDTH)]
        self.chunks = self.initialize_chunks()
        self.gate_place = []
        # self.create_village()
        # self.place_glyphs()

        # for x in range(0, WORLD_WIDTH):
        #     for y in range(0, WORLD_HEIGHT):
        #         if self.world[x][y].property == ChunkProperty.END:
        #             print(f"END CHUNK: {x}, {y}")
    

    def get_chunk_pos_from_player_pos(self, px, py):

        x = int(px / MAP_WIDTH)
        y = int(py / MAP_HEIGHT)

        return (x, y)


    def initialize_chunks(self):
        chunks = []
        for y in range(0, WORLD_HEIGHT):
            row = []
            for x in range(0, WORLD_WIDTH):
                row.append(Chunk((y, x)))
            chunks.append(row)
        return chunks        

    def get_current_tiles(self):

        return [tile for tile in self.get_current_chunk().tiles]


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


            elif difference_x >= -1 and difference_y > 0: # GATE_CORD_Y - GLYPH_Y > 0 means that gate has greater y - is further down.
                self.world[rand_map_place_x][rand_map_place_y].tiles[rand_chunk_place_x][rand_chunk_place_y] = Tile(False, type_of=arrow_down)


            # Should work

            self.world[rand_map_place_x][rand_map_place_y].property = ChunkProperty.HAS_DIRECTION


            # BUG ! SOMETIMES THE GLYPH ISN'T PLACED !


class GameMap:

    """
    Current map.

    """

    def __init__(self, width, height, current_chunk):
        self.width = width # of chunk
        self.height = height # of chunk
        self.elevation = MapElevation.ELEV_ABOVE
        self.current_chunk = current_chunk # an area of gameplay
        #self.entities = [] # make it local, and self.place_entities to return entities list

    # def initialize_chunk(self, world):

    #     chunk_x, chunk_y = world.get_chunk_pos_from_player_pos()
    #     current_chunk = world.chunks[chunk_x][chunk_y]

    #     chunk_start_x, chunk_start_y = world.get_chunk_pos_from_player_pos()
    #     chunk_start_x *= MAP_WIDTH
    #     chunk_start_y *= MAP_HEIGHT

    #     for y in range(chunk_start_y, chunk_start_y + self.height):
    #         for x in range(chunk_start_x, chunk_start_x + self.width):
    #             world.world_map[x][y] = Tile(False, type_of=sand)

    #             pos_in_chunk_x, pos_in_chunk_y = utils.get_pos_in_chunk(x, y)
    #             current_chunk.tiles[pos_in_chunk_x][pos_in_chunk_y] = Tile(False, type_of=sand)

    #     self.current_chunk = current_chunk

    def offload_chunk(self, chunk_x, chunk_y, world):#, player_x, player_y, world):

        chunk_start_x = chunk_x * MAP_WIDTH
        chunk_start_y = chunk_y * MAP_HEIGHT

        chunk_obj = world.chunks[chunk_x][chunk_y]

        for y in range(chunk_y, chunk_start_y + self.height):
            for x in range(chunk_start_x, chunk_start_x + self.width):
                world.world_map[x][y] = Tile(False, type_of=sand) # offloading means saving things into the big world_map 

                # pos_in_chunk_x, pos_in_chunk_y = utils.get_pos_in_chunk(x, y)
                # chunk_obj.tiles[pos_in_chunk_x][pos_in_chunk_y] = Tile(False, type_of=sand)

        chunk_obj.discovered = True

    def randomize_sand(self, chunk_x, chunk_y, world):

        chunk_obj = world.chunks[chunk_x][chunk_y]

        for y in range(1, self.height):
            for x in range(1, self.width):
                if chunk_obj.tiles[x][y].type_of == sand:
                    chunk_obj.tiles[x][y] = Tile(False, type_of=sand)
        print("dupa")
        self.current_chunk = chunk_obj

    def restore_chunk(self, chunk_x, chunk_y, entities, player, world):

        chunk_obj = world.chunks[chunk_x][chunk_y]

        for y in range(1, self.height):
            for x in range(1, self.width):

                chunk_obj.tiles[x][y] = Tile(False, type_of=sand)


        # Append offloaded objects in chunk.
        restored_entities = [player] 
        restored_entities.extend(chunk_obj.objects)
        self.current_chunk = chunk_obj
        
        return restored_entities


    def place_entities(self, entities):

        self.place_enemies(entities)
        # place objects etc.

    def is_blocked(self, x, y):

        x, y = utils.get_pos_in_chunk(x, y)

        if self.current_chunk.tiles[x][y].blocked:
            return True

        return False

    def place_enemies(self, entities):

        enemies_num = randint(0, MAX_MONSTERS_PER_CHUNK)

        for _ in range(enemies_num):

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


    def remove_entities(self, player, entities):


        """
        Removes entites leaving only player. In future, it checks which one are close to the player and doesn't remove them.
        
        """

        return [player]

    def get_entities(self, player, entities):

        return [e for e in entities if e != player]
