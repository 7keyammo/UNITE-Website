import type { Metadata, Viewport } from 'next';
import Link from 'next/link';
import Nav from '@/components/Nav';
import { getViewer } from '@/lib/membership';
import './globals.css';

export const metadata: Metadata = {
  title: { default: 'UNITE STEAM', template: '%s · UNITE STEAM' },
  description:
    'Afrocentric, youth-led STEAM learning from UNITE: the Homeschool Hub, Saturday School in Oakland, and custom curriculum.',
  metadataBase: new URL(process.env.NEXT_PUBLIC_SITE_URL || 'http://localhost:3000'),
};
// Every page checks who is logged in, so render on each request.
export const dynamic = 'force-dynamic';
export const viewport: Viewport = { themeColor: '#17141F', width: 'device-width', initialScale: 1 };

export default async function RootLayout({ children }: { children: React.ReactNode }) {
  const { user, devUnlocked } = await getViewer();
  return (
    <html lang="en">
      <head>
        <link rel="preconnect" href="https://fonts.googleapis.com" />
        <link rel="preconnect" href="https://fonts.gstatic.com" crossOrigin="" />
        {/* eslint-disable-next-line @next/next/no-page-custom-font */}
        <link
          rel="stylesheet"
          href="https://fonts.googleapis.com/css2?family=Baloo+2:wght@500;600;700;800&family=Public+Sans:ital,wght@0,400;0,500;0,600;1,400&family=IBM+Plex+Mono:wght@500;600&display=swap"
        />
      </head>
      <body>
        <div className="topbar">
          <div className="shell">
            <Link href="/" className="brand">
              UNITE<em> </em>STEAM
            </Link>
            <Nav />
            <Link href={user ? '/account' : '/login'} className="acctbtn">
              {user ? 'My account' : 'Log in'}
            </Link>
          </div>
        </div>
        {devUnlocked && (
          <div className="protobanner">
            <div className="shell">
              <p>
                <b>Dev preview.</b> DEV_UNLOCK_ALL is on, so member content is visible without logging in. This never
                applies in production.
              </p>
            </div>
          </div>
        )}
        <main>{children}</main>
        <footer>
          <p>
            <span className="footlinks">
              <span>&copy; {new Date().getFullYear()} UNITE &middot; Oakland, CA</span>
              <a href="https://unitehella.org" rel="noopener">unitehella.org</a>
              <Link href="/privacy">Privacy</Link>
              <Link href="/terms">Terms</Link>
              <Link href="/pricing#contact">Contact</Link>
            </span>
          </p>
        </footer>
      </body>
    </html>
  );
}
