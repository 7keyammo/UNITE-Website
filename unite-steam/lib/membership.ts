import 'server-only';
import type { User } from '@supabase/supabase-js';
import { createClient } from './supabase/server';
import type { Cadence, PlanKey } from './plans';

export type Membership = {
  plan: PlanKey | null;
  cadence: Cadence | null;
  status: string | null;
  current_period_end: string | null;
  stripe_customer_id: string | null;
  stripe_subscription_id: string | null;
};

export type Viewer = {
  user: User | null;
  membership: Membership | null;
  access: { homeschool: boolean; saturday: boolean };
  devUnlocked: boolean;
};

export const ACTIVE_STATUSES = ['active', 'trialing', 'past_due'];

export function isActive(m: Membership | null) {
  if (!m || !m.plan || !m.status) return false;
  return ACTIVE_STATUSES.includes(m.status);
}

/** Who is looking at the page, and what they have paid for. Always checked on the server. */
export async function getViewer(): Promise<Viewer> {
  const devUnlocked = process.env.NODE_ENV === 'development' && process.env.DEV_UNLOCK_ALL === '1';
  const supabase = await createClient();
  let user: User | null = null;
  let membership: Membership | null = null;
  if (supabase) {
    const { data } = await supabase.auth.getUser();
    user = data.user;
    if (user) {
      const { data: row } = await supabase
        .from('memberships')
        .select('plan,cadence,status,current_period_end,stripe_customer_id,stripe_subscription_id')
        .eq('user_id', user.id)
        .maybeSingle();
      membership = (row as Membership) ?? null;
    }
  }
  const active = isActive(membership);
  // Saturday School always includes the Homeschool Hub.
  const saturday = devUnlocked || (active && membership?.plan === 'saturday');
  const homeschool = devUnlocked || (active && (membership?.plan === 'homeschool' || membership?.plan === 'saturday'));
  return { user, membership, access: { homeschool, saturday }, devUnlocked };
}
