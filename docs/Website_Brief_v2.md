# Oathlight — Website Brief v2

Replaces the August design brief. Last updated: 15 November 2026.

## What exists

https://oathlight.app — a static site on GitHub Pages, built from this repository.

| Page | Purpose | Required by |
|---|---|---|
| `/` | Landing: what it is, how it works, waiting list | — |
| `/privacy.html` | Privacy policy | Google Play listing and Data safety form |
| `/terms.html` | Terms of use | — |
| `/delete.html` | What deletion removes, in-app path, request form | Google Play account-deletion URL |
| `/safety.html` | Child safety (CSAE) standards and point of contact | Google Play, because of anonymous parties |

Six languages: English at the root, `/uk/`, `/de/`, `/fr/`, `/es/`, `/it/`. Each page links to its own translations and carries `hreflang` alternates.

## How it is built

- All text is in `src/content/<lang>.json`; the six files have identical structure. `build.py` (no dependencies) writes every page. Edit `src/`, run `python build.py`, commit everything.
- Design is the Claude Design prototype, unchanged: Ember palette, Cinzel headings, one decorative element (the diamond).
- **No third parties.** Fonts are served from `/fonts/` (Cinzel; Cormorant SC for Cyrillic). No analytics, no cookies, no CDN. Keep it that way: the landing page promises it and the privacy policy states it.
- Both forms call insert-only functions in the app's Supabase project with the publishable key (`join_waitlist`, `request_account_deletion`). A form that fails says so and points to email — it never claims success.

## Rules for copy

- Second person singular and informal in every language.
- Calm, no exclamation marks, never loss-framed.
- About parties, never: chat, message, match, strangers, random, meet. Say: party, wanderers, marks, fire.
- Facts must match the app: party of **three**, **13** marks, **48** hours, parties **18+**, an account **is** required, five forms, level 42.
- The legal pages must match the app's real behaviour and `docs/data-collection.md` in the app repository. When the app starts collecting something new, the policy changes in the same release — in all six languages.

## Before the public release

1. `build.py`: `RELEASED = True`, `PLAY_URL` = the Play listing. The landing swaps the waiting list for the store button.
2. Replace the three screenshot placeholders on the landing with real screenshots (per language if possible).
3. Send the one launch email to `waitlist`, then delete the addresses — the policy says so.
4. Have the legal texts read by someone qualified. They were written from the code, not by a lawyer.
5. Have the German, French, Spanish and Italian texts read by native speakers.

## Operating it

- New waiting-list entries: `select * from public.waitlist order by created_at;`
- Open deletion requests: `select * from public.deletion_requests where handled_at is null;` — how to carry one out is at the bottom of migration `005_account_deletion.sql`.
- Mailboxes that must be answered: `hello@`, `privacy@`, `delete@`, `safety@oathlight.app`.
