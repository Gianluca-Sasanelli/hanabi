# -*- coding: utf-8 -*-

from others.card import Card
import random 

class Deck():
    N_CARDS_DEFAULT = 50
    N_CARDS_EXPERT = 55
    CARD_DISTRIBUTION = {
        1: 3,
        2: 2,
        3: 2,
        4: 2,
        5: 1
    }
    COLORS = ['Red', 'Blue', 'Yellow', 'Green', 'White']
    MAX_NUMBER = 5


    def __init__(self):
        self.n_cards = self.N_CARDS_DEFAULT
        self.playing_deck = []
        card_id = 1

        for color in self.COLORS:
            for number, count in self.CARD_DISTRIBUTION.items():
                for _ in range(count):
                    card = Card(color=color, number=number, card_id=card_id)
                    self.playing_deck.append(card)
                    card_id += 1
        self.shuffle()
    
    def shuffle(self):
        random.shuffle(self.playing_deck)
        return self.playing_deck


