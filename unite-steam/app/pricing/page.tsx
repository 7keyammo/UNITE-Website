import type { Metadata } from 'next';
import PriceGrid from '@/components/PriceGrid';
import ContactForm from '@/components/ContactForm';
import { getViewer, isActive } from '@/lib/membership';

export const metadata: Metadata = { title: 'Offerings & pricing' };

export default async function Pricing({ searchParams }: { searchParams: Promise<Record<string, string | undefined>> }) {
  const sp = await searchParams;
  const { membership } = await getViewer();
  const current = isActive(membership) ? membership!.plan : null;
  return (
    <div className="shell">
      <div className="offer-head">
        <span className="label">UNITE STEAM offerings</span>
        <h1>Five ways to work with us.</h1>
        <p>From free open content to custom curriculum design for organizations. Pick the level that fits your family or your team.</p>
      </div>
      {sp.checkout === 'cancelled' && <div className="notice info">Checkout was cancelled. You have not been charged.</div>}
      {sp.checkout === 'unavailable' && <div className="notice err">Online payment isn&rsquo;t switched on yet. Leave your details below or on the home page and we&rsquo;ll follow up.</div>}
      {sp.need === 'homeschool' && <div className="notice info">That page is for members. Choose Homeschool Hub or Saturday School to unlock it.</div>}

      <div className="ladder">
        <div className="rung"><div className="num">1</div><div><h3>Community &amp; open content</h3><p>Free digital content from UNITE, plus a space where homeschool parents can post and share their own tasks and activities.</p><span className="tag">Free / low cost</span></div></div>
        <div className="rung"><div className="num">2</div><div><h3>Saturday School</h3><p>Weekly in-person STEAM sessions in Oakland, led by our teachers. Includes full Homeschool Hub access.</p><span className="tag">Includes tier 1 + Homeschool Hub</span></div></div>
        <div className="rung"><div className="num">3</div><div><h3>Personalized homeschool curriculum</h3><p>An ongoing consultation. We build and tune a curriculum for your child, with regular check-ins.</p><span className="tag">Consultation</span></div></div>
        <div className="rung"><div className="num">4</div><div><h3>Private tutoring</h3><p>A one-on-one version of Saturday School: the same ritual and hands-on approach, just for your child.</p><span className="tag">1:1 sessions</span></div></div>
        <div className="rung"><div className="num">5</div><div><h3>Curriculum development for organizations</h3><p>We design STEAM curriculum for schools, nonprofits and youth programs, drawing on the UNITE STEAM method.</p><span className="tag">Custom / contract</span></div></div>
      </div>

      <div className="pickline"><h2>Homeschool Hub &amp; Saturday School</h2></div>
      <PriceGrid order={['homeschool', 'saturday']} featured="saturday" currentPlan={current} />
      <p style={{ margin: '-1rem 0 2rem', color: 'var(--ink-muted)', fontSize: '0.85rem' }}>
        Saturday School always includes everything in Homeschool Hub. Semester plans cover 6 months; longer commitments cost less per month. Cancel anytime from your account.
      </p>

      <div className="pickline" id="contact"><h2>Custom work &amp; community projects</h2></div>
      <p className="section-sub">Personalized curriculum, private tutoring and organization work are priced to fit. Tell us what you need and we&rsquo;ll follow up with a quote.</p>
      <ContactForm />
    </div>
  );
}
