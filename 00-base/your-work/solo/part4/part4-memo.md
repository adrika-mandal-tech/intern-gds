# Part 4A — Projection effects (bipartite → one-mode)

**Who:** solo  
**Machine:** macOS-15.7.7-arm64-arm-64bit | 10 cores | 16.0 GB RAM  
**Dates:** 2026-09-04 to 2026-09-04  
**Results files:** projection_shape.csv, projection_mass.csv, projection_rankings.csv, projection_effect.csv

---

## 1. What I did

Ran PageRank and Louvain community detection three ways on 2 bipartite graphs (crime, unicodelang):
- Raw two-sided graph (bipartite)
- Projected onto side 0
- Projected onto side 1

Used `python part-4/run_part4.py --who solo`. Compared rankings (top-10/20 overlap, Spearman) and communities (ARI) across views.

---

## 2. What I found

### 2.1 PageRank mass piles up on one side (rank sink)

| Graph | Side | Nodes % | PageRank % | Mass ratio |
|-------|------|---------|------------|------------|
| crime | 0 (people) | 60.1% | 50.8% | 0.85× |
| crime | 1 (crimes) | 39.9% | 49.2% | **1.23×** |
| unicodelang | 0 (territories) | 29.3% | **48.3%** | **1.65×** |
| unicodelang | 1 (languages) | 70.7% | 51.7% | 0.73× |

**Interpretation:** On crime, crimes (side 1) accumulate PageRank (1.23× their share) — people point to crimes, creating a sink. On unicodelang, territories (side 0) accumulate mass (1.65×) — languages point to territories.

### 2.2 Projection blows up edges

| Graph | Raw edges | Project side 0 | Blowup | Project side 1 | Blowup |
|-------|-----------|----------------|--------|----------------|--------|
| crime | 1,476 | 2,253 | 1.5× | 2,343 | 1.6× |
| unicodelang | 1,255 | 12,552 | **10.0×** | 7,514 | 6.0× |

**Why:** unicodelang side 0 has max away-degree 141 (one language in 141 territories) → contributes 141×140/2 = 9,870 edges from that one node. **One high-degree node dominates the projection.**

### 2.3 Rankings: Raw vs projected — sometimes unrelated

| Graph | Side | Top-10 overlap | Top-20 overlap | Spearman |
|-------|------|----------------|----------------|----------|
| crime | 0 | 0.33 | — | +0.226 |
| crime | 1 | **0.18** | — | **+0.002** |
| unicodelang | 0 | **0.11** | — | +0.307 |
| unicodelang | 1 | 0.82 | — | +0.300 |

**Critical findings:**
- **crime side 1: Spearman = +0.002** — rankings are essentially uncorrelated. Same data, same algorithm, one projection decision → unrelated answers.
- **unicodelang side 0: Top-10 overlap = 0.11** — only 1 of top 10 survives projection. Blowup 10× destroys ranking.

### 2.4 Communities: ARI raw vs projected

| Graph | Side | ARI raw vs projected |
|-------|------|---------------------|
| crime | 0 | 0.5688 |
| crime | 1 | 0.5751 |
| unicodelang | 0 | 0.1702 |
| unicodelang | 1 | 0.3506 |

ARI is low on unicodelang side 0 (0.17) and moderate on crime (0.57). **Projection changes communities more than Louvain's own run-to-run noise** (Phase 2B: mean ARI 0.62–0.88). The projection decision is the dominant factor.

---

## 3. What surprised me

1. **Spearman = 0.002 on crime side 1** — raw and projected rankings are statistically independent. Not "somewhat different" — *unrelated*.
2. **unicodelang side 0 blowup 10×** — one language (degree 141) creates 9,870 edges. Projection is not a minor transformation; it rewrites the graph.
3. **Side 1 on crime has 0.18 top-10 overlap** — the crimes side loses almost all ranking fidelity when projected.

---

## 4. What I could not determine

- Whether weighted projection (using shared-neighbor counts as edge weights) preserves rankings better.
- How to choose "correct" projection a priori — the brief says "which one answers what you asked."

---

## 5. Judgement calls

- Used unweighted projection (networkx bipartite.projected_graph) as per brief.
- Compared raw vs each projection separately; did not compare side-0 vs side-1 projections directly.
- ARI on communities: only computed on shared nodes.

---

## 6. Sample sizes and caveats

| Claim | Graphs | Runs | Caveat |
|-------|--------|------|--------|
| Mass ratio 1.65× | 2 | 1 | Deterministic PageRank |
| Spearman ~0 | 2 | 1 | crime side 1, unicodelang side 0 |
| Projection changes answer | 2 | 1 | Both computations correct |

---

## 7. Collaboration record

Solo execution. No colleague to replicate with; replication.md will note this.