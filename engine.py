import tcod
# import utils
import constants
import tcod.event
from ui_objects import view
from input_handlers import *
# from game_states import GameStates
# from map_objects import fov_functions
# from components.fighter import Fighter
from ui_objects import render_functions
# from map_objects.game_map import GameMap
# from map_objects.chunk import ChunkProperty
# from map_objects.game_world import GameWorld
from engine_functions.new_game import init_new_game, init_game
from engine_functions.main_menu import main_menu
# from entity import Entity, get_blocking_entities_at_location

def main():

    with tcod.console_init_root(constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT, f"{constants.title} {constants.version}",
                                fullscreen=False, order="F", renderer=tcod.RENDERER_SDL2) as root_console:

        key = tcod.Key()
        mouse = tcod.Mouse()


        tcod.console_set_default_foreground(0, tcod.white)
        title_screen_options = ["New Game", "Load Game", "Quit Game"]

        menu_key_handler = handle_keys(key, title_screen_settings)
        title_screen_con = tcod.console.Console(constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT, order="F")
        title_screen_menu = view.View("title_screen", title_screen_con, render_functions.render_title_screen, root_console, title_screen_options)
        map_console = tcod.console.Console(constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT, order="F")
        map_view = view.View("map_screen", map_console, render_functions.render_map, root_console, player, entities, game_map)

        while not tcod.console_is_window_closed():

            tcod.sys_wait_for_event(tcod.EVENT_KEY_PRESS, key, mouse, True)

            option = title_screen_menu.menu_returns.get('option')
            if option == 'New Game':
                state = main_loop(option, map_view, root_console, key, mouse)

            else:
                if option is not None:
                    raise SystemExit()


            title_screen_menu.render()
