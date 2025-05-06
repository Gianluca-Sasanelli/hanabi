# -*- coding: utf-8 -*-

from player import Player

class Agent(Player):

    COLORS = ['Red', 'Blue', 'Yellow', 'Green', 'White', 'Rainbow']
    MAX_NUMBER = 5

    def __init__(self, player, expert_mode):
        self.player = player
        self.expert_mode = expert_mode
        
        # At the beginning all possibilities are available
        if expert_mode:
            possible_colors = self.COLORS
        else:
            possible_colors = [color for color in self.COLORS if color != 'Rainbow']
        possible_numbers = range(1,self.MAX_NUMBER+1)
        self.known_info = [{"possible_colors": set(possible_colors),
                            "possible_numbers": set(possible_numbers)} for _ in player.cards]
    
    def receive_hint(self, hint_type, hint_info):
        """
        Updates the agent's belief about its hand based on a hint.
        """
        for card_pos, card in enumerate(self.player.cards):
            if hint_type == 'C': 
                if card.color == hint_info or card.color == "Rainbow":
                    if len(self.known_info[card_pos]["possible_colors"]) > 2:
                        self.known_info[card_pos]["possible_colors"] = {hint_info, 'Rainbow'}
                    else:
                        self.known_info[card_pos]["possible_colors"] = {'Rainbow'}
                else:
                    self.known_info[card_pos]["possible_colors"].discard(hint_info, 'Rainbow')
            elif hint_type == 'N':
                if card.number == hint_info:
                    self.known_info[card_pos]["possible_numbers"] = {hint_info}
                else:
                    self.known_info[card_pos]["possible_numbers"].discard(hint_info)
    
    def set_unknown_card(self, card_pos):
        """
        Updates the agent's belief about a new card.
        Player does not have information about this card.
        """

        # At the beginning all possibilities are available
        if self.expert_mode:
            possible_colors = self.COLORS
        else:
            possible_colors = [color for color in self.COLORS if color != 'Rainbow']
        possible_numbers = range(1,self.MAX_NUMBER+1)
        self.known_info[card_pos] = {"possible_colors": set(possible_colors),
                            "possible_numbers": set(possible_numbers)}
        
    def get_agent_knowledge(self, game):
        """
        This method returns all known information the agent has about the game.
        This is the information of other players' cards, some information about its own cards and information about the board.
        """
        board_view = game.get_board_view()
        other_players_cards = game.get_player_view(self.player_id)
        known_info = self.known_info
        
        knowledge = {
            "board": board_view,
            "other_players": other_players_cards,
            "own_cards": known_info
                     }
        
        return knowledge

    def decide_action(self, game, board):
        raise NotImplementedError('This method should be overriden by an Agent with implemented logic')