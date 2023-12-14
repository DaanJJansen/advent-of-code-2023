import re
from typing import List

class Pair():
    def __init__(self, left, right):
        self.left = int(left)
        self.right = int(right)
        self.distance = self.right-self.left

class Sequence():
    def __init__(self, arr: List):
        self.next_value = 0
        self.arr = arr
        #added for answer two
        self.arr.reverse()
        self.levels = []
        self.create_levels()
        self.extrapolate_levels()
        
    def create_levels(self):
        total_distance = 1
        arr = self.arr
        while total_distance > 0:
            new_pairs = self.define_pairs(arr)
            self.levels.append(new_pairs)
            total_distance = sum([abs(pair.distance) for pair in new_pairs])
            arr = [pair.distance for pair in new_pairs]

    def extrapolate_levels(self):
        for index, level in enumerate(reversed(self.levels)):
            last_pair = level[-1]
            if index == 0:
                distance = 0
            else:
                distance = self.levels[-(index)][-1].distance

            self.levels[-(index+1)].append(Pair(last_pair.right, (last_pair.right+last_pair.distance +distance)))
        self.next_value = self.levels[0][-1].right


    def define_pairs(self, arr):
        left =  arr[0:-1:1]
        right = arr[1::1]
        pairs = []
        for left,right in zip(left,right):
            pairs.append(Pair(left, right))
        return pairs

    @classmethod
    def from_string(cls, string):
        arr = string.split(" ")
        return cls(arr)

sequences = []
with open("day9/input.txt") as file:
    for line in file:
        sequences.append(Sequence.from_string(line.replace("\n", "")))

answer_1 = sum([sequence.next_value for sequence in sequences])
print("test")
#1996044973
#1995001592



