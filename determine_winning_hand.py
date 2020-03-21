import copy
import pprint
from hand import Hand
from rules import Rules, RULES


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


def leftover_sanity_check(leftovers):
    counter = [0] * 5
    for n in leftovers:
        counter[(n//10)-1] += 1
    return not(any(c % 3 != 0 for c in counter))


def find_winning_hands(starting_hand):
    options = []
    winning_hands = []
    completed = []

    if RULES == Rules.Jingting and not starting_hand.has_terminals_winds_dragons():
        return winning_hands

    pairs = get_pairs(starting_hand.left)
    combos = find_leftovers(pairs, starting_hand.left)
    for c in combos:
        if not leftover_sanity_check(c[1]):
            continue
        options.append(Hand(pair=c[0], left=c[1]))

    while len(options) > 0:
        hand = options.pop(0)
        if len(hand.left) == 0:
            continue
        triple_combos = find_leftovers(get_triples(hand.left), hand.left)
        sequence_combos = find_leftovers(get_sequences(hand.left), hand.left)

        for tc in triple_combos:
            if not leftover_sanity_check(tc[1]):
                continue
            triples = copy.deepcopy(hand.triples)
            triples.append(tc[0])
            new_hand = Hand(pair=hand.pair, triples=triples, sequences=hand.sequences, left=tc[1])
            if new_hand.is_completed():
                s_defined = sorted(triples + hand.sequences)
                if not (s_defined in completed):
                    winning_hands.append(new_hand)
                    completed.append(s_defined)
                continue
            options.append(new_hand)

        for sc in sequence_combos:
            if not leftover_sanity_check(sc[1]):
                continue
            seqs = copy.deepcopy(hand.sequences)
            seqs.append(sc[0])
            new_hand = Hand(pair=hand.pair, triples=hand.triples, sequences=seqs, left=sc[1])
            if new_hand.is_completed():
                s_defined = sorted(seqs + hand.triples)
                if not (s_defined in completed):
                    winning_hands.append(new_hand)
                    completed.append(s_defined)
                continue
            options.append(new_hand)

    return winning_hands


# Simple hand 1 [beginning terminal]
raw_hand = [31, 31, 31, 31, 32, 32, 33, 33, 34, 34, 34]
winnings = find_winning_hands(Hand(left=raw_hand))
assert len(winnings) == 2

# Simple hand 2 [ending terminal]
raw_hand = [45, 45, 46, 46, 47, 47, 48, 48, 49, 49, 49]
winnings = find_winning_hands(Hand(left=raw_hand))
assert len(winnings) == 2

# Simple hand 3 [wind]
raw_hand = [11, 11, 32, 32, 33, 33, 34, 34, 35, 35, 35]
winnings = find_winning_hands(Hand(left=raw_hand))
assert len(winnings) == 1

# Simple hand 4 [ending dragon]
raw_hand = [21, 21, 21, 45, 46, 47, 48, 48, 52, 53, 54]
winnings = find_winning_hands(Hand(left=raw_hand))
assert len(winnings) == 1

# Hand with no triples
raw_hand = [51, 51, 51, 52, 53, 54, 55, 56, 57, 58, 59]
winnings = find_winning_hands(Hand(left=raw_hand))
assert len(winnings) == 0

# Hand with no sequences
raw_hand = [11, 11, 11, 13, 13, 21, 21, 21, 23, 23, 23]
winnings = find_winning_hands(Hand(left=raw_hand))
assert len(winnings) == 0

# Hand with no terminals or winds or dragons
raw_hand = [32, 32, 32, 32, 33, 33, 34, 34, 35, 35, 35]
winnings = find_winning_hands(Hand(left=raw_hand))
assert len(winnings) == 0

# Full hand
raw_hand = [17, 17, 25, 25, 25, 32, 33, 34, 45, 45, 45, 57, 58, 59]
winnings = find_winning_hands(Hand(left=raw_hand))
pprint.pprint(winnings)
assert len(winnings) == 1
for w in winnings:
    w.print_converted()
