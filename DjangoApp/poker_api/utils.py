from random import shuffle

from .enumerations import (
    PokerHands,
    Rank,
    Suit,
)


class Card:
    "   Represent a card itself   "
    SUIT = None
    RANK = None
    VALUE = None
    
    def __init__(self, suit, rank):
        self.RANK = rank
        self.SUIT = suit
        self.VALUE = rank.value
 
    def __repr__(self):
        return f"<Card: {self.name()}>"

    def __gt__(self, other_instance):
        if not isinstance(other_instance, Card):
            # don't attempt to compare against unrelated types
            return NotImplemented
        return self.VALUE > other_instance.VALUE

    def __eq__(self, other_instance):
        if not isinstance(other_instance, Card):
            # don't attempt to compare against unrelated types
            return NotImplemented
        return self.VALUE == other_instance.VALUE

    def __hash__(self):
        return hash(self.name().encode())
    
    def name(self):
        return f"{self.RANK.value} of {self.SUIT.value}"
    
    
class CardDeck:
    
    __deck__ = []
    __popped__ = []

    def __init__(self):
        self.reset_deck()

    def reset_deck(self):
        self.__deck__ = []
        self.__popped__ = []
        for suit in Suit:
            for rank in Rank:
                self.__deck__.append(Card(suit, rank)) 
        shuffle(self.__deck__)

    def pop(self):
        card = self.__deck__.pop()
        self.__popped__.append(card)
        return card
    
    def in_deck(self, card):
        return card in self.__deck__
    
    def is_popped(self, card):
        return card in self.__popped__


class Player:
    """Represent one player in one particular game"""
    __username__ = None
    __hand__ = None
    __hand_size__ = 0
    __changes__ = 0
    __allow_changes__ = False
    
    def __init__(self, user_object, hand_size=5, allow_changes=False):
        self.__username__ = str(user_object)
        self.__hand__ = []
        self.__allow_changes__ = allow_changes
        self.__hand_size__ = hand_size
    
    def change_card(self, to_change, as_change):
        "Change card (from, to)"
        if self.__allow_changes__:
            if self.__changes__ < self.__hand_size__:
                self.remove_card(to_change)
                self.add_card(as_change)
                self.__changes__ += 1
            else:
                raise Exception("Max amount of changes reached")    
        else:
            raise Exception("Changes are not allowed")
    
    def add_card(self, card):
        if len(self.__hand__) < self.__hand_size__:
            self.__hand__.append(card)
        else:
            raise Exception("Maximum amount of cards reached")

    def is_me(self, user_object):
        return str(user_object) == self.__username__

    def remove_card(self, card):
        if len(self.__hand__) != 0:
            self.__hand__.remove(card)
        else:
            raise Exception("No card in hand")
    
    def get_hand(self):
        return self.__hand__
            

class Game:
    __games__ = []
    __players__ = None
    __winners__ = None
    __is_finished__ = None
    __is_started__ = False
    __card_deck__ = None
    __cards_in_hand = None
    
    def __init__(self, cards_in_hand=5):
        self.__players__ = []
        self.__winners__ = []
        self.__is_finished__ = False
        self.__card_deck__ = CardDeck()
        self.__cards_in_hand__ = cards_in_hand

    def add_player(self, player):
        if self.__is_started__:
            raise Exception("Game already started")

        if len(self.__players__) < 5:
            self.__players__.append(player)
            if len(self.__players__) == 5:
                self.start()
        else:
            raise Exception("Max number of players reached")
    
    def start(self):
        self.__is_started__ = True
        for player in self.__players__ and not self.__is_finished__:
            for _ in range(self.__cards_in_hand__):
                player.add_card(self.__card_deck__.pop())
        self.showdown()

    def check_hand(self, player):
        cards = player.get_hand()
        cards.sort(reverse=True)

        highest_hand = PokerHands.HIGH_CARD
        result = (PokerHands.HIGH_CARD, cards[0])
        
        if PokerHands.STRAIGHT > highest_hand:
            straight = self.check_straight(cards)
            if straight:
                if self.check_flush(straight):
                    highest_hand = PokerHands.STRAIGHT_FLUSH
                    result = (highest_hand, straight[0])
                else:
                    highest_hand = PokerHands.STRAIGHT
                    result = (highest_hand, straight[0])

        if PokerHands.QUADS > highest_hand:
            quads = self.check_duplicate_cards(cards, times=4)
            if quads:
                highest_hand = PokerHands.QUADS
                result = (highest_hand, quads[0])
        
        if PokerHands.ONE_PAIR > highest_hand:
            pair = self.check_duplicate_cards(cards, times=2)
            if pair:
                highest_hand = PokerHands.ONE_PAIR
                result = (highest_hand, pair[0])
                print(f"RESULT: {result}")
                
                other_cards = list(filter(lambda x: x != pair[0], cards))
                full_house = self.check_duplicate_cards(other_cards, times=3)
                if full_house:    ### https://boardgames.stackexchange.com/questions/13743/who-has-the-winning-hand-in-texas-holdem-different-full-house-hands
                    highest_hand = PokerHands.FULL_HOUSE
                    result = (highest_hand, (full_house[0], pair[0]))
                if PokerHands.TWO_PAIRS > highest_hand:
                    second_pair = self.check_duplicate_cards(other_cards, times=2)
                    if second_pair:
                        highest_hand = PokerHands.TWO_PAIRS
                        result = (highest_hand, (second_pair[0], pair[0]))
                
        if PokerHands.FLUSH > highest_hand:
            flush = self.check_flush(cards)
            if flush:
                highest_hand = PokerHands.FLUSH
                result = (highest_hand, flush[0])
        
        if PokerHands.SET > highest_hand:
            set_seq = self.check_duplicate_cards(cards, times=3)
            if set_seq:
                highest_hand = PokerHands.SET
                result = (highest_hand, set_seq[0])

        return result

    def showdown(self):
        results = dict()
        for player in self.__players__:
            results[player] = self.check_hand(player)
            print(f"{player}: {results[player]}")
        self.__winners__ = [player for player, value in results.items() if value == max(results.values())]
        self.__is_finished__ = True
        return max_values

    def get_players(self):
        return self.__players__

    def get_winners(self):
        return self.__winners__
 
    @staticmethod
    def check_duplicate_cards(hand, times=2):
        """Waiting for an <list:Cards> as an input, returns subsequence which is repeating"""
        hand.sort(reverse=True)    # To find senior subsequences first
        ranks = [element.VALUE for element in hand]
        unique_hand_ranks = list(set(ranks))
        for unique_rank in unique_hand_ranks:
            if ranks.count(unique_rank) == times:
                return list(filter(lambda x: x.VALUE == unique_rank, hand))
        return None

    @staticmethod
    def check_straight(hand):
        """Waiting for an <list:Cards> as an input, at least 4 elements long, returns subsequence which is straight"""
        hand.sort(reverse=True)    # To find senior subsequences first
        for subsequence in zip(*(hand[i:] for i in range(5))):
            ## Check if sequence is just a descending sequence - we're getting STRAIGHT_FLUSH
            if [x.VALUE for x in subsequence] == list(range(subsequence[0].VALUE,subsequence[-1].VALUE - 1, -1)):
                return list(subsequence)
        return None
        
    @staticmethod
    def check_flush(hand):
        hand.sort(reverse=True)
        hand_suits = [element.SUIT for element in hand]
        unique_hand_suits = list(set(hand_suits))
        for suit in unique_hand_suits:
            if hand_suits.count(suit) == 5:
                return list(filter(lambda x: x.SUIT == suit, hand))
        return None

    def change_card(self, player, card):
        player.change_card(card, self.__card_deck__.pop())

    def name(self):
        return f"Game with {len(self.__players__)} players, available: {not self.__is_finished__}"

    def is_finished(self):
        self.__is_finished__ = True

