import copy
import pprint
from tile import Tile


JINGTING_RULES = True


class Hand:
    def __init__(self, pair, triples, sequences, left):
        self.pair = pair
        self.triples = triples
        self.sequences = sequences
        self.left = left
        self.name = "Pair: "+str(self.pair) + "  Triples: "+str(self.triples) + "  Sequences: "+str(self.sequences)
        if len(self.left) > 0:
            self.name = self.name + "  Left: "+str(self.left)

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name


def check_terminals_winds_dragons(num_list):
    for n in num_list:
        if Tile.is_terminal_wind_dragon_from_comparison_value(n):
            return True
    return False


def get_pairs(nums_list):
    pairs = []
    for num in set(nums_list):
        if nums_list.count(num) >= 2:
            pairs.append([num, num])
    return pairs


def get_triples(nums_list):
    triples = []
    for num in set(nums_list):
        if nums_list.count(num) >= 3:
            triples.append([num, num, num])
    return triples


def get_sequences(nums_list):
    sequences = []
    dedupped = sorted(list(set(nums_list)))
    temp_seqs = [[dedupped[0]]]
    for i in range(1, len(dedupped)):
        last_num = dedupped[i-1]
        if dedupped[i] != last_num+1:
            temp_seqs = [[dedupped[i]]]
            continue
        temp = []
        for s in temp_seqs:
            s.append(dedupped[i])
            if len(s) == 3:
                sequences.append(s)
            else:
                temp.append(s)
        temp_seqs = temp
        temp_seqs.append([dedupped[i]])
    return sequences


def find_leftovers(combos, nums_list):
    possibilities = []
    for c in combos:
        left = copy.deepcopy(nums_list)
        for n in c:
            left.remove(n)
        possibilities.append((c, left))
    return possibilities


def find_winning_hands(nums_list):
    options = []
    winning_hands = []
    completed = []

    if JINGTING_RULES and not(check_terminals_winds_dragons(nums_list)):
        return winning_hands

    pairs = get_pairs(nums_list)
    combos = find_leftovers(pairs, nums_list)
    for c in combos:
        options.append(Hand(c[0], [], [], c[1]))

    while len(options) > 0:
        hand = options.pop(0)
        triple_combos = find_leftovers(get_triples(hand.left), hand.left)
        sequence_combos = find_leftovers(get_sequences(hand.left), hand.left)

        for tc in triple_combos:
            triples = copy.deepcopy(hand.triples)
            triples.append(tc[0])
            new_hand = Hand(hand.pair, triples, hand.sequences, tc[1])
            if len(tc[1]) == 0:
                if JINGTING_RULES:
                    if len(new_hand.sequences) == 0:
                        continue
                s_defined = sorted(triples + hand.sequences)
                if not (s_defined in completed):
                    winning_hands.append(new_hand)
                    completed.append(s_defined)
                continue
            options.append(new_hand)

        for sc in sequence_combos:
            seqs = copy.deepcopy(hand.sequences)
            seqs.append(sc[0])
            new_hand = Hand(hand.pair, hand.triples, seqs, sc[1])
            if len(sc[1]) == 0:
                if JINGTING_RULES:
                    if len(new_hand.triples) == 0:
                        continue
                s_defined = sorted(seqs + hand.triples)
                if not (s_defined in completed):
                    winning_hands.append(new_hand)
                    completed.append(s_defined)
                continue
            options.append(new_hand)

    return winning_hands


# Simple hand 1 [beginning terminal]
raw_hand = [31, 31, 31, 31, 32, 32, 33, 33, 34, 34, 34]
winnings = find_winning_hands(raw_hand)
assert len(winnings) == 2

# Simple hand 2 [ending terminal]
raw_hand = [45, 45, 46, 46, 47, 47, 48, 48, 49, 49, 49]
winnings = find_winning_hands(raw_hand)
assert len(winnings) == 2

# Simple hand 3 [wind]
raw_hand = [11, 11, 32, 32, 33, 33, 34, 34, 35, 35, 35]
winnings = find_winning_hands(raw_hand)
assert len(winnings) == 1

# Simple hand 4 [ending dragon]
raw_hand = [21, 21, 21, 45, 46, 47, 48, 48, 52, 53, 54]
winnings = find_winning_hands(raw_hand)
assert len(winnings) == 1

# Hand with no triples
raw_hand = [51, 51, 51, 52, 53, 54, 55, 56, 57, 58, 59]
winnings = find_winning_hands(raw_hand)
assert len(winnings) == 0

# Hand with no sequences
raw_hand = [11, 11, 11, 13, 13, 21, 21, 21, 23, 23, 23]
winnings = find_winning_hands(raw_hand)
assert len(winnings) == 0

# Hand with no terminals or winds or dragons
raw_hand = [32, 32, 32, 32, 33, 33, 34, 34, 35, 35, 35]
winnings = find_winning_hands(raw_hand)
assert len(winnings) == 0

# Full hand
raw_hand = [17, 17, 25, 25, 25, 32, 33, 34, 45, 45, 45, 57, 58, 59]
winnings = find_winning_hands(raw_hand)
pprint.pprint(winnings)
for w in winnings:
    pairs = []
    triples = []
    sequences = []
    for p in w.pair:
        pairs.append(Tile.create_from_comparison_value(p))
    for t in w.triples:
        row = []
        for n in t:
            row.append(Tile.create_from_comparison_value(n))
        triples.append(row)
    for s in w.sequences:
        row = []
        for n in s:
            row.append(Tile.create_from_comparison_value(n))
        sequences.append(row)
    print(pairs)
    print(triples)
    print(sequences)
assert len(winnings) == 1
