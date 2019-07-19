import tcod
import tcod.event
import constants
import render_functions
from input_handlers import handle_keys
from entity import Entity
from map_objects.game_map import GameMap

def main():

    game_map = GameMap(constants.MAP_WIDTH, constants.MAP_HEIGHT)

    player = Entity(int(constants.MAP_WIDTH / 2), int(constants.MAP_HEIGHT / 2), '@', tcod.white)

    entities = [player]
    tcod.console_set_custom_font('terminal8x8_gs_tc.png', tcod.FONT_TYPE_GREYSCALE | tcod.FONT_LAYOUT_TCOD)
    #with tcod.console_init_root(constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT, 'MirageRL',
    #                            fullscreen=False, order="F", renderer=tcod.RENDERER_SDL2) as root_console:

    with tcod.console_init_root(constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT, 'MirageRL',
                                fullscreen=False, order="F", renderer=tcod.RENDERER_SDL2) as root_console:

        con = tcod.console_new(constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT)
        key = tcod.Key()
        mouse = tcod.Mouse()

        render_functions.render_all(con, entities, game_map, constants.SCREEN_WIDTH, \
                                        constants.SCREEN_HEIGHT)
        tcod.console_flush()

        while not tcod.console_is_window_closed():

            tcod.sys_wait_for_event(tcod.EVENT_KEY_PRESS, key, mouse, True)

            tcod.console_set_default_foreground(0, tcod.white)

            action = handle_keys(key)

            action_move = action.get('move')
            action_exit = action.get('exit')
            action_fullscreen = action.get('fullscreen')

            if action_move:
                dx, dy = action_move
                if not game_map.is_blocked(player.x + dx, player.y + dy):
                    player.move(dx, dy)

            if action_exit:
                raise SystemExit()

            if action_fullscreen:
                tcod.console_set_fullscreen(not tcod.console_is_fullscreen())


            render_functions.render_all(con, entities, game_map, constants.SCREEN_WIDTH, \
                                        constants.SCREEN_HEIGHT)
            tcod.console_flush()

            tcod.sys_set_fps(60)
            
