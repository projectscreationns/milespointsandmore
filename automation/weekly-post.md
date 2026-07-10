# Weekly auto-post job

This is the exact task the scheduled cloud agent runs once a week. It runs inside a git
checkout of this repository. Follow every step.

## Steps

1. **Read `STYLE.md`** in the repo root, start to finish. Everything you write must match it.

2. **Research this week's best deals — PRIMARY SOURCES ARE DANSDEALS AND DOCTOR OF CREDIT.**
   These two are the signal; everything else is backup. Check them like this:

   **Doctor of Credit** (fetch directly — WebFetch works):
   - `https://www.doctorofcredit.com/best-current-credit-card-sign-bonuses/`
   - `https://www.doctorofcredit.com/best-bank-account-bonuses/`
   - `https://www.doctorofcredit.com/` (homepage, for the last ~7 days of news)

   **DansDeals** (⚠️ it 403-blocks direct WebFetch — do NOT WebFetch article pages. Instead):
   - `WebSearch` with `allowed_domains: ["dansdeals.com"]` and queries like "best credit card
     bonus", "increased offer", "best offer ever", "limited time" — read the titles + snippets.
   - Its RSS feed usually fetches fine: WebFetch `https://www.dansdeals.com/feed/` for the latest posts.
   - Their evergreen list: search for "The Best Credit Cards To Get Right Now" on dansdeals.com.

   Backup sources (only if the two above are thin): frequentmiler.com, awardwallet.com,
   thepointsguy.com; for **Australia** (still in scope): pointhacks.com.au, ozbargain.com.au,
   finder.com.au. Cover BOTH US (Chase/Amex/Citi-AA/Capital One/Barclays SUBs, increased offers,
   transfer bonuses) and AU (Amex AU/Qantas/Velocity, UBank/ING/Macquarie bonuses).
   Verify the offer is current and note the source URL. **Never invent an offer or a number.**

3. **Apply the "genuinely worth it" bar — this is the whole point.** Only write up a deal that
   clears AT LEAST ONE of these:
   - Flagged as **best-ever / all-time-high / increased / elevated** offer by the source.
   - **High value**: roughly ≥ $500 or ≥ 80k points/miles, OR a low-effort high-return card
     (e.g. a NO-annual-fee card with a big bonus, or an easy bank bonus with tiny spend).
   - **Time-sensitive** (ending soon / limited-time) or a **brand-new** launch worth flagging.
   Prefer deals that appear on BOTH DansDeals and DoC — that's the strongest signal. Skip
   run-of-the-mill or heavily-targeted YMMV offers unless they're genuinely remarkable. If nothing
   this week clears the bar, do NOT force it — write an evergreen strategy/tips post instead (step 3b).

3b. **Write** an original post **in Navees's voice** (see STYLE.md): first person, candid,
   numbers-driven, short paragraphs, a `<div class='callout'>` bottom line. Summarise the deal in
   your OWN words with your own take (do not copy DansDeals/DoC text — link/credit the source in
   spirit but write it fresh). Rotate topic types week to week (deal alert → strategy → redemption
   → comparison → rules). Prefer a concrete **deal alert** when a worth-it one exists.

4. **Self-review pass.** Re-read your draft against STYLE.md. If any sentence sounds generic,
   corporate, or like a press release, rewrite it. It must be indistinguishable from the existing
   posts. Confirm every factual claim traces to your research.

5. **Create the post file** at `content/posts/<YYYY-MM-DD>-<slug>.json` with this schema:
   ```json
   {
     "title": "...",
     "slug": "kebab-case-unique",
     "date": "<today, YYYY-MM-DD>",
     "updated": "<today>",
     "author": "Navees",
     "read_time": "2 min read",
     "cover_emoji": "🇦🇺",
     "tags": ["Deal", "Australia"],
     "summary": "One or two sentences for the card + meta description.",
     "body_html": "<p class='lead'>...</p> ... <div class='callout'>...</div>"
   }
   ```
   Use single quotes for HTML attributes inside `body_html`. Do NOT paste the disclaimer into the
   body — the site adds it automatically.

6. **Build & verify:** run `python build.py`. Confirm it prints the post count (should increase by
   one) and exits 0. If the build fails, fix the JSON — do NOT commit a broken build.

7. **Publish:** `git add -A && git commit -m "post: <title>" && git push`. Cloudflare Pages
   redeploys automatically. Done.

## Guardrails
- If research turns up nothing genuinely worth posting this week, it's fine to write a short
  evergreen strategy/tips post instead — but still in voice, still useful. Don't force a bad deal.
- One post per run. Never delete or rewrite existing posts.
- If anything fails (no network, build error you can't fix), STOP and do not push. The site simply
  stays as-is; a broken week is better than a broken site.
