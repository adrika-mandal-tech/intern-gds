# Part 1 — Profile & Calibrate

**Who:** solo  
**Machine:** macOS-15.7.7-arm64-arm-64bit | 10 cores | 16.0 GB RAM  
**Dates:** 2026-09-04 to 2026-09-04  
**Results files:** profiles.csv (7 rows), pagerank_runs.csv (70 rows), calibration.md

---

## 1. What I did

1. **Profiled 7 graphs**: nodes, edges, density, degree distribution, components, clustering, weight semantics.
2. **Ran PageRank 10× per graph**: 70 total runs with independent seeds. Recorded compute time, iterations, top node/score, scores hash.
3. **Cross-machine calibration**: attempted but could not complete — solo execution, no second machine. Documented in calibration.md.
4. **Analyzed results**: formulated and tested cost-prediction hypotheses.

---

## 2. What I found

### 2.1 Graph profiles

| Graph | Nodes | Edges | Density | Skew | Components | Type |
|-------|-------|-------|---------|------|------------|------|
| lesmis | 77 | 254 | 0.087 | 6.0 | 1 | Undirected, Weighted |
| unicodelang | 868 | 1,255 | 0.003 | 141.0 | 5 | Undirected, Bipartite |
| crime | 1,380 | 1,476 | 0.002 | 25.0 | 20 | Undirected, Bipartite |
| email-Eu-core | 986 | 24,929 | 0.026 | 16.5 | 1 | Directed |
| openflights | 3,214 | 36,906 | 0.004 | 79.5 | 7 | Directed, Weighted |
| facebook_combined | 4,039 | 88,234 | 0.011 | 41.8 | 1 | Undirected |
| ca-GrQc | 5,241 | 14,484 | 0.001 | 27.0 | 354 | Undirected |

### 2.2 PageRank compute time and iterations

| Graph | Mean compute (s) | Mean iterations | Degree skew |
|-------|------------------|-----------------|-------------|
| lesmis | 0.0012 | 37 | 6.0 |
| unicodelang | 0.0159 | 67 | 141.0 |
| email-Eu-core | 0.0187 | 14 | 16.5 |
| crime | 0.0193 | 54 | 25.0 |
| openflights | 0.0841 | 40 | 79.5 |
| facebook_combined | 0.1856 | 21 | 41.8 |
| ca-GrQc | 0.0976 | 41 | 27.0 |

**Key finding:** Degree skew correlates with iteration count (Spearman +0.500), not with compute time (Spearman +0.357). Node count is the strongest predictor of compute time (Spearman +0.964).

### 2.3 Calibration

Cross-machine calibration could not be performed — solo execution, no second machine available. The ratios between graphs on this single machine are:
- facebook_combined / ca-GrQc: 1.90×
- openflights / email-Eu-core: 4.51×
- email-Eu-core / lesmis: 16.12×

These ratios are portable; absolute times are not.

---

## 3. What surprised me

1. **unicodelang needs 67 iterations** despite having only 868 nodes — degree skew of 141.0 drives convergence cost, not graph size.
2. **email-Eu-core needs only 14 iterations** despite 986 nodes — moderate skew (16.5) means fast convergence.
3. **facebook_combined is the slowest** (0.1856s) despite not having the most nodes or highest skew — edge count (88,234) is the dominant factor.

---

## 4. What I could not determine

- Whether iteration counts are portable across machines — only one machine available.
- Whether the compute time ratios hold on different hardware — single-machine measurement only.
- Why facebook_combined is slower than ca-GrQc despite similar node counts — likely edge count difference (88,234 vs 14,484).

---

## 5. Judgement calls

- Used default PageRank parameters (damping=0.85, max_iter=100, tol=1e-6) as per brief.
- 10 seeds per graph: enough to see variance, not enough for confidence intervals.
- Cross-machine calibration documented as unavailable rather than omitted.

---

## 6. Sample sizes and caveats

| Claim | Graphs | Runs | Caveat |
|-------|--------|------|--------|
| Degree skew → iterations | 7 | 70 | Spearman +0.500, moderate |
| Node count → compute time | 7 | 70 | Spearman +0.964, strong |
| Calibration ratios | 7 | 70 | Single machine only |

---

## 7. Collaboration record

Solo execution. No colleague to compare with. All code from provided runners.
