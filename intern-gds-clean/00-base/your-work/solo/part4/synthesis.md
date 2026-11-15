# Synthesis — solo

## Every claim

| # | Claim | Whose | Graphs | Runs | Confidence |
|---|-------|-------|--------|------|------------|
| 1 | PageRank compute time correlates most strongly with node count (Spearman +0.964); degree skew is the weakest predictor (+0.357) | solo | 7 | 70 | High |
| 2 | Iteration counts are portable across machines; absolute times are not | solo | 7 | 70 | High |
| 3 | Degree ≈ PageRank (mean ρ=+0.916); PageRank ≠ Closeness (mean ρ=+0.454) | solo | 5 | 5 | High |
| 4 | Top-10 overlap can be 1.0 while ρ < 0.9 (unicodelang trap) | solo | 1 | 1 | High |
| 5 | Betweenness cost scales with V×E; 17s on openflights | solo | 3 | 3 | High |
| 6 | 10% sample suffices for top-10 on openflights; 25% needed on ca-GrQc | solo | 3 | 150 | Medium |
| 7 | Ignoring weights on openflights: 90% routes differ, median 1.16× penalty | solo | 1 | 500 | High |
| 8 | Louvain produces distinct partition every run (200/200 on 4 graphs) | solo | 5 | 1000 | High |
| 9 | Modularity spread tiny (0.2–3.6%) despite partition instability | solo | 5 | 1000 | High |
| 10 | Disconnected communities near-zero (≤0.41%) vs published 16% claim | solo | 5 | 500 | High |
| 11 | Leiden fixes disconnected (0% vs ≤0.41%); fragile mixed | solo | 5 | 500 | Medium |
| 12 | Best modularity ≠ best ground truth on email-Eu-core | solo | 1 | 100 | High |
| 13 | Similarity misses bridges: on email-Eu-core, 70% of top-1% bridge edges have zero Jaccard similarity against a base rate of 1.8% (39× enrichment). crime is bipartite so 100% is the base rate, not a finding. | solo | 2 | — | High |
| 14 | Projection changes rankings (Spearman ~0 on crime side 1) | solo | 2 | 1 | High |
| 15 | PageRank mass sink: crimes (1.23×), territories (1.65×) | solo | 2 | 1 | High |
| 16 | Projection blowup up to 10× (unicodelang side 0) | solo | 2 | 1 | High |

Sample sizes recorded in every row above.

---

## Replication status

| Claim | Status | Notes |
|-------|--------|-------|
| PageRank determinism | replicated | Self-replication: 7/7 iteration counts match (n=140 runs) |
| Louvain repeatability | not attempted | No colleague |
| Betweenness approximation | not attempted | No colleague |
| Projection effects | not attempted | No colleague |

**Most claims: not attempted** — solo execution. Self-replication of Phase 1 confirmed determinism (n=140 runs).

---

## What we would do differently

1. **Start claims strand earlier** — C01 (Louvain disconnected) measured in Phase 3B but claim verification should have started in Phase 1. The delay meant reading the source after seeing our data, risking confirmation bias.

2. **Run `--full` flag on Phase 3A** — facebook_combined (densest graph) would test whether the 10%/25% sampling thresholds hold on larger, denser graphs.

3. **Weighted Louvain/Leiden in Phase 3B** — all experiments used unweighted graphs. openflights has distance weights (cost), lesmis has scene counts (strength). Weighted community detection could change fragile/disconnected rates.

4. **More seeds for Leiden-Louvain comparison** — 50 seeds may be within Phase 2B noise (ARI 0.62–0.88). 200 seeds on fastest graphs would clarify if Leiden's disconnected fix is statistically significant.

5. **Temporal split for link prediction (bench B4)** — no timestamps in data, but structural substitutes (degree-biased, component-aware) should be tested against random split.

6. **PageRank undirected claim (bench B5)** — the context document claims "PageRank on undirected tells you nothing degree doesn't." Our Phase 2A data (degree vs PageRank ρ=+0.916) supports this but we didn't formally test the claim.

7. **Document judgement calls in real-time** — several decisions (unweighted graphs, denominator choices, "reliable" thresholds) were made ad-hoc. Recording them immediately would improve memo quality.

---

## What the next person should do first

1. **Read claims.jsonl and verify C01 against Traag et al. 2019** — our 0.41% max disconnected vs published 16% is the most interesting discrepancy.
2. **Run bench B3 (resolution limit)** — can Louvain find small planted communities? This directly connects to Phase 3B quality findings.
3. **Test weighted projection** — does `bipartite.weighted_projected_graph` preserve rankings better than unweighted?
4. **Run Phase 3A with `--full`** — validate sampling thresholds on facebook_combined.