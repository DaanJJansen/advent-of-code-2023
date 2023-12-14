from typing import List
import re

class Scorecard():
    def __init__(self, card_id, my_numbers: List[int], winning_numbers: List[int]):
        self.id = int(card_id)
        self.my_numbers = my_numbers
        self.winning_numbers = winning_numbers
        self.my_winning_numbers = set(self.my_numbers) & set(self.winning_numbers)
        self.winnings = self.caluculate_winnings()
        self.winning_score_cards = list(range(self.id + 1, self.id + len(self.my_winning_numbers)+1))
        self.multiplier = 0

    def caluculate_winnings(self):
        winnings = 0
        if len (self.my_winning_numbers):
            winnings = 1
            for x in range(1,len(self.my_winning_numbers)):
                winnings*= 2
        return winnings
    
    @classmethod
    def from_string(cls, scorecard_string: str):
        def extract_numbers(numbers_string):
            return re.findall(r"\d+", numbers_string)
        
        str_card_id, numbers = scorecard_string.split(":")
        card_id = extract_numbers(str_card_id).pop()
        str_my_numbers, str_winning_numbers = numbers.split("|")

        return cls(card_id, extract_numbers(str_my_numbers), extract_numbers(str_winning_numbers))
    


class Processors():
    def __init__(self):
        self.scorecards = []

    def run(self):
        with open("day4/input.txt") as file:
            for line in file:
                self.scorecards.append(Scorecard.from_string(line.replace("\n","")))

    def answer_1(self):
        return sum([scorecard.winnings for scorecard in self.scorecards],0)
    
    def answer_2(self):
        for scorecard in self.scorecards:
            for winning_score_card in scorecard.winning_score_cards:
                self.set_score_card_multiplier(scorecard.multiplier,winning_score_card)
        
        total_cards = len(self.scorecards)
        total_copies = sum([scorecard.multiplier for scorecard in self.scorecards])
        return total_cards + total_copies
    
    def set_score_card_multiplier(self,original_multiplier, card_id):
        winning_score_card = self.scorecards[card_id - 1]
        winning_score_card.multiplier += (original_multiplier+1)
        

processors = Processors()
processors.run()
print(processors.answer_1())
print(processors.answer_2())


print("test")