# Repository conventions

## Open Knowledge Format (OKF)

- `knowledge/` is an OKF v0.2 bundle. Follow the
  [official specification](https://github.com/GoogleCloudPlatform/open-knowledge-format/blob/main/SPEC.md).
- Store each concept in a Markdown file with parseable YAML frontmatter and a
  nonempty `type`. Use a descriptive title, description, tags, and explicit
  `status` (`draft`, `stable`, or `deprecated`).
- Keep `index.md` for directory listings and `log.md` for newest-first updates
  under `## YYYY-MM-DD` headings. Only the bundle-root index has frontmatter,
  containing `okf_version: "0.2"`.
- Link concepts using bundle-root paths, e.g. `/sectors/gdx.md`; folder indexes
  use relative links. Update the relevant index and `knowledge/log.md` when
  adding concepts or changing their scope.
- Record sources in `sources` with stable IDs and cite claims through matching
  Markdown footnotes. Separate confirmed definitions, user hypotheses,
  exploratory results, and unresolved methodology.
- Update `generated.by` and `generated.at` on meaningful edits. Add `verified`
  only for an independent review that actually occurred; authoring or format
  checks are not evidence of a validated market claim.
- `market_report` is our extension, not an OKF standard. Keep it consistent with
  implemented behavior. Unvalidated trading hypotheses remain exploratory and
  disabled; displaying descriptive data does not validate a trading rule.
- Keep research reproducible: record inputs, download dates, adjustment policy,
  sample sizes, baseline, overlap, drawdowns, and known biases alongside results.

## TODOs and research plans

- Keep topic-specific tasks in the relevant knowledge concept, under
  `# Research TODOs` for studies or `# TODOs` for other work.
- Use Markdown checkboxes (`- [ ]` / `- [x]`) for actionable tasks. Describe a
  study's thresholds, horizons, comparison baseline, risk measures, and biases
  explicitly so its completion can be assessed.
- Keep one authoritative checklist per task; link to it from related concepts
  rather than duplicating it. Research plans are not findings or enabled rules.
- The report header lists unchecked tasks from `Research TODOs` sections as
  one-sentence bullets. Keep each checkbox's description concise; put study
  parameters in supporting bullets. Checked tasks disappear on the next run.
- Only mark a task complete after the work and its evidence are recorded. Link
  the resulting study or artifact and update the knowledge log.
- Adding or reading a TODO does not by itself authorize starting the work;
  execute the task when the user's request includes it.

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
