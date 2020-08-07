

class OptionMenu:
	"""
	Base option menu class.
	Returns value.

	FIX: do something about having to pass con twice, because actual attribute of the class isn't passed into function.

	"""
	def __init__(self, name, con, view, func, *func_args, **func_kwargs):
		self.name = name
		self.con = con
		self.view = view
		self.func = func
		# self.view.menus[name] = self
		self.func_args = func_args
		self.func_kwargs = func_kwargs

	def render(self, key_handler):

		return self.func(*self.func_args, key_handler=key_handler)
