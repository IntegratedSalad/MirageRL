from ui_objects.view import View

class OptionView(View):
	

	def __init__(self, name, main_con, main_render_func, root_console, *args):
		super().__init__(name, main_con, main_render_func, root_console, *args)


	def render(self, key_handler):

		"""
		Returns dictionary with keys as name of consoles and functions (their return values.)

		"""

		result_func_list = {}

		for con in list(self.consoles.keys()):

			console_obj = self.consoles[con]['console']
			func = self.consoles[con]['func']
			args = self.consoles[con]['args']
			console_obj.clear()

			result_func_list[con] = func(console_obj, self.root_console, *args, key_handler=key_handler)


		return result_func_list

