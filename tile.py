from enum import IntEnum


class Tile:

    class Suite(IntEnum):
        WIND = 1
        DRAGON = 2
        DOT = 3
        STICK = 4
        NUM = 5

    class Wind(IntEnum):
        NORTH = 1
        EAST = 3
        SOUTH = 5
        WEST = 7

    class Dragon(IntEnum):
        GREEN = 1
        RED = 3
        WHITE = 5

    def __init__(self, suite, value):
        self.suite = suite
        self.value = value
        self.comparison_value = (self.suite * 10) + self.value
        if self.suite == Tile.Suite.WIND or self.suite == Tile.Suite.DRAGON:
            str_value = self.value.name
        else:
            str_value = str(self.value)
        self.name = self.suite.name + " " + str_value

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name

    def __eq__(self, other):
        return self.comparison_value == other.comparison_value

    def __lt__(self, other):
        return self.comparison_value < other.comparison_value


# w1 = Tile(Tile.Suite.WIND, Tile.Wind.NORTH)
# w2 = Tile(Tile.Suite.WIND, Tile.Wind.EAST)
# w3 = Tile(Tile.Suite.WIND, Tile.Wind.SOUTH)
# w4 = Tile(Tile.Suite.WIND, Tile.Wind.WEST)
# d1 = Tile(Tile.Suite.DRAGON, Tile.Dragon.GREEN)
# d2 = Tile(Tile.Suite.DRAGON, Tile.Dragon.RED)
# d3 = Tile(Tile.Suite.DRAGON, Tile.Dragon.WHITE)
# do1 = Tile(Tile.Suite.DOT, 1)
# do2 = Tile(Tile.Suite.DOT, 2)
# do3 = Tile(Tile.Suite.DOT, 3)
# do4 = Tile(Tile.Suite.DOT, 4)
# do5 = Tile(Tile.Suite.DOT, 5)
# st1 = Tile(Tile.Suite.STICK, 1)
# st2 = Tile(Tile.Suite.STICK, 2)
# st3 = Tile(Tile.Suite.STICK, 3)
# st4 = Tile(Tile.Suite.STICK, 4)
# st5 = Tile(Tile.Suite.STICK, 5)
# nu1 = Tile(Tile.Suite.NUM, 1)
# nu2 = Tile(Tile.Suite.NUM, 2)
# nu3 = Tile(Tile.Suite.NUM, 3)
# nu4 = Tile(Tile.Suite.NUM, 4)
# nu5 = Tile(Tile.Suite.NUM, 5)
#
# lt = [w1, w2, w3, w4, d1, d2, d3, do1, do2, do3, do4, do5, st1, st2, st3, st4, st5, nu1, nu2, nu3, nu4, nu5]