import tcod
import textwrap
import constants


def draw_window(con, x, y, width, height, options=None, key_handler=None):
    """
    Rectangular area.
    """
    pass

def draw_text(con, x, y, text, color_fg, color_bg=None):

	if len(text) > constants.SCREEN_WIDTH:
		wrapped_text = textwrap.wrap(text, width=constants.SCREEN_WIDTH)

		if len(wrapped_text) > constants.SCREEN_HEIGHT:
			raise ValueError(f" TEXT TOO LONG: {text}")

		for line in wrapped_text:

			con.print(x, y, line, fg=color_fg, bg=color_bg)

			y += 1 

		return

	con.print(x, y, text, fg=color_fg, bg=color_bg)



