import tcod
import textwrap
from data.game_data import constants
from data.game_data import variables

def draw_menu(con, x, y, width, height, options, **kwargs):

	"""
	
	TODO: FIX DISPLAYING OPTIONS

	"""

	key = kwargs.get('key_handler')
	entity = False

	try:
		if type(options[0]) != str: # options is a list of Entity type.
			entity = True # Return object and when drawing, access the .name attribute.
	except IndexError:
		pass

	if key is None:
		return None

	if key == 'up':

		variables.title_screen_choice -= 1 # CHANGE THAT VARIABLE NAME

		if variables.title_screen_choice < 0:
			variables.title_screen_choice = len(options) - 1

	if key == 'down':
		variables.title_screen_choice += 1

		if variables.title_screen_choice > len(options) - 1:
			variables.title_screen_choice = 0

	if key == 'exit':
		variables.title_screen_choice = 0
		return key

	color_active = (255, 255, 255)
	color_inactive = (114, 114, 114)

	if not entity:

		for index, option in enumerate(options):

			if index == variables.title_screen_choice:

				draw_text(con, x, y, option, color_active)

			else:
				draw_text(con, x, y, option, color_inactive)

			y += 1

	else:

		for index, option in enumerate(options):

			if index == variables.title_screen_choice:

				draw_text(con, x, y, option.name, color_active)

			else:
				draw_text(con, x, y, option.name, color_inactive)

			y += 1

	if key == 'enter' and len(options) > 0:

		to_return = options[variables.title_screen_choice]
		variables.title_screen_choice = 0 # change that to just choice_num
		return to_return
	
	return None


def draw_text(con, x, y, text, color_fg, color_bg=None, custom_width=0):

	if len(text) > constants.SCREEN_WIDTH and custom_width <= 0:

		wrapped_text = textwrap.wrap(text, width=constants.SCREEN_WIDTH - 2)

		if len(wrapped_text) > constants.SCREEN_HEIGHT:
			raise ValueError(f" TEXT TOO LONG: {text}")

		for line in wrapped_text:

			con.print(x, y, line, fg=color_fg, bg=color_bg)

			y += 1 

		return

	if custom_width > 0:

		wrapped_text = textwrap.wrap(text, width=custom_width)

		if len(wrapped_text) > constants.SCREEN_HEIGHT:
			raise ValueError(f"TEXT TOO LONG: {text}")

		for line in wrapped_text:
			con.print(x, y, line, fg=color_fg, bg=color_bg)

			y += 1

		return

	con.print(x, y, text, fg=color_fg, bg=color_bg)

def return_lines_of_wrapped_text(text, width):
	return len(textwrap.wrap(text, width=width))

def draw_colored_bar(con, x, y, char, value, color_bright, color_dark):
	"""E.g health bar or mana bar"""

	pass

def draw_text_multicolor():
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


def draw_tab_bar(con, x, y, width, height, color_fg, color_bg, options_in, options_out_dict, limit_to_show_arrow, **kwargs):
	"""
	Tab returns what has to be printed.

	Width and height is of one bar.

	limit_to_show_arrow is an int that tells function to show arrow when the bar spans over that many characters.


	"""

	key = kwargs.get('key_handler')

	for bar in options_in:

		draw_framing(con, x, y, chr(177), width, height, color_fg, color_bg)

		x += width

	if key == 'tab':
		if not (variables.tab_bar_choice + 1 + 1 > len(options_in)): 
			variables.tab_bar_choice += 1
		else:
			variables.tab_bar_choice = 0

	variables.tab_bar_actual_choice = options_in[variables.tab_bar_choice] # GLOBAL VARIABLE, VERY BAD PRACTICE

	return options_in[variables.tab_bar_choice]
	


def draw_popup(text, color_border):
	"""
	Dismissable window with framing and text. Automatically draws on the center of screen.

	"""
	pass


def draw_graphics(con, x, y, text, color_fg, color_bg=None):

	text_list = text.split()
	if len(text_list) > constants.SCREEN_WIDTH or len(text_list) > constants.SCREEN_HEIGHT:
		raise ValueError(f"Graphics too big: {text}")

	else:

		con.print(x, y, text, fg=color_fg, bg=color_bg)

