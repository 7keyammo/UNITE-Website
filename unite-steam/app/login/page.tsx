import type { Metadata } from 'next';
import { redirect } from 'next/navigation';
import LoginForm from '@/components/LoginForm';
import { hasSupabase } from '@/lib/supabase/env';
import { getViewer } from '@/lib/membership';
import { isCadence, isPlan, PLANS } from '@/lib/plans';

export const metadata: Metadata = { title: 'Log in', robots: { index: false } };

function safeNext(n?: string) {
  return n && n.startsWith('/') && !n.startsWith('//') ? n : '/account';
}

export default async function Login({ searchParams }: { searchParams: Promise<Record<string, string | undefined>> }) {
  const sp = await searchParams;
  let next = safeNext(sp.next);
  let heading: string | undefined;
  if (isPlan(sp.plan) && isCadence(sp.cadence)) {
    next = `/checkout?plan=${sp.plan}&cadence=${sp.cadence}`;
    heading = `Create an account for ${PLANS[sp.plan].name}`;
  }
  const { user } = await getViewer();
  if (user) redirect(next);
  const mode = sp.mode === 'signup' || heading ? 'signup' : 'login';
  return (
    <div className="shell">
      <LoginForm next={next} initialMode={mode} configured={hasSupabase()} heading={heading} />
    </div>
  );
}
