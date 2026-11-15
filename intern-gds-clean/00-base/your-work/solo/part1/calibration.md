# Part 1 Calibration — solo

**Machine:** macOS-15.7.7-arm64-arm-64bit | 10 cores | 16.0 GB RAM  
**Python:** 3.10.20 | networkx 3.4.2 | igraph 1.0.0 | leidenalg 0.12.0 | numpy 2.2.6 | scipy 1.15.3 | pandas 2.3.3 | matplotlib 3.10.9

---

## Cross-Machine Comparison

**Note:** This project is being executed solo. There is no colleague's machine to compare against. The calibration exercise described in the brief (comparing absolute times, ratios, and iteration counts across two machines) cannot be performed.

However, the following observations are recorded for reproducibility:

### Iteration Counts (should be deterministic across machines)

| Graph | Iterations (all 10 runs) |
|-------|--------------------------|
| lesmis | 37 |
| unicodelang | 67 |
| email-Eu-core | 14 |
| crime | 54 |
| openflights | 40 |
| facebook_combined | 21 |
| ca-GrQc | 41 |

All 7 graphs produced identical iteration counts across all 10 runs.

### Ratio Analysis (single-machine)

Since we cannot compare machines, we analyze the ratios between graphs on this single machine:

| Ratio | Value | Interpretation |
|-------|-------|----------------|
| facebook_combined / ca-GrQc (compute_s) | 1.90x | facebook_combined is ~2x slower despite 23% fewer nodes |
| ca-GrQc / facebook_combined (nodes) | 1.29x | ca-GrQc has 29% more nodes but is faster |
| openflights / email-Eu-core (compute_s) | 4.51x | openflights 4.6x slower despite similar node count |
| email-Eu-core / lesmis (compute_s) | 16.12x | email-Eu-core 16.1x slower with 12.8x more nodes |

### What Survives a Change of Machine

From the brief's framing:

> Someone reports "this took 86 seconds". Someone else reports "this took twice as long as the other graph". **Six months from now, which of those two statements is still useful, and why?**

**Answer:** The ratio statement survives. Absolute times are hardware-dependent; ratios between graphs on the *same* machine are algorithmic properties (driven by graph shape — degree skew, component structure, clustering). Iteration counts are completely deterministic and should match exactly across any machine running the same code with the same convergence tolerance.

---

## Summary

- **Absolute compute times:** Not comparable across machines (hardware-dependent)
- **Ratios between graphs:** Stable across machines; driven by graph topology
- **Iteration counts:** Identical across machines (deterministic algorithm)
- **All 7 graphs × 10 runs:** Produced identical scores (scores_hash matched within each graph)

**Recommendation for future multi-machine runs:** If a colleague runs this pack, compare their `pagerank_runs.csv` against this one. Check: (1) iteration counts match exactly, (2) compute-time ratios between graphs agree within ~10%, (3) any graph with non-identical scores across runs is flagged.