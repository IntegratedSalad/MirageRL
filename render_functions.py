import tcod

def render_all(con, entities, game_map, screen_width, screen_height, colors):

    for y in range(game_map.height):
        for x in range(game_map.width):

            wall = game_map.map[x][y].block_sight
            if wall:
                tcod.console_set_default_foreground(con, tcod.white)
                tcod.console_put_char(con, x, y, '#', tcod.BKGND_NONE)
            else:
                tcod.console_set_default_foreground(con, tcod.grey)
                tcod.console_put_char(con, x, y, '.', tcod.BKGND_NONE)

    for entity in entities:
        draw_entity(con, entity)

    tcod.console_blit(con, 0, 0, screen_height, screen_width, 0, 0, 0)

    clear_all(con, entities)


def clear_all(con, entities):
    for entity in entities:
        clear_entity(con, entity)

def draw_entity(con, entity):
    tcod.console_set_default_foreground(con, entity.color)
    tcod.console_put_char(con, entity.x, entity.y, entity.char, tcod.BKGND_NONE)

def clear_entity(con, entity):
    tcod.console_put_char(con, entity.x, entity.y, ' ', tcod.BKGND_NONE)
