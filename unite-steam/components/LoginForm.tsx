'use client';
import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { createClient } from '@/lib/supabase/client';

type Props = { next: string; initialMode: 'login' | 'signup'; configured: boolean; heading?: string };

export default function LoginForm({ next, initialMode, configured, heading }: Props) {
  const router = useRouter();
  const [mode, setMode] = useState<'login' | 'signup' | 'link'>(initialMode);
  const [busy, setBusy] = useState(false);
  const [err, setErr] = useState('');
  const [info, setInfo] = useState('');

  async function onSubmit(e: React.FormEvent<HTMLFormElement>) {
    e.preventDefault();
    setErr(''); setInfo('');
    const supabase = createClient();
    if (!supabase) { setErr('Accounts are not switched on yet. Please check back soon.'); return; }
    const fd = new FormData(e.currentTarget);
    const email = String(fd.get('email') || '').trim();
    const password = String(fd.get('password') || '');
    const redirectTo = `${window.location.origin}/auth/callback?next=${encodeURIComponent(next)}`;
    setBusy(true);
    try {
      if (mode === 'login') {
        const { error } = await supabase.auth.signInWithPassword({ email, password });
        if (error) throw error;
        router.push(next); router.refresh();
      } else if (mode === 'signup') {
        const { data, error } = await supabase.auth.signUp({ email, password, options: { emailRedirectTo: redirectTo } });
        if (error) throw error;
        if (data.session) { router.push(next); router.refresh(); }
        else setInfo('Check your email to confirm your account. The link brings you right back here.');
      } else {
        const { error } = await supabase.auth.signInWithOtp({ email, options: { emailRedirectTo: redirectTo, shouldCreateUser: false } });
        if (error) throw error;
        setInfo('If that email has an account, a sign-in link is on its way.');
      }
    } catch (e2) {
      setErr((e2 as Error).message || 'Something went wrong.');
    } finally {
      setBusy(false);
    }
  }

  const title = heading || (mode === 'signup' ? 'Create your parent account' : mode === 'link' ? 'Email me a sign-in link' : 'Log in');
  return (
    <form className="gate" onSubmit={onSubmit}>
      <h2>{title}</h2>
      <p>{mode === 'signup' ? 'A parent or guardian holds the account. Kids never need their own login.' : 'Members get full access to the content their plan includes.'}</p>
      {!configured && <div className="notice info">Accounts switch on once the site is connected to its database.</div>}
      <input name="email" type="email" placeholder="Email address" required autoComplete="email" />
      {mode !== 'link' && (
        <input name="password" type="password" placeholder={mode === 'signup' ? 'Choose a password (8+ characters)' : 'Password'} required minLength={mode === 'signup' ? 8 : undefined} autoComplete={mode === 'signup' ? 'new-password' : 'current-password'} />
      )}
      <button className="primary" type="submit" disabled={busy}>
        {busy ? 'One moment…' : mode === 'signup' ? 'Create account' : mode === 'link' ? 'Send link' : 'Log in'}
      </button>
      {err && <div className="notice err">{err}</div>}
      {info && <div className="notice ok">{info}</div>}
      <p className="mini">
        {mode === 'login' ? (
          <>New here? <button type="button" className="switch" onClick={() => setMode('signup')}>Create an account</button> &middot; <button type="button" className="switch" onClick={() => setMode('link')}>Forgot password?</button></>
        ) : (
          <>Already have an account? <button type="button" className="switch" onClick={() => setMode('login')}>Log in</button></>
        )}
      </p>
    </form>
  );
}
