import tcod

def render_all(con, entities, game_map, screen_width, screen_height, colors):

    for y in range(game_map.height):
        for x in range(game_map.width):

            tile = game_map._map[x][y]
            tcod.console_put_char_ex(con, x, y, tile.char, tile.color, (0, 0, 0))

    for entity in entities:
        draw_entity(con, entity)

    con.print(2, 2, string='fps{0}'.format(tcod.sys_get_fps()), fg=(255, 255, 255))
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
