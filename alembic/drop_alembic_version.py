from api.shared.db_connections import engine, get_postgres_url
import sqlalchemy as sa

def drop_alembic_version():
    """Drop the alembic_version table from the database."""
    print(f"Database URL: {get_postgres_url()}")
    
    # Use inspect to check if alembic_version table exists
    inspector = sa.inspect(engine)
    tables = inspector.get_table_names()
    
    if 'alembic_version' in tables:
        print("Found alembic_version table. Dropping it...")
        # Create a connection and execute the drop table command
        with engine.connect() as conn:
            conn.execute(sa.text("DROP TABLE alembic_version;"))
            conn.commit()
        print("Successfully dropped alembic_version table!")
    else:
        print("No alembic_version table found in the database.")

if __name__ == "__main__":
    drop_alembic_version() 