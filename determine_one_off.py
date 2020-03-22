import copy
from hand import Hand
from leftover_processor import LeftoverProcessor


def is_one_off(starting_hand):
    options = [starting_hand]
    checked = []
    waiting = []

    while len(options) > 0:
        hand = options.pop(0)
        if len(hand.left) <= 3:
            s_defined = sorted([hand.pair] + hand.triples + hand.sequences)
            if not (s_defined in checked):
                if hand.is_one_off():
                    waiting.extend(hand.waiting())
                checked.append(s_defined)
            continue

        leftover_processor = LeftoverProcessor(hand.left)
        if len(hand.pair) == 0:
            pair_combos = leftover_processor.get_pairs()
            for pc in pair_combos:
                options.append(Hand(pair=pc[0], triples=hand.triples, sequences=hand.sequences, left=pc[1]))

        triple_combos = leftover_processor.get_triples()
        sequence_combos = leftover_processor.get_sequences()
        for tc in triple_combos:
            triples = copy.deepcopy(hand.triples)
            triples.append(tc[0])
            new_hand = Hand(pair=hand.pair, triples=triples, sequences=hand.sequences, left=tc[1])
            options.append(new_hand)
        for sc in sequence_combos:
            seqs = copy.deepcopy(hand.sequences)
            seqs.append(sc[0])
            new_hand = Hand(pair=hand.pair, triples=hand.triples, sequences=seqs, left=sc[1])
            options.append(new_hand)

    if not waiting:
        return False, []
    return True, sorted(list(set(waiting)))


def find_waiting(hands):
    waiting = []
    for hand in hands:
        leftover_processor = LeftoverProcessor(hand.left)
        if len(hand.left) == 2:
            possible_pairs = leftover_processor.create_pairs()
            for pp in possible_pairs:
                if Hand(pair=pp[0], triples=hand.triples, sequences=hand.sequences).is_completed():
                    waiting.append(pp[1])
        elif len(hand.left) == 3:
            possible_triples = leftover_processor.create_triples()
            possible_sequences = leftover_processor.create_sequences()
            for pt in possible_triples:
                triples = copy.deepcopy(hand.triples)
                triples.append(pt[0])
                if Hand(pair=hand.pair, triples=triples, sequences=hand.sequences).is_completed():
                    waiting.append(pt[1])
            for ps in possible_sequences:
                sequences = copy.deepcopy(hand.sequences)
                sequences.append(ps[0])
                if Hand(pair=hand.pair, triples=hand.triples, sequences=sequences).is_completed():
                    waiting.append(ps[1])
    return sorted(list(set(waiting)))


raw_hand = [11, 31, 31, 31, 31, 32, 32, 33, 33, 34, 34]
one_off, waiting_list = is_one_off(Hand(left=raw_hand))
assert one_off
assert waiting_list == [11, 31, 34]

raw_hand = [41, 41, 45, 45, 45, 46, 46, 47, 47, 48, 48]
one_off, waiting_list = is_one_off(Hand(left=raw_hand))
assert one_off
assert waiting_list == [41, 45, 46, 47, 48, 49]
