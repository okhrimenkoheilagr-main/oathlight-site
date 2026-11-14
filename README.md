# Oathlight — website

Static site for [oathlight.app](https://oathlight.app), served by GitHub Pages from the root of `main`.

- `src/content/<lang>.json` — all text, one file per language
- `src/styles.css`, `src/forms.js` — styling and the two forms
- `build.py` — writes the pages (`python build.py`, no dependencies)
- everything else at the root is generated; edit `src/`, rebuild, commit

Languages live in `LANGS` in `build.py`. English is served at `/`, the others at `/<lang>/`.

## Before the store release

In `build.py` set `RELEASED = True` and `PLAY_URL` to the Play listing, then rebuild.

## Forms

Both forms call functions in the app's Supabase project (migration `004_site_forms.sql`
in the app repository). Put the project's **publishable** key into `SUPABASE_KEY` in
`src/forms.js`. Until then a form says it could not send and points to email — it never
claims a request was received.

## Fonts

Cinzel and Cormorant SC (SIL Open Font License 1.1) are served from `fonts/`, so the
pages make no third-party requests.
