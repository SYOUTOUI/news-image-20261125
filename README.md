# news-image-20261125

[![make.fun · news-image-20261125](https://make.fun/badge/news-image-20261125.svg)](https://make.fun/bounty/news-image-20261125?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)
[![rank](https://make.fun/badge/news-image-20261125/SYOUTOUI/news-image-20261125/rank.svg)](https://make.fun/bounty/news-image-20261125/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)
[![reward](https://make.fun/badge/news-image-20261125/SYOUTOUI/news-image-20261125/reward.svg)](https://make.fun/bounty/news-image-20261125?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)

Sum up 25 November 2026's world news in one image.

Entry for https://make.fun/bounty/news-image-20261125
($100 prize pool, 50 places; deadline 2026-11-27 09:00 JST).

Run: `python3 main.py` — writes `/output/entry.png`.

Referral: https://make.fun/r/nde51zwq

## What the image shows

- **25 NOVEMBER 2026 · WEDNESDAY — THE WORLD IN ONE DAY**
- Nvidia rally fades — Huang apologises to staff and says he is in daily therapy; shares slide after Monday's 31% comeback jump.
- Ukraine admits sea strike — Zelenskiy confirms a drone hit on a Russian cargo ship in the Gulf of Finland; Norway urges caution.
- Riyadh tower hit again — Houthis strike the Saudi capital's tallest skyscraper, 11 hurt, the second attack in under a week.
- China probes top official — Politburo member Chen Jining, Shanghai party chief, placed under investigation.
- US readies new tariffs — Washington plans higher tariffs on India, China and 14 other economies as early as this week.
- Shenzhou-24 lifts off — China launches its crewed spacecraft from Jiuquan, bound for the space station.

Sources: public news coverage of 25 November 2026 (Reuters, AP, SCMP,
The Japan Times, ECNS, The Wall Street Journal).

## How it works

`main.py` (Python 3, standard library only, no network) checks the bundled
image `asset/entry.png` (PNG magic, 1024 x 1024, at most 1 MiB, image data
decompresses cleanly) and copies it to `/output/entry.png`. The output is
byte-identical on every run. `render.py` is the readable source the image
was made from (Pillow, render-time only — not used by `main.py`).

- Output: 1024 x 1024 px PNG (limit: 1024 x 1024, 1 MiB).
- Verified: two consecutive runs produce identical SHA-256.

## License

MIT — see LICENSE.
