# Go-live runbook

The site is built and committed to git in this folder:
`C:\Users\nsell_x3c3zxa\milespointsandmore`

> Why not the OneDrive `Documents\Claude\Website` folder? Windows blocks normal programs
> (git, python) from writing there, so the working copy lives here instead. This folder is the
> real project now.

Follow these once and you're live + auto-updating. Total time ~15 minutes.

## 1. Put it on GitHub  (~3 min)

1. Go to <https://github.com/new> and create an **empty** repo named `milespointsandmore`
   (no README, no .gitignore — leave it empty). Public or private both work.
2. Open a terminal **in this folder** and run (replace `YOURNAME`):
   ```powershell
   cd C:\Users\nsell_x3c3zxa\milespointsandmore
   git remote add origin https://github.com/YOURNAME/milespointsandmore.git
   git push -u origin main
   ```
   Git will pop up a browser sign-in the first time — that's normal.

## 2. Connect Cloudflare Pages  (~5 min)

1. <https://dash.cloudflare.com> → **Workers & Pages** → **Create** → **Pages** →
   **Connect to Git** → pick `milespointsandmore`.
2. Build settings:
   - **Framework preset:** None
   - **Build command:** `python build.py`
   - **Build output directory:** `public`
3. **Save and Deploy.** In ~1 minute you'll have a live URL like
   `https://milespointsandmore.pages.dev`. Every future `git push` auto-redeploys.

## 3. Point your domain (milespointsandmore.com) at it  (~5 min, do this last)

Your domain is currently on Wix. Only switch after you're happy with the new site.
1. In the Cloudflare Pages project → **Custom domains** → **Set up a domain** →
   enter `milespointsandmore.com` and `www.milespointsandmore.com`.
2. Cloudflare shows the DNS records to add. Add them wherever your domain's DNS lives
   (Wix, or your registrar). If you move the whole domain to Cloudflare DNS, it's automatic.
3. Wait for it to go green (minutes to a few hours). Done — off Wix, $0 hosting.

## 4. Weekly auto-posting

Once the repo is on GitHub (step 1), the weekly agent defined in `automation/weekly-post.md`
can run and push new posts automatically. Ask Claude to "set up the weekly schedule" and it
will register the recurring job. Every run: finds a fresh AU/US deal → writes it in your voice
→ builds → pushes → Cloudflare redeploys.

## Editing by hand anytime
- New post: copy any file in `content/posts/`, change the fields, run `python build.py`,
  then `git add -A && git commit -m "new post" && git push`.
- Change wording/nav: edit `content/site.json`. Change the look: edit `assets/style.css`.
