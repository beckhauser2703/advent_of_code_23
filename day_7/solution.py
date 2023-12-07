from __future__ import annotations
from typing import List, Tuple, Optional
from enum import Enum, auto
from collections import Counter


class CardLabelPart1(Enum):
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


def from_string_to_cards_part_1(cards: str) -> List[CardLabelPart1]:
    from_char_to_label = {"2": CardLabelPart1.TWO,
                          "3": CardLabelPart1.THREE,
                          "4": CardLabelPart1.FOUR,
                          "5": CardLabelPart1.FIVE,
                          "6": CardLabelPart1.SIX,
                          "7": CardLabelPart1.SEVEN,
                          "8": CardLabelPart1.EIGHT,
                          "9": CardLabelPart1.NINE,
                          "T": CardLabelPart1.TEN,
                          "J": CardLabelPart1.JACK,
                          "Q": CardLabelPart1.QUEEN,
                          "K": CardLabelPart1.KING,
                          "A": CardLabelPart1.ACE, }
    return [from_char_to_label[x] for x in cards]


class HandPart1:
    def __init__(self, cards: str, bid: int):
        self.bid = bid
        self.cards = from_string_to_cards_part_1(cards)
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

    def __lt__(self, other: HandPart1) -> bool:
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
    hand_list = sorted([HandPart1(cards, int(bid)) for line in split_input
                        for cards, bid in [line.split()]])
    print(sum([(idx+1)*hand.bid for idx, hand in enumerate(hand_list)]))


class CardLabelPart2(Enum):
    JOKER = auto()
    TWO = auto()
    THREE = auto()
    FOUR = auto()
    FIVE = auto()
    SIX = auto()
    SEVEN = auto()
    EIGHT = auto()
    NINE = auto()
    TEN = auto()
    QUEEN = auto()
    KING = auto()
    ACE = auto()


def from_string_to_cards_part_2(cards: str) -> List[CardLabelPart2]:
    from_char_to_label = {"2": CardLabelPart2.TWO,
                          "3": CardLabelPart2.THREE,
                          "4": CardLabelPart2.FOUR,
                          "5": CardLabelPart2.FIVE,
                          "6": CardLabelPart2.SIX,
                          "7": CardLabelPart2.SEVEN,
                          "8": CardLabelPart2.EIGHT,
                          "9": CardLabelPart2.NINE,
                          "T": CardLabelPart2.TEN,
                          "J": CardLabelPart2.JOKER,
                          "Q": CardLabelPart2.QUEEN,
                          "K": CardLabelPart2.KING,
                          "A": CardLabelPart2.ACE, }
    return [from_char_to_label[x] for x in cards]


class HandPart2:
    def __init__(self, cards: str, bid: int):
        self.bid = bid
        self.cards = from_string_to_cards_part_2(cards)
        self.type = self.get_hand_type_from_cards()

    def get_hand_type_from_cards(self) -> HandType:
        counter = Counter(self.cards)
        if CardLabelPart2.JOKER in self.cards:
            number_of_jokers = counter[CardLabelPart2.JOKER]
            del counter[CardLabelPart2.JOKER]
            if number_of_jokers == 5:
                return HandType.FIVEOFAKIND
            key_with_highest_value = max(counter, key=counter.get)
            counter[key_with_highest_value] += number_of_jokers
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

    def __lt__(self, other: HandPart1) -> bool:
        if self.type.value != other.type.value:
            return self.type.value < other.type.value
        for card_pair in zip(self.cards, other.cards):
            if card_pair[0].value == card_pair[1].value:
                continue
            return card_pair[0].value < card_pair[1].value
        return True

    def __repr__(self) -> str:
        return f"{self.bid, self.type, self.type.value}"


def solution_part_2(input: str) -> None:
    split_input = input.split("\n")
    hand_list = sorted([HandPart2(cards, int(bid)) for line in split_input
                        for cards, bid in [line.split()]])
    print(sum([(idx+1)*hand.bid for idx, hand in enumerate(hand_list)]))


with open(r'day_7\puzzle_input.txt', 'r') as input:
    solution_part_1(input.read())
with open(r'day_7\puzzle_input.txt', 'r') as input:
    solution_part_2(input.read())
