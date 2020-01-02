import tcod
import tcod.event
import constants
import render_functions
import utils
from map_objects import fov_functions
from input_handlers import handle_keys
from entity import Entity, get_blocking_entities_at_location
from map_objects.game_map import GameMap, GameWorld, ChunkProperty
# from map_objects.game_world import GameWorld
from game_states import GameStates
from components.fighter import Fighter
from components.ai import BasicMonster

def main():


    game_world = GameWorld()
    player_fighter_component = Fighter(8, 2, 1)
    player = Entity(int((constants.WORLD_WIDTH * constants.MAP_WIDTH / 2) + constants.MAP_WIDTH / 2), int((constants.WORLD_HEIGHT * constants.MAP_HEIGHT / 2) + constants.MAP_HEIGHT / 2), '@', tcod.white, constants.PLAYER_NAME, fighter=player_fighter_component)
    px, py = game_world.get_chunk_pos_from_player_pos(player.x, player.y)
    game_world.chunks[px][py].property = ChunkProperty.START
    start_chunk_pos_x, start_chunk_pos_y = game_world.get_chunk_pos_from_player_pos(player.x, player.y)
    game_map = GameMap(constants.MAP_WIDTH, constants.MAP_HEIGHT, game_world.chunks[start_chunk_pos_x][start_chunk_pos_y])
    print(f"PLAYER POS: {player.x}, {player.y}")

    print(f"CURRENT CHUNK: {game_world.get_chunk_pos_from_player_pos(player.x, player.y)}")

    entities = [player]
    # game_map.place_entities(entities)

    tcod.console_set_custom_font('terminal8x8_gs_tc.png', tcod.FONT_TYPE_GREYSCALE | tcod.FONT_LAYOUT_TCOD)
   
    with tcod.console_init_root(constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT, f"{constants.title} {constants.version}",
                                fullscreen=False, order="F", renderer=tcod.RENDERER_SDL2) as root_console:


        #init():

        con = tcod.console.Console(constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT, order="F")
        key = tcod.Key()
        mouse = tcod.Mouse()

        game_state = GameStates.PLAYER_TURN

        render_functions.render_all(con, root_console, entities, game_map, constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT)
        tcod.console_flush()

        while not tcod.console_is_window_closed():

            # run():

            tcod.sys_wait_for_event(tcod.EVENT_KEY_PRESS, key, mouse, True)

            tcod.console_set_default_foreground(0, tcod.white)

            if game_state == GameStates.PLAYER_TURN:

                action = handle_keys(key)

                action_move = action.get('move')
                action_exit = action.get('exit')
                action_fullscreen = action.get('fullscreen')

                player_turn_results = []

                if action_move:
                    dx, dy = action_move

                    """ Check if player entered new chunk """

                    pos_in_chunk_x, pos_in_chunk_y = utils.get_pos_in_chunk(player.x, player.y) 

                    did_enter_new_chunk = utils.enter_new_chunk(pos_in_chunk_x + dx, pos_in_chunk_y + dy)
                    
                    if did_enter_new_chunk is not None:

                        old_chunk_x, old_chunk_y = game_world.get_chunk_pos_from_player_pos(player.x, player.y)
                        game_world.chunks[old_chunk_x][old_chunk_y].discovered = True

                        player.x += dx
                        player.y += dy

                        chunk_pos_x, chunk_pos_y = game_world.get_chunk_pos_from_player_pos(player.x, player.y)
                        print(game_world.chunks[chunk_pos_x][chunk_pos_y].discovered)

                        """Place this procedure in map and world classes accordingly."""


                        """Make better algorithm for that:


                        1. Offload entities and tiles if they are any.
                        2. Remove entities and tiles.
                        3. Update position of player.
                        4. Check if we are entering a new area (create enemies) or we are re-entering a previously visited area (restore enemies)
                        

                        """

                        # px, py, wx, wy = did_enter_new_chunk

                        print((player.x, player.y))
                        print(utils.get_pos_in_chunk(player.x, player.y))

                        # offload entities

                        # objects_to_offload = game_map.get_entities(player, entities)

                        # if game_world.get_current_chunk().objects == []:
                        #     game_world.get_current_chunk().objects = objects_to_offload
                        # else:
                        #     pass

                        # offloads
                        ##

                        # remove entities while keeping the player
                        entities = game_map.remove_entities(player, entities)

                        # update position of the player in world.
                        # game_world.update_position(wx, wy)
                        # We are in a new chunk

                        # if end
                        # print(f"PLAYER POS: {game_world.player_pos_x_in_world}, {game_world.player_pos_y_in_world}")
                        # if game_world.world[game_world.player_pos_x_in_world][game_world.player_pos_y_in_world].property == ChunkProperty.END:
                        #     print("You reached the end boi.")
                        ##

                        # Make new map
                        game_map = GameMap(constants.MAP_WIDTH, constants.MAP_HEIGHT, game_world.chunks[start_chunk_pos_x][start_chunk_pos_y])
                        # print(game_world.chunks[chunk_pos_x][chunk_pos_y])
                        print((chunk_pos_x, chunk_pos_y))

                        if not game_world.chunks[chunk_pos_x][chunk_pos_y].discovered:
                            game_map.randomize_sand(chunk_pos_x, chunk_pos_y, game_world)
                        else:
                            # We can place these positions, because they were updated in .update_position(wx, wy)
                            new_entities = game_map.restore_chunk(chunk_pos_x, chunk_pos_y, entities, player, game_world)
                            entities = new_entities
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
                                print(player.x, player.y)
                                print(utils.get_pos_in_chunk(player.x, player.y))

                    game_state = GameStates.ENEMY_TURN

                    # see if player walked to a new area. (chunk)

                if action_exit:
                    raise SystemExit()

                if action_fullscreen:
                    tcod.console_set_fullscreen(not tcod.console_is_fullscreen())

            if game_state == GameStates.ENEMY_TURN:

                for entity in entities:
                    if entity.ai:
                        enemy_turn_results = entity.ai.take_turn(player, game_map, entities)
                        #sprint(enemy_turn_results)

                        for enemy_turn_result in enemy_turn_results:

                            message = enemy_turn_result.get('message')
                            dead_entity = enemy_turn_result.get('dead')

                            if message:
                                print(message)

                            if dead_entity:
                                pass 

                game_state = GameStates.PLAYER_TURN

            render_functions.render_all(con, root_console, entities, game_map, constants.SCREEN_WIDTH, \
                                        constants.SCREEN_HEIGHT)


            tcod.console_flush()

            tcod.sys_set_fps(60)
            
