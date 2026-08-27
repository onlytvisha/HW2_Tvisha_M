"""Streamlit entrypoint.

Run with:
    streamlit run app/main.py
"""

import json
import sys
from pathlib import Path

# `streamlit run app/main.py` only puts this file's directory (app/) on
# sys.path, not the project root, so the sibling config/ and utils/
# packages need to be added explicitly.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import pandas as pd
import plotly.express as px
import streamlit as st

from config.settings import SUPABASE_TABLE
from utils.supabase_client import delete_rows, fetch_rows, insert_row, update_rows

st.set_page_config(page_title="Supabase + Streamlit", layout="wide")

st.title("Supabase + Streamlit")

table = st.sidebar.text_input("Table name", value=SUPABASE_TABLE)
st.sidebar.caption("Reads SUPABASE_TABLE from .env as the default.")

tab_browse, tab_insert, tab_update, tab_delete = st.tabs(
    ["Browse", "Insert", "Update", "Delete"]
)

with tab_browse:
    st.subheader(f"Rows in `{table}`")
    limit = st.slider("Row limit", 10, 100, 100, step=10)
    if st.button("Refresh", key="refresh"):
        st.cache_data.clear()

    @st.cache_data(ttl=30)
    def cached_fetch(table_name: str, row_limit: int):
        return fetch_rows(table_name, row_limit)

    try:
        rows = cached_fetch(table, limit)
        if rows:
            df = pd.DataFrame(rows)
            st.dataframe(df, use_container_width=True)

            numeric_cols = df.select_dtypes(include="number").columns.tolist()
            if numeric_cols:
                y_col = st.selectbox("Chart column", numeric_cols)
                fig = px.line(df, y=y_col, title=f"{y_col} over row order")
                st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No rows found.")
    except Exception as exc:
        st.error(f"Query failed: {exc}")

with tab_insert:
    st.subheader(f"Insert a row into `{table}`")
    st.caption("Enter one JSON object matching your table's columns.")
    new_row_json = st.text_area("Row JSON", value='{\n  "name": "example"\n}', height=150)
    if st.button("Insert row"):
        try:
            insert_row(table, json.loads(new_row_json))
            st.success("Row inserted.")
            st.cache_data.clear()
        except Exception as exc:
            st.error(f"Insert failed: {exc}")

with tab_update:
    st.subheader(f"Update rows in `{table}`")
    col1, col2 = st.columns(2)
    with col1:
        match_column = st.text_input("Match column", value="id")
        match_value = st.text_input("Match value")
    with col2:
        update_json = st.text_area(
            "Fields to update (JSON)", value='{\n  "name": "new value"\n}', height=120
        )
    if st.button("Update row(s)"):
        try:
            update_rows(table, match_column, match_value, json.loads(update_json))
            st.success("Row(s) updated.")
            st.cache_data.clear()
        except Exception as exc:
            st.error(f"Update failed: {exc}")

with tab_delete:
    st.subheader(f"Delete rows from `{table}`")
    del_column = st.text_input("Match column", value="id", key="del_col")
    del_value = st.text_input("Match value", key="del_val")
    confirm = st.checkbox("I understand this cannot be undone")
    if st.button("Delete row(s)", disabled=not confirm):
        try:
            delete_rows(table, del_column, del_value)
            st.success("Row(s) deleted.")
            st.cache_data.clear()
        except Exception as exc:
            st.error(f"Delete failed: {exc}")
