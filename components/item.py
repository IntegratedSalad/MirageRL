
class Item:
	def __init__(self, use_func=None, equipment=None, can_break=False, weight=0, effect=None, **kwargs):
		self.use_func = use_func
		self.equipment = equipment
		self.can_break = can_break
		self.weight = weight
		self.effect = effect

	def use(self, **kwargs):

		user = kwargs.get('user')

		kwargs = kwargs.update(user)

		if self.use_func is not None:

			result = use_func(**kwargs)

			return result

		else:
			return {'message': f"{self.owner.name} is not usable."}

	def __str__(self):
		return f"Item at: ({self.owner.x}{self.owner.y}) of name: {self.owner.name}"
