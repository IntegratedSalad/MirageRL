
class View:
	"""docstring for View"""
	def __init__(self, render_func, func_args):

		self.render_func = render_func


	def render(self):
		self.render_func(*func_args)


	def draw_menu(self, fullscreen=True, x=False, y=False):
		pass


		
		
		