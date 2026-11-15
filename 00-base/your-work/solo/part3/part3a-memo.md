# Part 3A — Betweenness cost, approximation, and weights

**Who:** solo  
**Machine:** macOS-15.7.7-arm64-arm-64bit | 10 cores | 16.0 GB RAM  
**Dates:** 2026-09-04 to 2026-09-04  
**Results files:** betweenness_exact.csv (3), betweenness_approx.csv (150), weights_effect.csv (500)

---

## 1. What I did

1. **Exact betweenness** on 3 graphs (email-Eu-core, openflights, ca-GrQc) using Brandes algorithm — ground truth.
2. **Sampled betweenness** at 5 fractions (1%, 2%, 5%, 10%, 25% of nodes) × 10 seeds each = 150 runs. Compared to exact via top-10 overlap, top-50 overlap, Spearman.
3. **Weights effect** on openflights: 500 random airport pairs, compared fewest-hops (unweighted) vs shortest-distance (weighted) paths. Measured cost ratio (hops distance / true shortest distance).

---

## 2. What I found

### 2.1 Exact betweenness cost

| Graph | Nodes | Edges | Time (s) | ms/node |
|-------|-------|-------|----------|---------|
| email-Eu-core | 986 | 16,064 | 2.8 | 2.83 |
| openflights | 3,214 | 18,858 | 16.2 | 5.04 |
| ca-GrQc | 5,241 | 14,484 | 23.3 | 4.44 |

Cost scales roughly with V×E. ca-GrQc (5,241 nodes, 14,484 edges) is slowest despite fewer edges than openflights — more nodes to process.

### 2.2 Sampled betweenness: How much is enough?

**Mean top-10 overlap vs exact (10 seeds per fraction):**

| Fraction | email-Eu-core | openflights | ca-GrQc |
|----------|---------------|-------------|---------|
| 1% | 0.34 (worst 0.18) | 0.47 (worst 0.33) | 0.32 (worst 0.18) |
| 2% | 0.33 (0.18) | 0.61 (0.43) | 0.51 (0.33) |
| 5% | 0.41 (0.33) | 0.79 (0.67) | 0.66 (0.54) |
| 10% | 0.62 (0.43) | 0.84 (0.67) | 0.73 (0.67) |
| 25% | 0.84 (0.67) | 0.93 (0.82) | 0.84 (0.67) |

**Verdict:** For reliable top-10 (mean overlap ≥ 0.8, worst ≥ 0.6):
- openflights: 10% sample (k=321) suffices
- email-Eu-core: 25% sample (k=246) needed
- ca-GrQc: 25% sample (k=1,310) needed

**Condition:** "10% sample works for top-10 on openflights; need 25% on ca-GrQc and email-Eu-core."

### 2.3 Top-10 vs Top-50 vs Spearman

At 10% sample:
- Top-10 overlap: 0.62–0.84
- Top-50 overlap: higher (easier to get right — more nodes to match)
- Spearman: lower (ranking *all* nodes is harder)

**Use top-10 overlap** if you only act on the top nodes. **Use Spearman** if you need full ranking fidelity.

### 2.4 Weights effect on openflights (500 airport pairs)

- **Routes differ**: 450/500 = **90.0%**
- **Cost ratio** (hops distance / true shortest distance) for differing routes:
  - Median: 1.16×
  - 90th percentile: 1.74×
  - Worst: 5.38×
- **No hop saving**: 159/450 (35.3%) of differing routes had same hop count but longer distance

**Interpretation:** Ignoring weights (treating distance as unweighted) gives you a different route 90% of the time. The median penalty is modest (16% longer), but the tail is severe (5.4× worse). Over 1/3 of the time you fly further *for no reduction in stops*.

---

## 3. What surprised me

1. **90% route difference** on openflights — weights matter enormously. Fewest-hops is a poor proxy for distance.
2. **35% of differing routes have same hop count** — the unweighted algorithm isn't even saving stops; it's just picking different intermediates that happen to be farther.
3. **1% sample is useless** (mean top-10 overlap 0.32–0.47). You need at least 5% to get signal.

---

## 4. What I could not determine

- How sampling quality scales with graph size — only 3 graphs.
- Whether the "10% rule" for openflights holds on facebook_combined (densest graph) — would need `--full` flag.
- Why ca-GrQc needs higher sample fraction than openflights despite similar edges — likely the 354 components create isolated regions that sampling misses.

---

## 5. Judgement calls

- "Reliable" = mean top-10 overlap ≥ 0.8, worst ≥ 0.6. Could choose stricter/looser threshold.
- 10 seeds per fraction: enough to see worst case, but not enough for confidence intervals.
- 500 airport pairs: sufficient for distribution shape, but single graph (openflights only).

---

## 6. Sample sizes and caveats

| Claim | Graphs | Runs | Caveat |
|-------|--------|------|--------|
| 10% sample for top-10 | 3 | 150 | ca-GrQc needs 25% |
| 90% routes differ | 1 (openflights) | 500 | Single graph; weights are distances (cost) |
| Median 1.16× penalty | 1 | 450 | Tail is 5.4×; not symmetric |

---

## 7. Collaboration record

Solo execution. Phase 2B established Louvain repeatability; this phase establishes betweenness approximation repeatability (10 seeds per setting).