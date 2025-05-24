from src.models.Card import Card
import random 
import uuid

N_CARDS_DEFAULT = 50
CARD_DISTRIBUTION = {
    1: 3,
    2: 2,
    3: 2,
    4: 2,
    5: 1
}
COLORS = ['Red', 'Blue', 'Yellow', 'Green', 'White']




def initalize_game():
    deck = []
    for color in COLORS:
        for number, count in CARD_DISTRIBUTION.items():
            for _ in range(count):
                card = Card(color=color, value=number, card_id=str(uuid.uuid4()))
                deck.append(card)
    random.shuffle(deck)
    return deck, str(uuid.uuid4())

