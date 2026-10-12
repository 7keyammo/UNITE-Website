'use client';
import Link from 'next/link';
import { useState } from 'react';

export default function RegisterForm() {
  const [state, setState] = useState<'idle' | 'sending' | 'done' | 'error'>('idle');
  const [msg, setMsg] = useState('');

  async function onSubmit(e: React.FormEvent<HTMLFormElement>) {
    e.preventDefault();
    const form = e.currentTarget;
    const body = Object.fromEntries(new FormData(form).entries());
    setState('sending');
    try {
      const res = await fetch('/api/interest', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(body),
      });
      const json = await res.json().catch(() => ({}));
      if (!res.ok) throw new Error(json.error || 'Something went wrong. Please try again.');
      setState('done');
      form.reset();
    } catch (err) {
      setState('error');
      setMsg((err as Error).message);
    }
  }

  return (
    <form className="regform" onSubmit={onSubmit}>
      <h3>Register your interest</h3>
      <p className="sub">Not ready to buy? Leave your details and we&rsquo;ll follow up.</p>
      <label htmlFor="rf-name">PARENT / GUARDIAN NAME</label>
      <input id="rf-name" name="parent_name" required maxLength={120} autoComplete="name" />
      <label htmlFor="rf-email">EMAIL</label>
      <input id="rf-email" name="email" type="email" required maxLength={200} autoComplete="email" />
      <label htmlFor="rf-age">CHILD&rsquo;S AGE RANGE</label>
      <select id="rf-age" name="age_range">
        <option>5 &amp; under</option>
        <option>Pre-teen</option>
        <option>Teenager</option>
        <option>Young adult</option>
        <option>Organization / not a child</option>
      </select>
      <label htmlFor="rf-int">I&rsquo;M INTERESTED IN</label>
      <select id="rf-int" name="interest">
        <option>Homeschool Hub</option>
        <option>Saturday School</option>
        <option>Personalized curriculum</option>
        <option>Private tutoring</option>
        <option>Curriculum for my organization</option>
      </select>
      <input type="text" name="website" tabIndex={-1} autoComplete="off" aria-hidden="true" style={{ display: 'none' }} />
      <button className="btn gold" type="submit" disabled={state === 'sending'}>
        {state === 'sending' ? 'Sending…' : 'Send my details'}
      </button>
      {state === 'done' && <div className="regdone" style={{ display: 'block' }}>Thank you! We&rsquo;ll be in touch soon.</div>}
      {state === 'error' && <div className="notice err">{msg}</div>}
      <Link className="btn ghost" href="/login?mode=signup" style={{ marginTop: '0.6rem', textAlign: 'center' }}>
        Or create an account now
      </Link>
    </form>
  );
}
