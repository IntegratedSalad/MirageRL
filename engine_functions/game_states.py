import enum

class GameStates(enum.Enum):

	TITLE_SCREEN = enum.auto()
	PLAYER_TURN = enum.auto()
	ENEMY_TURN = enum.auto()
	PLAYER_DEATH = enum.auto()
	END_OF_GAME = enum.auto()


