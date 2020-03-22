import copy
from tile import Tile


class LeftoverProcessor:
    def __init__(self, nums_list):
        self.nums_list = nums_list
        self.dedupped = set(nums_list)

    def __find_leftovers(self, combos):
        possibilities = []
        for c in combos:
            left = copy.deepcopy(self.nums_list)
            for n in c:
                left.remove(n)
            possibilities.append((c, left))
        return possibilities

    def get_pairs(self):
        pairs = []
        for num in self.dedupped:
            if self.nums_list.count(num) >= 2:
                pairs.append([num, num])
        return self.__find_leftovers(pairs)

    def get_triples(self):
        triples = []
        for num in self.dedupped:
            if self.nums_list.count(num) >= 3:
                triples.append([num, num, num])
        return self.__find_leftovers(triples)

    def get_sequences(self):
        sequences = []
        dedupped = sorted(list(self.dedupped))
        for i in range(len(dedupped)-2):
            if dedupped[i+1] == dedupped[i]+1 and dedupped[i+2] == dedupped[i]+2:
                sequences.append([dedupped[i], dedupped[i+1], dedupped[i+2]])
        return self.__find_leftovers(sequences)

    def create_pairs(self):
        if len(self.nums_list) != 2:
            return []
        pairs = []
        for num in self.dedupped:
            pairs.append(([num, num], num))
        return pairs

    def create_triples(self):
        if len(self.nums_list) != 3:
            return []
        triples = []
        for num in self.dedupped:
            if self.nums_list.count(num) >= 2:
                triples.append(([num, num, num], num))
        return triples

    def create_sequences(self):
        if len(self.nums_list) != 3:
            return []
        sequences = []
        dedupped = sorted(list(self.dedupped))
        for i in range(len(dedupped)-1):
            suite = dedupped[i] // 10
            if suite <= Tile.Suite.DRAGON or suite != dedupped[i+1]//10:
                continue
            if dedupped[i+1] == dedupped[i]+1:
                if dedupped[i] % 10 != 1:
                    sequences.append(([dedupped[i]-1, dedupped[i], dedupped[i+1]], dedupped[i]-1))
                if dedupped[i+1] % 10 != 9:
                    sequences.append(([dedupped[i], dedupped[i+1], dedupped[i]+2], dedupped[i]+2))
            elif dedupped[i+1] == dedupped[i]+2:
                sequences.append(([dedupped[i], dedupped[i]+1, dedupped[i+1]], dedupped[i]+1))

        # handles missed gap case when the list already a sequence
        if len(dedupped) == 3 and dedupped[1] == dedupped[0]+1 and dedupped[2] == dedupped[1]+1:
            sequences.append(([dedupped[0], dedupped[1], dedupped[2]], dedupped[1]))
        return sequences

    @staticmethod
    def leftover_sanity_check(leftovers):
        counter = [0] * 5
        for n in leftovers:
            counter[(n//10)-1] += 1
        return not(any(c % 3 != 0 for c in counter))


# ------ create_pairs testing ------
# too many for a pair
left = [31, 33, 33]
lp = LeftoverProcessor(left)
assert lp.create_pairs() == []

# two different numbers
left = [31, 34]
lp = LeftoverProcessor(left)
assert lp.create_pairs() == [([34, 34], 34), ([31, 31], 31)]

# two same number
left = [31, 31]
lp = LeftoverProcessor(left)
assert lp.create_pairs() == [([31, 31], 31)]

# ------ create_triples testing ------
# too little for a triple
left = [32, 33]
lp = LeftoverProcessor(left)
assert lp.create_triples() == []

# one pair + one individual
left = [31, 32, 32]
lp = LeftoverProcessor(left)
assert lp.create_triples() == [([32, 32, 32], 32)]

# three same number
left = [33, 33, 33]
lp = LeftoverProcessor(left)
assert lp.create_triples() == [([33, 33, 33], 33)]

# three different numbers
left = [31, 32, 33]
lp = LeftoverProcessor(left)
assert lp.create_triples() == []

# ------ create_sequences testing ------
# too little for a triple
left = [32, 33]
lp = LeftoverProcessor(left)
assert lp.create_sequences() == []

# one pair + sequential, includes 1
left = [31, 32, 32]
lp = LeftoverProcessor(left)
assert lp.create_sequences() == [([31, 32, 33], 33)]

# three numbers (two sequential, one of different suite), includes 9
left = [38, 39, 41]
lp = LeftoverProcessor(left)
assert lp.create_sequences() == [([37, 38, 39], 37)]

# three numbers (two sequential, one wind), middle numbers
left = [11, 34, 35]
lp = LeftoverProcessor(left)
assert lp.create_sequences() == [([33, 34, 35], 33), ([34, 35, 36], 36)]

# three numbers (two gap sequential, one dragon)
left = [23, 37, 39]
lp = LeftoverProcessor(left)
assert lp.create_sequences() == [([37, 38, 39], 38)]

# one triple
left = [33, 33, 33]
lp = LeftoverProcessor(left)
assert lp.create_sequences() == []

# one sequence, middle numbers
left = [33, 34, 35]
lp = LeftoverProcessor(left)
assert lp.create_sequences() == \
       [([32, 33, 34], 32), ([33, 34, 35], 35), ([33, 34, 35], 33), ([34, 35, 36], 36), ([33, 34, 35], 34)]

# three "gap sequential" winds
left = [11, 13, 15]
lp = LeftoverProcessor(left)
assert lp.create_sequences() == []
