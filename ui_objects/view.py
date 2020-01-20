import tcod
import constants

class View:
	"""Class handling data and behaviour of views.

		View contains everything that visible on screen - it is the screen.
		It has one or more consoles.
	"""
	def __init__(self, name, main_con, main_render_func, root_console, *args):

		self.name = name
		self.main_con = main_con
		self.main_render_func = main_render_func
		self.root_console = root_console
		self.main_con_args = args

		self.consoles = {self.name: {'console': self.main_con, 'func': self.main_render_func, 'args': self.main_con_args}}
		# self.consoles = {self.name: (self.main_con, self.main_render_func, self.main_con_args)}
		# updating arguments will be done via view.consoles['name']['args']



	# def render(self):

	# 	# for console in consoles:

	# 		# do work...
	# 	pass

	def render(self, *rargs):

		# iterate over dict
		self.main_con.clear()
		self.main_render_func(self.main_con, self.root_console, *rargs)


	def add_console(self, name, func, *func_args):
		"""Adds console to display additional content."""
		console = tcod.console.Console(constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT, order="F")
		self.consoles[name] = {'console': console, 'func': func, 'args': func_args}



		