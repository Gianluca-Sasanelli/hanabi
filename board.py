# -*- coding: utf-8 -*-

from deck import Deck

class Board():

    MAX_HINTS = 8
    LIFES = 3
    
    INIT_CARDS = {
            'Red' : 0,
            'Blue' : 0,
            'Yellow' : 0,
            'Green' : 0,
            'White' : 0
            }
    INIT_CARDS_RAINBOW = {
            'Red' : 0,
            'Blue' : 0,
            'Yellow' : 0,
            'Green' : 0,
            'White' : 0,
            'Rainbow' : 0
            }
    
    VICTORY = 0

    def __init__(self, expert_mode = True):

        self.endgame = False

        # Initialize the lifes count and the hints count
        self.hints = self.MAX_HINTS
        self.lifes = self.LIFES
        
        # Initialize the discard pile
        self.discard_pile = []

        # Initialize the deck
        self.expert_mode = expert_mode
        self.deck = Deck(self.expert_mode)

        # Initialize the played_cards
        # TODO: Change the logic of the played_cards pile to be a list containing the cards list
        if self.expert_mode == True:
            self.played_cards = self.INIT_CARDS_RAINBOW
        else:
            self.played_cards = self.INIT_CARDS
    
    def get_board_view(self):

        board_view = {
            "n_hints": self.hints,
            "n_lifes": self.lifes,
            "discard_pile": self.discard_pile,
            "played_cards": self.played_cards
            }

        return board_view
    
