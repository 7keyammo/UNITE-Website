import { NextResponse, type NextRequest } from 'next/server';
import { createAdminClient } from '@/lib/supabase/admin';
import { clean, isEmail } from '@/lib/forms';

export async function POST(req: NextRequest) {
  const b = await req.json().catch(() => ({}));
  if (clean(b.website, 200)) return NextResponse.json({ ok: true }); // bot trap
  const row = {
    parent_name: clean(b.parent_name, 120),
    email: clean(b.email, 200).toLowerCase(),
    age_range: clean(b.age_range, 60),
    interest: clean(b.interest, 80),
  };
  if (!row.parent_name || !isEmail(row.email)) return NextResponse.json({ error: 'Please add your name and a valid email.' }, { status: 400 });
  const admin = createAdminClient();
  if (!admin) return NextResponse.json({ error: 'Sign-ups open very soon. Please try again shortly.' }, { status: 503 });
  const { error } = await admin.from('interest_signups').insert(row);
  if (error) return NextResponse.json({ error: 'We could not save that. Please try again.' }, { status: 500 });
  return NextResponse.json({ ok: true });
}
