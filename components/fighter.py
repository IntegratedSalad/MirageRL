from data.game_data import constants
from misc import utils
from ui_objects.render_order import RenderOrder

class Fighter:

	def __init__(self, hp, defense, attack_value):
		self.hp = hp
		self.defense = defense
		self.attack_value = attack_value
		self.inventory = {'food': [], 'weapon': [],  'armor': []}

	def take_damage(self, amount):
		results = []

		self.hp -= amount

		if self.hp <= 0:
			results.append({'dead': self.owner})

		return results

	def attack(self, target): # we pass an entity!
		results = []

		damage = self.attack_value - target.fighter.defense # change that

		if damage > 0:
			results.append({'message': '{0} attacks {1} and deals {2} damage!'.format(self.owner.name.title(), target.name.title(), str(damage))})
			results.extend(target.fighter.take_damage(damage))
		else:
			results.append({'message': '{0} misses {1}'.format(self.owner.name.title(), target.name.title())})
			
		return results

	def get_item(self, entities, game_map):

		results = []

		p_x, p_y = self.owner.position_in_chunk # player's position in chunk
		for e in entities:

			i_x, i_y = e.position_in_chunk

			if (i_x == p_x) and (i_y == p_y) and e.item is not None:
				self.inventory[e.item.category].append(e) 
				entities.remove(e)
				results.append({'message': "{0} picks up {1}.".format(self.owner.name.title(), e.name.title())})
				print(self.inventory)

		return results

	def die(self):
		desaturate_val = 30
		self.owner.ai = None
		self.owner.char = '%'
		self.owner.blocks = False
		self.owner.render_order = RenderOrder.CORPSE
		r, g, b = self.owner.color
		self.owner.color = (utils.desaturate(r, desaturate_val), utils.desaturate(g, desaturate_val), utils.desaturate(b, desaturate_val))
		self.owner.fighter = None
