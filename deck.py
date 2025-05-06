# -*- coding: utf-8 -*-

from card import Card
import random 

class Deck():

    '''
    Define all playing cards of a playing deck, each card is defined by id, number and color
    '''

    N_CARDS_DEFAULT = 50
    N_CARDS_EXPERT = 55
    CARD_DISTRIBUTION = {
        1: 3,
        2: 2,
        3: 2,
        4: 2,
        5: 1
    }
    CARD_DISTRIBUTION_RAINBOW = {
        1: 1,
        2: 1,
        3: 1,
        4: 1,
        5: 1
    }
    COLORS = ['Red', 'Blue', 'Yellow', 'Green', 'White']
    COLORS_RAINBOW = ['Red', 'Blue', 'Yellow', 'Green', 'White', 'Rainbow']
    MAX_NUMBER = 5


    def __init__(self, expert_mode = True):
        '''
        params:
            expert_mode = True: Bool: when set to True, rainbow cards are included
        '''

        if expert_mode == True:
            self.n_cards = self.N_CARDS_EXPERT
        else:
            self.n_cards = self.N_CARDS_DEFAULT


        self.playing_deck = []
        card_id = 1

        for color in self.COLORS:
            for number, count in self.CARD_DISTRIBUTION.items():
                for _ in range(count):
                    card = Card(color=color, number=number, card_id=card_id)
                    self.playing_deck.append(card)
                    card_id += 1
        
        if expert_mode == True: 
            for number, count in self.CARD_DISTRIBUTION_RAINBOW.items():
                for _ in range(count):
                    card = Card(color='Rainbow', number=number, card_id=card_id)
                    self.playing_deck.append(card)
                    card_id += 1
        
        self.shuffle()
    
    def shuffle(self):
        '''
        Shuffles the playing deck before the beginning of a game
        '''
        random.shuffle(self.playing_deck)

        return self.playing_deck


