import copy
import pprint


class Hand:
    def __init__(self, pair, sets, left):
        self.pair = pair
        self.sets = sets
        self.left = left

    def __repr__(self):
        str_rep = "Pair: " + str(self.pair) + "  Sets: " + str(self.sets)
        if len(self.left) > 0:
            str_rep = str_rep + "  Left: " + str(self.left)
        return str_rep

    def __str__(self):
        str_rep = "Pair: " + str(self.pair) + "  Sets: " + str(self.sets)
        if len(self.left) > 0:
            str_rep = str_rep + "  Left: " + str(self.left)
        return str_rep


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
    dedupped = list(set(nums_list))
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

    pairs = get_pairs(nums_list)
    possi = find_leftovers(pairs, nums_list)
    for p in possi:
        options.append(Hand([p[0]], [], p[1]))

    while len(options) > 0:
        hand = options.pop(0)
        combos = get_triples(hand.left)
        combos.extend(get_sequences(hand.left))
        if len(combos) == 0:
            continue

        possi = find_leftovers(combos, hand.left)
        for p in possi:
            defined = copy.deepcopy(hand.sets)
            defined.append(p[0])
            if len(p[1]) == 0:
                s_defined = sorted(defined)
                if not(s_defined in completed):
                    winning_hands.append(Hand(hand.pair, s_defined, []))
                    completed.append(s_defined)
                continue
            options.append(Hand(hand.pair, defined, p[1]))
    return winning_hands


raw_hand = [2, 2, 2, 2, 3, 3, 4, 4, 5, 5, 5]
winnings = find_winning_hands(raw_hand)
print(len(winnings))
pprint.pprint(winnings)

raw_hand = [3, 3, 4, 4, 5, 5, 6, 6, 7, 7, 7]
winnings = find_winning_hands(raw_hand)
print(len(winnings))
pprint.pprint(winnings)
