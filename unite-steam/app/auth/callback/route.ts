import { NextResponse, type NextRequest } from 'next/server';
import { createClient } from '@/lib/supabase/server';

// Email confirmation and sign-in links land here.
export async function GET(request: NextRequest) {
  const url = new URL(request.url);
  const code = url.searchParams.get('code');
  const nextParam = url.searchParams.get('next') || '/account';
  const next = nextParam.startsWith('/') && !nextParam.startsWith('//') ? nextParam : '/account';
  const supabase = await createClient();
  if (code && supabase) {
    const { error } = await supabase.auth.exchangeCodeForSession(code);
    if (!error) return NextResponse.redirect(new URL(next, url.origin));
  }
  return NextResponse.redirect(new URL('/login?error=link', url.origin));
}
