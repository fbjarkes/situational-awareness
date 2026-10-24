---
type: Reference
title: Project decisions
description: Recorded requirements, proposals, and knowledge authoring conventions.
tags: [project, knowledge, methodology]
status: draft
generated:
  by: codex/market-report-poc
sources:
  - id: okf-spec
    resource: https://github.com/GoogleCloudPlatform/open-knowledge-format/blob/main/SPEC.md
    title: Official Open Knowledge Format specification
---
# Discussion record

- User requirement: each report section contains one simple chart or table
  and a one- or two-sentence interpretation.
- User instruction: follow the OKF specification for structuring concepts and maintaining provenance.
- Project decision: adopt a structured approach for recording requirements, proposals, and knowledge authoring conventions using OKF.-

This note preserves provenance for project choices; it is not independent
evidence for market claims.

# Bundle conventions

This bundle follows OKF v0.2 structural conventions.[^okf-spec]
Concepts use YAML frontmatter with a nonempty type and a Markdown body.
Indexes list contents; the log records updates under dated headings.
Leading-slash concept links resolve from the knowledge bundle root.

The `market_report` mapping is a project-specific extension. Its fields
describe candidate report rules and metric settings, not standard OKF keys.
No report loader or executable rule engine is implemented yet.

# Review and evidence

Use `status: draft` for incomplete concepts. Record actual independent review
events in `verified` only after they occur. Document generation and format
checks are not empirical validation of a market hypothesis.

Before enabling an insight, record its sources, sample period, method,
results, limitations, and evidence status. Keep authoring history distinct
from empirical support. Never infer that a reviewed document proves its
underlying hypothesis.

[^okf-spec]: Official specification, particularly concept structure, provenance, lifecycle, links, indexes, and logs.
