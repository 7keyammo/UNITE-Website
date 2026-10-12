# UNITE STEAM — unitesteam.com

Next.js site for the Homeschool Hub and Saturday School: public pages, parent accounts (Supabase),
subscriptions (Stripe), and a library whose story content is only sent to paying members.

## Where data lives
| What | Where |
|---|---|
| Parent accounts and passwords | Supabase Auth |
| Plan, billing period, status, renewal date | Supabase table `memberships` (written only by the Stripe webhook) |
| "Register your interest" form | Supabase table `interest_signups` |
| Consult / tutoring / organization requests | Supabase table `consult_requests` |
| Card details and invoices | Stripe only (never touches this site) |
| Wonder Ship books and art | `lib/content/wonder-ship.js`, server-only, sent to members after a server-side check |

> **`lib/content/wonder-ship.js` is generated — do not edit it by hand.**
> It is built from the book engine in `../wonder-ship/build/`. Change the words in
> `specs.py` or the art in `art.py`, then run `python3 bot.py build` from
> `../wonder-ship/build/`. That one command also rebuilds the free reader app, the
> print PDFs, the EPUBs and the presentation decks, so nothing can drift apart.
> The weekly book bot runs it every Monday, so a new book lands here on its own.

View sign-ups and requests in Supabase → Table Editor.

## Launch steps
1. **Supabase**: create a project. In SQL Editor, run `supabase/migrations/0001_init.sql`.
   Auth → URL Configuration: Site URL `https://unitesteam.com`, add redirect `https://unitesteam.com/auth/callback`.
2. **Stripe** (test mode first): `STRIPE_SECRET_KEY=sk_test_... npm run stripe:setup` creates the products and 6 prices.
   Developers → Webhooks → add endpoint `https://unitesteam.com/api/webhooks/stripe` with events
   `checkout.session.completed`, `customer.subscription.created`, `customer.subscription.updated`, `customer.subscription.deleted`.
   Settings → Billing → Customer portal: turn it on (lets families update cards and cancel).
3. **Vercel**: import this project, add the variables from `.env.example`, deploy.
4. **Domain**: add `unitesteam.com` and `www.unitesteam.com` to the Vercel project.
5. **Test**: sign up, buy with card `4242 4242 4242 4242`, confirm the library unlocks, cancel in the portal, confirm it locks.
6. Swap Stripe to live keys, re-run `npm run stripe:setup` with the live key, add the live webhook, redeploy.

## Prices (edit `lib/plans.ts` and `scripts/stripe-setup.mjs` together)
| Plan | Monthly | Semester (6 mo) | Annual |
|---|---|---|---|
| Homeschool Hub | $14 | $75 | $120 |
| Saturday School (includes Hub) | $89 | $420 | $750 |

## Local development
```
cp .env.example .env.local   # fill in test keys
npm install
npm run dev
```
Set `DEV_UNLOCK_ALL=1` in `.env.local` to preview member pages without logging in (ignored in production).
For webhooks locally: `stripe listen --forward-to localhost:3000/api/webhooks/stripe`.

## Before launch
- Have the draft Privacy and Terms pages reviewed.
- Confirm the Impact Hub stats on the home page are current.
- Brand colors are tokens at the top of `app/globals.css` (`--brand-*`); swap in exact unitehella.org values when known.
