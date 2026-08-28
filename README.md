# Streamlit + Supabase + Modal

A starter project that combines:
- **Streamlit** for the UI
- **Supabase** as the database/backend
- **Modal** for offloading heavy/serverless compute out of the Streamlit process

## Project structure

```
streamlit-supabase-app/
├── app/
│   ├── __init__.py
│   └── main.py            # Streamlit entrypoint (streamlit run app/main.py)
├── config/
│   ├── __init__.py
│   └── settings.py        # Loads .env / secrets, exposes typed config values
├── data/
│   └── .gitkeep            # Local data cache/exports (gitignored, folder kept)
├── utils/
│   ├── __init__.py
│   ├── supabase_client.py # Cached Supabase client + CRUD helpers
│   └── modal_functions.py # Example Modal remote function
├── .env                    # Your local secrets (never commit this)
├── .env.example             # Template listing required env vars
├── .gitignore
├── requirements.txt
└── README.md
```

**Why this layout:**
- `app/` only contains UI/page code — it imports from `config` and `utils` rather than talking to Supabase or Modal directly.
- `config/settings.py` is the single place environment variables are read, so secrets never get scattered across files.
- `utils/` holds reusable logic: `supabase_client.py` for DB access, `modal_functions.py` for functions that run remotely on Modal instead of in the Streamlit process.
- `data/` is for local/generated data artifacts (CSV exports, cached files) — its contents are gitignored but the folder is tracked via `.gitkeep`.

## Setup

### 1. Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate        # macOS/Linux
venv\Scripts\activate           # Windows
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Supabase

1. Create a project at [supabase.com](https://supabase.com).
2. Go to **Project Settings -> API** and copy the **Project URL** and an **API key** (publishable/anon key for read-mostly/public use, service_role key only for trusted server-side use — never ship the service_role key to a browser).
3. Copy `.env.example` to `.env` and fill in `SUPABASE_URL`, `SUPABASE_KEY`, and `SUPABASE_TABLE`.

```bash
cp .env.example .env
```

4. Create the table: open the Supabase Dashboard -> **SQL Editor** -> New query, paste the contents of [`data/schema.sql`](data/schema.sql), and run it. This creates the `items` table and Row Level Security policies that let the app's publishable/anon key read and write it (Supabase blocks all access by default until policies exist). The policies are intentionally permissive for local dev — tighten them before using this with real/public data.

Alternatively, for deployment on Streamlit Community Cloud, put the same values in `.streamlit/secrets.toml` (already gitignored) instead of `.env`.

### 4. Configure Modal

1. Sign up at [modal.com](https://modal.com) and install the CLI (already in `requirements.txt`).
2. Authenticate once locally:

```bash
modal token new
```

   This writes credentials to `~/.modal.toml` — you don't need to put them in `.env` for local dev. `MODAL_TOKEN_ID` / `MODAL_TOKEN_SECRET` in `.env.example` are only needed for CI or hosted environments that can't run `modal token new` interactively.
3. Deploy the example Modal function:

```bash
modal deploy utils/modal_functions.py
```

### 5. Run the app

```bash
streamlit run app/main.py
```

## Notes

- Secrets (`.env`, `.env.local`, `.streamlit/secrets.toml`, Modal's `.modal.toml`) are all gitignored — double-check `git status` before committing if you ever add new secret files.
- The Browse tab caches Supabase reads for 30s (`st.cache_data`) and provides a manual **Refresh** button.
- Swap `SUPABASE_TABLE` in `.env` to point the app at a different table without touching code.
