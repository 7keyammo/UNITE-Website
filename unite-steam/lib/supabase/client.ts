'use client';
import { createBrowserClient } from '@supabase/ssr';
import { SUPABASE_URL, SUPABASE_ANON_KEY, hasSupabase } from './env';

export function createClient() {
  if (!hasSupabase()) return null;
  return createBrowserClient(SUPABASE_URL, SUPABASE_ANON_KEY);
}
