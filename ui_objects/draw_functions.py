import tcod
import textwrap
import constants
import variables

def draw_menu(con, x, y, width, height, options, key_handler):

	if key_handler is not None:

		key = key_handler
	else:
		return None

	print(key)

	if key == 'up':

		variables.title_screen_choice -= 1

		if variables.title_screen_choice < 0:
			variables.title_screen_choice = len(options) - 1

	if key == 'down':
		variables.title_screen_choice += 1

		if variables.title_screen_choice > len(options) - 1:
			variables.title_screen_choice = 0

	color_active = (255, 255, 255)
	color_inactive = (114, 114, 114)

	_x = int(constants.SCREEN_WIDTH / 2)
	_y = int(constants.SCREEN_HEIGHT / 2)

	for index, option in enumerate(options):

		if index == variables.title_screen_choice:

			draw_text(con, _x, _y, option, color_active)

		else:
			draw_text(con, _x, _y, option, color_inactive)

		_y += 1

	if key == 'enter':
		return options[variables.title_screen_choice]
	
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



