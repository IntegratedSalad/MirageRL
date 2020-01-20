import tcod
import constants
import textwrap
from map_objects.chunk import MapElevation
from utils import get_pos_in_chunk, get_chunk_pos
from ui_objects.draw_functions import *
from get_art import get_title

"""
Every function must have con and root_con in args. (for now)
Render functions are logic that is displayed in consoles.

"""


def render_map(con, root_con, player, entities, current_game_map):

    """Map is what's happening in the game."""

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

    con.blit(dest=root_con, dest_x=1, dest_y=1, src_x=0, src_y=0, width=constants.MAP_WIDTH, height=constants.MAP_HEIGHT)

    clear_all(con, entities)

def render_title_screen(con, root_con, options, **key_handler):
    option = draw_menu(con, 0, 0, width=constants.SCREEN_WIDTH, height=constants.SCREEN_HEIGHT, options=options, key_handler=key_handler)
    draw_text(con, constants.SCREEN_WIDTH - len(constants.version), constants.SCREEN_HEIGHT - 1, constants.version, (255, 255, 255))
    draw_text(con, 47, 15, "RL", (245, 183, 60))
    draw_graphics(con, 9, 6, get_title(), (245, 183, 60))

    if option is not None:
        return option

    con.blit(dest=root_con, dest_x=0, dest_y=0, src_x=0, src_y=0, width=constants.SCREEN_WIDTH, height=constants.SCREEN_HEIGHT)
    
def render_messages(con, root_con, msglog):

    for message in reversed(msglog.messages):

        y = 0

        # if len(message) > constants.MAP_WIDTH: <- wrap!
        #     pass

        draw_text(con, 0, y, message.text, message.fgcolor, message.bgcolor)

        y += 1 


    con.blit(dest=root_con, dest_x=1, dest_y=constants.MAP_HEIGHT + 2, src_x=0, src_y=0, width=constants.MAP_WIDTH, height=constants.MESSAGES_ON_SCREEN)

def render_esc_menu():
    pass

def render_death_screen(con, root_con):

    draw_text(con, int(constants.SCREEN_WIDTH / 2) - int(len("You have perished.") / 2), int(constants.SCREEN_HEIGHT / 2), "You have perished", tcod.color.Color(100, 0, 0))

    con.blit(dest=root_con, dest_x=0, dest_y=0, src_x=0, src_y=0, width=constants.SCREEN_WIDTH, height=constants.SCREEN_HEIGHT)
    

def clear_all(con, entities):
    for entity in entities:
        clear_entity(con, entity)

def draw_entity(con, entity):
    tcod.console_set_default_foreground(con, entity.color)
    if entity.name == 'Pysio':
        print(entity.x, entity.y)
    x, y = get_pos_in_chunk(entity.x, entity.y)
    tcod.console_put_char(con, x, y, entity.char, tcod.BKGND_NONE)

def clear_entity(con, entity):
    x, y = get_pos_in_chunk(entity.x, entity.y)
    tcod.console_put_char(con, x, y, ' ', tcod.BKGND_NONE)
