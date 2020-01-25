import enum
from data.game_data.constants import *
from map_objects.tile import Tile
from map_objects.tile_types import *

class MapElevation(enum.Enum):

    ELEV_ABOVE = enum.auto()
    ELEV_BELOW = enum.auto()

class ChunkProperty(enum.Enum):

    NONE = enum.auto()
    HAS_DIRECTION = enum.auto()
    START = enum.auto()
    END = enum.auto()

class Chunk:


    """
    Class that represents one area of gameplay. Used for storing data.

    """

    def __init__(self, pos):
        self.pos = pos
        self.property = ChunkProperty.NONE
        self.discovered = False
        self.objects = []
        self.tiles = [[Tile(False, type_of=sand) for y in range(MAP_HEIGHT)] for x in range(MAP_WIDTH)]

    def __str__(self):
        return f"\t\t+Chunk type+\n PROPERTY: {self.property} \n \
                                 \n OBJECTS: {self.objects} \n \t\t DISCOVERED: {self.discovered} \n \t\t POS: {self.pos}"

    def __mem__(self):
        return f"{hex(id(self))}"

