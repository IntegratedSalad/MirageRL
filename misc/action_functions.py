
def action_heal(**kwargs):

	target = kwargs.get('target')

	amount = kwargs.get('heal_amount')

	target.fighter.hp += amount

	return 'trash'

def action_equip(**kwargs):

	target = kwargs.get('target')
	item = kwargs.get('item')

	# before this function executes, we check if there is already an item.
	slot = kwargs.get('slot')

	target.fighter.equipment[slot] = item

	return 'equipped'
