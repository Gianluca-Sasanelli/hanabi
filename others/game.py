# -*- coding: utf-8 -*-

from others.deck import Deck
from others.board import Board
from others.card import Card
from others.player import Player
from others.action import Action

class Game:
    """
    Represents a full game of Hanabi.

    Handles the setup of the board and players, and will include the logic
    for turn-based actions, scorekeeping, and game state.
    """

    POSSIBLE_N_PLAYERS = [2, 3, 4, 5]
    CARDS_PER_PLAYER_CONFIG = {
        2: 5,
        3: 5,
        4: 4,
        5: 4
    }

    def __init__(self, n_players, expert_mode=True, verbose = True):
        """
        Initialize the game with players and the board.

        Args:
            n_players (int): Number of players (must be 2-5).
            expert_mode (bool): If True, includes the Rainbow color.
        """
        assert n_players in self.POSSIBLE_N_PLAYERS, "Number of players must be between 2 and 5."

        self.expert_mode = expert_mode
        self.verbose = verbose
        self.n_players = n_players
        self.cards_per_player = self.CARDS_PER_PLAYER_CONFIG[n_players]
        # TODO: locate endgame and victory logic in the correct places
        self.endgame = False
        self.victory = False

        self.board = Board(expert_mode=self.expert_mode)

        self.players = []
        players_cards = [[] for _ in range(n_players)]

        for card_pos in range(self.cards_per_player):
            for player_id in range(n_players):
                new_card = self.board.deck.playing_deck.pop(0)
                players_cards[player_id].append(new_card)

        for player_id in range(n_players):
            player_cards = players_cards[player_id]
            new_player = Player(player_id=player_id, cards=player_cards)
            self.players.append(new_player)
        
        self.current_player_index = 0
    
    def get_player_view(self, player_id):
            player = self.get_player_by_id(player_id)
            visible_hands = {}
            for other in self.players:
                if other.player_id != player.player_id:
                    cards_info = []
                    for card in other.cards:
                        card_info = {"Color" : card.color, "Number" : card.number}
                        cards_info.append(card_info)
                    visible_hands[other.player_id] = cards_info

            return visible_hands
    
    def get_board_view(self):
            """
            Returns a dictionary with the player's view of the game.
            Every player can see the hints count, the lifes count, the discard pile and the played cards.

            Returns:
                dict: Keys are names different game parameters, values are those parameters.
            """
            discarded_cards = []
            for discarded_card in self.board.discard_pile:
                discarded_card_info = {"Color" : discarded_card.color, "Number" : discarded_card.number}
                discarded_cards.append(discarded_card_info)

            board_info = {"Lifes" : self.board.lifes,
                          "Hints" : self.board.hints,
                          "Discard Pile" : discarded_cards,
                          "Played Cards" : self.board.played_cards,}

            return board_info
    
    def get_player_by_id(self, player_id):
        for player in self.players:
            if player.player_id == player_id:
                return player
        raise ValueError(f"No player with ID {player_id}")


    
    def play_turn(self, action_type, action_params):
        if self.endgame:
            print("Game is already over.")
            return

        current_player = self.players[self.current_player_index]

        action_params.setdefault("player", current_player)
        action_params.setdefault("board", self.board)

        try:
            action = Action(action_type, action_params)
        except Exception as e:
            print(f"Invalid action: {e}")
            return

        # After performing the action, move to the next player
        self.next_turn()

    def next_turn(self):
        self.current_player_index = (self.current_player_index + 1) % self.n_players

    def get_current_player(self):
        return self.players[self.current_player_index]

