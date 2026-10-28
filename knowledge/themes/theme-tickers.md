---
type: Dataset
title: Theme ticker universes
description: Shared manifest of dated ticker lists for active project themes.
tags: [themes, tickers, constituents, membership]
status: draft
generated:
  by: codex/market-report-poc
  at: "2026-10-28T21:55:00Z"
sources:
  - id: gdx-holdings
    resource: /sectors/gdx.md
    title: Dated GDX holdings table
---
# Universe manifest

**Manifest updated: 2026-10-28.** This shared file records where each theme's
tickers are stored. Existing authoritative lists are linked rather than copied;
the manifest update date does not imply holdings were refreshed.

| Theme ID | Membership as of | Ticker list | Eligible securities | Selection |
|---|---|---|---:|---|
| gold-miners | 2026-10-22 | [GDX holdings](/sectors/gdx.md) | 59 | Security rows only; exclude cash and Other/Cash |

# Gold miners

Use the issuer ticker column in the [GDX holdings table](/sectors/gdx.md).
The existing snapshot contains 59 securities, with multiple exchanges and issuer
ticker labels that require provider-specific resolution.[^gdx-holdings]
GDX itself is a proxy, not an additional member of its own constituent universe.

Keep membership dates, source/retrieval dates, exclusions, and provider symbols
explicit. Raw bars and local symbol maps remain under ignored `data/`; this file
contains knowledge about membership, not downloaded prices. For future custom
themes without an existing holdings concept, add a dated ticker table here with
theme ID, issuer ticker, provider-qualified symbol, source, and membership dates.
Do not interpret this fixed snapshot as historical point-in-time membership.

[^gdx-holdings]: GDX knowledge holdings snapshot as of 2026-10-22; no new holdings download performed for this manifest.
