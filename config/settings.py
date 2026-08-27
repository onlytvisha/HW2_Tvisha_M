"""Central place for environment-driven configuration.

Loads variables from a local .env file (via python-dotenv) and exposes
them as plain module attributes so the rest of the app never touches
os.environ directly.
"""

import os

from dotenv import load_dotenv

load_dotenv()

# --- Supabase ---
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")
SUPABASE_TABLE = os.environ.get("SUPABASE_TABLE", "items")

# --- Modal ---
# Modal's own auth normally lives in ~/.modal.toml (set via `modal token new`
# or `modal token set`), but these let a deployment inject credentials
# through environment variables / Streamlit secrets instead.
MODAL_TOKEN_ID = os.environ.get("MODAL_TOKEN_ID")
MODAL_TOKEN_SECRET = os.environ.get("MODAL_TOKEN_SECRET")

# --- App ---
APP_ENV = os.environ.get("APP_ENV", "development")


def require_supabase_config() -> None:
    """Raise a clear error if Supabase credentials are missing."""
    if not SUPABASE_URL or not SUPABASE_KEY:
        raise RuntimeError(
            "Missing SUPABASE_URL / SUPABASE_KEY. Copy .env.example to .env "
            "(or set st.secrets) and fill in your Supabase project's API URL "
            "and key from Project Settings -> API."
        )
