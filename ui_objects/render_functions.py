import tcod
from data.game_data import constants
import textwrap
from map_objects.chunk import MapElevation
from misc.utils import get_pos_in_chunk, get_chunk_pos
from ui_objects.draw_functions import *
from ui_objects.get_art import get_title

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

    for entity in sorted(entities, key=lambda x: x.render_order.value):
        
        player_chunk = get_chunk_pos(player.x, player.y)
        entity_chunk = get_chunk_pos(entity.x, entity.y)

        if player_chunk == entity_chunk: # without this, entity close to the player (which we are processing) would appear on player's chunk.
            draw_entity(con, entity)

    con.blit(dest=root_con, dest_x=1, dest_y=1, src_x=0, src_y=0, width=constants.MAP_WIDTH, height=constants.MAP_HEIGHT)

    clear_all(con, entities)

def render_title_screen(con, root_con, options, **kwargs):

    key_handler = kwargs.get('key_handler')

    option = draw_menu(con, constants.STARTING_MENU_X, constants.STARTING_MENU_Y, width=constants.SCREEN_WIDTH, height=constants.SCREEN_HEIGHT, options=options, key_handler=key_handler)
    draw_text(con, constants.SCREEN_WIDTH - len(constants.version), constants.SCREEN_HEIGHT - 1, constants.version, (255, 255, 255))
    draw_graphics(con, 14, 6, get_title(), (245, 183, 60))
    draw_text(con, 52, 22, "RL", (245, 183, 60))

    con.blit(dest=root_con, dest_x=0, dest_y=0, src_x=0, src_y=0, width=constants.SCREEN_WIDTH, height=constants.SCREEN_HEIGHT)

    if option is not None:
        return option

    
def render_messages(con, root_con, msglog):

    y = 0

    for message in reversed(msglog.messages):

        # if len(message) > constants.MAP_WIDTH: <- wrap!
        #     pass

        draw_text(con, 0, y, message.text, message.fgcolor, message.bgcolor)

        y += 1 


    con.blit(dest=root_con, dest_x=1, dest_y=constants.MAP_HEIGHT + 2, src_x=0, src_y=0, width=constants.MSGS_WIDTH, height=constants.MESSAGES_ON_SCREEN)

def render_stats(con, root_con, *args):

    player = args[0]

    draw_text(con, 1, 1, f"HP: {str(player.hp)}", (240, 0, 0))

    con.blit(dest=root_con, dest_x=constants.MAP_WIDTH + 1, dest_y=1, src_x=0, src_y=0, width=constants.STAT_WIDTH, height=constants.STAT_HEIGHT)

def render_inventory_menu(con, root_con, options, **kwargs):
    """
    Options is just a inventory list.
    Data is a list o dictionary of additional elements to print.

    Divide it into two cons?

    BUG: WHEN EFFECT DOES NOT APPLY, IT RENDERS ITS DESCRIPTION ANYWAY.

    """

    key_handler = kwargs.get('key_handler')
    data = kwargs.get('data')

    _x = 1
    _y = 1

    option = draw_menu(con, _x, _y, width=constants.INVENTORY_MAIN_WINDOW_WIDTH, height=constants.INVENTORY_MAIN_WINDOW_HEIGHT, options=options, key_handler=key_handler)

    if len(options) > 0:
        current_option_descr_str = options[variables.title_screen_choice].item.description

        for obj in options:

            attributes = list(obj.item.attributes.values())

            __x = 2 # icon is printed 2 characters after item name.
            __y = return_lines_of_wrapped_text(current_option_descr_str, constants.INVENTORY_SECONDARY_WINDOW_WIDTH) + 6
            # Description of attribute of an object is printed 2 characters after the description

            for attr in attributes:

                applies, _, icon, color, desc = attr
                if applies:

                    print()
                    print()
                    print()
                    print(applies)
                    print(desc)
                    draw_text(con, len(obj.name) + __x, _y, icon, color)
                    draw_text(con, 40, __y, desc, color)

                __x += 1
                __y += 1

            _y += 1

        current_option_name_str = options[variables.title_screen_choice].name
        len_current_option = len(current_option_name_str)
        center = int(constants.INVENTORY_SECONDARY_WINDOW_WIDTH / 2) + 41
        pos = center - int(len_current_option / 2)

        draw_text(con, pos, 2, current_option_name_str, (255, 255, 255)) # Name of the item in the secondary window.

        draw_text(con, 40, 5, current_option_descr_str, (255, 255, 255), custom_width=constants.INVENTORY_SECONDARY_WINDOW_WIDTH) # Description of the item in the secondary window.

    draw_framing(con, 0, 0, chr(177), 39, constants.SCREEN_HEIGHT - 4, (217, 217, 0), (0, 0, 0)) # Main inv window framing
    draw_framing(con, 38, 0, chr(177), 30, constants.SCREEN_HEIGHT - 4, (217, 217, 0), (0, 0, 0)) # Second inv window framing

    con.blit(dest=root_con, dest_x=0, dest_y=4, src_x=0, src_y=0, width=constants.SCREEN_WIDTH, height=constants.SCREEN_HEIGHT)

    if option is not None:
        return option

def render_esc_menu():
    pass

def render_death_screen(con, root_con):

    draw_text(con, int(constants.SCREEN_WIDTH / 2) - int(len("You have perished.") / 2), int(constants.SCREEN_HEIGHT / 2), "You have perished", 
        tcod.color.Color(100, 0, 0))

    con.blit(dest=root_con, dest_x=0, dest_y=0, src_x=0, src_y=0, width=constants.SCREEN_WIDTH, height=constants.SCREEN_HEIGHT)
    

def clear_all(con, entities):
    # add render priority.
    for entity in entities:
        clear_entity(con, entity)

def draw_entity(con, entity):
    tcod.console_set_default_foreground(con, entity.color)
    x, y = get_pos_in_chunk(entity.x, entity.y)
    tcod.console_put_char(con, x, y, entity.char, tcod.BKGND_NONE)

def clear_entity(con, entity):
    x, y = get_pos_in_chunk(entity.x, entity.y)
    tcod.console_put_char(con, x, y, ' ', tcod.BKGND_NONE)
