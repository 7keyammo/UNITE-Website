'use client';
import { useCallback, useEffect, useRef, useState } from 'react';
import { useRouter } from 'next/navigation';
import type { ReaderPage } from '@/lib/types';

type Props = { slug: string; title: string; pages: ReaderPage[] };

export default function Reader({ slug, title, pages }: Props) {
  const router = useRouter();
  const rootRef = useRef<HTMLDivElement>(null);
  const [idx, setIdx] = useState(0);
  const [playing, setPlayingState] = useState(true);
  const [progress, setProgress] = useState(0);
  const [picked, setPicked] = useState<Record<number, number>>({});
  const manualPause = useRef(false);
  const elapsed = useRef(0);
  const playingRef = useRef(true);
  const idxRef = useRef(0);

  const setPlaying = useCallback((v: boolean, internal = false) => {
    playingRef.current = v;
    setPlayingState(v);
    if (!internal) manualPause.current = !v;
  }, []);

  const go = useCallback(
    (n: number) => {
      const next = Math.max(0, Math.min(pages.length - 1, n));
      idxRef.current = next;
      setIdx(next);
      elapsed.current = 0;
      setProgress(0);
      // Choose pages pause the timer until the kids pick.
      if (pages[next].type === 'choose') setPlaying(false, true);
      else if (!playingRef.current && !manualPause.current) setPlaying(true, true);
    },
    [pages, setPlaying],
  );

  // Pacing timer: auto-advances each page after its own number of seconds.
  useEffect(() => {
    const t = setInterval(() => {
      if (!playingRef.current) return;
      elapsed.current += 0.25;
      const secs = pages[idxRef.current].secs;
      setProgress(Math.min(100, (elapsed.current / secs) * 100));
      if (elapsed.current >= secs) {
        if (idxRef.current < pages.length - 1) go(idxRef.current + 1);
        else setPlaying(false);
      }
    }, 250);
    return () => clearInterval(t);
  }, [pages, go, setPlaying]);

  const exit = useCallback(() => {
    if (document.fullscreenElement) document.exitFullscreen().catch(() => {});
    router.push(`/library/${slug}`);
  }, [router, slug]);

  useEffect(() => {
    const onKey = (e: KeyboardEvent) => {
      if (e.key === 'ArrowRight') { go(idxRef.current + 1); e.preventDefault(); }
      else if (e.key === 'ArrowLeft') go(idxRef.current - 1);
      else if (e.key === 'p' || e.key === 'P' || e.key === ' ') { setPlaying(!playingRef.current); e.preventDefault(); }
      else if (e.key === 'Escape' && !document.fullscreenElement) exit();
    };
    document.addEventListener('keydown', onKey);
    const prev = document.body.style.overflow;
    document.body.style.overflow = 'hidden';
    return () => { document.removeEventListener('keydown', onKey); document.body.style.overflow = prev; };
  }, [go, setPlaying, exit]);

  const touchX = useRef(0);
  const choose = (pageIdx: number, optIdx: number) => {
    setPicked((p) => ({ ...p, [pageIdx]: optIdx }));
    if (!manualPause.current) setTimeout(() => setPlaying(true, true), 400);
  };
  const toggleFs = () => {
    if (!document.fullscreenElement) rootRef.current?.requestFullscreen?.().catch(() => {});
    else document.exitFullscreen().catch(() => {});
  };

  return (
    <div className="reader" ref={rootRef}>
      <div
        className="stage"
        onTouchStart={(e) => { touchX.current = e.touches[0].clientX; }}
        onTouchEnd={(e) => {
          const dx = e.changedTouches[0].clientX - touchX.current;
          if (Math.abs(dx) > 50) go(idxRef.current + (dx < 0 ? 1 : -1));
        }}
      >
        <div className="timerwrap"><div className="timerbar" style={{ width: progress + '%' }} /></div>
        <button className="bignav left" aria-label="Previous" onClick={() => go(idx - 1)} />
        <button className="bignav right" aria-label="Next" onClick={() => go(idx + 1)} />
        <button className="tapedge left" aria-label="Previous" disabled={idx === 0} onClick={() => go(idx - 1)}>&lsaquo;</button>
        <button className="tapedge right" aria-label="Next" disabled={idx === pages.length - 1} onClick={() => go(idx + 1)}>&rsaquo;</button>
        {pages.map((p, i) => {
          const pick = picked[i];
          const swap = pick !== undefined ? p.options?.[pick]?.swapSvg : null;
          return (
            <div key={i} className={'page' + (i === idx ? ' show' : '')} aria-hidden={i !== idx}>
              <div className="art" dangerouslySetInnerHTML={{ __html: swap || p.artSvg }} />
              <div className="kicker">{p.kicker}</div>
              {p.type === 'choose' ? (
                <>
                  <div className="choose-q">{p.q}</div>
                  <div className="choose">
                    {p.options?.map((o, oi) => (
                      <button key={oi} className={'choice' + (pick === oi ? ' picked' : '')} onClick={() => choose(i, oi)}>
                        <span className="cart" dangerouslySetInnerHTML={{ __html: o.iconSvg }} />
                        <span className="clabel">{o.label}</span>
                      </button>
                    ))}
                  </div>
                  <div className="chosen-note">{pick !== undefined ? p.note || 'Great choice!' : ''}</div>
                </>
              ) : (
                <>
                  <div className="line">{p.line}</div>
                  <div className="cue">{p.cue}</div>
                  {p.note ? <div className="grownups">{p.note}</div> : null}
                </>
              )}
            </div>
          );
        })}
      </div>
      <div className="rbar">
        <button onClick={exit}>&#10005; Exit</button>
        <button className="playbtn" onClick={() => setPlaying(!playing)}>
          {playing ? '❚❚ Pause' : '▶ Play'}
        </button>
        <span className="pageno">{idx + 1} / {pages.length}</span>
        <div className="dots">
          {pages.map((p, i) => (
            <button key={i} aria-label={`Page ${i + 1}`} className={'dot' + (p.type === 'choose' ? ' stop' : '') + (i === idx ? ' on' : '')} onClick={() => go(i)} />
          ))}
        </div>
        <span className="rtitle">{title}</span>
        <button onClick={toggleFs}>&#9974; Fullscreen</button>
      </div>
    </div>
  );
}
