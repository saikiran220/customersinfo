-- Run this in Supabase Dashboard: SQL Editor → New query → paste and Run
-- Safe to run multiple times (idempotent). Creates "users" table and allows anon to insert/select.

-- Create table
CREATE TABLE IF NOT EXISTS public.users (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name TEXT NOT NULL,
  father_name TEXT NOT NULL,
  mobile_no TEXT NOT NULL,
  created_at TIMESTAMPTZ DEFAULT now()
);

-- Enable Row Level Security (RLS)
ALTER TABLE public.users ENABLE ROW LEVEL SECURITY;

-- Drop policies if they exist so this script can be re-run
DROP POLICY IF EXISTS "Allow anon insert" ON public.users;
DROP POLICY IF EXISTS "Allow anon select" ON public.users;

-- Allow anonymous (anon key) to insert and select
CREATE POLICY "Allow anon insert" ON public.users
  FOR INSERT TO anon WITH CHECK (true);

CREATE POLICY "Allow anon select" ON public.users
  FOR SELECT TO anon USING (true);
