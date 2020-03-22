import copy
from tile import Tile
from rules import Rules, RULES
from leftover_processor import LeftoverProcessor


class Hand:
    def __init__(self, pair=None, triples=None, sequences=None, left=None):
        self.pair = [] if pair is None else pair
        self.triples = [] if triples is None else triples
        self.sequences = [] if sequences is None else sequences
        self.left = [] if left is None else left
        self.name = "Pair: "+str(self.pair) + "  Triples: "+str(self.triples) + "  Sequences: "+str(self.sequences)
        if len(self.left) > 0:
            self.name = self.name + "  Left: "+str(self.left)
        self.__has_terminals_winds_dragons = None
        self.__waiting = None

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name

    def is_completed(self):
        if len(self.left) != 0:
            return False
        if RULES == Rules.Jingting:
            if len(self.triples) == 0 or len(self.sequences) == 0:
                return False
            if not self.has_terminals_winds_dragons():
                return False
        return True

    def has_terminals_winds_dragons(self):
        if self.__has_terminals_winds_dragons is None:
            for sg in self.sequences:
                if any(Tile.is_terminal_wind_dragon_from_comparison_value(s) for s in sg):
                    self.__has_terminals_winds_dragons = True
                    return self.__has_terminals_winds_dragons

            if len(self.pair) > 0 and Tile.is_terminal_wind_dragon_from_comparison_value(self.pair[0]):
                self.__has_terminals_winds_dragons = True
            elif any(Tile.is_terminal_wind_dragon_from_comparison_value(tg[0]) for tg in self.triples):
                self.__has_terminals_winds_dragons = True
            elif any(Tile.is_terminal_wind_dragon_from_comparison_value(l) for l in self.left):
                self.__has_terminals_winds_dragons = True
            else:
                self.__has_terminals_winds_dragons = False
        return self.__has_terminals_winds_dragons

    def is_one_off(self):
        if self.__waiting is None:
            self.waiting()
        if len(self.__waiting) == 0:
            return False
        return True

    def waiting(self):
        if self.__waiting is None and (len(self.left) > 3 or len(self.left) == 0):
            self.__waiting = []
        elif self.__waiting is None:
            waiting = []
            leftover_processor = LeftoverProcessor(self.left)
            if len(self.left) == 2:
                possible_pairs = leftover_processor.create_pairs()
                for pp in possible_pairs:
                    if Hand(pair=pp[0], triples=self.triples, sequences=self.sequences).is_completed():
                        waiting.append(pp[1])
            elif len(self.left) == 3:
                possible_triples = leftover_processor.create_triples()
                possible_sequences = leftover_processor.create_sequences()
                for pt in possible_triples:
                    triples = copy.deepcopy(self.triples)
                    triples.append(pt[0])
                    if Hand(pair=self.pair, triples=triples, sequences=self.sequences).is_completed():
                        waiting.append(pt[1])
                for ps in possible_sequences:
                    sequences = copy.deepcopy(self.sequences)
                    sequences.append(ps[0])
                    if Hand(pair=self.pair, triples=self.triples, sequences=sequences).is_completed():
                        waiting.append(ps[1])
            self.__waiting = sorted(list(set(waiting)))
        return self.__waiting

    def print_converted(self):
        pairs = []
        triples = []
        sequences = []
        for p in self.pair:
            pairs.append(Tile.create_from_comparison_value(p))
        for t in self.triples:
            row = []
            for n in t:
                row.append(Tile.create_from_comparison_value(n))
            triples.append(row)
        for s in self.sequences:
            row = []
            for n in s:
                row.append(Tile.create_from_comparison_value(n))
            sequences.append(row)
        print(pairs)
        print(triples)
        print(sequences)
