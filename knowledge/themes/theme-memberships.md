---
type: Dataset
title: Theme memberships
description: Shared dated stock-to-theme relationships and references to existing constituent snapshots.
tags: [themes, tickers, membership]
status: draft
generated:
  by: codex/market-report-poc
  at: "2026-10-28T22:38:39Z"
sources:
  - id: gdx-holdings
    resource: /sectors/gdx.md
    title: GDX dated holdings snapshot
---
# Memberships

One row represents one security-to-subtheme relationship. Multiple relationships
per stock are allowed. No reviewed stock assignments have yet been added for the
new proposed themes; the table is intentionally empty.

| Symbol | Theme ID | Subtheme ID | Role | Exposure | Valid from | Valid to | Reviewed | Rationale | Source |
|---|---|---|---|---|---|---|---|---|---|

Use provider-qualified symbols. Unknown validity dates are left blank, not inferred
from a review date. Follow [methodology](/themes/methodology.md) when adding rows.

# Existing universe references

| Theme ID | Membership as of | Authoritative ticker list | Securities | Selection |
|---|---|---|---:|---|
| gold-miners | 2026-10-22 | [GDX holdings](/sectors/gdx.md) | 59 | Security rows; exclude cash and Other/Cash |

GDX membership remains in its existing authoritative holdings table.[^gdx-holdings]
Issuer labels require provider resolution; GDX itself is a proxy, not an additional
constituent. This dated snapshot is not historical point-in-time membership.
The manifest review does not constitute a new holdings download.

[^gdx-holdings]: Existing GDX holdings snapshot as of 2026-10-22; linked without duplicating the ticker list.
