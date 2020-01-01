import tcod
from map_objects.game_map import MapElevation
from utils import get_pos_in_chunk

def render_all(con, entities, current_game_map, screen_width, screen_height):

    for y in range(1, current_game_map.height):
        for x in range(1, current_game_map.width):

            if current_game_map.elevation == MapElevation.ELEV_BELOW:
                # add here fov and desaturate with value put in constants
                pass

            tile = current_game_map.current_chunk.tiles[x][y]
            tcod.console_put_char_ex(con, x, y, tile.char, tile.color, (0, 0, 0))

    for entity in entities:
        draw_entity(con, entity)

    tcod.console_blit(con, 0, 0, screen_height, screen_width, 0, 0, 0)

    clear_all(con, entities)


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
