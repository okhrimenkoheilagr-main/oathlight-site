#!/usr/bin/env python3
"""Builds the Oathlight site: six languages, five pages each, no dependencies.

    python build.py

Source lives in src/ (content/<lang>.json, styles.css, forms.js); the pages are
written to the repository root, which is what GitHub Pages serves. English sits
at the root, every other language in its own folder (/uk/, /de/ ...).

Before the store release, set RELEASED to True and PLAY_URL to the listing.
"""
import html
import json
import pathlib
import shutil

ROOT = pathlib.Path(__file__).parent
SRC = ROOT / 'src'
DOMAIN = 'https://oathlight.app'
LANGS = ['en', 'uk', 'de', 'fr', 'es', 'it']
LANG_NAMES = {'en': 'English', 'uk': 'Українська', 'de': 'Deutsch', 'fr': 'Français', 'es': 'Español', 'it': 'Italiano'}
PAGES = ['index', 'privacy', 'terms', 'delete', 'safety']
RELEASED = False
PLAY_URL = '#'
# Terms and safety: party members are known by their heroes' names (22 November);
# terms and the deletion page: the subscription (27 November).
UPDATED = {'en': '27 November 2026', 'uk': '27 листопада 2026', 'de': '27. November 2026',
           'fr': '27 novembre 2026', 'es': '27 de noviembre de 2026', 'it': '27 novembre 2026'}
# The privacy policy changes on its own schedule: Google sign-in and the copy of tasks on the phone
# (20 November); what a party sees — heroes' names (22 November); Google Tasks — who holds the
# imported tasks, how they are protected and kept (25 November, for Google's OAuth review);
# a party lasts 24 hours; marks go when the fire goes out, the party 3 days later, after the
# fire summary (26 November); the subscription — what is kept, how it is checked, how long (27 November).
# Safety standards: party members known by their heroes' names, a 24-hour fire (26 November).
SAFETY_UPDATED = {'en': '26 November 2026', 'uk': '26 листопада 2026', 'de': '26. November 2026',
                  'fr': '26 novembre 2026', 'es': '26 de noviembre de 2026', 'it': '26 novembre 2026'}
PRIVACY_UPDATED = {'en': '27 November 2026', 'uk': '27 листопада 2026', 'de': '27. November 2026',
                   'fr': '27 novembre 2026', 'es': '27 de noviembre de 2026', 'it': '27 novembre 2026'}


def updated_on(page, lang):
    return {'privacy': PRIVACY_UPDATED, 'safety': SAFETY_UPDATED}.get(page, UPDATED)[lang]


e = html.escape


def rich(text):
    """Escapes text, then turns [label](target) into a link and *x* into emphasis."""
    import re
    out = e(text, quote=False)
    out = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', lambda m: f'<a href="{m.group(2)}">{m.group(1)}</a>', out)
    return re.sub(r'\*([^*]+)\*', r'<span class="em">\1</span>', out)


def prefix(lang):
    return '' if lang == 'en' else f'{lang}/'


def url(lang, page):
    return '/' + prefix(lang) + ('' if page == 'index' else f'{page}.html')


def head(c, lang, page, title, description):
    alternates = ''.join(
        f'<link rel="alternate" hreflang="{l}" href="{DOMAIN}{url(l, page)}">\n' for l in LANGS)
    return f'''<!DOCTYPE html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(description)}">
<link rel="canonical" href="{DOMAIN}{url(lang, page)}">
{alternates}<link rel="alternate" hreflang="x-default" href="{DOMAIN}{url('en', page)}">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="stylesheet" href="/styles.css">
</head>
'''


def langs_nav(lang, page):
    links = ''.join(
        f'<a href="{url(l, page)}" lang="{l}"{" aria-current=\"true\"" if l == lang else ""}>{LANG_NAMES[l]}</a>'
        for l in LANGS)
    return f'<nav class="langs" aria-label="Language">{links}</nav>'


def footer(c, lang, page, home=False):
    n = c['nav']
    links = [(url(lang, 'index'), n['home'])] if not home else []
    links += [(url(lang, p), n[p]) for p in ('privacy', 'terms', 'delete', 'safety') if p != page]
    links.append(('mailto:hello@oathlight.app', 'hello@oathlight.app'))
    anchors = ''.join(f'<a href="{h}">{e(t)}</a>' for h, t in links)
    if home:
        return f'''  <footer class="site-footer site-footer--home">
    <div class="site-footer__brand">
      <span class="site-footer__word">Oathlight</span>
      <span class="site-footer__copy">© 2026 · {e(n['madeQuietly'])}</span>
    </div>
    <nav class="site-footer__links" aria-label="Footer">{anchors}</nav>
    {langs_nav(lang, page)}
  </footer>'''
    return f'  <footer class="site-footer">{anchors}{langs_nav(lang, page)}</footer>'


def logo(lang, small=True):
    size = 'diamond--sm' if small else 'diamond--logo'
    return f'<a href="{url(lang, "index")}" class="logo"><span class="diamond {size}"></span><span class="logo__word">Oathlight</span></a>'


def form_attrs(c):
    f = c['forms']
    return f'data-lang="{c["lang"]}" data-done="{e(f["done"])}" data-failed="{e(f["failed"])}"'


STORE_SVG = '<svg width="21" height="23" viewBox="0 0 24 26" fill="none" aria-hidden="true"><path d="M2 2.2 13.6 13 2 23.8c-.6-.4-1-1.1-1-2V4.2c0-.9.4-1.6 1-2Z" fill="currentColor"/><path d="M15.3 14.7 18.9 18l-13 5.9 9.4-9.2Z" fill="currentColor" opacity=".8"/><path d="M15.3 11.3 5.9 2.1l13 5.9-3.6 3.3Z" fill="currentColor" opacity=".8"/><path d="M20.6 9 23 10.9c.8.6.8 1.6 0 2.2L20.6 15l-3.9-3 3.9-3Z" fill="currentColor" opacity=".6"/></svg>'


def store_button(c):
    h = c['home']
    return f'<a class="store-btn" href="{PLAY_URL}">{STORE_SVG}<span class="store-btn__text"><span class="store-btn__small">{e(h["storeSmall"])}</span><span class="store-btn__big">Google Play</span></span></a>'


def signup(c):
    h = c['home']
    return f'''<form class="signup" data-signup {form_attrs(c)}>
            <input class="input" type="email" name="email" required placeholder="you@example.com" aria-label="{e(h['emailLabel'])}">
            <button class="btn" type="submit">{e(h['joinButton'])}</button>
          </form>'''


def page_index(c, lang):
    h = c['home']
    cards = ''.join(f'<div class="card"><span class="diamond"></span><h3>{e(t)}</h3><p>{e(p)}</p></div>' for t, p in h['cards'])
    numerals = ['I', 'II', 'III', 'IV']
    steps = ''.join(f'<div class="step"><span class="step__num">{numerals[i]}</span><h3>{e(t)}</h3><p>{e(p)}</p></div>' for i, (t, p) in enumerate(h['steps']))
    shots = ''.join(f'<figure class="shot"><div class="shot__frame">{e(a)}<br>{e(b)}</div><figcaption>{e(cap)}</figcaption></figure>' for a, b, cap in h['shots'])
    # The road, shown with a real hero: the Strategist's five forms, one per ten levels.
    roman = ['I', 'II', 'III', 'IV', 'V']
    form_levels = [1, 10, 20, 30, 40]
    forms = ''.join(
        f'<figure class="form-card"><img src="/img/strategist-f{i + 1}.webp" width="464" height="576" loading="lazy" '
        f'alt="{e(h["formsClass"])} · {e(h["formWord"])} {roman[i]}">'
        f'<figcaption><span class="form-card__num">{roman[i]}</span> {e(h["levelWord"])} {form_levels[i]}</figcaption></figure>'
        for i in range(5))
    return head(c, lang, 'index', h['title'], h['description']) + f'''<body data-released="{'true' if RELEASED else 'false'}" data-glow="true">
<div class="page">
  <div class="glow" aria-hidden="true"></div>
  <header class="site-header site-header--home">
    {logo(lang, small=False)}
    <nav class="site-nav" aria-label="Main">
      <a href="#different">{e(h['navWhat'])}</a>
      <a href="#how">{e(h['navHow'])}</a>
      <a href="#join" class="is-accent only-prerelease">{e(h['navJoin'])}</a>
    </nav>
  </header>
  <main>
    <section class="hero">
      <div class="hero__inner">
        <p class="eyebrow eyebrow--accent only-released"><span class="eyebrow__line"></span>{e(h['eyebrowReleased'])}</p>
        <p class="eyebrow only-prerelease"><span class="eyebrow__line"></span>{e(h['eyebrowPre'])}</p>
        <h1>{e(h['h1'])}</h1>
        <p class="hero__lead">{e(h['lead'])}</p>
        <div class="only-prerelease">
          {signup(c)}
          <p class="form-note">{e(h['formNote'])}</p>
        </div>
        <div class="hero__store only-released">
          {store_button(c)}
          <span class="hero__store-note">{e(h['storeNote'])}</span>
        </div>
      </div>
    </section>
    <section id="different" class="section">
      <h2 class="section__title">{e(h['differentTitle'])}</h2>
      <div class="cards">{cards}</div>
    </section>
    <section id="how" class="section">
      <h2 class="section__title">{e(h['howTitle'])}</h2>
      <div class="steps">{steps}</div>
    </section>
    <section id="forms" class="section">
      <div class="shots-head">
        <h2 class="section__title">{e(h['formsTitle'])}</h2>
        <p>{e(h['formsNote'])}</p>
      </div>
      <div class="forms">{forms}</div>
    </section>
    <section class="section">
      <div class="shots-head">
        <h2 class="section__title">{e(h['shotsTitle'])}</h2>
        <p>{e(h['shotsNote'])}</p>
      </div>
      <div class="shots">{shots}</div>
    </section>
    <section id="join" class="section join">
      <div class="join__inner">
        <div class="only-prerelease">
          <h2>{e(h['joinTitle'])}</h2>
          <p>{e(h['joinText'])}</p>
          {signup(c)}
        </div>
        <div class="only-released">
          <h2>{e(h['releasedTitle'])}</h2>
          <p>{e(h['releasedText'])}</p>
          {store_button(c)}
        </div>
      </div>
    </section>
  </main>
{footer(c, lang, 'index', home=True)}
</div>
<script src="/forms.js"></script>
</body>
</html>
'''


def block(b):
    kind = b[0]
    if kind == 'p':
        return f'<p>{rich(b[1])}</p>'
    if kind == 'h':
        return f'<h3>{e(b[1])}</h3>'
    if kind == 'ul':
        # One span per item: the item is a flex row (bullet, text), so a link or an
        # emphasis left bare would become a column of its own.
        return '<ul>' + ''.join(f'<li><span>{rich(i)}</span></li>' for i in b[1]) + '</ul>'
    if kind == 'quote':
        return f'<blockquote>{rich(b[1])}</blockquote>'
    if kind == 'table':
        head_row = ''.join(f'<th>{e(x)}</th>' for x in b[1])
        rows = ''.join('<tr>' + ''.join(f'<td>{rich(x)}</td>' for x in r) + '</tr>' for r in b[2])
        return f'<table><thead><tr>{head_row}</tr></thead><tbody>{rows}</tbody></table>'
    raise ValueError(kind)


def page_legal(c, lang, page):
    d = c[page]
    toc = ''.join(f'<li><span>{i}</span><a href="#s{i}">{e(s["title"])}</a></li>' for i, s in enumerate(d['sections'], 1))
    body = ''.join(
        f'<section id="s{i}"><h2>{i} · {e(s["title"])}</h2>{"".join(block(b) for b in s["blocks"])}</section>'
        for i, s in enumerate(d['sections'], 1))
    return head(c, lang, page, f'{d["title"]} — Oathlight', d['lead']) + f'''<body>
<div class="page page--legal">
  <header class="site-header">{logo(lang)}</header>
  <div class="legal-wrap">
    <div class="legal">
      <p class="kicker">{e(d['kicker'])}</p>
      <h1 class="page-title">{e(d['title'])}</h1>
      <p class="updated">{e(c['nav']['updated'])} {updated_on(page, lang)}</p>
      <p class="page-lead">{rich(d['lead'])}</p>
      <div class="legal-grid">
        <nav class="toc" aria-label="{e(c['nav']['contents'])}">
          <span class="toc__label">{e(c['nav']['contents'])}</span>
          <ol>{toc}</ol>
        </nav>
        <article class="legal-body">{body}</article>
      </div>
    </div>
  </div>
{footer(c, lang, page)}
</div>
</body>
</html>
'''


def page_delete(c, lang):
    d = c['delete']
    chips = d['path']
    path = '<span class="path__arrow" aria-hidden="true">→</span>'.join(
        f'<span class="path__chip{" path__chip--end" if i == len(chips) - 1 else ""}">{e(x)}</span>' for i, x in enumerate(chips))
    removed = ''.join(f'<li><span class="diamond"></span>{e(x)}</li>' for x in d['removed'])
    timing = ''.join(f'<div class="timing__item"><span class="timing__big">{e(a)}</span><span class="timing__text">{e(b)}</span></div>' for a, b in d['timing'])
    return head(c, lang, 'delete', f'{d["title"]} — Oathlight', d['lead']) + f'''<body>
<div class="page">
  <header class="site-header">{logo(lang)}</header>
  <main class="narrow">
    <p class="kicker">{e(d['kicker'])}</p>
    <h1 class="page-title">{e(d['title'])}</h1>
    <p class="page-lead">{e(d['lead'])}</p>
    <section class="panel">
      <h2>{e(d['inAppTitle'])}</h2>
      <p>{e(d['inAppText'])}</p>
      <p class="path">{path}</p>
    </section>
    <section class="block">
      <h2 class="spaced">{e(d['formTitle'])}</h2>
      <p>{e(d['formText'])}</p>
      <form class="stack-form" data-delete {form_attrs(c)} data-done="{e(d['formDone'])}">
        <label>{e(d['emailLabel'])}
          <input class="input" type="email" name="email" required placeholder="you@example.com">
        </label>
        <label>{e(d['noteLabel'])}
          <textarea class="textarea" name="note" rows="3" maxlength="1000"></textarea>
        </label>
        <button class="btn" type="submit">{e(d['send'])}</button>
      </form>
      <p class="small">{rich(d['formAlt'])}</p>
    </section>
    <section class="block">
      <h2>{e(d['removedTitle'])}</h2>
      <ul class="dlist">{removed}</ul>
      <p>{e(d['removedNote'])}</p>
      <p>{e(d['keptNote'])}</p>
    </section>
    <section class="panel panel--warn">
      <p class="panel__flag"><span class="diamond"></span>{e(d['warnFlag'])}</p>
      <h2>{e(d['warnTitle'])}</h2>
      <p>{rich(d['warnText'])}</p>
    </section>
    <section class="block" style="margin-bottom:0">
      <h2>{e(d['timingTitle'])}</h2>
      <div class="timing">{timing}</div>
    </section>
  </main>
{footer(c, lang, 'delete')}
</div>
<script src="/forms.js"></script>
</body>
</html>
'''


def build():
    for lang in LANGS:
        c = json.loads((SRC / 'content' / f'{lang}.json').read_text(encoding='utf-8'))
        c['lang'] = lang
        out = ROOT / prefix(lang)
        out.mkdir(exist_ok=True)
        pages = {'index': page_index(c, lang), 'delete': page_delete(c, lang)}
        for page in ('privacy', 'terms', 'safety'):
            pages[page] = page_legal(c, lang, page)
        for page, text in pages.items():
            # Links written inside the content point at the English page;
            # send them to this language's copy instead.
            for target in ('privacy', 'terms', 'delete', 'safety'):
                text = text.replace(f'href="/{target}.html"', f'href="{url(lang, target)}"')
            (out / f'{page}.html').write_text(text, encoding='utf-8')
    for name in ('styles.css', 'forms.js', 'favicon.svg'):
        shutil.copy(SRC / name, ROOT / name)
    shutil.copytree(SRC / 'img', ROOT / 'img', dirs_exist_ok=True)
    (ROOT / 'CNAME').write_text('oathlight.app\n')
    (ROOT / '.nojekyll').write_text('')
    urls = ''.join(f'<url><loc>{DOMAIN}{url(l, p)}</loc></url>\n' for l in LANGS for p in PAGES)
    (ROOT / 'sitemap.xml').write_text(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{urls}</urlset>\n')
    (ROOT / 'robots.txt').write_text(f'User-agent: *\nAllow: /\nSitemap: {DOMAIN}/sitemap.xml\n')
    print('built', len(LANGS) * len(PAGES), 'pages')


if __name__ == '__main__':
    build()
