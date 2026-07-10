# Weekly auto-maintenance job

Runs once a week inside a git checkout of this repo. There are TWO jobs each run, and they are
different on purpose:

- **JOB A — always:** keep the **Best Cards page** (`content/best-cards.json`) current.
- **JOB B — only if warranted:** publish an **article** — but ONLY for genuinely *just-out* /
  breaking / viral news. No filler. Most weeks there may be nothing worth an article, and that's fine.

The two primary sources for everything are **DansDeals** and **Doctor of Credit**.

## How to read the sources
- **Doctor of Credit** (WebFetch works directly):
  `https://www.doctorofcredit.com/` (homepage = last few days of news),
  `https://www.doctorofcredit.com/best-current-credit-card-sign-bonuses/`,
  `https://www.doctorofcredit.com/best-bank-account-bonuses/`.
- **DansDeals** (⚠️ 403-blocks direct WebFetch of article pages — do NOT WebFetch those). Use
  `WebSearch` with `allowed_domains: ["dansdeals.com"]` (queries: "best offer ever", "increased",
  "limited time", "just", plus the deal name), and WebFetch the RSS feed
  `https://www.dansdeals.com/feed/`.
- Backup only if needed: frequentmiler.com, awardwallet.com; AU: pointhacks.com.au, ozbargain.com.au.
- Verify every number against the source. NEVER invent an offer or a number.

## Steps

1. `git pull --rebase` in the repo (ignore errors). Then READ `STYLE.md` fully and obey the voice.

2. **JOB A — refresh the Deals board** (`content/best-deals.json`). This is a CURATED board of the
   genuinely-good, not-everywhere plays from DansDeals + DoC — NOT a generic "top 5 credit cards" list.
   The sections (keep TIGHT — ~6-8 deals total, this must match the audience, not a rich person):
   - **🔥 The Hack Right Now** — the single viral/limited-time play everyone's on (e.g. Paze). 1-2 items.
   - **💳 Best Sign-Up Bonuses** — card SUBs a NORMAL churner can actually hit with everyday spend
     (~$24k/yr, $2k/mo). Prefer $0-fee big bonuses and genuine all-time-highs. ~3 items.
   - **🇦🇺 Australia** — the author is AU-based: current Qantas/Velocity card bonuses, AU bank/savings
     offers (UBank/ING/Macquarie style, Amex AU). ~1-2 items. Use pointhacks.com.au / ozbargain.com.au.
   - **🏦 Easy Bank Bonuses** — ACHIEVABLE only: normal direct deposit, roughly $200-$500, low effort.
     ~2 items. **DO NOT** include high-net-worth bonuses that need parking $50k-$250k+ (Citi $2k, HSBC
     $7k, etc.) — the audience doesn't have that money and doesn't care. Keep it real and attainable.
   Re-check DoC (homepage + best-bank-account-bonuses + best-current-credit-card-sign-bonuses) and
   DansDeals (search + RSS). Update numbers, swap in new hot plays, delete anything expired/mediocre.
   Keep `why` lines in Navees's voice (short, candid, numbers-first) and `source` accurate
   ("DansDeals" / "Doctor of Credit" / both). Keep it TIGHT — this page must never feel clogged with
   obvious stuff. Set `"updated"` to today's date every run.
   **Each item needs an `"image"` (brand logo)** so the Deals grid looks like the blog. For each brand,
   reuse an existing file in `assets/img/deals/` if present, else download the logo once via
   `https://unavatar.io/<brand-domain>` (e.g. unavatar.io/chase.com, /citi.com, /sofi.com,
   /americanexpress.com, /aa.com, /ihg.com) into `assets/img/deals/<brand>.png` and set
   `"image": "/assets/img/deals/<brand>.png"`. Prefer the highest-resolution result. If no logo is
   available, omit `image` (the page falls back to a section emoji tile).

3. **JOB B — article, ONLY for just-out news.** Scan DoC homepage + DansDeals (search + RSS) for
   something that genuinely **just dropped in the last few days** and is worth shouting about:
   - a brand-new or newly-increased **best-ever** offer,
   - a viral hack / limited-time play (think the DansDeals **Paze** post that blew up),
   - a program change / devaluation / news item people need to know now.
   The bar: would a points nerd say "did you see this?!" If nothing clears that bar, **write NO article
   this run** — Job A alone is a fine week. Do not manufacture news. Evergreen "best card" lists belong
   on the Best Cards page, NOT in an article.

4. If Job B is warranted: write ONE short article in Navees's voice, in your OWN words (don't copy
   DansDeals/DoC text). First-person, candid, numbers-driven, short paragraphs, a
   `<div class='callout'>` bottom line, and lead with the freshness ("just dropped", "as of today").
   Then self-review against STYLE.md and rewrite anything that sounds generic. Save it as
   `content/posts/<YYYY-MM-DD>-<slug>.json` (schema: title, slug, date=today, updated=today,
   author "Navees", read_time, cover_emoji, tags, summary, body_html with single-quoted attributes;
   do NOT paste the disclaimer — the footer adds it; add a "cover" only if you have a real
   non-copyright image URL, else omit).

5. **Build:** `python build.py`. Confirm it exits 0. Never commit a broken build.

6. **Publish:** `git add -A && git commit -m "<what changed>" && git push`. Cloudflare auto-redeploys.
   If push fails on auth/remote, STOP and tell the user to finish GO-LIVE.md step 1.

7. **Report:** what you changed on the Best Cards page, whether you posted an article (and why / why not),
   and the source(s).

## Guardrails
- Best Cards lists: exactly 5 cashback + 5 travel, never more. This is a tight, curated page.
- Articles are for NEWS only. A normal week = update Best Cards, post no article. That is correct, not lazy.
- Never edit or delete the author's existing seed posts. One new article per run at most.
- If research or build genuinely fails, STOP and don't push. A skipped week is fine.
