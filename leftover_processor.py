import copy


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
        return self.__find_leftovers(sequences)

    @staticmethod
    def leftover_sanity_check(leftovers):
        counter = [0] * 5
        for n in leftovers:
            counter[(n//10)-1] += 1
        return not(any(c % 3 != 0 for c in counter))