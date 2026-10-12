import Link from 'next/link';
export default function NotFound() {
  return (
    <div className="shell"><div className="placeholder"><span className="label">404</span><h3>We couldn&rsquo;t find that page</h3><p><Link href="/" style={{ color: 'var(--coral)', fontWeight: 600 }}>Back to the home page</Link></p></div></div>
  );
}
