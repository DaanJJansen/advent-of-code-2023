from dataclasses import dataclass
from abc import ABC, abstractmethod
from typing import List


class Card():
    instances = []
    def __init__(self, symbol: str, rank: str):
        self.symbol = symbol
        self.rank = rank
        Card.instances.append(self)

    @classmethod
    def get(cls,value):
        return [inst for inst in cls.instances if inst.symbol == value].pop()
       

class Hand():
    def __init__(self, cards: List[Card], bet: int):
        self.cards = cards
        self.bet = bet
        self.score = self.calculate_score()

    def calculate_score(self):
        counts = list(set([(card,self.cards.count(card)) for card in self.cards]))
        first_level_score = Scores.calculate_score(counts)
        second_level_score = "".join([card.rank for card in self.cards])
        return str(first_level_score) + second_level_score

    @classmethod
    def from_string(cls, hand_string: str):
        cards = [] 
        str_cards, bet = hand_string.split(" ")
        for card in str_cards:
            cards.append(Card.get(card))
        return cls(cards=cards, bet=int(bet))


class Scores():
    instances = []
    def __init__(self, similiar_cards: int, points: int, pairs: int):
        self.similiar_cards = similiar_cards
        self.points = points
        self.pairs = pairs
        Scores.instances.append(self)

    @classmethod
    def calculate_score(cls, counts: List[tuple[Card, int]]):
        for score in cls.instances:
            count_pairs = len([card for card in counts if card[1] in score.similiar_cards])
            if set(score.similiar_cards).issubset(set([card[1] for card in counts])) and score.pairs == count_pairs:
                return int(score.points)
        raise Exception("Score not found")


five_of_a_kind = Scores(similiar_cards=[5], points=7, pairs=1)
four_of_a_kind = Scores(similiar_cards=[4], points=6, pairs=1)
full_house = Scores(similiar_cards=[3,2], points=5, pairs=2)
tree_of_a_kind = Scores(similiar_cards=[3], points=4, pairs=1)
two_pairs = Scores(similiar_cards=[2,2], points=3, pairs=2)
one_pair = Scores(similiar_cards=[2], points=2, pairs=1)
high_card = Scores(similiar_cards=[1], points=1, pairs=5)

card_A = Card(symbol="A", rank="13")
card_K = Card(symbol="K", rank="12")
card_Q = Card(symbol="Q", rank="11")
card_J = Card(symbol="J", rank="10")
card_T = Card(symbol="T", rank="09")
card_9 = Card(symbol="9", rank="08")
card_8 = Card(symbol="8", rank="07")
card_7 = Card(symbol="7", rank="06")
card_6 = Card(symbol="6", rank="05")
card_5 = Card(symbol="5", rank="04")
card_4 = Card(symbol="4", rank="03")
card_3 = Card(symbol="3", rank="02")
card_2 = Card(symbol="2", rank="01")

hands = []
with open("input.txt") as file:
    for line in file:
       hands.append(Hand.from_string(line.replace("\n",""))) 

hands.sort(key=lambda x: x.score, reverse=False)
amount = 0
for rank, hand in enumerate(hands):
    amount =amount + (hand.bet * (rank + 1))
    print(rank, hand.score, hand.bet, amount)

print(amount)
