"""Thin wrapper around the Supabase client plus a few CRUD helpers."""

import streamlit as st
from supabase import Client, create_client

from config.settings import SUPABASE_KEY, SUPABASE_URL, require_supabase_config


@st.cache_resource
def get_client() -> Client:
    require_supabase_config()
    return create_client(SUPABASE_URL, SUPABASE_KEY)


def fetch_rows(table: str, limit: int = 100) -> list[dict]:
    client = get_client()
    response = client.table(table).select("*").limit(limit).execute()
    return response.data


def insert_row(table: str, payload: dict) -> None:
    get_client().table(table).insert(payload).execute()


def update_rows(table: str, match_column: str, match_value, payload: dict) -> None:
    get_client().table(table).update(payload).eq(match_column, match_value).execute()


def delete_rows(table: str, match_column: str, match_value) -> None:
    get_client().table(table).delete().eq(match_column, match_value).execute()
