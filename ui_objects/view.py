
class View:
	"""Class handling data and behaviour of views.

		View contains everything that visible on screen.
	"""
	def __init__(self, render_func, *func_args):

		self.render_func = render_func
		self.func_args = func_args

	def render(self):
		self.render_func(*self.func_args)

		