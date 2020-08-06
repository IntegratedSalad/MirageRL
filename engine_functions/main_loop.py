import tcod
from misc import utils
from data.game_data import constants
import tcod.event
from ui_objects import view
from engine_functions.input_handlers import *
from engine_functions.game_states import GameStates
from map_objects import fov_functions
from components.fighter import Fighter
from ui_objects import render_functions
from map_objects.game_map import GameMap
from map_objects.chunk import ChunkProperty
# from map_objects.game_world import GameWorld
from engine_functions.new_game import init_new_game, init_game
from engine_functions.main_menu import main_menu
from components.entity import Entity, get_blocking_entities_at_location
from ui_objects.message import Message

def main_loop(root_con, key, mouse, current_view, game_world, player, game_map, entities, close_entities, mlog):

    render_args = None
    game_state = GameStates.PLAYER_TURN

    while not tcod.console_is_window_closed():

        tcod.sys_wait_for_event(tcod.EVENT_KEY_PRESS, key, mouse, True)

        action = handle_keys(key, movement_settings)

        if game_state == GameStates.PLAYER_TURN:

            action_move = action.get('move')
            action_exit = action.get('exit')
            action_fullscreen = action.get('fullscreen')
            action_pass = action.get('pass')
            action_save = action.get('save')
            action_get_item = action.get('get')

            if action_save:
                print("Saving...")
                return {'save': (game_world, game_map, player, entities, close_entities, mlog)}

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

                    close_entities = set(
                        [e for e in entities if e.distance_to(player) < constants.DISTANCE_TO_PROCESS_ENTITY and e != player])
                    all_entities = set([e for e in entities if e != player])
                    to_offload = list(all_entities.difference(close_entities))

                    game_map.offload_chunk(game_world.chunks[old_chunk_x][old_chunk_y], player, list(to_offload))
                    entities = game_map.remove_entities(player, entities)
                    entities += list(close_entities)

                    print(chunk_pos_x, chunk_pos_y)
                    print(game_world.chunks[chunk_pos_x][chunk_pos_y].discovered)

                    # print(
                    #     f"CLOSE ENTITIES: {len(close_entities)}\nALL ENTITIES: {len(all_entities)}\nENTITIES TO OFFLOAD: {len(to_offload)}")

                    # # Make new map
                    game_map = GameMap(constants.MAP_WIDTH, constants.MAP_HEIGHT,
                                       game_world.chunks[chunk_pos_x][chunk_pos_y])

                    if not game_world.chunks[chunk_pos_x][chunk_pos_y].discovered:
                        game_map.randomize_sand(chunk_pos_x, chunk_pos_y, game_world)
                    else:
                        # here we should randomize...
                        new_entities = game_map.restore_chunk(chunk_pos_x, chunk_pos_y, entities, player, game_world)
                        entities = new_entities + list(close_entities)
                    ##

                else:
                    for e in entities:
                        print(e.name)

                    if not game_map.is_blocked(player.x + dx, player.y + dy):

                        target = get_blocking_entities_at_location(entities, player.x + dx, player.y + dy)

                        if target:
                            # do damage etc.
                            attack_results = player.fighter.attack(target)
                            player_turn_results.extend(attack_results)

                        else:
                            player.move(dx, dy)

                game_state = GameStates.ENEMY_TURN

                # for player_turn_result in player_turn_results:

                #     received_msg = player_turn_result.get('message')
                #     received_dead_entity = player_turn_result.get('dead')

                #     if received_msg:
                #         msg = Message(received_msg, (255, 255, 255))
                #         mlog.add_msg(msg)

                #     if received_dead_entity:
                #         received_dead_entity.fighter.die()
                #         msg = Message(f"{received_dead_entity.name.capitalize()} is dead.", constants.COLOR_DARK_RED)
                #         mlog.add_msg(msg)


            if action_exit:
                raise SystemExit()

            if action_fullscreen:
                tcod.console_set_fullscreen(not tcod.console_is_fullscreen())

            if action_pass:
                game_state = GameStates.ENEMY_TURN

            if action_get_item:
                get_item_results = player.fighter.get_item(entities, game_map)
                if get_item_results is not None:
                    player_turn_results.extend(get_item_results)
                game_state = GameStates.ENEMY_TURN

            for player_turn_result in player_turn_results:

                received_msg = player_turn_result.get('message')
                received_dead_entity = player_turn_result.get('dead')

                if received_msg:
                    msg = Message(received_msg, (255, 255, 255))
                    mlog.add_msg(msg)

                if received_dead_entity:
                    received_dead_entity.fighter.die()
                    msg = Message(f"{received_dead_entity.name.capitalize()} is dead.", constants.COLOR_DARK_RED)
                    mlog.add_msg(msg)

            current_view.consoles['view_MAP']['args'] = (player, entities, game_map)

        if game_state == GameStates.ENEMY_TURN:

            for entity in entities:
                if entity.ai:
                    enemy_turn_results = entity.ai.take_turn(player, game_map, entities)

                    for enemy_turn_result in enemy_turn_results:

                        received_message = enemy_turn_result.get('message')
                        received_dead_entity = enemy_turn_result.get('dead')

                        if received_message:
                            msg = Message(received_message, (255, 255, 255))
                            mlog.add_msg(msg)

                        if received_dead_entity:
                            game_state = GameStates.PLAYER_DEATH
                            # player is dead
                            mlog.add_msg(f"{received_dead_entity.name} is dead.", (255, 255, 255))
                            entity.fighter.die()

            if game_state != GameStates.PLAYER_DEATH:
                game_state = GameStates.PLAYER_TURN

        if game_state == GameStates.PLAYER_DEATH:

            death_console = tcod.console.Console(constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT, order="F")

            action = handle_keys(key, movement_settings)

            if action.get('exit'):
                raise SystemExit()

            current_view = view.View("death_screen", death_console, render_functions.render_death_screen, root_con)

        current_view.render()

        tcod.console_flush()

        tcod.sys_set_fps(60)
