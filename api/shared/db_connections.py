from supabase import create_client
from contextlib import contextmanager
import os
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

supabase_client = create_client(SUPABASE_URL, SUPABASE_KEY)


def get_supabase_client():
    return supabase_client


@contextmanager
def get_db_session():
    try:
        yield supabase_client
    except Exception as e:
        print(f"Database error: {e}")
        raise
