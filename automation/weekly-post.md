# Weekly auto-post job

This is the exact task the scheduled cloud agent runs once a week. It runs inside a git
checkout of this repository. Follow every step.

## Steps

1. **Read `STYLE.md`** in the repo root, start to finish. Everything you write must match it.

2. **Research this week's best deals** (aim for the single most useful, or a tight roundup).
   Search for offers from roughly the last 7–14 days, covering BOTH:
   - **US**: Chase / Amex / Citi-AA / Capital One / Barclays sign-up bonuses, increased offers,
     transfer bonuses, program news.
   - **Australia**: Amex AU / Qantas / Velocity bonus points, UBank/ING/Macquarie/BOQ savings &
     account bonuses, Revolut/Wise changes.
   Good sources to check: doctorofcredit.com, frequentmiler.com, thepointsguy.com,
   pointhacks.com.au, ozbargain.com.au, finder.com.au, awardwallet.com.
   Verify the offer is current and note the source URL. **Never invent an offer or a number.**

3. **Pick one** angle and write an original post **in Navees's voice** (see STYLE.md):
   first person, candid, numbers-driven, short paragraphs, a `<div class='callout'>` bottom line.
   Rotate topic types week to week (deal alert → strategy → redemption → comparison → rules) so
   it doesn't feel repetitive. Prefer a concrete **deal alert** when a good one exists.

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
