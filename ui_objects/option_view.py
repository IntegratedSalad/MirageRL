from ui_objects.view import View

class OptionView(View):
	

	def __init__(self, name, main_con, main_render_func, root_console, *args):
		super().__init__(name, main_con, main_render_func, root_console, *args)


	def render(self, key_handler, **kwargs):

		"""
		Returns dictionary with keys as name of consoles and functions (their return values.)

		"""

		result_func_dict = {}

		print(list(self.consoles.keys()))

		for con in list(self.consoles.keys()):

			console_obj = self.consoles[con]['console']
			func = self.consoles[con]['func']
			args = self.consoles[con]['args'] # you can update args but not keyword args?
			console_obj.clear()

			result_func_dict[con] = func(console_obj, self.root_console, *args, key_handler=key_handler, **kwargs)


		return result_func_dict


	def set_render_order(self, console_priority_tuple):

		"""Resets self.consoles to be ordered by console_priority_tuple

		console_priority_tuple = (name, priority)[str, int]
		"""
		pass

