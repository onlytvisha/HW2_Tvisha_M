"""Example Modal remote function, callable from the Streamlit app.

Deploy it once with:
    modal deploy utils/modal_functions.py

Streamlit calls it via `modal.Function.from_name(...)` (see
`utils/modal_client.py`), so the app and this file can be deployed/updated
independently.
"""

import modal

app = modal.App("streamlit-supabase-app")

image = modal.Image.debian_slim().pip_install("pandas", "supabase")


@app.function(image=image, secrets=[modal.Secret.from_name("custom-secret")])
def heavy_computation(payload: dict) -> dict:
    """CPU-heavy aggregation over Supabase rows, run off the Streamlit process.

    Uses the `custom-secret` Modal secret for SUPABASE_KEY so the service
    role/anon key never has to be duplicated into Modal's own env config.
    """
    import os

    import pandas as pd
    from supabase import create_client

    rows = payload.get("rows")
    if rows is None:
        supabase_url = payload["supabase_url"]
        supabase_key = os.environ["SUPABASE_KEY"]
        table = payload["table"]
        client = create_client(supabase_url, supabase_key)
        rows = client.table(table).select("*").execute().data

    df = pd.DataFrame(rows)
    numeric_cols = df.select_dtypes(include="number").columns.tolist()
    summary = {col: df[col].describe().to_dict() for col in numeric_cols}
    return {"row_count": len(df), "columns": list(df.columns), "summary": summary}


@app.local_entrypoint()
def main():
    result = heavy_computation.remote({"rows": [{"a": 1}, {"a": 2}]})
    print(result)
