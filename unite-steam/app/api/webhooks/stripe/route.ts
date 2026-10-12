import { NextResponse, type NextRequest } from 'next/server';
import type Stripe from 'stripe';
import { getStripe } from '@/lib/stripe';
import { syncSubscription } from '@/lib/billing';

// Stripe calls this when someone pays, renews, changes plan, or cancels.
export async function POST(req: NextRequest) {
  const stripe = getStripe();
  const secret = process.env.STRIPE_WEBHOOK_SECRET;
  if (!stripe || !secret) return NextResponse.json({ error: 'not configured' }, { status: 503 });

  const body = await req.text();
  const sig = req.headers.get('stripe-signature') ?? '';
  let event: Stripe.Event;
  try {
    event = stripe.webhooks.constructEvent(body, sig, secret);
  } catch {
    return NextResponse.json({ error: 'bad signature' }, { status: 400 });
  }

  try {
    switch (event.type) {
      case 'checkout.session.completed': {
        const s = event.data.object as Stripe.Checkout.Session;
        if (s.mode === 'subscription' && s.subscription) {
          const id = typeof s.subscription === 'string' ? s.subscription : s.subscription.id;
          await syncSubscription(await stripe.subscriptions.retrieve(id));
        }
        break;
      }
      case 'customer.subscription.created':
      case 'customer.subscription.updated':
      case 'customer.subscription.deleted':
        await syncSubscription(event.data.object as Stripe.Subscription);
        break;
    }
  } catch (err) {
    console.error('stripe webhook failed', event.type, err);
    return NextResponse.json({ error: 'handler failed' }, { status: 500 });
  }
  return NextResponse.json({ received: true });
}
