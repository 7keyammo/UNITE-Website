import Link from 'next/link';
import { notFound } from 'next/navigation';
import { SHELVES } from '@/lib/shelves';

export default async function Shelf({ params }: { params: Promise<{ age: string }> }) {
  const { age } = await params;
  const s = SHELVES.find((x) => x.slug === age);
  if (!s) notFound();
  return (
    <div className="shell">
      <div className="placeholder">
        <span className="label">{s.name} shelf</span>
        <h3>Coming soon</h3>
        <p>{s.note} Members get access automatically as each shelf opens.</p>
        <p style={{ marginTop: '1rem' }}><Link href="/library" style={{ color: 'var(--coral)', fontWeight: 600 }}>Browse the 5 &amp; under shelf &rarr;</Link></p>
      </div>
    </div>
  );
}
