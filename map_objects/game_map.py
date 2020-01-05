import tcod
import utils
from constants import *
from entity import Entity
from random import randint
# from data.item_data import item_dat
from data.monster_data import mon_dat
from map_objects.tile import Tile
from map_objects.tile_types import *
from components.fighter import Fighter
from components.ai import BasicMonster
from map_objects.chunk import MapElevation

class GameMap:

    """
    Current map.
    This class and its functions operate on chunk and world_map tiles.

    """

    def __init__(self, width, height, current_chunk):
        self.width = width # of chunk
        self.height = height # of chunk
        self.elevation = MapElevation.ELEV_ABOVE
        self.current_chunk = current_chunk # an area of gameplay

    def offload_chunk(self, chunk, player, entities):

        chunk.discovered = True
        chunk.objects = self.get_entities(player, entities)

        # offload items

    def randomize_sand(self, chunk_x, chunk_y, world):

        chunk_obj = world.chunks[chunk_x][chunk_y]

        for y in range(0, self.height):
            for x in range(0, self.width):
                if chunk_obj.tiles[x][y].type_of == sand:
                    chunk_obj.tiles[x][y] = Tile(False, type_of=sand)

        self.current_chunk = chunk_obj

    def restore_chunk(self, chunk_x, chunk_y, entities, player, world):

        chunk_start_x = chunk_x * MAP_WIDTH
        chunk_start_y = chunk_y * MAP_HEIGHT

        chunk_obj = world.chunks[chunk_x][chunk_y]

        for y in range(chunk_start_y, chunk_start_y + self.height):
            for x in range(chunk_start_x, chunk_start_x + self.width):
                #restore items
                pass

        # Append offloaded objects in chunk.
        restored_entities = [player] 
        restored_entities.extend(chunk_obj.objects)
        self.current_chunk = chunk_obj
        
        return restored_entities


    def place_entities(self, chunk_x, chunk_y, entities):

        self.place_enemies(chunk_x, chunk_y, entities)
        # place objects etc.

    def is_blocked(self, x, y):

        x, y = utils.get_pos_in_chunk(x, y)

        if self.current_chunk.tiles[x][y].blocked:
            return True

        return False

    def place_enemies(self, chunk_x, chunk_y, entities):

        enemies_num = randint(1, MAX_MONSTERS_PER_CHUNK)

        for _ in range(0, enemies_num):

            x = chunk_x * MAP_WIDTH + randint(0, self.width - 1)
            y = chunk_y * MAP_HEIGHT + randint(0, self.height - 1)

            if not any([entity for entity in entities if entity.x == x and entity.y == y]):

                if randint(0, 100) < 50:

                    m_glyph, m_color, m_name, m_fighter_stats, m_ai, m_ai_args = mon_dat.monsters['dessert_snake']

                else:
                    m_glyph, m_color, m_name, m_fighter_stats, m_ai, m_ai_args = mon_dat.monsters['dessert_snake']


            m_color_r, m_color_g, m_color_b = m_color
            m_hp, m_def, m_atkval = m_fighter_stats
            
            monster_fighter_component = Fighter(m_hp, m_def, m_atkval)
            monster = Entity(x, y, m_glyph, tcod.color.Color(m_color_r, m_color_g, m_color_b), m_name, blocks=True, fighter=monster_fighter_component, ai=m_ai())
            entities.append(monster)


    def remove_entities(self, player, entities):


        """
        Removes entites leaving only player. In future, it checks which one are close to the player and doesn't remove them.
        
        """

        return [player]

    def get_entities(self, player, entities):

        return [e for e in entities if e != player]
