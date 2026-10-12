'use client';
import Link from 'next/link';
import { usePathname } from 'next/navigation';

const LINKS = [
  { href: '/', label: 'Home' },
  { href: '/library', label: 'Library' },
  { href: '/saturday-school', label: 'Saturday School' },
  { href: '/pricing', label: 'Pricing' },
];

export default function Nav() {
  const path = usePathname();
  return (
    <nav className="tabs" aria-label="Main">
      {LINKS.map((l) => {
        const active = l.href === '/' ? path === '/' : path.startsWith(l.href);
        return (
          <Link key={l.href} href={l.href} className={active ? 'active' : undefined}>
            {l.label}
          </Link>
        );
      })}
    </nav>
  );
}
