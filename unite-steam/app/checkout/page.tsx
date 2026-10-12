import type { Metadata } from 'next';
import Link from 'next/link';
import { redirect } from 'next/navigation';
import { getViewer, isActive } from '@/lib/membership';
import { CADENCES, isCadence, isPlan, PLANS } from '@/lib/plans';

export const metadata: Metadata = { title: 'Checkout', robots: { index: false } };

export default async function Checkout({ searchParams }: { searchParams: Promise<Record<string, string | undefined>> }) {
  const { plan, cadence } = await searchParams;
  if (!isPlan(plan) || !isCadence(cadence)) redirect('/pricing');
  const { user, membership } = await getViewer();
  if (!user) redirect(`/login?plan=${plan}&cadence=${cadence}`);
  const p = PLANS[plan];
  const switching = isActive(membership) && membership!.plan !== plan;
  return (
    <div className="shell">
      <form className="gate" action="/api/checkout" method="post">
        <h2>{p.name}</h2>
        <p>
          ${p.price[cadence]}{CADENCES[cadence].suffix}, billed {CADENCES[cadence].label.toLowerCase()} to {user.email}. You can cancel anytime from your account.
        </p>
        {switching && <div className="notice info">This replaces your current plan. Any unused time is credited to your next bill.</div>}
        <input type="hidden" name="plan" value={plan} />
        <input type="hidden" name="cadence" value={cadence} />
        <button className="primary" type="submit">Continue to secure payment</button>
        <p className="mini">Payments are handled by Stripe. <Link href="/pricing" style={{ color: 'var(--coral)' }}>Change plan</Link></p>
      </form>
    </div>
  );
}
