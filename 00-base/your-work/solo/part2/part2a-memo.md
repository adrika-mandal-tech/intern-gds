# Part 2A — Do the four centrality measures agree?

**Who:** solo  
**Machine:** macOS-15.7.7-arm64-arm-64bit | 10 cores | 16.0 GB RAM  
**Dates:** 2026-09-04 to 2026-09-04  
**Results files:** centrality_scores.csv, centrality_agreement.csv, centrality_cost.csv, disagreements.csv

---

## 1. What I did

Ran four centrality measures (degree, PageRank, closeness, betweenness) on 5 graphs (lesmis, unicodelang, crime, email-Eu-core, openflights) using `python part-2/run_part2a.py --who solo`. Each graph loaded unweighted; directed graphs converted to undirected. Computed pairwise Spearman correlation and top-10 overlap for all 6 measure pairs per graph. Recorded computation cost per measure. Identified top 5 nodes with largest degree-vs-betweenness rank gap per graph.

---

## 2. What I found

### 2.1 Degree vs PageRank: Strongest agreement overall

Across 5 graphs, degree vs PageRank had mean Spearman ρ = +0.916 (range +0.864 to +0.994) and mean top-10 overlap = 0.80 (range 0.54 to 1.00). On email-Eu-core they are nearly identical (ρ=+0.994, top-10=0.82). On unicodelang they agree on the top-10 (overlap = 1.00) despite high ρ (+0.864) — the bipartite structure causes high correlation but the top nodes are the same.

### 2.2 PageRank vs Closeness: Weakest agreement overall

Across 5 graphs, mean Spearman ρ = +0.454 (range +0.023 to +0.928). On crime ρ=+0.023 (near zero) and top-10 overlap=0.18 — the two measures disagree almost completely. On email-Eu-core they agree well (ρ=+0.928). The spread is the finding, not the average.

### 2.3 The unicodelang trap: High ρ, low top-10 overlap

On unicodelang, degree vs betweenness has ρ=+0.984 but top-10 overlap=0.43. This happens because the bipartite graph has a few very high-degree nodes that dominate the ranking, but the tail ordering differs. If you only need the top-10, correlation alone misleads.

### 2.4 Cost scaling

- Degree: ~0.000s on all graphs (trivial)
- PageRank: 0.001s (lesmis) to 0.011s (openflights) — scales with edges
- Closeness: 0.001s (lesmis) to 4.18s (openflights) — all-pairs shortest paths
- Betweenness: 0.006s (lesmis) to 17.2s (openflights) — Brandes algorithm O(VE)

Openflights betweenness (3,214 nodes) takes 17s vs email-Eu-core (986 nodes, 24,929 edges) at 3s — betweenness scales closer to V×E than E alone.

### 2.5 Named disagreements

| Graph | Node | Degree rank | Betweenness rank | Gap | Direction |
|-------|------|-------------|------------------|-----|-----------|
| lesmis | 60 | 24 | 69 | 45 | degree ranks it higher |
| unicodelang | 8 | 325 | 142 | 183 | betweenness ranks it higher |
| crime | 1053 | 30 | 580 | 550 | degree ranks it higher |
| email-Eu-core | 414 | 670 | 52 | 618 | betweenness ranks it higher |
| openflights | 815 | 809 | 3122 | 2313 | degree ranks it higher |

On email-Eu-core, node 414 has low degree but sits on many shortest paths between departments — a structural broker.

---

## 3. What surprised me

1. **PageRank vs closeness on crime (ρ=+0.023)** — near-zero correlation on a bipartite graph. PageRank flows across sides; closeness is trapped in components.
2. **Top-10 overlap can be 1.0 while ρ < 0.9** — unicodelang degree vs PageRank: ρ=+0.864 but top-10=1.00. The top nodes are the same; the tail differs.
3. **Betweenness on openflights (17s) vs email-Eu-core (3s)** — openflights has more edges (18,858 vs 16,064) and 3.2x nodes. Betweenness scales closer to V×E than E alone.

---

## 4. What I could not determine

- Whether the degree-PageRank agreement on email-Eu-core (ρ=+0.994) is due to the graph being nearly regular or the directed→undirected conversion. Would need to test on directed version.
- Exact extrapolation of betweenness cost to 30,000 nodes — only 5 data points, different shapes. Linear in edges? Quadratic? Cannot say confidently.

---

## 5. Judgement calls

- Used unweighted graphs for all 5 (per brief). openflights weights are distances (cost); lesmis weights are scene counts (strength). Mixing would confuse comparison.
- Top-5 disagreements per graph (not top-10) as specified in brief.
- Averaged Spearman across graphs for "most/least agreement" but reported per-graph spread — the variation is the finding.

---

## 6. Sample sizes and caveats

| Claim | Graphs | Runs | Caveat |
|-------|--------|------|--------|
| Degree≈PageRank | 5 | 1 | Single run per graph; deterministic |
| PageRank≠Closeness | 5 | 1 | crime ρ=+0.023 is extreme; component structure |
| Cost scaling | 5 | 1 | Only 5 points; shapes differ |

---

## 7. Collaboration record

Solo execution. No colleague to compare with. All code from provided runners.