import tcod

class BasicMonster:
	def take_turn(self, target, game_map, entities): # fov_map
		results = []

		monster = self.owner

		if monster.distance_to(target) >= 2:

			monster.move_astar(target, entities, game_map)

		elif target.fighter.hp > 0:
			#attack
			attack_results = monster.fighter.attack(target)
			results.extend(attack_results)

		return results
			



# actually we have to implement fov, but turn off it, when the player is outside cavern


		
