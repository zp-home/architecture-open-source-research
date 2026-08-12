# Repository Research Method

## Candidate collection

Search each capability separately. Use precise terms such as `event driven backtest`, `limit order book simulator`, `RL experiment tracker`, `model registry`, `risk gateway`, and the target language/runtime. Search a local-language platform such as Gitee only when it is relevant to the deployment ecosystem or target integration.

Collect a short list first; then read sources. A candidate without a readable license, release/commit history, or clear ownership cannot be an adoption recommendation.

## Evidence fields

Capture these fields for every shortlisted repository:

| Field | Evidence needed |
| --- | --- |
| Identity | Canonical URL, owner, default branch, release/ref considered |
| License | Repository LICENSE file and notable dependency restrictions |
| Scope | Verified supported workload, data model, language, runtime, and extension points |
| Maintenance | Latest release/commit, issue/PR activity, bus-factor clues |
| Quality | Tests, CI, examples, benchmarks, docs, security process |
| Operations | Packaging, deployment, configuration, state/recovery, telemetry |
| Fit | Latency, data, regulatory, security, and team-fit constraints |
| Decision | Adopt, extend, borrow patterns, research only, or reject |

## Scoring

Use scoring only to structure discussion, never to replace judgment. Rate each candidate 0-3 for functional fit, operational maturity, maintenance, security/license fit, performance fit, and extension cost. State the evidence behind each score.

Reject or quarantine a candidate for absent/unclear licensing, archive-only status without a maintained fork, incompatible copyleft/commercial terms, unsafe credential handling, missing testability, or fundamentally mismatched market/execution assumptions.

## Trading-specific review

Verify whether a project uses trades, L1, L2, or L3 data; supports partial fills and queue modeling; models latency; handles sessions/contracts; and distinguishes backtest from live execution. Crypto and equities projects often provide useful patterns but do not prove compatibility with Chinese futures exchange or CTP semantics.
