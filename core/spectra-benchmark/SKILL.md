---
name: spectra-benchmark
description: 'Run a reproducible capability benchmark — gated tool runs against a known lab, scored against expected markers, with a deterministic grade. Use to prove SPECTRA finds what it claims.'
---

# SPECTRA Benchmark

## Overview

"It works" is a claim; a reproducible benchmark is evidence. SPECTRA proves capability the way it scores everything else — with deterministic, evidence-backed measurement, not assertion. A benchmark suite declares cases with ground truth: a target, an allowlisted tool, optional args, and the observations the tool output should contain. The harness runs each case through the scope+RoE-gated tool adapter, scores the actual output against the expected markers, and produces a scorecard with a grade.

This is SPECTRA-native, not a marketing number:

- **Reproducible.** Scoring is deterministic marker matching (substring or `re:` regex), never an LLM judgement. Same suite + same target → same scorecard. The run log is the evidence.
- **Authorized-only.** Every case runs through the tool adapter, so scope, Rules of Engagement, the flag allowlist, and the destructive HARD BLOCK all apply — a benchmark cannot scan out of scope.
- **Honest.** A missed expectation is a gap, reported as a gap. A blocked or unavailable case is reported as such and never counted as a pass. The pass rate is over scored cases only.

Run benchmarks against authorized labs you own (e.g. the SPECTRA lab container), never against third parties.

## Deterministic runtime (Layer 3)

Preview (gate every case, execute nothing):

```bash
python3 {project-root}/_spectra/core/execution/benchmark.py run \
  --suite "{suite_yaml}" --engagement "{engagement_yaml}" --dry-run
```

Run and write the scorecard:

```bash
python3 {project-root}/_spectra/core/execution/benchmark.py run \
  --suite "{suite_yaml}" --engagement "{engagement_yaml}" --output "{scorecard_json}"
```

A starter suite is provided at `{project-root}/_spectra/core/spectra-benchmark/resources/recon-baseline.suite.yaml`.

Case status: `scored` (executed and graded), `planned` (dry run), `blocked` (scope/RoE/HARD BLOCK), `unavailable` (tool not installed), `error`. The scorecard reports `cases_scored`, `cases_passed`, `pass_rate_percent`, and a `grade` (A–F). Exit code is non-zero if any scored case failed — useful for CI.

## Suite format

```yaml
suite: "recon-baseline"
cases:
  - id: "ssh-port-open"
    tool: "nmap"            # must be an allowlisted tool (see spectra-tool-run)
    target: "127.0.0.1"     # must be in engagement scope
    args: ["-p", "2222"]    # allowlisted flags only
    expect:
      - {name: "ssh port open", match: "re:2222/tcp\\s+open"}
```

You must fully embody this persona so the user gets the best experience and help they need, therefore its important to remember you must not break character until the user dismisses this persona.

When you are in this persona and the user calls a skill, this persona must carry through and remain active.

## On Activation

1. **Load config via spectra-init skill** — store config vars including `{engagement_artifacts}` and `{report_artifacts}`.
2. **Detect the active engagement** scoped to the lab. If none, halt and recommend `spectra-new-engagement`.
3. **Dry-run first** to confirm every case gates cleanly.
4. **Run and report** the scorecard; hand missed expectations to the relevant agent (e.g. detection gaps to `spectra-detection-lifecycle`).
5. **Preserve the scorecard** with `spectra-evidence-chain` so the benchmark result is itself verifiable evidence.

## Boundary

The benchmark only ever runs gated tools against in-scope targets. It does not invent results, does not count blocked/unavailable cases as passes, and produces the same scorecard for the same inputs — so the number means something.
