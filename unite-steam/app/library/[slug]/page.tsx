import type { Metadata } from 'next';
import Link from 'next/link';
import { notFound } from 'next/navigation';
import { readerPages, summary } from '@/lib/books';
import { getViewer } from '@/lib/membership';

type Params = { params: Promise<{ slug: string }> };

export async function generateMetadata({ params }: Params): Promise<Metadata> {
  const b = summary((await params).slug);
  return { title: b ? b.title : 'Book' };
}

export default async function BookOutline({ params }: Params) {
  const { slug } = await params;
  const b = summary(slug);
  if (!b) notFound();
  const { user, access } = await getViewer();
  const pages = access.homeschool ? readerPages(slug) : null;

  return (
    <div className="bookpage">
      <div className="shell crumb"><Link href="/library" style={{ color: 'var(--ink-muted)', fontSize: '0.85rem' }}>&larr; Back to the library</Link></div>
      <div className="shell bookhead">
        <span className="label">The Wonder Ship series</span>
        <h1>{b.title}</h1>
        <p className="blurb">{b.blurb}</p>
        {b.curriculum ? (
          <p className="curric">
            <strong>Feeds</strong> {b.curriculum}
            <br />
            <span>
              EFV = Energy, Frequency &amp; Vibration (15 lessons, K–2). STEAM = STEAM + Music
              (15 classes, K–2).
            </span>
          </p>
        ) : null}
        <div className="metaline">
          <span className="m">{b.pageCount} pages</span>
          <span className="m">~{b.minutes} min</span>
          <span className="m">{b.chooseCount} choose moments</span>
          {b.world ? <span className="m">{b.world}</span> : null}
        </div>
      </div>
      <div className="shell">
        {pages ? (
          <>
            <div className="actrow">
              <Link className="act primary" href={`/read/${slug}`}>&#9654; Read (timed)</Link>
            </div>
            <div className="section-head"><h2>Page by page</h2></div>
            <p className="section-sub">
              Every page: the read-aloud line, the movement or choice, and about how long to linger. Gold pages are <b>Your Turn</b>, where the kids decide.
            </p>
            <div className="spreads">
              {pages.map((p, i) => (
                <div key={i} className={'spread beat' + (p.type === 'choose' ? ' interact' : '')}>
                  <div className="thumb" dangerouslySetInnerHTML={{ __html: p.artSvg }} />
                  <div>
                    {p.type === 'choose' ? (
                      <>
                        <h4>{i + 1}. {p.kicker} &mdash; tap to choose</h4>
                        <p>{p.q}</p>
                        <span className="move pick">&#128072; kids pick from {p.options?.length} options</span>
                      </>
                    ) : (
                      <>
                        <h4>{i + 1}. {p.kicker}</h4>
                        <p>{p.line}</p>
                        <span className="move">&#9995; {p.cue}</span>
                      </>
                    )}
                  </div>
                  <div className="secs">{p.secs}s</div>
                </div>
              ))}
            </div>
          </>
        ) : (
          <div className="gate" style={{ margin: '1.5rem auto 4rem' }}>
            <h2>&#128274; Members only</h2>
            <p>The full page-by-page story, read-aloud lines and Your Turn moments unlock with Homeschool Hub or Saturday School.</p>
            <Link className="btn dark" href={user ? '/pricing?need=homeschool' : `/login?next=/library/${slug}`} style={{ display: 'block' }}>
              {user ? 'Choose a plan' : 'Log in to read'}
            </Link>
            {!user && <p className="mini">New here? <Link href="/pricing" style={{ color: 'var(--coral)', fontWeight: 600 }}>See plans</Link></p>}
          </div>
        )}
      </div>
    </div>
  );
}
