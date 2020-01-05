
class Fighter:

	def __init__(self, hp, defense, attack_value):
		self.hp = hp
		self.defense = defense
		self.attack_value = attack_value

	def take_damage(self, amount):
		results = []

		self.hp -= amount

		print(self.owner.name, self.hp)

		if self.hp <= 0:
			print("DEDE")
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
