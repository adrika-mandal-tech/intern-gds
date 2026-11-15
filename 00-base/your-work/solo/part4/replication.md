# Replication — solo

## The claim I tested

Since this is solo execution, there is no colleague's headline finding to replicate. The replication exercise as designed for a pair cannot be performed.

**Self-replication instead:** I re-ran the Phase 1 PageRank experiment (the foundation for all later phases) to verify determinism. Sample size: 7 graphs × 10 runs each = 70 runs per invocation; 2 invocations = 140 runs total.

## What I ran

Re-ran `python part-1/run_part1.py --who solo` a second time (separate invocation).

## What I got

| Graph | Iterations (run 1) | Iterations (run 2) | Match? |
|-------|-------------------|-------------------|--------|
| lesmis | 37 | 37 | ✅ |
| unicodelang | 67 | 67 | ✅ |
| email-Eu-core | 14 | 14 | ✅ |
| crime | 54 | 54 | ✅ |
| openflights | 40 | 40 | ✅ |
| facebook_combined | 21 | 21 | ✅ |
| ca-GrQc | 41 | 41 | ✅ |

**All 7 graphs: identical iteration counts across independent runs (n=10 runs per graph per invocation).** Scores hashes also matched within each graph.

## Verdict

**replicated** — The PageRank implementation is fully deterministic. Iteration counts (the portable metric from Phase 1) are invariant across runs (n=140 total runs).

## What we shared

Solo execution. No colleague to share with. All code from provided runners.