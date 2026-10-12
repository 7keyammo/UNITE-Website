'use client';
import { useState } from 'react';

export default function ContactForm({ defaultKind = 'curriculum' }: { defaultKind?: string }) {
  const [state, setState] = useState<'idle' | 'sending' | 'done' | 'error'>('idle');
  const [msg, setMsg] = useState('');
  async function onSubmit(e: React.FormEvent<HTMLFormElement>) {
    e.preventDefault();
    const form = e.currentTarget;
    setState('sending');
    try {
      const res = await fetch('/api/contact', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(Object.fromEntries(new FormData(form).entries())),
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
    <form className="contactform" onSubmit={onSubmit} id="contact-form">
      <label htmlFor="cf-kind">WHAT CAN WE HELP WITH?</label>
      <select id="cf-kind" name="kind" defaultValue={defaultKind}>
        <option value="curriculum">Personalized homeschool curriculum</option>
        <option value="tutoring">Private tutoring</option>
        <option value="org">Curriculum for my organization</option>
        <option value="other">Community projects / something else</option>
      </select>
      <label htmlFor="cf-name">YOUR NAME</label>
      <input id="cf-name" name="name" required maxLength={120} autoComplete="name" />
      <label htmlFor="cf-email">EMAIL</label>
      <input id="cf-email" name="email" type="email" required maxLength={200} autoComplete="email" />
      <label htmlFor="cf-org">ORGANIZATION (OPTIONAL)</label>
      <input id="cf-org" name="organization" maxLength={160} />
      <label htmlFor="cf-msg">TELL US A LITTLE MORE</label>
      <textarea id="cf-msg" name="message" rows={4} maxLength={2000} />
      <input type="text" name="website" tabIndex={-1} autoComplete="off" aria-hidden="true" style={{ display: 'none' }} />
      <button className="btn dark" type="submit" disabled={state === 'sending'}>
        {state === 'sending' ? 'Sending…' : 'Send request'}
      </button>
      {state === 'done' && <div className="notice ok">Thanks! We&rsquo;ll reply by email soon.</div>}
      {state === 'error' && <div className="notice err">{msg}</div>}
    </form>
  );
}
