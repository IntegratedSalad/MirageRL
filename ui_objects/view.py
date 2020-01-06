
class View:
	"""Class handling data and behaviour of views.

		View contains everything that visible on screen - it is the screen.
		It has one or more consoles.
	"""
	def __init__(self, name, main_con, render_func, root_console, *func_args):

		self.name = name
		self.main_con = main_con
		self.render_func = render_func
		self.root_console = root_console
		self.func_args = func_args
		# change that to be more "precise":

		self.consoles = {self.name: (self.main_con, self.render_func)}
		self.menu_returns = {'option': None}


	def render(self):

		# iterate over dict


		val = self.render_func(self.main_con, self.root_console, *self.func_args)

		if val is not None:
			val = val.get('option')
			self.menu_returns['option'] = val


	def add_console(self, name, func, *func_args):
		"""Adds console to display additional content."""
		pass

		