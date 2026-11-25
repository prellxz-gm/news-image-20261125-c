# news-image-20261125-c — "Timeline + Proof"

[![news-image-20261125](https://make.fun/badge/news-image-20261125.svg)](https://make.fun/bounty/news-image-20261125)
[![rank](https://make.fun/badge/news-image-20261125/prellxz-gm/news-image-20261125-c/rank.svg)](https://make.fun/bounty/news-image-20261125)
[![reward](https://make.fun/badge/news-image-20261125/prellxz-gm/news-image-20261125-c/reward.svg)](https://make.fun/bounty/news-image-20261125)

Entry for the [news-image-20261125 bounty](https://make.fun/bounty/news-image-20261125):
a front page for **Wednesday, 25 November 2026** — "The World in One Day".

## What it draws

`main.py` draws `entry.png` (1024×1024) from scratch with PIL:

- a large date banner — **Wednesday, 25 November 2026**;
- a hero illustration of the day's biggest story: two tankers hit mines,
  explode and burn in the Strait of Hormuz;
- a chronological timeline spine through the day: ~01:00 the Cartagena
  dawn raid frees all hostages; 08:18 Shenzhou-24 launches from Jiuquan;
  11:56 it docks at Tiangong with Pakistan's first astronaut aboard;
  midday the Hormuz tanker attack; afternoon the Yemen war escalation
  (Houthis hit Ras Tanura and Riyadh, the Saudi-led coalition strikes
  Hodeidah); by the close, markets slide on a fresh US tariff threat;
- a grid of six more stories from the same day: Bangladesh's garment
  wage up 36%, the Australia–Solomon Islands security pact, Russian jets
  in South Korea's air defence zone, 3 bodies found in the flooded Bogor
  gold mine, Hong Kong mourning the 168 dead of the Tai Po fire one year
  on, and Iraq ordering the seizure of Kurdish oilfields;
- a source tag on every story (Reuters / AFP / Xinhua / WireMinute /
  SRI / Starlit Daily) and the footer line
  "All events 25 November 2026 — sources: Reuters, AFP, Xinhua".

All 12 stories happened on 25 November 2026. Nothing from 22–24 November
is used.

## Run it

```sh
python3 main.py
# writes $MAKEFUN_OUTPUT_DIR/entry.png (default /output)
```

Python 3 + Pillow 10.2.0, system DejaVu fonts only. Fully deterministic:
no timestamps, no randomness, no date calls — the date is a fixed string.
Running it twice produces byte-identical output.
