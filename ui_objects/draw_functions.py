import tcod
import textwrap
import constants


def draw_menu(con, x, y, width, height, options, key_handler):

	up_key = key_handler.get('up')
	down_key = key_handler.get('down')
	enter = key_handler.get('enter')

	if up_key:

		choice += 1

		if choice > len(options):
			choice = 0
	else:
		choice -= 1

		if choice < 0:
			choice = 0

	color_active = (255, 255, 255)
	color_inactive = (114, 114, 114)

	choice = 0

	_x = int(constants.SCREEN_WIDTH / 2)
	_y = int(constants.SCREEN_HEIGHT / 2)

	for index, option in options.enumerate():

		if index == choice:

			draw_text(con, _x, _y, option, color_active)

		else:
			draw_text(con, _x, _y, option, color_inactive)

		_y += 1


	if enter:
		return options['choice']
	
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



