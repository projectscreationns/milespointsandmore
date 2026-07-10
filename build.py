#!/usr/bin/env python3
"""
Miles, Points and More - static site generator.

Zero third-party dependencies (Python standard library only) so it runs
reliably in the weekly automation and on any host (Cloudflare Pages, GitHub
Pages, etc.).

Usage:
    python build.py            # build the site into ./public
    python build.py --serve    # build, then serve locally at http://localhost:8000
"""

from __future__ import annotations

import json
import re
import shutil
import sys
from datetime import datetime, timezone
from email.utils import format_datetime
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CONTENT = ROOT / "content"
POSTS_DIR = CONTENT / "posts"
PAGES_DIR = CONTENT / "pages"
TEMPLATES = ROOT / "templates"
ASSETS = ROOT / "assets"
OUT = ROOT / "public"

TOKEN = re.compile(r"\{\{\s*(\w+)\s*\}\}")


# --------------------------------------------------------------------------- #
# Helpers
# --------------------------------------------------------------------------- #
def load_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as fh:
        return json.load(fh)


def render(template: str, context: dict) -> str:
    """Replace {{ key }} tokens with values from context (missing -> '')."""
    return TOKEN.sub(lambda m: str(context.get(m.group(1), "")), template)


def read_template(name: str) -> str:
    return (TEMPLATES / name).read_text(encoding="utf-8")


def parse_date(value: str) -> datetime:
    """Accept YYYY-MM-DD; fall back to epoch on bad input so build never crashes."""
    try:
        return datetime.strptime(value, "%Y-%m-%d").replace(tzinfo=timezone.utc)
    except (ValueError, TypeError):
        return datetime(1970, 1, 1, tzinfo=timezone.utc)


def human_date(dt: datetime) -> str:
    return dt.strftime("%b %d, %Y").replace(" 0", " ")


# --------------------------------------------------------------------------- #
# Load content
# --------------------------------------------------------------------------- #
def load_site() -> dict:
    site = load_json(CONTENT / "site.json")
    site.setdefault("subscribe_embed", "")
    site.setdefault("contact_email", "")
    return site


def load_posts() -> list:
    posts = []
    for path in sorted(POSTS_DIR.glob("*.json")):
        data = load_json(path)
        data["_date"] = parse_date(data.get("date", ""))
        data["date_human"] = human_date(data["_date"])
        data["slug"] = data.get("slug") or path.stem
        data["url"] = f"/post/{data['slug']}/"
        data.setdefault("author", "Navees")
        data.setdefault("read_time", "")
        data.setdefault("cover_emoji", "✈️")
        data.setdefault("tags", [])
        data.setdefault("summary", "")
        data.setdefault("body_html", "")
        posts.append(data)
    posts.sort(key=lambda p: p["_date"], reverse=True)
    return posts


# --------------------------------------------------------------------------- #
# HTML fragments
# --------------------------------------------------------------------------- #
def nav_html(site: dict, active: str = "") -> str:
    items = []
    for label, href in site["nav"]:
        cls = ' class="active"' if label.lower() == active.lower() else ""
        items.append(f'<a href="{href}"{cls}>{escape(label)}</a>')
    return "\n".join(items)


def tag_html(tags: list) -> str:
    return "".join(f'<span class="tag">{escape(t)}</span>' for t in tags)


def cover_img(post: dict, css_class: str) -> str:
    """Return an <img> for the post cover, or an emoji tile fallback if no image."""
    cover = post.get("cover")
    alt = escape(post.get("title", ""))
    if cover:
        return f'<img class="{css_class}" src="{escape(cover)}" alt="{alt}" loading="lazy">'
    return (f'<span class="{css_class} cover-fallback" role="img" aria-label="{alt}">'
            f'{post.get("cover_emoji", "✈️")}</span>')


def featured_card(post: dict) -> str:
    meta = post["date_human"]
    if post.get("read_time"):
        meta += "  ·  " + escape(post["read_time"])
    return f"""
      <a class="fcard" href="{post['url']}">
        <div class="fcard__img">{cover_img(post, 'fcard__cover')}</div>
        <div class="fcard__body">
          <div class="fcard__meta">{meta}</div>
          <div class="fcard__title">{escape(post['title'])}</div>
          <p class="fcard__summary">{escape(post.get('summary', ''))}</p>
        </div>
      </a>"""


def post_card(post: dict, featured: bool = False) -> str:
    if featured:
        return featured_card(post)
    meta = post["date_human"]
    if post["read_time"]:
        meta += "  ·  " + escape(post["read_time"])
    cat = escape(post.get("category", "Finance"))
    return f"""
      <article class="card" data-category="{cat}">
        <a class="card__cover" href="{post['url']}">{cover_img(post, 'card__img')}</a>
        <div class="card__body">
          <div class="card__meta">{meta}</div>
          <h2 class="card__title"><a href="{post['url']}">{escape(post['title'])}</a></h2>
          <p class="card__summary">{escape(post.get('summary', ''))}</p>
          <div class="card__tags">{tag_html(post.get('tags', []))}</div>
        </div>
      </article>"""


def subscribe_block(site: dict) -> str:
    if site.get("subscribe_embed"):
        return f'<section class="subscribe">{site["subscribe_embed"]}</section>'
    email = site.get("contact_email", "")
    action = f"mailto:{email}?subject=Subscribe%20me" if email else "#"
    return f"""
    <section class="subscribe">
      <h3>Never Miss a New Post.</h3>
      <form class="subscribe__form" action="{action}" method="post">
        <input type="email" name="email" placeholder="Enter your email" aria-label="Email address" required>
        <button type="submit">Subscribe</button>
      </form>
    </section>"""


DISCLAIMER = (
    "None of this is financial advice. Everything here is simply an opinion. "
    "Always check current terms with the provider and consult a licensed financial "
    "adviser before making any financial decisions."
)


# --------------------------------------------------------------------------- #
# Page builders
# --------------------------------------------------------------------------- #
def write(path: Path, html: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(html, encoding="utf-8")


def page_context(site: dict, active: str, title: str, description: str, path: str) -> dict:
    return {
        "site_title": escape(site["title"]),
        "site_tagline": escape(site["tagline"]),
        "nav": nav_html(site, active),
        "title": escape(title),
        "page_title": escape(title),
        "description": escape(description or site["tagline"]),
        "canonical": site["base_url"].rstrip("/") + path,
        "base_url": site["base_url"].rstrip("/"),
        "year": str(datetime.now(timezone.utc).year),
        "logo_svg": site.get("logo_svg", ""),
        "subscribe": subscribe_block(site),
        "footer_note": escape(site.get("footer_note", "")),
        "disclaimer": DISCLAIMER,
        "socials": socials_html(site),
    }


def socials_html(site: dict) -> str:
    links = site.get("socials", [])
    if not links:
        return ""
    out = []
    for label, href in links:
        out.append(f'<a href="{escape(href)}" rel="me noopener" target="_blank">{escape(label)}</a>')
    return " · ".join(out)


def build_home(site: dict, posts: list, base: str) -> None:
    tpl = read_template("index.html")
    featured = post_card(posts[0], featured=True) if posts else ""
    rest = "\n".join(post_card(p) for p in posts[1:])
    ctx = page_context(site, "Home", site["title"], site["tagline"], "/")
    ctx["featured"] = featured
    ctx["cards"] = rest
    ctx["hero_img"] = site.get("hero_image", "/assets/img/point-of-this.jpg")
    ctx["hero_headline"] = escape(site.get("hero_headline", "Fly in seats I could never actually afford."))
    content = render(tpl, ctx)
    ctx["content"] = content
    write(OUT / "index.html", render(base, ctx))


def build_articles(site: dict, posts: list, base: str) -> None:
    tpl = read_template("articles.html")
    cards = "\n".join(post_card(p) for p in posts)
    ctx = page_context(site, "Articles", "Articles", "Every post - deals, strategy, redemptions.", "/articles/")
    ctx["cards"] = cards
    ctx["content"] = render(tpl, ctx)
    write(OUT / "articles" / "index.html", render(base, ctx))


def build_posts(site: dict, posts: list, base: str) -> None:
    tpl = read_template("post.html")
    for i, post in enumerate(posts):
        updated = ""
        if post.get("updated") and post["updated"] != post.get("date"):
            updated = "Updated " + human_date(parse_date(post["updated"]))
        ctx = page_context(site, "Articles", post["title"], post.get("summary", ""), post["url"])
        hero = ""
        if post.get("cover"):
            hero = (f'<figure class="post__hero"><img src="{escape(post["cover"])}" '
                    f'alt="{escape(post["title"])}"></figure>')
        ctx.update({
            "post_title": escape(post["title"]),
            "date_human": post["date_human"],
            "updated": updated,
            "read_time": escape(post["read_time"]),
            "author": escape(post["author"]),
            "cover_emoji": post["cover_emoji"],
            "hero": hero,
            "tags": tag_html(post.get("tags", [])),
            "body": post["body_html"],
        })
        ctx["content"] = render(tpl, ctx)
        write(OUT / "post" / post["slug"] / "index.html", render(base, ctx))


def build_pages(site: dict, base: str) -> None:
    tpl = read_template("page.html")
    for path in sorted(PAGES_DIR.glob("*.html")):
        meta_path = path.with_suffix(".json")
        meta = load_json(meta_path) if meta_path.exists() else {}
        slug = path.stem
        title = meta.get("title", slug.title())
        ctx = page_context(site, title, title, meta.get("description", ""), f"/{slug}/")
        ctx["page_heading"] = escape(title)
        ctx["body"] = path.read_text(encoding="utf-8")
        ctx["content"] = render(tpl, ctx)
        write(OUT / slug / "index.html", render(base, ctx))


def section_photo(title: str) -> str:
    """Premium category photo used as the deal-card cover, chosen by section."""
    t = title.lower()
    if "hack" in t:
        return "/assets/img/deals/photo-phone.jpg"
    if "australia" in t:
        return "/assets/img/deals/photo-plane.jpg"
    if "bank" in t:
        return "/assets/img/deals/photo-money.jpg"
    return "/assets/img/deals/photo-card1.jpg"  # card sign-up bonuses (default)


def deal_card(item: dict, emoji: str, photo: str) -> str:
    """Deal card: premium category photo cover + small brand-logo badge."""
    src = item.get("source", "")
    src_html = f'<div class="card__meta">{escape(src)}</div>' if src else ""
    meta = item.get("meta", "")
    reqt_html = f'<div class="card__reqt">{escape(meta)}</div>' if meta else ""
    logo = item.get("image")
    badge = (f'<span class="card__logobadge"><img src="{escape(logo)}" alt="" loading="lazy"></span>'
             if logo else "")
    cover = (f'<div class="card__cover card__cover--photo" '
             f'style="background-image:url(\'{escape(photo)}\')">{badge}</div>')
    return f"""
      <article class="card">
        {cover}
        <div class="card__body">
          {src_html}
          <h2 class="card__title">{escape(item.get('name',''))}</h2>
          <div class="card__detail">{escape(item.get('detail',''))}</div>
          {reqt_html}
          <p class="card__summary">{escape(item.get('why',''))}</p>
        </div>
      </article>"""


def deal_section(section: dict) -> str:
    title = section.get("title", "")
    emoji = title.split(" ", 1)[0] if title else "✈️"
    photo = section_photo(title)
    cards = "\n".join(deal_card(i, emoji, photo) for i in section.get("items", []))
    return f"""
    <p class="section-label section-label--left">{escape(title)}</p>
    <section class="grid deals-grid">
      {cards}
    </section>"""


def build_best_deals(site: dict, base: str) -> None:
    data_path = CONTENT / "best-deals.json"
    if not data_path.exists():
        return
    data = load_json(data_path)
    tpl = read_template("best-deals.html")
    ctx = page_context(site, "Deals", "Best Deals Right Now",
                       "The best current deals from DansDeals and Doctor of Credit - bank bonuses, "
                       "viral hacks, and cards at all-time-high offers. Kept tight and current.",
                       "/deals/")
    ctx["intro"] = escape(data.get("intro", ""))
    ctx["updated"] = escape(human_date(parse_date(data.get("updated", ""))))
    ctx["sections"] = "\n".join(deal_section(s) for s in data.get("sections", []))
    ctx["content"] = render(tpl, ctx)
    write(OUT / "deals" / "index.html", render(base, ctx))


def build_feeds(site: dict, posts: list) -> None:
    base_url = site["base_url"].rstrip("/")
    # RSS
    items = []
    for p in posts[:20]:
        link = base_url + p["url"]
        pub = format_datetime(p["_date"])
        items.append(f"""    <item>
      <title>{escape(p['title'])}</title>
      <link>{link}</link>
      <guid isPermaLink="true">{link}</guid>
      <pubDate>{pub}</pubDate>
      <description>{escape(p.get('summary', ''))}</description>
    </item>""")
    rss = f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0">
  <channel>
    <title>{escape(site['title'])}</title>
    <link>{base_url}/</link>
    <description>{escape(site['tagline'])}</description>
    <language>en</language>
{chr(10).join(items)}
  </channel>
</rss>
"""
    write(OUT / "rss.xml", rss)

    # Sitemap
    urls = ["/", "/articles/", "/deals/"]
    urls += [p["url"] for p in posts]
    for path in sorted(PAGES_DIR.glob("*.html")):
        urls.append(f"/{path.stem}/")
    entries = "\n".join(
        f"  <url><loc>{base_url}{u}</loc></url>" for u in urls
    )
    sitemap = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{entries}
</urlset>
"""
    write(OUT / "sitemap.xml", sitemap)

    # robots.txt
    write(OUT / "robots.txt", f"User-agent: *\nAllow: /\nSitemap: {base_url}/sitemap.xml\n")


def copy_assets() -> None:
    if ASSETS.exists():
        shutil.copytree(ASSETS, OUT / "assets", dirs_exist_ok=True)


# --------------------------------------------------------------------------- #
# Main
# --------------------------------------------------------------------------- #
def build() -> None:
    site = load_site()
    posts = load_posts()
    # Clean previous output but tolerate locked files (e.g. a running preview
    # server on Windows). Files are overwritten in place; stale ones are removed
    # where possible.
    if OUT.exists():
        shutil.rmtree(OUT, ignore_errors=True)
    OUT.mkdir(parents=True, exist_ok=True)
    base = read_template("base.html")
    build_home(site, posts, base)
    build_articles(site, posts, base)
    build_posts(site, posts, base)
    build_pages(site, base)
    build_best_deals(site, base)
    build_feeds(site, posts)
    copy_assets()
    print(f"Built {len(posts)} posts -> {OUT}")


def serve() -> None:
    import http.server
    import os
    import socketserver

    os.chdir(OUT)
    port = 8000
    handler = http.server.SimpleHTTPRequestHandler
    with socketserver.TCPServer(("", port), handler) as httpd:
        print(f"Serving {OUT} at http://localhost:{port} (Ctrl+C to stop)")
        httpd.serve_forever()


if __name__ == "__main__":
    build()
    if "--serve" in sys.argv:
        serve()
