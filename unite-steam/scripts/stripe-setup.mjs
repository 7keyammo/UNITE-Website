// Creates the UNITE STEAM products and the 6 subscription prices in Stripe.
// Usage: STRIPE_SECRET_KEY=sk_test_... npm run stripe:setup   (safe to re-run)
import Stripe from 'stripe';

const key = process.env.STRIPE_SECRET_KEY;
if (!key) { console.error('Set STRIPE_SECRET_KEY first.'); process.exit(1); }
const stripe = new Stripe(key);

const PLANS = {
  homeschool: { name: 'Homeschool Hub', price: { monthly: 14, semester: 75, annual: 120 } },
  saturday: { name: 'Saturday School (includes Homeschool Hub)', price: { monthly: 89, semester: 420, annual: 750 } },
};
const CAD = { monthly: ['month', 1], semester: ['month', 6], annual: ['year', 1] };

for (const [plan, p] of Object.entries(PLANS)) {
  const existing = await stripe.products.search({ query: `metadata['unite_plan']:'${plan}'` });
  const product = existing.data[0] ?? (await stripe.products.create({ name: p.name, metadata: { unite_plan: plan } }));
  for (const [cad, [interval, count]] of Object.entries(CAD)) {
    const lookup_key = `unite_${plan}_${cad}`;
    const amount = p.price[cad] * 100;
    const have = await stripe.prices.list({ lookup_keys: [lookup_key], active: true, limit: 1 });
    if (have.data[0]?.unit_amount === amount) { console.log('ok     ', lookup_key); continue; }
    await stripe.prices.create({
      product: product.id, currency: 'usd', unit_amount: amount,
      recurring: { interval, interval_count: count },
      lookup_key, transfer_lookup_key: true, nickname: `${p.name} ${cad}`,
    });
    console.log('created', lookup_key, `$${p.price[cad]}`);
  }
}
