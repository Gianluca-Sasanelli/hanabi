from api.shared.db_connections import get_postgres_session
import uuid
from api.models.models import Card
from api.models.enums import CardColor, CardValue

def seed_cards():
    session = next(get_postgres_session())
    existing_count = session.query(Card).count()
    if existing_count > 0:
        print(f"Cards already seeded. Found {existing_count} cards in database.")
        return
    
    cards = []
    
    for color in CardColor:
        for _ in range(3):
            cards.append(Card(id=uuid.uuid4(), color=color, value=CardValue.ONE))
        
        for _ in range(2):
            cards.append(Card(id=uuid.uuid4(), color=color, value=CardValue.TWO))
        
        for _ in range(2):
            cards.append(Card(id=uuid.uuid4(), color=color, value=CardValue.THREE))
        
        for _ in range(2):
            cards.append(Card(id=uuid.uuid4(), color=color, value=CardValue.FOUR))
        
        cards.append(Card(id=uuid.uuid4(), color=color, value=CardValue.FIVE))
    
    session.add_all(cards)
    
    session.commit()
    
    print(f"Successfully seeded {len(cards)} cards.")
    return cards

if __name__ == "__main__":
    seed_cards()
