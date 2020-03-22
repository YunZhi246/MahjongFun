from enum import Enum

# triple = three tiles of the exact same value
# sequence = three consecutive dot, stick or number tiles

# Rules:
# Basic - a complete hand consists of one pair and the rest of the tiles form triples and sequences
# Jingting - includes basic rules and a complete hand must contain the following:
#   1. a terminal, wind or dragon
#   2. at least one triple
#   3. at least one sequence


class Rules(Enum):
    Basic = 1
    Jingting = 2


RULES = Rules.Jingting
