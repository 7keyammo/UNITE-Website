import type { Metadata } from 'next';
export const metadata: Metadata = { title: 'Terms' };

export default function Terms() {
  return (
    <div className="shell prose">
      <h1>Terms of service</h1>
      <div className="notice info">Draft for review before launch. Have this checked by someone qualified for your situation.</div>
      <h2>Memberships</h2>
      <p>Homeschool Hub and Saturday School are subscriptions billed monthly, every six months (semester), or yearly. Saturday School includes Homeschool Hub access. Plans renew automatically until cancelled.</p>
      <h2>Cancelling</h2>
      <p>You can cancel anytime from your account. Access continues until the end of the period you have paid for.</p>
      <h2>Saturday School</h2>
      <p>Sessions run in person in Oakland. Cohorts are small, about 10 students. We confirm your cohort and start date by email after you join. A parent or guardian is responsible for drop-off and pick-up.</p>
      <h2>Content</h2>
      <p>The Wonder Ship books and other library content are for your household&rsquo;s own learning. Please don&rsquo;t share your login or redistribute the material.</p>
      <h2>Changes</h2>
      <p>We may update prices or these terms. We will tell members by email before a price change affects them.</p>
    </div>
  );
}
