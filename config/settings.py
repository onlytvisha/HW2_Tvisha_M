"""Central place for environment-driven configuration.

Loads variables from a local .env file (via python-dotenv) when running
locally, and falls back to st.secrets when running on Streamlit
Community Cloud (which exposes the dashboard's Secrets box that way,
not as plain environment variables). Either way, the rest of the app
reads plain module attributes here instead of touching os.environ or
st.secrets directly.
"""

import os

import streamlit as st
from dotenv import load_dotenv

load_dotenv()


def _get(key: str, default=None):
    if key in os.environ:
        return os.environ[key]
    try:
        return st.secrets[key]
    except Exception:
        return default


# --- Supabase ---
SUPABASE_URL = _get("SUPABASE_URL")
SUPABASE_KEY = _get("SUPABASE_KEY")
SUPABASE_TABLE = _get("SUPABASE_TABLE", "items")

# --- Modal ---
# Modal's own auth normally lives in ~/.modal.toml (set via `modal token new`
# or `modal token set`), which isn't available on Streamlit Community Cloud.
# There, set MODAL_TOKEN_ID / MODAL_TOKEN_SECRET in .streamlit/secrets.toml;
# the modal SDK itself only checks os.environ, so re-export them here for it.
MODAL_TOKEN_ID = _get("MODAL_TOKEN_ID")
MODAL_TOKEN_SECRET = _get("MODAL_TOKEN_SECRET")
if MODAL_TOKEN_ID and MODAL_TOKEN_SECRET:
    os.environ.setdefault("MODAL_TOKEN_ID", MODAL_TOKEN_ID)
    os.environ.setdefault("MODAL_TOKEN_SECRET", MODAL_TOKEN_SECRET)

# --- App ---
APP_ENV = _get("APP_ENV", "development")


def require_supabase_config() -> None:
    """Raise a clear error if Supabase credentials are missing."""
    if not SUPABASE_URL or not SUPABASE_KEY:
        raise RuntimeError(
            "Missing SUPABASE_URL / SUPABASE_KEY. Copy .env.example to .env "
            "(or set st.secrets) and fill in your Supabase project's API URL "
            "and key from Project Settings -> API."
        )
