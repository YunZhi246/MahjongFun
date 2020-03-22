import copy
from tile import Tile
from rules import Rules, RULES
from leftover_processor import LeftoverProcessor


class Hand:
    def __init__(self, pair=None, triples=None, sequences=None, left=None):
        self.__pair = [] if pair is None else pair
        self.__triples = [] if triples is None else triples
        self.__sequences = [] if sequences is None else sequences
        self.__left = [] if left is None else left
        self.__has_terminals_winds_dragons = None
        self.__waiting = None

        self.__name = "Pair: " + str(self.__pair) + "  Triples: " + str(self.__triples) + "  Sequences: " + str(self.__sequences)
        if len(self.__left) > 0:
            self.__name = self.__name + "  Left: " + str(self.__left)

    def __repr__(self):
        return self.__name

    def __str__(self):
        return self.__name

    def get_pair(self):
        return copy.deepcopy(self.__pair)

    def get_triples(self):
        return copy.deepcopy(self.__triples)

    def get_sequences(self):
        return copy.deepcopy(self.__sequences)

    def get_left(self):
        return copy.deepcopy(self.__left)

    def get_left_length(self):
        return len(self.__left)

    def get_waiting(self):
        if self.__waiting is None and (len(self.__left) > 3 or len(self.__left) == 0):
            self.__waiting = []
        elif self.__waiting is None:
            waiting = []
            leftover_processor = LeftoverProcessor(self.get_left())
            if len(self.__left) == 2:
                possible_pairs = leftover_processor.create_pairs()
                for pp in possible_pairs:
                    if Hand(pair=pp[0], triples=self.get_triples(), sequences=self.get_sequences()).is_completed():
                        waiting.append(pp[1])
            elif len(self.__left) == 3:
                possible_triples = leftover_processor.create_triples()
                possible_sequences = leftover_processor.create_sequences()
                for pt in possible_triples:
                    triples = self.get_triples()
                    triples.append(pt[0])
                    if Hand(pair=self.get_pair(), triples=triples, sequences=self.get_sequences()).is_completed():
                        waiting.append(pt[1])
                for ps in possible_sequences:
                    sequences = self.get_sequences()
                    sequences.append(ps[0])
                    if Hand(pair=self.get_pair(), triples=self.get_triples(), sequences=sequences).is_completed():
                        waiting.append(ps[1])
            self.__waiting = sorted(list(set(waiting)))
        return copy.deepcopy(self.__waiting)

    def is_completed(self):
        if len(self.__left) != 0:
            return False
        if RULES == Rules.Jingting:
            if len(self.__triples) == 0 or len(self.__sequences) == 0:
                return False
            if not self.has_terminals_winds_dragons():
                return False
        return True

    def is_one_off(self):
        if self.__waiting is None:
            self.get_waiting()
        if len(self.__waiting) == 0:
            return False
        return True

    def has_terminals_winds_dragons(self):
        if self.__has_terminals_winds_dragons is None:
            for sg in self.__sequences:
                if any(Tile.is_terminal_wind_dragon_from_comparison_value(s) for s in sg):
                    self.__has_terminals_winds_dragons = True
                    return self.__has_terminals_winds_dragons

            if len(self.__pair) > 0 and Tile.is_terminal_wind_dragon_from_comparison_value(self.__pair[0]):
                self.__has_terminals_winds_dragons = True
            elif any(Tile.is_terminal_wind_dragon_from_comparison_value(tg[0]) for tg in self.__triples):
                self.__has_terminals_winds_dragons = True
            elif any(Tile.is_terminal_wind_dragon_from_comparison_value(l) for l in self.__left):
                self.__has_terminals_winds_dragons = True
            else:
                self.__has_terminals_winds_dragons = False
        return self.__has_terminals_winds_dragons

    def print_converted(self):
        pairs = []
        triples = []
        sequences = []
        for p in self.__pair:
            pairs.append(Tile.create_from_comparison_value(p))
        for t in self.__triples:
            row = []
            for n in t:
                row.append(Tile.create_from_comparison_value(n))
            triples.append(row)
        for s in self.__sequences:
            row = []
            for n in s:
                row.append(Tile.create_from_comparison_value(n))
            sequences.append(row)
        print(pairs)
        print(triples)
        print(sequences)
