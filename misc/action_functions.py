
def action_heal(**kwargs):

	target = kwargs.get('target')

	amount = kwargs.get('heal_amount')

	target.fighter.hp += amount

	return 'trash'


