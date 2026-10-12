import type { Metadata } from 'next';
import { notFound, redirect } from 'next/navigation';
import Reader from '@/components/Reader';
import { readerPages, summary } from '@/lib/books';
import { getViewer } from '@/lib/membership';

type Params = { params: Promise<{ slug: string }> };

export async function generateMetadata({ params }: Params): Promise<Metadata> {
  const b = summary((await params).slug);
  return { title: b ? `Read: ${b.title}` : 'Read', robots: { index: false } };
}

export default async function ReadPage({ params }: Params) {
  const { slug } = await params;
  const b = summary(slug);
  if (!b) notFound();
  const { user, access } = await getViewer();
  // The server checks membership before any story content is sent.
  if (!access.homeschool) redirect(user ? '/pricing?need=homeschool' : `/login?next=/read/${slug}`);
  const pages = readerPages(slug)!;
  return <Reader slug={slug} title={b.title} pages={pages} />;
}
