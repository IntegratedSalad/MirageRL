import tcod
import textwrap
from data.game_data import constants
from data.game_data import variables

def draw_menu(con, x, y, width, height, options, **kwargs):

	"""
	
	TODO: FIX DISPLAYING OPTIONS
	This are hard coded to drawing menu.

	"""

	key = kwargs.get('key_handler')

	if key is None:
		return None

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

	_x = int(constants.SCREEN_WIDTH / 2) + 7
	_y = int(constants.SCREEN_HEIGHT / 2) + 7

	for index, option in enumerate(options):

		if index == variables.title_screen_choice:

			draw_text(con, _x, _y, option, color_active)

		else:
			draw_text(con, _x, _y, option, color_inactive)

		_y += 1

	if key == 'enter':
		to_return = options[variables.title_screen_choice]
		variables.title_screen_choice = 0 # change that to just choice_num
		return to_return
	
	return None

def draw_tab(con, x, y, width, height, options, **kwargs):
	pass

def draw_text(con, x, y, text, color_fg, color_bg=None):

	if len(text) > constants.SCREEN_WIDTH:
		print(text)
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


def draw_framing(con, start_x, start_y, char, width, height, color_fg, color_bg, fill=False, fill_data=None):

	if fill and fill_data is None:
		raise TypeError("You have to provide data for filling while drawing framing!")

	if not fill:

		for x in range(width):
			for y in range(height):

				if (y == 0 or y == height - 1) or (x == 0 or x == width - 1):

					con.print(start_x + x, start_y + y, char, color_fg, color_bg)

	else:
		for x in range(width):
			for y in range(height):

				if (y == 0 or y == height - 1) or (x == 0 or x == width - 1):

					con.print(start_x + x, start_y + y, char, color_fg, color_bg)
				else:
					con.print(start_x + x, start_y + y, fill_data['filling_char'], fill_data['filling_color_fg'], fill_data['filling_color_bg'])




def draw_graphics(con, x, y, text, color_fg, color_bg=None):

	text_list = text.split()
	if len(text_list) > constants.SCREEN_WIDTH or len(text_list) > constants.SCREEN_HEIGHT:
		raise ValueError(f"Graphics too big: {text}")

	else:

		con.print(x, y, text, fg=color_fg, bg=color_bg)


