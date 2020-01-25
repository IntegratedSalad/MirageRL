from data.game_data.constants import *
from map_objects.tile import Tile
from random import randint, choice
from map_objects.chunk import Chunk
from map_objects.tile_types import *
from map_objects.chunk import ChunkProperty

class GameWorld:

    """
    Handles chunks initialization and world related features.
    Accessing chunks is done via self.world_map list.

    """


    def __init__(self):
        self.world_map = [[Tile(False, type_of=sand) for y in range(0, WORLD_HEIGHT * MAP_HEIGHT)] for x in range(0, WORLD_WIDTH * MAP_WIDTH)]
        self.chunks = self.initialize_chunks()
        self.gate_place = []
        self.create_village()
        self.place_glyphs()

        for x in range(0, WORLD_WIDTH):
            for y in range(0, WORLD_HEIGHT):
                if self.chunks[x][y].property == ChunkProperty.END:
                    print(f"END CHUNK: {x}, {y}")
    

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

        border = randint(0, 3) # clockwise, 0 is top.

        if border == 0:
            start_x = randint(0, WORLD_WIDTH - size)
            for _ in range(size):
                self.chunks[start_x][0].property = ChunkProperty.END

                self.gate_place.append((start_x, 0))

                start_x += 1

        if border == 1:
            start_y = randint(0, WORLD_HEIGHT - size)
            for _ in range(size):
                self.chunks[WORLD_WIDTH - 1][start_y].property = ChunkProperty.END

                self.gate_place.append((WORLD_WIDTH - 1, start_y))

                start_y += 1

        if border == 2:
            start_x = randint(0, WORLD_WIDTH - size)
            for _ in range(size):
                self.chunks[start_x][WORLD_HEIGHT - 1].property = ChunkProperty.END

                self.gate_place.append((start_x, WORLD_HEIGHT - 1))

                start_x += 1

        if border == 3:
            start_y = randint(0, WORLD_HEIGHT - size)
            for _ in range(size):
                self.chunks[0][start_y].property = ChunkProperty.END

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
                self.chunks[rand_map_place_x][rand_map_place_y].tiles[rand_chunk_place_x][rand_chunk_place_y] = Tile(False, type_of=arrow_left)


            elif difference_x >= -1 and difference_y < 0:
                self.chunks[rand_map_place_x][rand_map_place_y].tiles[rand_chunk_place_x][rand_chunk_place_y] = Tile(False, type_of=arrow_up)


            elif difference_x > -2 and difference_y > 0:
                self.chunks[rand_map_place_x][rand_map_place_y].tiles[rand_chunk_place_x][rand_chunk_place_y] = Tile(False, type_of=arrow_right)


            elif difference_x >= -1 and difference_y > 0: # GATE_CORD_Y - GLYPH_Y > 0 means that gate has greater y - is further down.
                self.chunks[rand_map_place_x][rand_map_place_y].tiles[rand_chunk_place_x][rand_chunk_place_y] = Tile(False, type_of=arrow_down)

            self.chunks[rand_map_place_x][rand_map_place_y].property = ChunkProperty.HAS_DIRECTION
