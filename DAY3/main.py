import re
from multipledispatch import dispatch
from typing import List
from itertools import tee

class Line():
    def __init__(self, line):
        self.line = line
        self.max_characters = len(line)-1
        self.possible_part_numbers = re.finditer(r'\d+', self.line)
        self.gears = re.finditer(r'[*]', self.line)

    def get_characters(self,list_range: List[int]):
        range = self.fix_range_values(list_range)
        characters = []
        for index in range:
            characters.append(self.line[index])
        return characters
    
    def get_part_numbers(self, index):
        parts = []
        self.possible_part_numbers, copy_parts = tee(self.possible_part_numbers)
        for part in copy_parts:
            if (part.span()[0]-1) <= index <= part.span()[1]:
                parts.append(int(part.group(0)))
        return parts

    def fix_range_values(self, span: List[int]):
        range = span.copy()
        if range[0] < 0:
            range.remove(range[0])
        if range[-1] > self.max_characters:
            range.pop()
        return range


class Engine():
    def __init__(self):
        self.data = []
        self.real_parts = []
        self.complete_data = ""
        self.gears = []

    def add_data(self, data):
        self.data.append(Line(data))
        self.complete_data += data

    def get_adjacent_lines(self, line_number):
        lines = []
        if not line_number == 0:
            lines.append(self.data[line_number-1])
        lines.append(self.data[line_number])
        if not line_number == (len(self.data)-1):
            lines.append(self.data[line_number+1])
        return lines

    def process_real_parts(self):
        self.symbols = set(re.findall(r'[^0-9.]', self.complete_data))
        for current_line_index, line in enumerate(self.data):
            for part in line.possible_part_numbers:
                list_range = self.extend_span(part.span())

                all_adjacent_characters = []
                for line in self.get_adjacent_lines(current_line_index):
                    all_adjacent_characters.extend(line.get_characters(list_range))

                real_part = any(adjacent_characters in self.symbols for adjacent_characters in all_adjacent_characters)
                if real_part:
                    self.real_parts.append(part.group(0))

                print(current_line_index,real_part,part.group(0), all_adjacent_characters)
        
    def process_gears_ratios(self):
        for current_line_index, line in enumerate(self.data):
            for gear_ratio in line.gears:
                index = gear_ratio.span()[0]

                all_adjacent_gears = []
                for line in self.get_adjacent_lines(current_line_index):
                    all_adjacent_gears.extend(line.get_part_numbers(index))

                if len(all_adjacent_gears) == 2:
                    self.gears.append(all_adjacent_gears[0] * all_adjacent_gears[1])

    @staticmethod
    def extend_span(span):
        list_range = []
        for x in range(span[0]-1, span[1]+1):
            list_range.append(x)
        return list_range
    
my_engine = Engine()
with open("day3/input.txt") as file:
    for index, line in enumerate(file):
       my_engine.add_data(line.replace("\n",""))

# my_engine.process_real_parts()
# answer = sum([int(part_no) for part_no in my_engine.real_parts],0)
# print(answer)

my_engine.process_gears_ratios()
answer_part2 = sum([gear for gear in my_engine.gears],0)
print(answer_part2)