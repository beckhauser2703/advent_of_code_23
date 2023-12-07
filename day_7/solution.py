from __future__ import annotations
from typing import List, Tuple, Optional
from enum import Enum, auto
from collections import Counter


class CardLabel(Enum):
    TWO = auto()
    THREE = auto()
    FOUR = auto()
    FIVE = auto()
    SIX = auto()
    SEVEN = auto()
    EIGHT = auto()
    NINE = auto()
    TEN = auto()
    JACK = auto()
    QUEEN = auto()
    KING = auto()
    ACE = auto()


class HandType(Enum):
    HIGHCARD = auto()
    ONEPAIR = auto()
    TWOPAIR = auto()
    THREEOFAKIND = auto()
    FULLHOUSE = auto()
    FOUROFAKIND = auto()
    FIVEOFAKIND = auto()


def from_string_to_cards(cards: str) -> List[CardLabel]:
    from_char_to_label = {"2": CardLabel.TWO,
                          "3": CardLabel.THREE,
                          "4": CardLabel.FOUR,
                          "5": CardLabel.FIVE,
                          "6": CardLabel.SIX,
                          "7": CardLabel.SEVEN,
                          "8": CardLabel.EIGHT,
                          "9": CardLabel.NINE,
                          "T": CardLabel.TEN,
                          "J": CardLabel.JACK,
                          "Q": CardLabel.QUEEN,
                          "K": CardLabel.KING,
                          "A": CardLabel.ACE, }
    return [from_char_to_label[x] for x in cards]


class Hand:
    def __init__(self, cards: str, bid: int):
        self.bid = bid
        self.cards = from_string_to_cards(cards)
        self.type = self.get_hand_type_from_cards()

    def get_hand_type_from_cards(self) -> HandType:
        counter = Counter(self.cards)
        if len(counter.keys()) == 5:
            return HandType.HIGHCARD
        if len(counter.keys()) == 1:
            return HandType.FIVEOFAKIND
        if 4 in counter.values():
            return HandType.FOUROFAKIND
        if 3 in counter.values():
            if 2 in counter.values():
                return HandType.FULLHOUSE
            else:
                return HandType.THREEOFAKIND
        if len(counter.keys()) == 3:
            return HandType.TWOPAIR
        return HandType.ONEPAIR

    def __lt__(self, other: Hand) -> bool:
        if self.type.value != other.type.value:
            return self.type.value < other.type.value
        for card_pair in zip(self.cards, other.cards):
            if card_pair[0].value == card_pair[1].value:
                continue
            return card_pair[0].value < card_pair[1].value
        return True

    def __repr__(self) -> str:
        return f"{self.type, self.type.value}"


def solution_part_1(input: str) -> None:
    split_input = input.split("\n")
    hand_list = sorted([Hand(cards, int(bid)) for line in split_input
                        for cards, bid in [line.split()]])
    print(sum([(idx+1)*hand.bid for idx, hand in enumerate(hand_list)]))


def solution_part_2(input: str) -> None:
    ...


with open(r'day_7\puzzle_input.txt', 'r') as input:
    solution_part_1(input.read())
# with open(r'day_7\puzzle_input.txt', 'r') as input:
    # solution_part_2(input.read())
