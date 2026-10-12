import type { Metadata } from 'next';
import Link from 'next/link';
import { redirect } from 'next/navigation';
import { getViewer, isActive } from '@/lib/membership';
import { CADENCES, PLANS } from '@/lib/plans';

export const metadata: Metadata = { title: 'My account', robots: { index: false } };

export default async function Account({ searchParams }: { searchParams: Promise<Record<string, string | undefined>> }) {
  const sp = await searchParams;
  const { user, membership, access } = await getViewer();
  if (!user) redirect('/login?next=/account');
  const active = isActive(membership);
  const plan = active && membership?.plan ? PLANS[membership.plan] : null;
  const renew = membership?.current_period_end ? new Date(membership.current_period_end).toLocaleDateString('en-US', { month: 'long', day: 'numeric', year: 'numeric' }) : null;

  return (
    <div className="shell">
      <div className="offer-head"><span className="label">Your account</span><h1>Welcome back</h1><p>{user.email}</p></div>
      {sp.checkout === 'success' && !active && (
        <div className="notice ok">Payment received, thank you! Your access switches on within a few seconds. Refresh this page if it hasn&rsquo;t yet.</div>
      )}
      {sp.checkout === 'success' && active && <div className="notice ok">You&rsquo;re all set. Welcome to {plan?.name}!</div>}
      {sp.billing === 'unavailable' && <div className="notice err">Billing isn&rsquo;t available right now. Please try again later.</div>}

      <div className="acctstatus">
        <p>
          <b>Plan:</b> {plan ? `${plan.name}${membership?.cadence ? ` (${CADENCES[membership.cadence].label.toLowerCase()})` : ''}` : 'No active plan'}
          {plan && membership?.status === 'past_due' && ' · payment past due, please update your card'}
          {plan && renew && ` · renews ${renew}`}
        </p>
        <div style={{ display: 'flex', gap: '0.5rem', flexWrap: 'wrap' }}>
          {membership?.stripe_customer_id && (
            <form action="/api/billing-portal" method="post"><button type="submit">Manage billing</button></form>
          )}
          <form action="/auth/signout" method="post"><button type="submit">Log out</button></form>
        </div>
      </div>

      <div className="pickline"><h2>Your access</h2></div>
      <div className="pricegrid">
        <div className="pricecard">
          <h3>Homeschool Hub</h3>
          <p style={{ fontSize: '0.88rem', color: 'var(--ink-muted)' }}>{access.homeschool ? '✓ Full access to the library' : 'Not included in your plan'}</p>
          {access.homeschool ? <Link className="btn dark" href="/library" style={{ textAlign: 'center' }}>Open the library</Link> : <Link className="btn dark" href="/pricing" style={{ textAlign: 'center' }}>See plans</Link>}
        </div>
        <div className="pricecard">
          <h3>Saturday School</h3>
          <p style={{ fontSize: '0.88rem', color: 'var(--ink-muted)' }}>{access.saturday ? '✓ You have a seat. We email you your cohort details.' : 'Not included in your plan'}</p>
          {!access.saturday && <Link className="btn dark" href="/saturday-school" style={{ textAlign: 'center' }}>Add Saturday School</Link>}
        </div>
      </div>
    </div>
  );
}
