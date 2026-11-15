# Part 3B — Do the communities hold together?

**Who:** solo  
**Machine:** macOS-15.7.7-arm64-arm-64bit | 10 cores | 16.0 GB RAM  
**Dates:** 2026-09-04 to 2026-09-04  
**Results files:** community_quality.csv (500 rows), ground_truth_scores.csv (100 rows), similarity_vs_bridges.csv

---

## 1. What I did

1. **Louvain vs Leiden** (50 seeds each) on 5 graphs. Every community checked for connectivity using `gdslab.stats.community_connectivity`: disconnected (multiple components), fragile (bridge splits two ≥2-node pieces), pendant (leaf node).
2. **Ground truth** on email-Eu-core: scored each run's communities against 42 real departments using NMI and ARI.
3. **Similarity vs bridges**: Computed Jaccard similarity and edge betweenness for all edges on crime and email-Eu-core. Analyzed top 1% by betweenness.

---

## 2. What I found

### 2.1 Disconnected communities (the headline)

| Graph | Louvain disconnected | Leiden disconnected | Louvain fragile | Leiden fragile | Louvain pendant | Leiden pendant |
|-------|---------------------|---------------------|-----------------|----------------|-----------------|----------------|
| unicodelang | 0.00% | 0.00% | 83.63% | 75.33% | 16.37% | 24.67% |
| crime | 0.00% | 0.00% | 85.76% | 84.67% | 14.24% | 15.33% |
| email-Eu-core | 0.00% | 0.00% | 12.83% | 13.17% | 87.17% | 86.83% |
| openflights | **0.41%** | **0.00%** | 48.92% | 48.53% | 40.13% | 41.42% |
| ca-GrQc | **0.01%** | **0.00%** | 15.30% | 15.16% | 40.47% | 40.21% |

**Published claim (Traag et al. 2019):** Louvain disconnected up to 16%, badly connected up to 25%.

**Our measurement:** Disconnected rate is **near-zero** on 4/5 graphs (0–0.41%). Only openflights shows any (0.41%). **Our numbers do not support the published 16% claim** on these graphs.

**Fragile rate** (the "badly connected" proxy) varies enormously: 12.8% (email) to 85.8% (crime). Leiden reduces fragile slightly on unicodelang/crime but not consistently.

### 2.2 Leiden vs Louvain: Does it fix the defect?

- **Disconnected:** Leiden achieves 0% on all 5 graphs vs Louvain's 0–0.41%. **Yes, it fixes the rare disconnected case.**
- **Fragile:** Mixed. Leiden reduces fragile on unicodelang (83.6%→75.3%) and crime (85.8%→84.7%) but not on others.
- **Modularity:** Leiden modularity slightly higher on average (not measured here but expected).
- **Phase 2B noise floor:** Louvain mean ARI vs run 1 is 0.62–0.88. Leiden-Louvain ARI difference must exceed this to be meaningful. Not directly measured here.

### 2.3 Ground truth on email-Eu-core (42 departments)

| Algorithm | Mean NMI vs truth | Mean ARI vs truth | Mean communities |
|-----------|-------------------|-------------------|------------------|
| Louvain | 0.577 | 0.308 | 6–8 |
| Leiden | 0.573 | 0.305 | 6–8 |

**Critical finding:** The run with **highest modularity does NOT consistently score best against truth**. Modularity optimization ≠ ground truth recovery. Both algorithms find ~6–8 communities vs real 42 — they merge departments. The ARI is low (0.308/0.305), indicating that the detected communities barely overlap with the known department structure.

### 2.4 Similarity vs bridges (top 1% edges by betweenness)

| Graph | Top 1% edges | Zero similarity | % zero |
|-------|--------------|-----------------|--------|
| crime | 14 | 14 | **100%** |
| email-Eu-core | 160 | 112 | **70%** |

**Why:** Bridges connect dense clusters with few shared neighbors → Jaccard = 0. The most important edges (by traffic) are precisely the ones similarity *misses*.

**Consequence:** If you use similarity for "related items," you systematically never suggest the bridge relationships that hold the network together.

---

## 3. What surprised me

1. **Disconnected rate near-zero** — published 16% claim not reproduced on these 5 graphs. Either the claim was on different graph types, or Louvain implementation improved.
2. **Fragile rates 13–86%** — enormous variation. "Badly connected" depends heavily on graph structure.
3. **100% zero similarity on crime bridges** — every single high-betweenness edge in crime has Jaccard=0. Similarity is blind to bridges.
4. **Best modularity ≠ best ground truth** — the objective function is misaligned with reality.

---

## 4. What I could not determine

- Whether Leiden's lower disconnected rate is statistically significant given Phase 2B noise (Louvain ARI spread 0.62–0.88).
- Why disconnected rate differs so much from published claim — different graphs? Different Louvain implementation (networkx vs original)?
- Whether weighted Louvain/Leiden would change disconnected/fragile rates.

---

## 5. Judgement calls

- Used n_assessed (communities ≥3 nodes) as denominator per stats.py — excludes trivial communities.
- Reported fragile as "badly connected" proxy since original claim says "badly connected up to 25%".
- Ground truth comparison: used NMI/ARI on overlapping nodes only (some nodes may be missing from labels).

---

## 6. Sample sizes and caveats

| Claim | Graphs | Runs | Caveat |
|-------|--------|------|--------|
| Disconnected ≤0.41% | 5 | 50 each | Published claim 16% not reproduced |
| Leiden fixes disconnected | 5 | 50 each | Effect size small; within Phase 2B noise? |
| Fragile 13–86% | 5 | 50 each | Definition-dependent; varies by graph |
| Best modularity ≠ best truth | 1 (email) | 50 each | Single graph; 42 departments |

---

## 7. Collaboration record

Solo execution. Phase 2B Louvain repeatability (ARI 0.62–0.88) sets noise floor for this comparison.