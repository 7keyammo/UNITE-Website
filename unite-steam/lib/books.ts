import 'server-only';
import { art, chooseArt, BOOKS, ORDER } from './content/wonder-ship.js';

type RawOption = { icon: string; label: string; go: string | null };
type RawPage = {
  type: 'read' | 'choose';
  art: string;
  kicker: string;
  line?: string;
  cue?: string;
  q?: string;
  note?: string;
  options?: RawOption[];
  secs?: number;
};
type RawBook = {
  title: string;
  blurb: string;
  status: 'ready' | 'draft';
  cover: () => string;
  pages: RawPage[];
  week?: number;
  world?: string;
  curriculum?: string;
};

const books = BOOKS as Record<string, RawBook>;
const order = ORDER as string[];

export type BookSummary = {
  slug: string;
  title: string;
  blurb: string;
  status: 'ready' | 'draft';
  pageCount: number;
  minutes: number;
  chooseCount: number;
  week?: number;
  world?: string;
  /** K-2 lessons this book feeds, e.g. "EFV L3,L6 · STEAM C4". */
  curriculum?: string;
};

import type { ReaderPage } from './types';
export type { ReaderPage };

function minutes(b: RawBook) {
  return Math.round(b.pages.reduce((a, p) => a + (p.secs || 60), 0) / 60);
}

export function listBooks(): BookSummary[] {
  return order.map((slug) => summary(slug)!);
}

export function summary(slug: string): BookSummary | null {
  const b = books[slug];
  if (!b) return null;
  return {
    slug,
    title: b.title,
    blurb: b.blurb,
    status: b.status,
    pageCount: b.pages.length,
    minutes: minutes(b),
    chooseCount: b.pages.filter((p) => p.type === 'choose').length,
    week: b.week,
    world: b.world,
    curriculum: b.curriculum,
  };
}

export function coverSvg(slug: string): string {
  return books[slug]?.cover() ?? '';
}

/** Members only. Callers must check access before calling. */
export function readerPages(slug: string): ReaderPage[] | null {
  const b = books[slug];
  if (!b) return null;
  return b.pages.map((p) => ({
    type: p.type,
    artSvg: art(p.art),
    kicker: p.kicker,
    line: p.line,
    cue: p.cue,
    q: p.q,
    note: p.note,
    options: p.options?.map((o) => ({ iconSvg: art(o.icon), label: o.label, swapSvg: chooseArt(o.go) })),
    secs: p.secs || 60,
  }));
}
