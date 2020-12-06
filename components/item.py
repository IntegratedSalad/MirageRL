
class Item:
	def __init__(self, use_func=None, equipment=None, can_break=False, weight=0, effect=None, category='junk', **kwargs):

		"""
		use_func 

		category - type of an item e.g consumable, armor etc.

		"""
		self.use_func = use_func
		self.equipment = equipment
		self.can_break = can_break
		self.weight = weight
		self.effect = effect
		self.category = category
		self.JSON_file = {} # a way to have customizable and data driven behaviour?
		self.identifier = id(self)
		self.kwargs = kwargs
		self.attributes = {

		} # NAME: (IS_PRESENT, EFFECT_FUNCTION, ICON, COLOR, DESCRIPTION)
		self.description = ""



	def use(self, **kwargs):
		"""

		Make using items like sending messages - result applies at the end of the round.

		"""

		kwargs.update(self.kwargs) # make that into one dictionary with keys added in the instantiation of the item object and while callling
								   # the .use method.
		if self.use_func is not None:

			result = self.use_func(**kwargs)

			return result

		else:
			return {'message': f"{self.owner.name} is not usable."}

	def __str__(self):
		return f"ITEM -{self.identifier}- \n ATTRS {self.attributes}"
