import { NextResponse, type NextRequest } from 'next/server';
import { getStripe } from '@/lib/stripe';
import { createClient } from '@/lib/supabase/server';
import { createAdminClient } from '@/lib/supabase/admin';
import { CADENCES, isCadence, isPlan, lookupKey, PLANS } from '@/lib/plans';
import { isActive, type Membership } from '@/lib/membership';
import { siteOrigin } from '@/lib/site';

const go = (req: NextRequest, path: string) => NextResponse.redirect(new URL(path, req.url), { status: 303 });

export async function POST(req: NextRequest) {
  const form = await req.formData();
  const plan = form.get('plan');
  const cadence = form.get('cadence');
  if (!isPlan(plan) || !isCadence(cadence)) return go(req, '/pricing');

  const supabase = await createClient();
  const user = supabase ? (await supabase.auth.getUser()).data.user : null;
  if (!user) return go(req, `/login?plan=${plan}&cadence=${cadence}`);

  const stripe = getStripe();
  const admin = createAdminClient();
  if (!stripe || !admin) return go(req, '/pricing?checkout=unavailable');

  const { data: row } = await admin
    .from('memberships')
    .select('plan,cadence,status,current_period_end,stripe_customer_id,stripe_subscription_id')
    .eq('user_id', user.id)
    .maybeSingle();
  const membership = row as Membership | null;
  if (isActive(membership) && membership!.plan === plan) return go(req, '/account');

  let customerId = membership?.stripe_customer_id ?? null;
  if (!customerId) {
    const customer = await stripe.customers.create({ email: user.email ?? undefined, metadata: { user_id: user.id } });
    customerId = customer.id;
    await admin.from('memberships').upsert({ user_id: user.id, stripe_customer_id: customerId }, { onConflict: 'user_id' });
  }

  // Prefer the prices created by `npm run stripe:setup`; fall back to an inline price.
  const found = await stripe.prices.list({ lookup_keys: [lookupKey(plan, cadence)], active: true, limit: 1 });
  const c = CADENCES[cadence];
  const lineItem = found.data[0]
    ? { price: found.data[0].id, quantity: 1 }
    : {
        quantity: 1,
        price_data: {
          currency: 'usd',
          unit_amount: PLANS[plan].price[cadence] * 100,
          recurring: { interval: c.interval, interval_count: c.count },
          product_data: { name: `${PLANS[plan].name} (${c.label})` },
        },
      };

  const origin = await siteOrigin();
  const meta = { user_id: user.id, plan, cadence };
  const session = await stripe.checkout.sessions.create({
    mode: 'subscription',
    customer: customerId,
    client_reference_id: user.id,
    line_items: [lineItem],
    subscription_data: { metadata: meta },
    metadata: meta,
    allow_promotion_codes: true,
    success_url: `${origin}/account?checkout=success`,
    cancel_url: `${origin}/pricing?checkout=cancelled`,
  });
  return NextResponse.redirect(session.url!, { status: 303 });
}
