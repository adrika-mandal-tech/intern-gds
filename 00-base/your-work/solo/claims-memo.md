# Claims Memo — solo

**Date:** 2026-09-10  
**Status:** 1 of 12 claims verified; 11 pending primary-source research

---

## Summary

| Claim ID | Topic | Verdict | Grade | Evidence |
|----------|-------|---------|-------|----------|
| C01 | Community detection | REJECTED | Production | Our measurement: 0–0.43% disconnected vs claimed 16% |
| C02 | Graph-augmented retrieval | PENDING | Research | Requires primary-source verification |
| C03 | Industrial deployment | PENDING | Research | Requires primary-source verification |
| C04 | Industrial deployment | PENDING | Research | Requires primary-source verification |
| C05 | Industrial deployment | PENDING | Research | Requires primary-source verification |
| C06 | Graph-augmented retrieval | PENDING | Research | Requires primary-source verification |
| C07 | Construction quality | PENDING | Research | Requires primary-source verification |
| C08 | Memory and representation | PENDING | Research | Requires primary-source verification |
| C09 | Scaling | PENDING | Research | Requires primary-source verification |
| C10 | Algorithm detail | PENDING | Research | Requires primary-source verification |
| C11 | Link prediction | PENDING | Research | Requires primary-source verification |
| C12 | When graphs help | PENDING | Research | Requires primary-source verification |

---

## C01 — Louvain Disconnected Rate (REJECTED)

**Claim:** Louvain produces communities that are internally disconnected at rates up to 16%, and badly connected at rates up to 25%.

**Primary Source:** Traag, Waltman & van Eck (2019) — "Louvain" paper

**Our Measurement:**
- Disconnected rate: 0% on 4/5 graphs, max 0.43% on openflights
- Fragile rate (badly connected proxy): 12.9%–85.8% depending on graph
- Leiden: 0% disconnected on all 5 graphs

**Verdict:** REJECTED. The 16% claim is not reproduced on our 5 graphs. Our max disconnected rate is 0.43% (openflights), which is 37× lower than the claimed 16%.

**Why the discrepancy?** The published claim may reflect different graph types, different Louvain implementations, or different community size thresholds. Our measurement uses networkx Louvain with default parameters on 5 real-world graphs.

**Grade:** Production — this is a claim about algorithm behavior that we measured directly.

---

## C02–C12 — Pending Research

These claims require manual primary-source research:
1. Locate the primary source (paper, documentation, blog post)
2. Find the exact quote or data point
3. Verify it says what is claimed
4. Record verdict and grade

**Current status:** All 11 claims are scaffolded with topic, claim text, and context, but evidence, verdict, and grade are not yet filled.

**Next steps:**
- C02: Find HippoRAG paper (NeurIPS 2024) and verify 89.1% vs 68.2% recall numbers
- C03: Find LinkedIn paper (arXiv 2404.17723 / SIGIR 2024) and verify 28.6% reduction
- C04: Find Pinterest / PinSage paper (KDD 2018) and verify 25-30% engagement improvement
- C05: Find Airbnb engineering blog post and verify 7B nodes, 11B edges, 5M edges/day
- C06: Find Microsoft GraphRAG paper (arXiv 2404.16130) and verify 72-83% preference
- C07: Find published evaluation of graph construction quality and verify 66% entity presence
- C08: Find benchmarking write-up comparing graph libraries and verify 9GB vs 14GB vs 93GB
- C09: Find original Louvain paper and verify "scales to millions of nodes" claim
- C10: Find PageRank textbook or documentation and verify damping factor 0.85 claim
- C11: Find link-prediction literature and verify Adamic-Adar claim
- C12: Find published evaluation comparing graph-augmented and standard retrieval

---

*End of claims memo. See claims.jsonl for structured claim records.*
