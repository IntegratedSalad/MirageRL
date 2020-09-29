from ui_objects.view import View
from data.game_data import variables

class OptionView(View):
	

	def __init__(self, name, main_con, main_render_func, root_console, *args):
		super().__init__(name, main_con, main_render_func, root_console, *args)


	def render(self, key_handler, **kwargs):

		"""
		Returns dictionary with keys as name of consoles and functions (their return values.)

		"""

		result_func_dict = {}

		get_update = kwargs.get('update_from_console')
		player = kwargs.get('player')

		# here update needed consoles

		"""UPDATE OF THE CONSOLE THAT RENDERS INVENTORY HAS TO BE UPDATED AFTER RENDERING (CALLING FUNCTION OF) THE TAB_BAR

		Tab bar changes the variable of options (category of items).

		!It shouldn't be a global variable, inventory screen console should get options from inventory tab bar.!

		REWRITE IT TO WORK WITH CONSOLES UPDATING CONSOLES BEFORE THEY RENDER
		BEST PRACTICE WOULD BE TO CALL THE FUNCTIONS CHANGING DATA, WITHOUT RENDERING WHAT THEY DRAW AND THEN RENDER IT WITH DATA
		THAT THEY RETURN AND IS USED BY OTHER CONSOLES


		"""

		args_to_update = None
		console_with_update = None
		console_to_update = None

		print(list(self.consoles.keys()))

		if get_update is not None:
			console_to_update = get_update[0]
			console_with_update = get_update[1]

		for con in list(self.consoles.keys()):
			"""con is a string"""

			console_obj = self.consoles[con]['console']

			if con == console_to_update:
				self.consoles[con]['args'] = [player.fighter.inventory[variables.tab_bar_actual_choice]] # VERY BAD ARCHITECTURE
			
			args = self.consoles[con]['args']
			func = self.consoles[con]['func']
			console_obj.clear()
			result_func_dict[con] = func(console_obj, self.root_console, *args, key_handler=key_handler, **kwargs)

		return result_func_dict

	def cipa(self, key_handler, **kwargs):

		"""
		Returns dictionary with keys as name of consoles and functions (their return values.)

		"""

		result_func_dict = {}

		get_update = kwargs.get('update_from_console')
		print(get_update)

		# here update needed consoles

		"""UPDATE OF THE CONSOLE THAT RENDERS INVENTORY HAS TO BE UPDATED AFTER RENDERING (CALLING FUNCTION OF) THE TAB_BAR

		Tab bar changes the variable of options (category of items).

		!It shouldn't be a global variable, inventory screen console should get options from inventory tab bar.!

		"""

		# args_to_update = None
		# args = None

		# if get_update is not None:
		# 	console_to_update = get_update[0]
		# 	console_with_update = get_update[1]

		for con in list(self.consoles.keys()):
			"""con is a string"""

			# if get_update is not None:

			# 	if con == console_to_update:
			# 		"""
			# 		Console to update should be ordered after console with update!

			# 		"""
			# 		args = args_to_update
			# 		# self.update_console(console_to_update, args_to_update)

			console_obj = self.consoles[con]['console']
			func = self.consoles[con]['func']

			# if get_update is None or con != console_to_update:
			args = self.consoles[con]['args'] # you can update args but not keyword args?

			console_obj.clear()

			# if con == 'inventory_screen': print(args)

			# print(args, con)
			# if con == 'inventory_screen': exit(0)

			result_func_dict[con] = func(console_obj, self.root_console, *args, key_handler=key_handler, **kwargs)

			# if get_update is not None:

			# 	if con == console_with_update:
			# 		args_to_update = self.consoles[con]['args']


		return result_func_dict

	def set_render_order(self, console_priority_list):

		"""Resets self.consoles to be ordered by console_priority_tuple

		console_priority_tuple = [(name, priority)][[str, int]]
		"""

		sorted_list_consoles = sorted(console_priority_list, key=lambda x: x[1])

		new_console_dict = {}

		for c in sorted_list_consoles:
			new_console_dict[c[0]] = self.consoles[c[0]]

		self.consoles = new_console_dict

