from enum import Enum, IntEnum


class PokerHands(IntEnum):
    STRAIGHT_FLUSH = 8
    QUADS = 7
    FULL_HOUSE = 6
    FLUSH = 5
    STRAIGHT = 4
    SET = 3
    TWO_PAIRS = 2
    ONE_PAIR = 1
    HIGH_CARD = 0


class Rank(IntEnum):
    """   To express values of each rank   """
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9
    TEN = 10
    JACK = 11
    QUEEN = 12
    KING = 13
    ACE = 14


class Suit(Enum):
    SPADES = 'spades'
    HEARTS = 'hearts'
    DIAMONDS = 'diamonds'
    CLUBS = 'clubs'

