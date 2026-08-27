-- Run this once in the Supabase SQL Editor (Dashboard -> SQL Editor -> New query)
-- for the project referenced by SUPABASE_URL in your .env.
--
-- Creates the table the Streamlit app reads/writes by default
-- (SUPABASE_TABLE=items) and opens it up to the publishable/anon key used
-- by the app, since Supabase enables Row Level Security by default and
-- blocks all access until policies exist.
--
-- NOTE: the policies below allow anyone with the publishable key to read
-- AND write this table. That's fine for local dev / coursework, but
-- tighten it (e.g. require auth, restrict to specific columns/rows)
-- before using this with real/public data.

create table if not exists public.items (
    id bigint generated always as identity primary key,
    name text not null,
    created_at timestamptz not null default now()
);

alter table public.items enable row level security;

drop policy if exists "Allow public read" on public.items;
create policy "Allow public read" on public.items
    for select using (true);

drop policy if exists "Allow public insert" on public.items;
create policy "Allow public insert" on public.items
    for insert with check (true);

drop policy if exists "Allow public update" on public.items;
create policy "Allow public update" on public.items
    for update using (true) with check (true);

drop policy if exists "Allow public delete" on public.items;
create policy "Allow public delete" on public.items
    for delete using (true);
