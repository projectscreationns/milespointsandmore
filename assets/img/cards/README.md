# Real card images go here

Drop a card image in this folder and the Deals page uses it automatically instead of the
styled placeholder tile.

## Naming
Name the file after the card's `card_name` in `content/best-deals.json`, lowercased with
dashes. Examples:

| card_name in best-deals.json | filename to drop here    |
|------------------------------|--------------------------|
| Sapphire Preferred           | `sapphire-preferred.png` |
| Ink Business Cash            | `ink-business-cash.png`  |
| IHG Rewards Premier          | `ihg-rewards-premier.png`|
| Qantas Amex Ultimate         | `qantas-amex-ultimate.png` |
| SoFi Checking                | `sofi-checking.png`      |

`.png`, `.jpg`, `.jpeg`, `.webp` and `.avif` all work. PNG with a transparent background
looks best. Roughly 600–900px wide is plenty.

Alternatively, set `"card_image": "/assets/img/cards/whatever.png"` on the deal itself.

Then run `python build.py` and push (the weekly automation does this for you too).

## Where to legitimately get card art

1. **Issuer affiliate programs** — the proper source. Joining gives you licensed card
   images *and* pays you per approved signup. This is how DansDeals / Doctor of Credit
   display real card art.
   - Chase: apply via a network like Impact / CJ Affiliate
   - American Express: `americanexpress.com/us/affiliate-program`
   - Capital One, Citi: available through CJ Affiliate / Rakuten Advertising
   - Card aggregators (CardRatings, Credit-Land, FlexOffers) bundle many issuers at once
     and are the usual starting point for a small blog.
2. **Issuer press / media kits** — some publish downloadable card imagery for editorial use.
3. **Photograph your own cards** — you hold most of these. A straight-on shot on a plain
   background looks great, and it's unambiguously yours to publish. Blur the number,
   expiry, name and CVV, or use an expired card.

Until a real image is dropped here, the site renders a styled card-shaped tile using the
`card_colors` in `best-deals.json` — same shape and slot, so swapping in the real thing
changes nothing else.
