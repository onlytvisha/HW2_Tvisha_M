"""Example Modal remote function, callable from the Streamlit app.

Deploy it once with:
    modal deploy utils/modal_functions.py

Then call it from Streamlit either by importing `heavy_computation` and using
`.remote(...)`, or by looking it up via `modal.Function.from_name(...)` if
the app is deployed separately from where Streamlit runs.
"""

import modal

app = modal.App("streamlit-supabase-app")

image = modal.Image.debian_slim().pip_install("pandas")


@app.function(image=image)
def heavy_computation(payload: dict) -> dict:
    """Placeholder for CPU/GPU-heavy work you don't want to run in Streamlit."""
    import pandas as pd

    df = pd.DataFrame(payload.get("rows", []))
    return {"row_count": len(df), "columns": list(df.columns)}


@app.local_entrypoint()
def main():
    result = heavy_computation.remote({"rows": [{"a": 1}, {"a": 2}]})
    print(result)
