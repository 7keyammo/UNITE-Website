import { NextResponse, type NextRequest } from 'next/server';
import { getStripe } from '@/lib/stripe';
import { createClient } from '@/lib/supabase/server';
import { createAdminClient } from '@/lib/supabase/admin';
import { siteOrigin } from '@/lib/site';

export async function POST(req: NextRequest) {
  const supabase = await createClient();
  const user = supabase ? (await supabase.auth.getUser()).data.user : null;
  if (!user) return NextResponse.redirect(new URL('/login?next=/account', req.url), { status: 303 });
  const stripe = getStripe();
  const admin = createAdminClient();
  const { data } = admin ? await admin.from('memberships').select('stripe_customer_id').eq('user_id', user.id).maybeSingle() : { data: null };
  if (!stripe || !data?.stripe_customer_id) return NextResponse.redirect(new URL('/account?billing=unavailable', req.url), { status: 303 });
  const portal = await stripe.billingPortal.sessions.create({ customer: data.stripe_customer_id, return_url: `${await siteOrigin()}/account` });
  return NextResponse.redirect(portal.url, { status: 303 });
}
