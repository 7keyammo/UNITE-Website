import { NextResponse, type NextRequest } from 'next/server';
import { createAdminClient } from '@/lib/supabase/admin';
import { clean, isEmail } from '@/lib/forms';

const KINDS = ['curriculum', 'tutoring', 'org', 'other'];

export async function POST(req: NextRequest) {
  const b = await req.json().catch(() => ({}));
  if (clean(b.website, 200)) return NextResponse.json({ ok: true }); // bot trap
  const kind = KINDS.includes(b.kind) ? b.kind : 'other';
  const row = {
    kind,
    name: clean(b.name, 120),
    email: clean(b.email, 200).toLowerCase(),
    organization: clean(b.organization, 160) || null,
    message: clean(b.message, 2000) || null,
  };
  if (!row.name || !isEmail(row.email)) return NextResponse.json({ error: 'Please add your name and a valid email.' }, { status: 400 });
  const admin = createAdminClient();
  if (!admin) return NextResponse.json({ error: 'Requests open very soon. Please try again shortly.' }, { status: 503 });
  const { error } = await admin.from('consult_requests').insert(row);
  if (error) return NextResponse.json({ error: 'We could not save that. Please try again.' }, { status: 500 });
  return NextResponse.json({ ok: true });
}
