-- UNITE STEAM: memberships, interest sign-ups and consult requests.
-- Parents hold the accounts. No child names or birthdates are stored.

create table if not exists public.memberships (
  user_id uuid primary key references auth.users(id) on delete cascade,
  plan text check (plan in ('homeschool','saturday')),
  cadence text check (cadence in ('monthly','semester','annual')),
  status text,                         -- mirrors the Stripe subscription status
  current_period_end timestamptz,
  stripe_customer_id text unique,
  stripe_subscription_id text unique,
  updated_at timestamptz not null default now()
);

create table if not exists public.interest_signups (
  id bigint generated always as identity primary key,
  created_at timestamptz not null default now(),
  parent_name text not null,
  email text not null,
  age_range text,
  interest text,
  user_id uuid references auth.users(id) on delete set null
);

create table if not exists public.consult_requests (
  id bigint generated always as identity primary key,
  created_at timestamptz not null default now(),
  kind text not null check (kind in ('curriculum','tutoring','org','other')),
  name text not null,
  email text not null,
  organization text,
  message text
);

alter table public.memberships enable row level security;
alter table public.interest_signups enable row level security;
alter table public.consult_requests enable row level security;

-- Members can read their own membership. Only the server (service role) writes.
drop policy if exists "read own membership" on public.memberships;
create policy "read own membership" on public.memberships
  for select to authenticated using ((select auth.uid()) = user_id);

-- interest_signups and consult_requests have no client policies:
-- they are written and read only by the server and by staff in the Supabase dashboard.
