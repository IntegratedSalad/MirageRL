import tcod
import utils
import constants
import tcod.event
from ui_objects import view
from input_handlers import *
from game_states import GameStates
from map_objects import fov_functions
from components.fighter import Fighter
from ui_objects import render_functions
from map_objects.game_map import GameMap
from map_objects.chunk import ChunkProperty
from map_objects.game_world import GameWorld
from engine_functions.new_game import init_new_game, init_game
from engine_functions.main_menu import main_menu
from entity import Entity, get_blocking_entities_at_location

def main():

    with tcod.console_init_root(constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT, f"{constants.title} {constants.version}",
                                fullscreen=False, order="F", renderer=tcod.RENDERER_SDL2) as root_console:

        tcod.console_set_default_foreground(0, tcod.white)

        title_screen_con = tcod.console.Console(constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT, order="F")
        key = tcod.Key()
        mouse = tcod.Mouse()

        game_state = GameStates.TITLE_SCREEN

        mode_chosen = None

        title_screen_options = ["New Game", "Load Game", "Quit Game"]

        # main menu

        if GameStates.TITLE_SCREEN and mode_chosen is None:

            # view_obj = view.View("title", title_screen_con, render_functions.render_title_screen, root_console, title_screen_options, action)

            # view_obj.render()
            pass



        initialization = init_new_game()
        game_world = initialization.get('game_world')
        player = initialization.get('player')
        game_map = initialization.get('game_map')
        entities = initialization.get('entities')
        close_entities = initialization.get('close_entities')
        start_chunk_pos_x = initialization.get('start_chunk_pos_x')
        start_chunk_pos_y = initialization.get('start_chunk_pos_y')


        game_state = GameStates.PLAYER_TURN

        map_console = tcod.console.Console(constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT, order="F")

        view_obj = view.View("map_screen", map_console, render_functions.render_map, root_console, player, entities, game_map)
        view_obj.render()
        tcod.console_flush()

        while not tcod.console_is_window_closed():

            tcod.sys_wait_for_event(tcod.EVENT_KEY_PRESS, key, mouse, True)
            action = handle_keys(key, movement_settings)


            if game_state == GameStates.PLAYER_TURN:

                action_move = action.get('move')
                action_exit = action.get('exit')
                action_fullscreen = action.get('fullscreen')
                action_pass = action.get('pass')

                player_turn_results = []

                if action_move:
                    dx, dy = action_move

                    """ Check if player entered new chunk """

                    pos_in_chunk_x, pos_in_chunk_y = utils.get_pos_in_chunk(player.x, player.y) 

                    if utils.enter_new_chunk(pos_in_chunk_x + dx, pos_in_chunk_y + dy):

                        """
                        Here is code for changing chunks.
                        If player.x, player.y + direction from action_move goes beyond the chunk area,
                        he is changing chunks.
                        We don't have to calculate in which way he went, because get_chunk_pos_from_player_pos does that automatically.
                        We don't have to calculate on what place in the next chunk he will appear, because in the render_functions file and
                        draw entity function, his position is calculated from world pos (0...WORLD_HEIGHT or _WIDTH) to (0...CHUNK_HEIGHT or _WIDTH).
                        Next, we create two sets - close_entities and all_entities. Then, we exclude close entities from all, and add those that are close,
                        to final entities list.
                        Offloaded entities are those who are far and won't chase the player. We are storing them in chunk.objects list.

                        """

                        old_chunk_x, old_chunk_y = game_world.get_chunk_pos_from_player_pos(player.x, player.y)

                        player.x += dx
                        player.y += dy

                        chunk_pos_x, chunk_pos_y = game_world.get_chunk_pos_from_player_pos(player.x, player.y)
                        if game_world.chunks[chunk_pos_x][chunk_pos_y].property == ChunkProperty.END:
                            print("END")

                        # process only these, which are far.

                        close_entities = set([e for e in entities if e.distance_to(player) < constants.DISTANCE_TO_PROCESS_ENTITY and e != player])
                        all_entities = set([e for e in entities if e != player])
                        to_offload = list(all_entities.difference(close_entities))

                        game_map.offload_chunk(game_world.chunks[old_chunk_x][old_chunk_y], player, list(to_offload))
                        entities = game_map.remove_entities(player, entities)
                        entities += list(close_entities)

                        print(f"CLOSE ENTITIES: {len(close_entities)}\nALL ENTITIES: {len(all_entities)}\nENTITIES TO OFFLOAD: {len(to_offload)}")

                        # Make new map
                        game_map = GameMap(constants.MAP_WIDTH, constants.MAP_HEIGHT, game_world.chunks[start_chunk_pos_x][start_chunk_pos_y])

                        if not game_world.chunks[chunk_pos_x][chunk_pos_y].discovered:
                            game_map.randomize_sand(chunk_pos_x, chunk_pos_y, game_world)
                        else:
                            new_entities = game_map.restore_chunk(chunk_pos_x, chunk_pos_y, entities, player, game_world)
                            entities = new_entities + list(close_entities)
                        ##

                    else:

                        if not game_map.is_blocked(player.x + dx, player.y + dy):

                            target = get_blocking_entities_at_location(entities, player.x + dx, player.y + dy)

                            if target:
                                # do damage etc.
                                attack_results = player.fighter.attack(target)
                                player_turn_results.extend(attack_results)

                            else:
                                player.move(dx, dy)

                    game_state = GameStates.ENEMY_TURN

                    for player_turn_result in player_turn_results:

                        message = player_turn_result.get('message')

                        if message:
                            print(message)

                if action_exit:
                    raise SystemExit()

                if action_fullscreen:
                    tcod.console_set_fullscreen(not tcod.console_is_fullscreen())

                if action_pass:
                    game_state = GameStates.ENEMY_TURN

            if game_state == GameStates.ENEMY_TURN:

                for entity in entities:
                    if entity.ai:
                        enemy_turn_results = entity.ai.take_turn(player, game_map, entities)

                        for enemy_turn_result in enemy_turn_results:

                            message = enemy_turn_result.get('message')
                            dead_entity = enemy_turn_result.get('dead')

                            if message:
                                print(message)

                            if dead_entity:
                                game_state = GameStates.PLAYER_DEATH
                                # player is dead
                                print(dead_entity.name + " is dead")


                if game_state != GameStates.PLAYER_DEATH:
                    game_state = GameStates.PLAYER_TURN


            if game_state == GameStates.PLAYER_DEATH:

                death_console = tcod.console.Console(constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT, order="F")

                action = handle_keys(key)

                if action.get('exit'):
                    raise SystemExit()

                view_obj = view.View("death_screen", death_console, render_functions.render_death_screen, root_console)


            view_obj.render()

            tcod.console_flush()

            tcod.sys_set_fps(60)


