import enum

class GameStates(enum.Enum):

	PLAYER_TURN = enum.auto()
	ENEMY_TURN = enum.auto()
	PLAYER_DEATH = enum.auto()


