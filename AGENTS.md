# Repository conventions

## Market bar downloads

- Persist downloaded daily bars through `bar_store.save_bars`, including downloads
  obtained through a connected tool in chat. The raw-data layout is
  `data/research/day/<download-date>/<encoded-symbol>.json`.
- Use the actual fetch timestamp; download dates are derived in Stockholm time.
  The directory date is not the bar's session date or the report date.
- Read raw histories through `bar_store.load_bars`. Select an explicit download
  date for reproducible research, or use the latest complete batch. Do not
  silently combine download dates or providers.
- Do not create new combined raw-price files outside this store. Legacy combined
  snapshots can still be imported. Derived index snapshots and symbol maps may
  live elsewhere under `data/`; report outputs belong under `reports/`.
- Keep `data/`, including `data/research/`, out of Git. Preserve fetch metadata,
  session-date treatment, and input hashes when generating derived results.
- Keep the report format concise: one chart or table and one or two sentences
  of interpretation per section. See README.md and the OKF knowledge bundle.
