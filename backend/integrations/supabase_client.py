import os
from typing import Optional

try:
    from supabase import create_client, Client
except Exception:
    create_client = None  # type: ignore
    Client = object  # type: ignore



def get_supabase_client():
    """Create and return a Supabase client using service role for backend access.

    Requires environment variables:
      - SUPABASE_URL
      - SUPABASE_SERVICE_ROLE_KEY
    """
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
    if not url or not key:
        raise RuntimeError(
            "SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY must be set for Supabase integration"
        )
    if create_client is None:
        raise RuntimeError(
            "supabase package is not installed. Add 'supabase' to requirements.txt"
        )
    return create_client(url, key)


