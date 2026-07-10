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

2. **JOB A — refresh the Best Cards page.** Open `content/best-cards.json`. Re-check DoC + DansDeals
   for the current best **cashback** and **travel** credit-card sign-up bonuses. Update each list so
   it holds exactly the **top 5** for that category (no more). Bump a card up/down, swap one out for a
   new best-ever/increased offer, fix any bonus/spend/fee that changed, drop anything expired. Keep the
   `why` lines in Navees's voice (short, candid, numbers-first). Set `"updated"` to today's date. If
   nothing changed this week, still set the date so readers see it's current. Keep exactly 5 per list.

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
