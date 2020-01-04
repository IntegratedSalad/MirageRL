from components.ai import *

"""
'name': (GLYPH, COLOR(R, G, B), NAME, (HP, DEFENSE, ATKVAL), AI, AI_ARGS)

"""
	
monsters = { \

	'colony_of_ants': ('a', (127, 0, 0), 'ant colony', (3, 1, 2), BasicMonster, None),
	'dessert_snake': ('s', (191, 191, 0), 'dessert snake', (3, 1, 4), BasicMonster, None)




}


"""
Monsters have to be spawned based on level of player and where he is.



"""