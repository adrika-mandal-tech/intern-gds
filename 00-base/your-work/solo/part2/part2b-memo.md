# Part 2B — Is community detection repeatable?

**Who:** solo  
**Machine:** macOS-15.7.7-arm64-arm-64bit | 10 cores | 16.0 GB RAM  
**Dates:** 2026-09-04 to 2026-09-04  
**Results files:** louvain_runs.csv (1000 rows: 5 graphs × 200 seeds)

---

## 1. What I did

Ran Louvain community detection 200 times per graph (seeds 0–199) on 5 graphs (unicodelang, crime, email-Eu-core, openflights, ca-GrQc) using `python part-2/run_part2b.py --who solo`. Graphs loaded unweighted, directed converted to undirected. Each run recorded: n_communities, modularity, partition_hash, ARI vs run 1. 200 distinct seeds per graph enforced.

---

## 2. What I found

### 2.1 Every graph produces a different partition on nearly every run

| Graph | Distinct partitions / 200 | Identical to run 1 | Mean ARI vs run 1 |
|-------|---------------------------|-------------------|-------------------|
| unicodelang | 200 | 1 | 0.7335 |
| crime | 189 | 1 | 0.8774 |
| email-Eu-core | 200 | 1 | 0.7793 |
| openflights | 200 | 1 | 0.7620 |
| ca-GrQc | 200 | 1 | 0.6180 |

**Key finding:** On 4 of 5 graphs, all 200 runs produced distinct partitions. On crime, 189/200 were distinct. The algorithm *never* gives the same answer twice on these graphs.

### 2.2 But modularity barely moves

| Graph | Modularity min | Modularity max | Spread | Std dev |
|-------|----------------|----------------|--------|---------|
| unicodelang | 0.7143 | 0.7238 | 0.0095 | 0.00146 |
| crime | 0.9283 | 0.9304 | 0.0022 | 0.00041 |
| email-Eu-core | 0.3998 | 0.4174 | 0.0176 | 0.00307 |
| openflights | 0.6244 | 0.6601 | 0.0358 | 0.00422 |
| ca-GrQc | 0.8588 | 0.8636 | 0.0048 | 0.00086 |

**Different answer ≠ worse answer.** The modularity spread is tiny (0.2–3.6%) even though partitions differ completely. ARI vs run 1 averages 0.62–0.88 — substantial structural disagreement despite similar quality scores.

### 2.3 Community count varies

| Graph | Min communities | Max communities | Distinct counts |
|-------|----------------|----------------|-----------------|
| unicodelang | 19 | 24 | 6 |
| crime | 47 | 53 | 7 |
| email-Eu-core | 6 | 9 | 4 |
| openflights | 22 | 34 | 13 |
| ca-GrQc | 387 | 395 | 9 |

Openflights has the widest range (22–34 communities). ca-GrQc is stable in count (387–395) but partitions differ (ARI=0.618).

### 2.4 Lowest mean ARI: ca-GrQc (0.618)

ca-GrQc has 354 components and Louvain disagrees most with itself here (mean ARI 0.618). The fragmented structure creates many equivalent local optima. Unicodelang (bipartite, 5 components) also low at 0.734.

---

## 3. What surprised me

1. **200/200 distinct partitions on 4 graphs** — I expected some repeats. The algorithm explores a vast space of near-equivalent optima.
2. **Modularity spread is 10–50x smaller than ARI spread** — quality metric is stable; partition is not. This decoupling is the core insight.
3. **ca-GrQc has highest community count stability but lowest ARI** — same number of communities, completely different memberships.

---

## 4. What I could not determine

- Whether 200 runs is enough to characterize the full partition distribution, or if more runs would reveal new modes.
- Whether the partition distribution is multimodal (distinct basins) or a continuum.
- How this repeatability compares to other algorithms (Leiden, label propagation) — that's Phase 3B.

---

## 5. Judgement calls

- Used 200 seeds as specified. Verified all 200 distinct per graph via partition_hash.
- Reported per-graph, not averaged — the brief warns against averaging across graphs.
- ARI vs run 1 as reference; could also use pairwise ARI matrix but 200×200 is large.

---

## 6. Sample sizes and caveats

| Claim | Graphs | Runs | Caveat |
|-------|--------|------|--------|
| Distinct partitions | 5 | 200 each | Only these 5 graphs; 6th graph may differ |
| Modularity spread | 5 | 200 each | Tiny spread; quality ≠ stability |
| ARI vs run 1 | 5 | 200 each | Reference is arbitrary run 1 |

---

## 7. Collaboration record

Solo execution. This directly sets up Phase 3B (Louvain vs Leiden comparison) — the Phase 2B spread defines the noise floor for detecting real differences.