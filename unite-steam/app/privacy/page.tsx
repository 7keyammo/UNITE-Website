import type { Metadata } from 'next';
export const metadata: Metadata = { title: 'Privacy' };

export default function Privacy() {
  return (
    <div className="shell prose">
      <h1>Privacy policy</h1>
      <div className="notice info">Draft for review before launch. Have this checked by someone qualified for your situation.</div>
      <h2>Who holds the account</h2>
      <p>UNITE STEAM accounts are held by a parent, guardian or organization contact. Children do not create accounts or log in, and we do not ask for children&rsquo;s names, birthdates, photos or contact details through this site.</p>
      <h2>What we collect</h2>
      <ul>
        <li>Account details: your email address and a password (stored securely by our authentication provider, Supabase).</li>
        <li>Membership details: your plan, billing period and subscription status.</li>
        <li>Payments: handled by Stripe. We never see or store your full card number.</li>
        <li>Forms: the name, email, age range and interests you send through our registration and contact forms.</li>
      </ul>
      <h2>How we use it</h2>
      <p>To give members access to what they paid for, to confirm Saturday School seats, to reply to your questions, and to send occasional updates you asked for. We do not sell your information.</p>
      <h2>Your choices</h2>
      <p>You can cancel your plan anytime from your account. To have your account and data deleted, contact us and we will remove it.</p>
      <h2>Contact</h2>
      <p>UNITE, Oakland, California. Use the contact form on the pricing page.</p>
    </div>
  );
}
