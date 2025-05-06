# -*- coding: utf-8 -*-

class Discard:
    """
    Represents a discard action in the game of Hanabi.

    This class captures all the necessary updates and checks that occur when
    a player chooses to discard a card from their hand. It handles adding the
    card to the discard pile, drawing a new one, incrementing the available hints,
    and checking for endgame conditions when a critical card is lost.

    Attributes:
        player (Player): The player performing the discard.
        card_position (int): Index of the card being discarded.
        board (Board): The current state of the game board.
    """

    def __init__(self, player, card_position, board, agents):
        """
        Initializes and executes a discard action.

        Args:
            player (Player): The player discarding the card.
            card_position (int): The index of the card in the player's hand to discard.
            board (Board): The game board containing the deck, discard pile, and hints.
        """
        self.player = player
        self.card_position = card_position
        self.board = board
        self.agents = agents
        # TODO: Change the information the player has when discarding a card

        if self.board.hints == 8:
            raise ValueError("Hints are already at maximum! Not possible to discard")

        self.update_board()
        endgame, message = self.check_endgame()
        if endgame:
            self.board.endgame = True
            print(message)
        self.agents[player.player_id].set_unknown_card(self.card_position)

    def update_board(self):
        """
        Updates the board state after discarding a card.

        - Increments the available hint tokens (if not already at max).
        - Moves the discarded card to the discard pile.
        - Replaces the discarded card with a new one from the deck.
        """
        # Increase the hint count (assumes external logic limits this to max 8)
        self.board.hints += 1

        # Move the card to the discard pile
        discarded_card = self.player.cards[self.card_position]
        self.board.discard_pile.append(discarded_card)

        # Remove the card from the player's hand
        self.player.cards.pop(self.card_position)

        # Replace with a new card from the deck if available
        if self.board.deck:
            new_card = self.board.deck.playing_deck.pop(0)
            self.player.cards.insert(self.card_position, new_card)
        
        else:
            # Add None card if the deck is not available for the remaining cards to keep their position
            self.player.cards.insert(self.card_position, None)

    def check_endgame(self):
        """
        Determines whether discarding this card causes an unwinnable state.

        Returns:
            bool: True if the game should end due to discarding a critical card, else False.
            str: Message explaining if GAMEOVER and why.

        Logic:
        - Discarding a 'Rainbow' or a number 5 (which are unique) results in game over.
        - Discarding the third and final copy of a 1 also causes game over.
        - Discarding the second and final copy of any other card results in game over.
        """
        discarded_card = self.player.cards[self.card_position]
        discard_pile = self.board.discard_pile

        # Case 1: Unique card
        if discarded_card.color == 'Rainbow' or discarded_card.number == 5:
            self.board.endgame = True 
            return True, f"GAME OVER: You have discarded the only {discarded_card.number} for {discarded_card.color}"

        # Case 2: Card number 1 (3 copies)
        elif discarded_card.number == 1:
            discarded_copies = sum(
                1 for other_card in discard_pile if discarded_card.check_equal(other_card)
            )
            if discarded_copies == 2:
                self.board.endgame = True 
                return True, f"GAME OVER: You have discarded the last {discarded_card.number} for {discarded_card.color}"
            return False, None

        # Case 3: All other cards (2 copies)
        else:
            discarded_copies = sum(
                1 for other_card in discard_pile if discarded_card.check_equal(other_card)
            )
            if discarded_copies == 1:
                self.board.endgame = True 
                return True, f"GAME OVER: You have discarded the last {discarded_card.number} for {discarded_card.color}"
            return False, None

class Hint:
    """
    Represents a hint action in the game of Hanabi.

    When a player gives a hint to another player, this class captures all the relevant
    information (e.g., who gave the hint, what type it was, and what info was shared),
    updates the board state, and updates the receiver’s card status.

    Attributes:
        player (Player): The player giving the hint.
        hint_receiver (Player): The player receiving the hint.
        hint_type (str): Type of hint — 'C' for color or 'N' for number.
        hint_info (str | int): The actual hint value — a color (e.g., 'Blue') or a number (e.g., 2).
        board (Board): The current board state object.
    """

    def __init__(self, player, hint_receiver, hint_type, hint_info, board, agents):
        """
        Initializes a Hint object and immediately applies its effects.

        Args:
            player (Player): Player giving the hint.
            hint_receiver (Player): Player receiving the hint.
            hint_type (str): Either 'C' for color or 'N' for number.
            hint_info (str): The actual color or number given as a hint.
            board (Board): The current board instance (to update hint tokens).

        Effects:
            - Decreases the number of available hints on the board.
            - Updates the receiver’s card knowledge based on the hint.
        """
        self.player = player
        self.hint_receiver = hint_receiver
        self.hint_type = hint_type
        self.hint_info = hint_info
        self.board = board
        self.agents = agents

        if self.board.hints == 0:
            raise ValueError("No hints are available!")

        self.update_board()
        self.update_hint_receiver_status()
        self.agents[hint_receiver.player_id].receive_hint(self.hint_type, self.hint_info)

    def update_hint_receiver_status(self):
        """
        Updates the hint status of the cards in the hint receiver's hand
        based on the given hint.
        """
        for card in self.hint_receiver.cards:
            card.check_hint(hint_type=self.hint_type, hint_info=self.hint_info)

    def update_board(self):
        """
        Updates the game board by decrementing the available hint tokens.
        """
        self.board.hints -= 1      

class Play:
    """
    Represents a play action in the game of Hanabi.

    This class handles the logic for playing a card from a player's hand,
    updating the board state accordingly — either successfully playing the card,
    discarding it if incorrect, and handling game-over conditions if critical cards are lost.

    Attributes:
        player (Player): The player taking the action.
        card_position (int): The index of the card in the player's hand to be played.
        board (Board): The current state of the game board.
    """

    def __init__(self, player, card_position, board):
        """
        Initializes a Play action.

        Args:
            player (Player): The player performing the play.
            card_position (int): Index of the card to play from the player's hand.
            board (Board): The current board object representing game state.
        """
        self.player = player
        self.card_position = card_position
        self.board = board

        self.update_board()
        endgame, message = self.check_endgame()
        if endgame:
            self.board.endgame = True
            print(message)
        self.agents[player.player_id].set_unknown_card(self.card_position)
    


    def update_board(self):
        """
        Executes the play action, modifying the board and player state.

        - If the play is valid (i.e., the card continues the sequence), the card is added to the board.
        - If invalid, the card is discarded.
        - If the card is critical and its loss results in an unwinnable game, end-game logic is triggered.
        - The card is removed from the player's hand and replaced with a new one from the deck.
        """
        playing_card = self.player.cards[self.card_position]

        if self.possible_to_play():
            self.board.played_cards[playing_card.color] = playing_card.number
            # TODO: implement logic to flag the victory if it is produced
        else:
            endgame, message = self.check_endgame()
            if endgame:
                self.board.endgame = True 
                print(message)
            else:
                if self.board.lifes == 0:
                    self.board.endgame = True 
                    print('GAME OVER: Reached limit of lifes!')
                else:
                    self.board.lifes += -1
                    self.board.discard_pile.append(playing_card)

        # Remove the played/discarded card from the player's hand
        self.player.cards.pop(self.card_position)

        # Replace with a new card from the deck if available
        if self.board.deck:
            new_card = self.board.deck.playing_deck.pop(0)
            self.player.cards.insert(self.card_position, new_card)
        
        else:
            # Add None card if the deck is not available for the remaining cards to keep their position
            self.player.cards.insert(self.card_position, None)

    def possible_to_play(self):
        """
        Checks if the selected card can be legally played to the board.

        Returns:
            bool: True if the card follows the correct sequence on the board, else False.
        """
        played_cards = self.board.played_cards
        playing_card = self.player.cards[self.card_position]
        return played_cards[playing_card.color] + 1 == playing_card.number

    def check_endgame(self):
        """
        Determines whether discarding this card causes an unwinnable state.

        Returns:
            bool: True if the game should end due to discarding a critical card, else False.

        Logic:
        - Discarding a 'Rainbow' or a number 5 (which are unique) results in game over.
        - Discarding the third and final copy of a 1 also causes game over.
        - Discarding the second and final copy of any other card results in game over.
        """
        discarded_card = self.player.cards[self.card_position]
        discard_pile = self.board.discard_pile

        # Case 1: Unique card
        if discarded_card.color == 'Rainbow' or discarded_card.number == 5:
            self.board.endgame = True 
            return True, f"GAME OVER: You have discarded the only {discarded_card.number} for {discarded_card.color}"

        # Case 2: Card number 1 (3 copies)
        elif discarded_card.number == 1:
            discarded_copies = sum(
                1 for other_card in discard_pile if discarded_card.check_equal(other_card)
            )
            if discarded_copies == 2:
                self.board.endgame = True 
                return True, f"GAME OVER: You have discarded the last {discarded_card.number} for {discarded_card.color}"
            return False, None

        # Case 3: All other cards (2 copies)
        else:
            discarded_copies = sum(
                1 for other_card in discard_pile if discarded_card.check_equal(other_card)
            )
            if discarded_copies == 1:
                self.board.endgame = True 
                return True, f"GAME OVER: You have discarded the last {discarded_card.number} for {discarded_card.color}"
            return False, None
        
    def check_victory(self):
        # TODO: Implement this
        self.victory = self.victory

class Action:
    """
    Represents a game action taken by a player during their turn in Hanabi.

    This class acts as a wrapper for specific action types such as giving a hint,
    playing a card, or discarding a card. It initializes the appropriate action
    class based on the given action type.

    Attributes:
        action_type (str): Type of the action, must be one of 'Hint', 'Play', or 'Discard'.
        action_params (dict): Parameters required to perform the action.
        action (Hint | Play | Discard): Instantiated action object corresponding to the type.
    """

    # Valid action types
    ACTIONS = ['Hint', 'Play', 'Discard']

    # Mapping of action type strings to their corresponding classes
    ACTION_CLASSES = {
        'Hint': Hint,
        'Play': Play,
        'Discard': Discard
    }

    def __init__(self, action_type, action_params):
        """
        Initializes an Action object.

        Args:
            action_type (str): The type of action ('Hint', 'Play', or 'Discard').
            action_params (dict): Parameters used to instantiate the corresponding action.

        Raises:
            ValueError: If the action_type is not recognized.
        """
        if action_type not in self.ACTION_CLASSES:
            raise ValueError(f"Unknown action type: {action_type}")

        self.action_type = action_type
        self.action_params = action_params
        self.action = self.ACTION_CLASSES[self.action_type](**self.action_params)
        