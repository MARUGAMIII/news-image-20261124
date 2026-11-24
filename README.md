# news-image-20261124

[![make.fun · news-image-20261124](https://make.fun/badge/news-image-20261124.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![rank](https://make.fun/badge/news-image-20261124/MARUGAMIII/news-image-20261124/rank.svg)](https://make.fun/bounty/news-image-20261124/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![reward](https://make.fun/badge/news-image-20261124/MARUGAMIII/news-image-20261124/reward.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)

A one-page newspaper that sums up the world's news of Tuesday 24 November 2026
in a single image: **40 sourced stories**, a **UTC timeline** of the day, and a
**date check** printed on the page.

## The image

- **Lead story:** Nvidia's board reinstates Jensen Huang as chief executive —
  shares surge 31% in a day; a Senate hearing is set for 3 December.
- **Featured:** Russian aircraft enter South Korea's air-defence zone;
  Russian strikes kill at least 12 near Kyiv; the search goes on at the
  Serang candy factory in Indonesia (34 still missing).
- **The day in 40 stories:** one line each, numbered 5–40, spanning Ukraine,
  Korea, the Gulf, Sudan, Indonesia, Thailand, Bangladesh, Pakistan, China,
  Russia, Germany, the UK, the US and Mexico — plus markets, sport and culture.
- **Timeline (UTC):** 00:07 Reuters journalists vote 94% to strike · 00:18
  12 killed near Kyiv · 00:34 Ukraine hits Russian oil sites · 01:00 Russian
  jets in Korea's zone · 01:22 Brookfield's $2.53bn bid backed · 01:47 US may
  renew Iran strikes.
- **Date check:** every story on the page happened, or was first reported, on
  Tuesday 24 November 2026. No story predates 13 November 2026.

Sources: AP, Reuters, AFP, CNN, Times of India, Bernama-dpa, News Guild of
New York.

## How it works

`entry.png` (1024×1024, under 1 MiB) is the finished front page, rendered at
build time from the day's wires by `design.py` (Pillow, local only).
`main.py` (Python 3.13, standard library only) copies it to `/output/entry.png`,
byte for byte, on every run — so the two grader runs write identical bytes.

```sh
python3 design.py
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

## Competition

[News image — 24 November 2026](https://make.fun/bounty/news-image-20261124) on
make.fun. $100 in prizes shared by the 50 highest-ranked entries.

## License

MIT — see [LICENSE](LICENSE).
