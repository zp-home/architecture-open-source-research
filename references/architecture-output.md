# Architecture Output Contract

## Per-module template

For each module, document:

1. Purpose and explicit non-goals.
2. Inputs and outputs, including event/API schemas and schema ownership.
3. State model: storage, ordering, idempotency key, replay/recovery, retention.
4. Methods: critical algorithms, retry/time-out policy, concurrency, and resource limits.
5. Open-source basis: URL/ref, decision, verified reusable pieces, required extensions.
6. Failure modes: stale data, duplication, outage, overload, corrupted state, and safe behavior.
7. Security/governance: identities, secrets, permissions, audit record, approval gates.
8. Tests and acceptance: unit/integration/replay/load/chaos checks plus measurable thresholds.

## Futures/RL module order

1. Data adapter and immutable event store.
2. Reference data and exchange-rule service.
3. Data-quality and feature service.
4. Event replay, order book, fill and latency simulator.
5. Baselines and experiment tracking.
6. RL environment, trainer, evaluator, and model registry.
7. Real-time feature/inference service.
8. Risk gateway, execution adapter, account/order state.
9. Shadow, paper trading, observability, audit, rollback, and human control.

## Promotion gates

Define a stop condition at every stage. A model must not advance from historical replay to shadow mode, shadow mode to paper trading, or paper trading to limited capital without passing chronology, cost, fill, latency, risk, reproducibility, and operational-recovery checks.
