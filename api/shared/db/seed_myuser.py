from api.shared.db_connections import get_postgres_session
import uuid
import bcrypt
from api.models.models import User

def seed_myuser():
    session = next(get_postgres_session())
    
    # Check if user already exists
    existing_user = session.query(User).filter(User.email == "thebrezen@gmail.com").first()
    if existing_user:
        print("User already exists")
        return existing_user
    
    password = "Hanabi00"
    hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
    
    user = User(
        username="brezen",
        email="thebrezen@gmail.com",
        password=hashed_password.decode("utf-8")
    )
    
    session.add(user)
    session.commit()
    
    print(f"Successfully created user {user.username}")
    return user

if __name__ == "__main__":
    seed_myuser()
