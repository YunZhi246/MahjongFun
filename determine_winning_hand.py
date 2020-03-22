import copy
from hand import Hand
from rules import Rules, RULES
from leftover_processor import LeftoverProcessor


def find_winning_hands(starting_hand):
    if RULES == Rules.Jingting and not starting_hand.has_terminals_winds_dragons():
        return []

    options = []
    winning_hands = []
    completed = []

    leftover_processor = LeftoverProcessor(starting_hand.left)
    combos = leftover_processor.get_pairs()
    for c in combos:
        if not LeftoverProcessor.leftover_sanity_check(c[1]):
            continue
        options.append(Hand(pair=c[0], left=c[1]))

    while len(options) > 0:
        hand = options.pop(0)
        if len(hand.left) == 0:
            continue
        leftover_processor = LeftoverProcessor(hand.left)
        triple_combos = leftover_processor.get_triples()
        sequence_combos = leftover_processor.get_sequences()

        for tc in triple_combos:
            if not LeftoverProcessor.leftover_sanity_check(tc[1]):
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
            if not LeftoverProcessor.leftover_sanity_check(sc[1]):
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
assert len(winnings) == 1
