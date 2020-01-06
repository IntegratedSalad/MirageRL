import tcod
import textwrap
import constants


def draw_menu(con, x, y, width, height, options, key_handler):

	key_handler.get('up')
	key_handler.get('down')

	for option in options:
		pass

	return None

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


def draw_bar(con, x, y, char, value, color_bright, color_dark):
	"""E.g health bar or mana bar"""

	pass



