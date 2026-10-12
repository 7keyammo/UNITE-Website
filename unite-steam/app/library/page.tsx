import type { Metadata } from 'next';
import Link from 'next/link';
import { coverSvg, listBooks } from '@/lib/books';
import { getViewer } from '@/lib/membership';

export const metadata: Metadata = { title: 'Library: 5 & under' };

export default async function Library() {
  const { access } = await getViewer();
  const books = listBooks();
  return (
    <div className="u5">
      <div className="pbanner">
        <div className="shell">
          <span className="who">Homeschool Hub &middot; ages 3&ndash;5</span>
          <h1 className="wordmark">The Wonder Ship</h1>
          <p className="mission">
            The classroom becomes a time ship. Kids calm it with their breath, power it up with a clapping beat, then travel
            under the sea, into space, and back to the dinosaurs with Mr. Domkam and Mr. Johnson.
          </p>
          <div className="shipstrip">
            <span className="chip">Breathe to calm the ship</span>
            <span className="chip">Clap to power up</span>
            <span className="chip">Travel &amp; explore</span>
            <span className="chip">Land &amp; share</span>
          </div>
        </div>
      </div>
      <div className="shell">
        <div className="section-head"><h2>The books</h2></div>
        <p className="section-sub">
          Each book is a 20&ndash;30 minute guided read-aloud with movement cues and tap-to-choose moments.
          {access.homeschool ? ' Tap a cover for the outline, or Read for the full timed story.' : ' Members can open every page; anyone can browse the covers.'}
        </p>
        <div className="booklib">
          {books.map((b) => (
            <Link key={b.slug} className="bookcard" href={`/library/${b.slug}`}>
              <div className="cover">
                <div style={{ height: '100%' }} dangerouslySetInnerHTML={{ __html: coverSvg(b.slug) }} />
                <div className="ctitle">{b.title}</div>
              </div>
              <div className="bookbody">
                <p>{b.blurb}</p>
                <div className="statusrow">
                  <span className={'pill ' + b.status}>{b.status === 'ready' ? 'Ready' : 'Draft'}</span>
                  <span className="label">~{b.minutes} min</span>
                  {access.homeschool ? (
                    <span className="readbtn">&#9654; Open</span>
                  ) : (
                    <span className="readbtn lockbadge">&#128274; Members only</span>
                  )}
                </div>
              </div>
            </Link>
          ))}
        </div>
        {!access.homeschool && (
          <div className="gate" style={{ margin: '2.4rem auto 3rem' }}>
            <h2>Unlock the full library</h2>
            <p>Every book, page and Read mode is included with Homeschool Hub, or with Saturday School.</p>
            <Link className="btn dark" href="/pricing" style={{ display: 'block' }}>See plans</Link>
          </div>
        )}
      </div>
    </div>
  );
}
