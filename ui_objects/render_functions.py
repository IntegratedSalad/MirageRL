import tcod
import constants
from map_objects.chunk import MapElevation
from utils import get_pos_in_chunk, get_chunk_pos

def render_map(con, root_con, player, entities, current_game_map, screen_width, screen_height):

    for y in range(0, current_game_map.height):
        for x in range(0, current_game_map.width):

            if current_game_map.elevation == MapElevation.ELEV_BELOW:
                # add here fov and desaturate with value put in constants
                pass

            tile = current_game_map.current_chunk.tiles[x][y]
            tcod.console_put_char_ex(con, x, y, tile.char, tile.color, (0, 0, 0))

    for entity in entities:
        
        player_chunk = get_chunk_pos(player.x, player.y)
        entity_chunk = get_chunk_pos(entity.x, entity.y)

        if player_chunk == entity_chunk: # without this, entity close to the player (which we are processing) would appear on player's chunk.
            draw_entity(con, entity)

    con.blit(dest=root_con, dest_x=1, dest_y=1, src_x=0, src_y=0, width=screen_width, height=screen_height)

    clear_all(con, entities)

def render_esc_menu():
    pass

def clear_all(con, entities):
    for entity in entities:
        clear_entity(con, entity)

def draw_entity(con, entity):
    tcod.console_set_default_foreground(con, entity.color)
    x, y = get_pos_in_chunk(entity.x, entity.y)
    tcod.console_put_char(con, x, y, entity.char, tcod.BKGND_NONE)

def clear_entity(con, entity):
    x, y = get_pos_in_chunk(entity.x, entity.y)
    tcod.console_put_char(con, x, y, ' ', tcod.BKGND_NONE)