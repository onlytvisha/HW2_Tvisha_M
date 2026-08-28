"""Streamlit-side helper for calling the deployed Modal function.

Looks the function up by name instead of importing modal_functions.py
directly, so Streamlit doesn't need Modal's own dependencies (pandas'
statistics aside) baked into its environment, and the two can be
deployed/updated independently.
"""

import modal

MODAL_APP_NAME = "streamlit-supabase-app"
MODAL_FUNCTION_NAME = "heavy_computation"


def run_heavy_computation(supabase_url: str, table: str) -> dict:
    """Run the Supabase aggregation on Modal and return its result.

    Requires `modal deploy utils/modal_functions.py` to have been run at
    least once so the function is registered under MODAL_APP_NAME.
    """
    fn = modal.Function.from_name(MODAL_APP_NAME, MODAL_FUNCTION_NAME)
    return fn.remote({"supabase_url": supabase_url, "table": table})
