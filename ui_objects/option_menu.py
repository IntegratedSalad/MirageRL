

class OptionMenu:
	"""
	Base option menu class.
	TODO: Plan how menus will work in views.


	"""
	def __init__(self, con, variables, name, view, func, *func_args):
		self.con = con
		self.variables = variables
		self.name = name
		self.view = view
		self.func = func
		self.view.menus[name] = self
		self.func_args = func_args


