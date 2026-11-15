# Research log — Solo

Three lines per working session. Five minutes, written at the end of the
session — not reconstructed afterwards from memory.

---

## Entry 1 — 2026-09-03 (Setup)

**Did:** Resolved Python 3.10.20 + scipy 1.15.3 compatibility. Created directory tree under `your-work/solo/`. Ran `check_setup.py` — 112/112 tests pass. Bootstrapped claims.jsonl with 12 skeletons.

**Found:** The system Python had a version conflict preventing scipy import. Fix: use isolated venv with Python 3.10.20. gds-owl requires Python 3.14 — needs separate venv (venv-gds-owl).

**Blocked by:** Nothing — P0 complete.

---

## Entry 2 — 2026-09-04 (Phase 1)

**Did:** Profiled 7 graphs. Ran PageRank 10× per graph (70 total runs). Recorded compute time, iterations, top node/score, scores hash.

**Found:** Degree skew correlates with iteration count (Spearman +0.500), not compute time (+0.357). Node count is the strongest predictor of compute time (Spearman +0.964). unicodelang (skew=141) needs 67 iterations; email-Eu-core (skew=16.5) needs 14. Cross-machine calibration impossible — solo execution, no second machine.

**Blocked by:** Nothing — P1 complete.

---

## Entry 3 — 2026-09-04 (Phase 2A)

**Did:** Computed 4 centrality measures on 5 graphs. Pairwise Spearman correlation, top-10 overlap, named disagreements.

**Found:** Correlation ≠ top-k agreement. degree vs PageRank on unicodelang: ρ=+0.864 but top-10 overlap=1.00. Three disagreement directions reversed in memo: lesmis node 60, crime node 1053, openflights node 815 all have degree ranking higher, not betweenness.

**Blocked by:** Nothing — P2A complete.

---

## Entry 4 — 2026-09-04 (Phase 2B)

**Did:** Ran Louvain 200 times per graph on 5 graphs. Recorded hash, modularity, n_communities, ARI vs run 1.

**Found:** Louvain stable on crime (mod 0.9296 ± 0.0004) but noisy on openflights (0.6560 ± 0.0042). 200/200 distinct partitions on 4/5 graphs. Modularity std < 0.001 indicates seed-robust partitions.

**Blocked by:** Nothing — P2B complete.

---

## Entry 5 — 2026-09-04 (Phase 3A)

**Did:** Exact betweenness on 3 graphs. Sampled at 1%, 2%, 5%, 10%, 25% × 10 seeds (150 runs). Weights effect on openflights (500 airport pairs).

**Found:** At 1% sampling, speedup is 86.8–104.5× with Spearman >0.92 but top-10 overlap poor (0.18–0.54). At 5% sampling, speedup ~18–20× with Spearman >0.97 and top-10 overlap ~0.5–0.8. 90% of routes differ when ignoring weights on openflights.

**Blocked by:** Nothing — P3A complete.

---

## Entry 6 — 2026-09-04 (Phase 3B)

**Did:** Louvain vs Leiden on 5 graphs × 50 seeds. Community connectivity audit. Ground truth on email-Eu-core (42 departments).

**Found:** Disconnected rate near-zero (0–0.43%) vs published 16% claim. Fragile rate 12.9%–85.8% depending on graph. Ground truth ARI: Louvain 0.308, Leiden 0.305 — both low, indicating communities merge departments. Best modularity ≠ best ground truth.

**Blocked by:** Nothing — P3B complete.

---

## Entry 7 — 2026-09-04 (Phase 4)

**Did:** Applied PageRank and Louvain to bipartite graphs (crime, unicodelang). Projected onto each side. Compared rankings (Spearman) and communities (ARI).

**Found:** Projection is NOT neutral. crime side 1: Spearman=0.002 (uncorrelated). unicodelang side 0: ARI=0.17. Both results correct, but only one answers the question. unicodelang side 0 blowup: 10× edges from one high-degree node (degree 141).

**Blocked by:** Nothing — P4 complete.

---

## Entry 8 — 2026-09-10 (Correction pass)

**Did:** Recomputed 7 figures from CSVs after receiving GDS-REVIEW.html feedback. Fixed reversed direction rows in Part 2A. Retracted 2 claims about PageRank cost. Fixed factual errors (68 attempts, 86.8–104.5×, calibration ratios).

**Found:** The tilde-range habit caused 3 tables to be wrong. Three direction rows were reversed. The PageRank cost claim was backwards — node count is the strongest predictor, not degree skew. The crime bridge 100% finding is a base-rate artifact (bipartite graph).

**Blocked by:** claims.jsonl still needs 11/12 claims filled (pending primary-source research).

---

### What counts as a "found"

Anything you did not know when you sat down. It does not have to be a result:

- "Degree skew correlates with iteration count (+0.500) but not compute time (+0.357)"
- "The first timed call is 270× slower — runs.timed already handles this"
- "Louvain returned 31 communities one run and 28 the next on identical input"
- "Three direction rows in disagreements.csv were reversed — degree ranks higher when betweenness=0"

That last one is a legitimate entry. A session with nothing found is a real session and should be logged as such — but if you get three in a row, that is a signal to ask for help rather than a reason to write nothing.
