import 'server-only';
import type Stripe from 'stripe';
import { createAdminClient } from './supabase/admin';
import { getStripe } from './stripe';
import { ACTIVE_STATUSES } from './membership';

function periodEnd(sub: Stripe.Subscription): string | null {
  // Newer Stripe API versions keep the period on the subscription item.
  const item = sub.items?.data?.[0] as unknown as { current_period_end?: number } | undefined;
  const legacy = (sub as unknown as { current_period_end?: number }).current_period_end;
  const ts = item?.current_period_end ?? legacy;
  return ts ? new Date(ts * 1000).toISOString() : null;
}

/** Mirror a Stripe subscription into the memberships table. */
export async function syncSubscription(sub: Stripe.Subscription) {
  const admin = createAdminClient();
  if (!admin) throw new Error('Supabase admin client not configured');
  const customerId = typeof sub.customer === 'string' ? sub.customer : sub.customer.id;

  let userId = sub.metadata?.user_id;
  if (!userId) {
    const { data } = await admin.from('memberships').select('user_id').eq('stripe_customer_id', customerId).maybeSingle();
    userId = data?.user_id;
  }
  if (!userId) return { skipped: 'no user for subscription ' + sub.id };

  const { data: row } = await admin.from('memberships').select('stripe_subscription_id').eq('user_id', userId).maybeSingle();
  const isActiveNow = ACTIVE_STATUSES.includes(sub.status);

  if (row?.stripe_subscription_id && row.stripe_subscription_id !== sub.id) {
    // An older or different subscription. Ignore it unless this one is the live one.
    if (!isActiveNow) return { skipped: 'stale subscription ' + sub.id };
    // The family switched plans: cancel the previous subscription and credit unused time.
    const stripe = getStripe();
    try {
      await stripe?.subscriptions.cancel(row.stripe_subscription_id, { prorate: true });
    } catch {
      /* already cancelled */
    }
  }

  const { error } = await admin.from('memberships').upsert(
    {
      user_id: userId,
      plan: sub.metadata?.plan ?? null,
      cadence: sub.metadata?.cadence ?? null,
      status: sub.status,
      current_period_end: periodEnd(sub),
      stripe_customer_id: customerId,
      stripe_subscription_id: sub.id,
      updated_at: new Date().toISOString(),
    },
    { onConflict: 'user_id' },
  );
  if (error) throw error;
  return { ok: true };
}
