# -*- coding: utf-8 -*-

from others.card import Card

class Player():
    '''
    Player contains the information associated with each player.
    It acts as a wrapper around the agents.
    params:
        player_id: code to identify each player
        n_cards: number of cards the player has
        deck: deck of the cards
    '''

    def __init__(self, player_id, cards):
        self.player_id = player_id
        self.cards = cards