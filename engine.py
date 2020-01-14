import tcod
# import utils
import constants
import tcod.event
from ui_objects import view
from ui_objects import option_menu
from input_handlers import *
# from game_states import GameStates
# from map_objects import fov_functions
# from components.fighter import Fighter
from ui_objects import render_functions
from ui_objects.draw_functions import draw_text
# from map_objects.game_map import GameMap
# from map_objects.chunk import ChunkProperty
# from map_objects.game_world import GameWorld
from engine_functions.new_game import init_new_game, init_game
from engine_functions.main_menu import main_menu
from engine_functions.main_loop import main_loop
# from entity import Entity, get_blocking_entities_at_location

def main():

    with tcod.console_init_root(constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT, f"{constants.title} {constants.version}",
                                fullscreen=False, order="F", renderer=tcod.RENDERER_SDL2) as root_console:

        key = tcod.Key()
        mouse = tcod.Mouse()

        tcod.console_set_default_foreground(0, tcod.white)
        title_screen_options = ["New Game", "Load Game", "Quit Game"]
        title_screen_con = tcod.console.Console(constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT, order="F")
        title_screen_menu = option_menu.OptionMenu(
                                    "title_screen", 
                                    title_screen_con, 
                                    None, 
                                    render_functions.render_title_screen, 
                                    title_screen_con, 
                                    root_console,  
                                    title_screen_options, 
                                    key_handler={}
                                    )

        menu_key_handler = handle_keys(key, title_screen_settings)
        title_screen_menu.render(menu_key_handler)
        tcod.console_flush()

        option = None

        while option is None:
            tcod.sys_wait_for_event(tcod.EVENT_KEY_PRESS, key, mouse, True)

            menu_key_handler = handle_keys(key, title_screen_settings)

            option = title_screen_menu.render(menu_key_handler)

            tcod.console_flush()

            if option == 'New Game':
                title_screen_con.clear()
                draw_text(title_screen_con, int((constants.SCREEN_WIDTH / 2) - 8), int(constants.SCREEN_HEIGHT / 2), "Loading...", (255, 255, 255))
                title_screen_con.blit(dest=root_console, dest_x=0, dest_y=0, src_x=0, src_y=0, width=constants.SCREEN_WIDTH, height=constants.SCREEN_HEIGHT)
                tcod.console_flush()
                break

            if option == 'Quit Game' or tcod.console_is_window_closed():
                raise SystemExit()

        initialization = init_new_game()
        game_world = initialization.get('game_world')
        player = initialization.get('player')
        game_map = initialization.get('game_map')
        entities = initialization.get('entities')
        close_entities = initialization.get('close_entities')
        start_chunk_pos_x = initialization.get('start_chunk_pos_x')
        start_chunk_pos_y = initialization.get('start_chunk_pos_y')

        map_console = tcod.console.Console(constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT, order="F")
        current_view_game_map = view.View("map_screen", map_console, render_functions.render_map, root_console, player, entities, game_map)
        current_view_game_map.render()
        tcod.console_flush()

        while not tcod.console_is_window_closed():

            tcod.sys_wait_for_event(tcod.EVENT_KEY_PRESS, key, mouse, True)

            state = main_loop(root_console, key, mouse, current_view_game_map, game_world, player, game_map, entities, close_entities, start_chunk_pos_x, start_chunk_pos_y)

            tcod.console_flush()

            tcod.sys_set_fps(60)
