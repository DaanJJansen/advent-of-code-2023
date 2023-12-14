from typing import List
import re
from dataclasses import dataclass


class Marble():
    instances = []
    def __init__(self, color: str, configuration_number: int):
        self.color = color
        self.configuration_number = configuration_number
        Marble.instances.append(self)

    @classmethod
    def get(cls,value):
        return [inst for inst in cls.instances if inst.color == value].pop()

@dataclass
class MarblePlayed():
    marble: Marble
    number: int

class Round():
    def __init__(self, marbles: List[Marble]):
        self.marbles = marbles

    @classmethod
    def from_string(cls, round_string: str):
        played_marbles = []
        for str_marbles in round_string.split(","):
            number, colour = re.findall(r'\w+', str_marbles)
            played_marbles.append(MarblePlayed(Marble.get(colour), int(number)))
        return cls(marbles=played_marbles)


class Games():
    def __init__(self, id, rounds: List[Round]):
        self.id = id
        self.rounds = rounds
        self.max_marbles, self.valid_config = self.get_max_marbles()

    def get_max_marbles(self):
        max_marbles = []
        within_config = []

        for marble in Marble.instances:
            marbles_by_color=[played_marble for rnd in self.rounds for played_marble in rnd.marbles if played_marble.marble == marble]
            marble_count = 0
            if len(marbles_by_color):
                marble_count = max(marbles_by_color, key=lambda x: x.number).number
            max_marbles.append((marble, marble_count))
            within_config.append(marble.configuration_number >= marble_count)

        return max_marbles, all(within_config)
    
    @classmethod
    def from_string(cls, game_string: str):
        id_string, rounds_string = game_string.split(":")
        id = re.findall(r'\d+', id_string).pop()

        rounds = []
        for round in rounds_string.split(";"):
            rounds.append(Round.from_string(round))
        return cls(id=int(id),rounds=rounds)


red_marble = Marble(color="red", configuration_number=12)
blue_marble = Marble(color="blue", configuration_number=14)
green_marble = Marble(color="green", configuration_number=13)

games = []
with open("day2/input.txt") as file:
    for line in file:
       games.append(Games.from_string(line.replace("\n",""))) 


amount = sum([game.id for game in games if game.valid_config],0)
print(amount)

amount_part_2 = 0
for game in games:
    count = 1
    for marble, min_number in game.max_marbles:
        count *= min_number
    amount_part_2 += count

print(amount_part_2)
