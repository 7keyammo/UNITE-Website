import type { Metadata } from 'next';
import PriceGrid from '@/components/PriceGrid';
import { getViewer, isActive } from '@/lib/membership';

export const metadata: Metadata = { title: 'Saturday School' };

export default async function SaturdaySchool() {
  const { membership } = await getViewer();
  const current = isActive(membership) ? membership!.plan : null;
  return (
    <div className="shell">
      <div className="offer-head">
        <span className="label">In person &middot; Oakland</span>
        <h1>Saturday School</h1>
        <p>Weekly hands-on STEAM sessions, led live by Mr. Domkam and Mr. Johnson. Every Saturday School seat includes full Homeschool Hub access, so families get the in-person energy and the at-home follow-through together.</p>
      </div>
      <div className="satwrap">
        <div className="satcard">
          <span className="label" style={{ color: 'var(--space-1)' }}>Currently running</span>
          <h3>Saturday pilot sessions at Circuit Launch</h3>
          <p>Small-group pilot cohorts meeting at Circuit Launch in Oakland, building toward a dedicated UNITE STEAM classroom space.</p>
          <p>Each session mirrors the Wonder Ship ritual: calm the ship, power it up, travel somewhere new, explore hands-on, and land together.</p>
          <div className="satmeta">
            <span>&#128197; Saturdays</span>
            <span>&#128205; Circuit Launch, Oakland</span>
            <span>&#128106; About 10 students per cohort</span>
          </div>
        </div>
        <div className="satcard" style={{ background: 'var(--deep-bg)' }}>
          <h3 style={{ color: 'var(--deep-ink)' }}>What&rsquo;s included</h3>
          <ul style={{ listStyle: 'none', padding: 0, margin: 0, display: 'flex', flexDirection: 'column', gap: '0.5rem', color: 'var(--ink-muted)', fontSize: '0.92rem' }}>
            <li>&#10003; A seat in the weekly in-person session</li>
            <li>&#10003; Full Homeschool Hub access (all books and tasks)</li>
            <li>&#10003; Progress shared with parents after each session</li>
            <li>&#10003; Priority access as new age shelves launch</li>
          </ul>
          <p className="seatnote">After you join, we email you to confirm your cohort and start date.</p>
        </div>
      </div>
      <div className="pickline"><h2>Choose how you join</h2></div>
      <PriceGrid order={['saturday', 'homeschool']} featured="saturday" currentPlan={current} />
    </div>
  );
}
