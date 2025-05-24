# -*- coding: utf-8 -*-

from others.deck import Deck

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
    
    VICTORY = 0

    def __init__(self, expert_mode = True):
        self.endgame = False
        self.hints = self.MAX_HINTS
        self.lifes = self.LIFES
    
        self.discard_pile = []

        self.deck = Deck(self.expert_mode)

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
    
