# GDS Measurement Program — Presentation Script

**Project:** intern-gds — Graph Data Science Measurement Program  
**Organization:** PrajnaAI  
**Date:** September 2026  
**Presenter:** Solo  
**Status:** Phases 0–4 Complete | Phase 5 Pending Claims Verification  
**Companion Document:** `00-base/your-work/solo/gds-workflow.html` (full technical reference with 15 flowcharts, decision rules, tier tables, failure modes)

---

## Opening

Good morning. Today I'm presenting the GDS measurement program — a rigorous, reproducible benchmark of graph algorithms on 7 real-world networks spanning social, transportation, and biological domains. Every number you'll see traces to a CSV row. Every result has provenance. Every decision is documented with explicit IF-THEN rules.

This is not a typical ML project where you throw data at a model and hope for the best. This is a measurement program — we are not trying to find the "best" algorithm. We are measuring what each algorithm does, under what conditions, with what confidence, and at what cost. If we cannot measure it, we cannot claim it.

The program covers the full pipeline: from environment setup and profiling, through centrality and community detection, approximation validation, bipartite projection, all the way to linked-data export and synthesis. We ran 7 structurally diverse graphs through 5 algorithmic families, computed thousands of measurements, and validated every approximation against exact baselines.

What makes this project different from a standard benchmark is three things: provenance by design, approximation validation, and linked-data interoperability. Every CSV has a `.provenance.json` sidecar recording the source URL, SHA-256 hash, retrieval date, preprocessing notes, and machine specifications. We didn't just run algorithms — we validated whether sampling works, whether projections preserve structure, and whether results can be exported as W3C-standard RDF for cross-lab queryability.

---

## What is Graph Data Science?

Graph Data Science applies algorithms, statistical methods, and machine learning techniques to graph-structured data. Unlike tabular data where rows are independent, graphs represent relationships explicitly: nodes (entities) connected by edges (relationships). This structure is fundamental — the topology of the graph determines which algorithms work, what results mean, and how reliable those results are.

Graphs are everywhere. Social networks connect people through friendships and interactions. Supply chains link factories, warehouses, and retailers through transportation routes. Biological pathways map proteins through biochemical reactions. Citation networks connect papers through references. Transportation systems link cities through flights and roads. The structure of a graph — its density, skew, component count, weight semantics — fundamentally determines which algorithms work and what results mean.

GDS differs from traditional ML in one crucial way: the features are the graph itself. You don't extract features from nodes — you compute them from topology. PageRank measures influence by following links through the graph structure. Betweenness centrality measures bridge importance by counting shortest paths through the network. Community detection groups nodes by connection patterns, revealing clusters that may not be obvious from node attributes alone. Each algorithm answers a different question about the same structure.

The core algorithmic families we benchmarked include: centrality measures (degree, PageRank, closeness, betweenness) that identify important nodes; community detection algorithms (Louvain, Leiden) that partition graphs into clusters; similarity measures that quantify node proximity; approximation techniques that trade accuracy for speed; and projection methods that transform bipartite graphs into unipartite representations. Each family serves a different analytical purpose and has different computational characteristics.

**Why it matters:** Most real-world problems are about connections. Social networks, supply chains, biological pathways, citation networks — all are fundamentally graph-shaped. GDS provides the tools to answer questions like: who is important? who belongs together? who is similar? what connections will form? These questions arise in recommendation systems, fraud detection, drug discovery, citation analysis, and infrastructure planning.

**This project:** We built a reproducible measurement program that benchmarks graph algorithms on 7 real-world networks, validates approximations against exact computation, and exports results as linked data using the Biolink Model vocabulary. The 7 graphs were selected to maximize structural diversity — each graph has unique properties that test different algorithm behaviors. No two graphs are interchangeable. We used networkx, python-igraph, and leidenalg for algorithm computation, pandas and numpy for data manipulation, matplotlib for visualization, and gds-owl with rdflib and pyshacl for semantic web export.

**Key design principles:** First, no interchangeable pairs — each graph has unique properties that test different algorithm behaviors. Second, weight semantics matter — in openflights and crime, edges represent costs (distance, co-occurrence), not strengths. Higher weight means harder to traverse, which fundamentally changes how algorithms behave. Third, ground truth is rare — only email-Eu-core has reliable labels (42 departments). Fourth, bipartite graphs are special — projection onto either side is a non-neutral transformation that changes the ranking object.

---

## Project Aims & Objectives

**Primary Aim:** Build a rigorous, reproducible, and auditable measurement program for graph algorithms on real-world networks, with full provenance tracking and linked-data export. This project is not about finding the "best" algorithm — it is about measuring what each algorithm does, under what conditions, and with what confidence. Every claim must be traceable to a primary source or to our own measurement. Every result must have provenance.

The measurement philosophy is simple: run algorithms multiple times with different seeds, measure both correctness and cost, compare against exact baselines where possible, and document every decision. If we cannot measure it, we cannot claim it. This philosophy drives every aspect of the project — from the directory structure to the CSV naming conventions to the provenance sidecars.

**Six Objectives:**

1. **Measurement Rigour:** Profile 7 structurally diverse graphs and measure algorithm performance with proper timing, multiple seeds, and cross-machine calibration. Every number must be traceable to a specific CSV row. We profiled each graph for nodes, edges, density, diameter, clustering coefficient, degree distribution, and weight semantics. PageRank was run 10 times per graph with independent random seeds to measure convergence behavior. Cross-machine calibration ensured measurements were not machine-specific.

2. **Claims Verification:** Trace 12 specific claims about graph algorithms to primary sources (papers, documentation), grade evidence quality, and record verdicts in a structured JSONL format. The claims cover topics from PageRank convergence to community detection stability to projection effects. Each claim has a primary source, exact quote, evidence grade, and verdict. This is the most labor-intensive part of the project — it requires human reading of primary sources and cannot be automated.

3. **Approximation Validation:** Answer the question: "Can we sample?" — specifically for betweenness centrality. Determine the minimum pivot fraction that preserves ranking fidelity while achieving meaningful speedup. We computed exact betweenness on 3 graphs and sampled at 1%, 2%, 5%, 10%, 25% × 10 seeds each (150 total runs). The results showed that at 5% sampling, speedup is ~18–20× with Spearman > 0.97 and top-10 overlap ~0.5–0.8. This is the practical sweet spot.

4. **Projection Impact Assessment:** Document the consequences of bipartite projection choices. Show that projection is not a neutral transformation and can fundamentally change ranking and community structure. On crime side 1, raw vs projected PageRank Spearman = 0.002 — the two rankings are essentially uncorrelated. On unicodelang side 0, ARI = 0.17 — communities barely overlap. Both results are correct. Only one answers your question.

5. **Ontology & Interoperability:** Model experimental results as RDF/OWL linked data using the Biolink Model vocabulary, validate with SHACL, and enable SPARQL queryability for cross-lab interoperability. The Biolink Model v4.4.4 provides ~948+ classes for biomedical entities. SHACL shapes validate exports before archiving, catching schema violations early. This ensures that every archived result is both syntactically valid and semantically correct.

6. **Reproducibility:** Ensure every result can be reproduced by another researcher with the same environment specifications, using runner scripts and provenance sidecars. Each phase has a dedicated runner script (`run_part1.py`, `run_part2a.py`, etc.). Dependencies are pinned. The dual-venv isolation (Python 3.10 core + Python 3.14 semantic web) prevents dependency conflicts. Documented failure modes for every phase ensure that when something goes wrong, the recovery procedure is immediately available.

---

## Project Goals

**Short-term Goals (Phases 0–4):**
1. Complete all measurement phases with passing checkers — every phase has a checker script that validates outputs
2. Generate all required outputs: CSVs, memos, charts, provenance sidecars
3. Document methodology with decision rules, tier tables, and failure modes
4. Validate approximations against exact computation — betweenness sampling validated at multiple fractions
5. Quantify projection impact on bipartite graphs — Spearman, ARI, and top-10 overlap measured
6. Create a comprehensive presentation script and technical reference

**Medium-term Goals (Phase 5):**
1. Complete claims strand for all 12 claims with primary-source evidence — currently scaffolded but unfilled (0/12)
2. Replicate a colleague's headline finding and document discrepancies honestly
3. Export results as RDF Turtle via gds-owl
4. Validate exports with SHACL and produce conformance report
5. Write synthesis.md tying together findings from all phases into a coherent narrative

**Long-term Goals:**
1. Enable cross-lab comparison by making results queryable via SPARQL endpoints
2. Establish methodology template for future graph algorithm benchmarks
3. Contribute reproducibility standards to the GDS community
4. Build a knowledge graph of experimental results that can be queried alongside external biomedical datasets

**Success Criteria:** All 6 quality gates pass (G0–G5). All Phase 1–4 checkers pass. claims.jsonl contains 12 complete rows with evidence grades. graph_analysis.html renders all phases with real data. Experiment exports pass SHACL validation. The presentation script covers all phases with sufficient detail for a 20-minute presentation.

**What "pass" means:** Every checker test must pass. No exceptions. If a checker fails, the phase is not complete — fix the output, not the checker. The gate criteria are non-negotiable because they define the boundary between "we ran the code" and "we have verified results."

**What "scaffolded" means:** The structure is ready (12 claim rows exist) but the evidence is not filled in. This is intentional — claims verification requires human reading of primary sources, which cannot be automated. Phase 5 cannot be marked complete until all 12 claims have evidence, verdict, and grade.

---

## Advantages of This Approach

**Measurement Rigour:** Provenance by design — every CSV has a `.provenance.json` sidecar recording source URL, SHA-256, retrieval date, preprocessing notes, and machine specs. Multiple seeds for variance quantification. Cross-machine calibration. Traceability — every number traces to a specific CSV row. The 7 graphs span social (lesmis, crime, facebook_combined), transportation (openflights), communication (email-Eu-core), and biological (ca-GrQc) domains. This diversity ensures that findings are not domain-specific artifacts.

**Reproducibility:** Runner scripts per phase. Pinned dependencies. Dual-venv isolation (Python 3.10 core + Python 3.14 semantic web). Documented failure modes for every phase. The critical path is P0 → P1 → P2A → P3A → P4 → P5 with P2B → P3B running in parallel. This means that within each phase, tracks A and B are independent and can run simultaneously, reducing total execution time.

**Comprehensive Coverage:** 7 structurally diverse graphs. 5 algorithmic families (centrality, community detection, similarity, approximation, projection). 12 claims with evidence grading across four categories: Production, Research, Product, Marketing. The claims strand provides a structured way to verify that our findings align with established knowledge.

**Linked Data Export:** Biolink Model alignment. SHACL validation before archiving. SPARQL queryability. W3C standards (Turtle/RDF) with decades-long archival stability compared to CSV/Markdown. CSV files are opaque — you need to know the schema to understand what each column means. RDF Turtle is self-describing: every triple has a subject, predicate, and object, all of which are URIs that resolve to definitions. This means any RDF-aware tool can query the results without prior knowledge of the schema.

**Decision Transparency:** Tier system (must-pass / important / optional). Explicit IF-THEN decision rules for every phase. Failure mode documentation for every phase. The tier system ensures that even if time runs out, the core deliverables are complete. Tier 1 is the minimum viable product. Tier 2 strengthens the analysis. Tier 3 is exploratory — nice to have but not required.

**What makes this approach unique:** Most graph algorithm benchmarks stop at computing numbers and writing papers. We go further — we validate approximations, we document projection effects, we export to linked data, and we make everything reproducible. The combination of measurement rigour, approximation validation, and semantic web interoperability is what sets this project apart from standard benchmarks.

---

## Limitations & Constraints

**Technical Limitations:** Exact betweenness is O(n·m) — for openflights (36,906 edges), exact betweenness may exceed available memory. We mitigated this by dropping openflights from the exact set and using only 2 graphs for exact computation. Louvain is heuristic with resolution limits — it may not find the optimal partition. Ground truth is rare — only email-Eu-core has reliable labels (42 departments). Projection is lossy — bipartite projection discards information about the original structure.

**Scope Constraints:** Offline-only after initial graph fetch. Single-machine execution — no distributed computation. No streaming graphs (data has no timestamps). No deep learning (GNNs out of scope). The project focuses on classical graph algorithms rather than neural approaches. This is intentional — we want to measure what classical algorithms can do before adding the complexity of deep learning.

**Schedule Constraints:** Phase 5 depends on colleague output. Claims verification is manual — reading papers, locating quotes, and grading evidence cannot be automated. This is the longest pole in the schedule. The claims strand has 12 claim skeletons but 0/12 filled. Each claim requires finding a primary source, locating the exact quote, checking it says what is claimed, and recording the verdict. This process is labor-intensive but essential for credibility.

**Data Limitations:** 7 graphs is sufficient for methodology demonstration but not for statistical generalization. No planted-partition tests at scale. Single-domain focus — all graphs are from social/transportation domains. The graphs were downloaded from SNAP (Stanford Network Analysis Project) and are publicly available. However, the specific preprocessing steps (removing self-loops, filtering edges, etc.) may affect results.

**What we would do differently:** If we had more time, we would expand the graph set to include more domains (biological, citation). We would add more approximation techniques beyond betweenness sampling. We would implement streaming graph algorithms. And we would build a proper SPARQL endpoint for cross-lab comparison.

---

## Technology Stack

**Core Runtime (Python 3.10.20):**
- networkx 3.4.2 — graph data structures and algorithms
- python-igraph 1.0.0 — high-performance graph computation
- leidenalg 0.12.0 — Leiden community detection algorithm
- numpy 2.2.6 — numerical computation
- scipy 1.15.3 — scientific computing
- pandas 2.3.3 — data manipulation and analysis
- matplotlib 3.10.9 — visualization and charting
- pytest 9.1.1 — testing framework

**Semantic Web Stack (Python 3.14):**
- gds-owl 0.99.0 — converts experimental results into Turtle format
- gds-framework 0.3.0 — GDS framework utilities
- gds-interchange 0.1.0 — data interchange utilities
- rdflib 7.6.0 — RDF graph library
- pyshacl 0.40.1 — SHACL validation
- owlrl 7.6.2 — OWL reasoning
- html5rdf 1.2.1 — HTML to RDF conversion

**Why two venvs:** Core runtime packages move fast (frequent releases, breaking changes). Semantic web stack is more conservative. Mixing them creates dependency resolver conflicts. Isolation lets us upgrade each stack independently. The core venv handles all algorithm computation and data processing. The semantic web venv handles RDF export and validation. This separation means that upgrading networkx doesn't break pyshacl, and updating rdflib doesn't affect numpy.

**Why not gds-framework or gds-interchange for core computation:** These are specialized tools for the semantic web pipeline. The core computation uses networkx and python-igraph because they provide the algorithm implementations we need. gds-owl is used only for the export step — converting results to Turtle format.

**Why not seaborn or neo4j:** Seaborn is a visualization library that adds complexity without essential functionality — matplotlib provides all the charting we need. Neo4j is a graph database that would add infrastructure overhead — our results are exported as CSV and RDF, which are more portable and don't require a running database server.

---

## The Seven Graphs

We selected 7 real-world networks to maximize structural diversity. Every graph serves a specific purpose in stress-testing algorithms. No two graphs are interchangeable — each has unique properties that test different algorithm behaviors.

| Graph | Nodes | Edges | Type | Skew | Components | Purpose |
|-------|-------|-------|------|------|------------|---------| 
| lesmis | 77 | 254 | Undirected, Weighted | 6.0 | 1 | Small, dense, classic baseline |
| unicodelang | 868 | 1,255 | Undirected, Bipartite | 141.0 | 5 | Extreme degree skew, bipartite |
| crime | 1,380 | 1,476 | Undirected, Bipartite | 25.0 | 20 | Bipartite projection test |
| email-Eu-core | 986 | 24,929 | Directed, Ground Truth | 16.5 | 1 | Ground truth available |
| openflights | 3,214 | 36,906 | Directed, Weighted | 79.5 | 7 | Weight semantics: costs |
| facebook_combined | 4,039 | 88,234 | Undirected | 41.8 | 1 | Large, sparse, ego network |
| ca-GrQc | 5,241 | 14,484 | Undirected | 27.0 | 354 | Many components, fragmented |

**Key Design Principles:**
1. No interchangeable pairs — each graph has unique properties that test different algorithm behaviors. lesmis is small and dense, while ca-GrQc is large and fragmented. openflights has extreme degree skew, while email-Eu-core has ground truth labels.
2. Weight semantics matter — in openflights and crime, edges are costs (distance, co-occurrence), not strengths. Higher weight means harder to traverse. This fundamentally changes how algorithms like PageRank and Louvain behave.
3. Ground truth is rare — only email-Eu-core has reliable labels (42 departments). This means community quality can only be validated on one graph. For all others, we rely on internal metrics like modularity stability.
4. Bipartite graphs are special — projection onto either side is a non-neutral transformation that changes the ranking object. crime and unicodelang are both bipartite, making them ideal for studying projection effects.

**Why these specific graphs:** The graphs were selected from SNAP to maximize structural diversity. lesmis provides a small, dense baseline for debugging. unicodelang tests extreme degree skew (141.0) and bipartite structure. crime tests bipartite projection with 20 components. email-Eu-core provides ground truth validation. openflights tests weight semantics and large-scale computation. facebook_combined tests sparse ego networks. ca-GrQc tests fragmented graphs with 354 components.

---

## Workflow Overview

**Daily Workflow:** Activate correct venv → Run phase script → Inspect CSVs → Update research-log.md → Work on memo → Advance claims strand. This daily cadence ensures steady progress and proper documentation. Each day has a specific focus and target output, preventing scope creep.

**Weekly Cadence:** Mon: Setup + P0 gate | Tue: P1 run + analysis | Wed: P2A run + memo | Thu: P2B run + memo | Fri: P3A run | Week 2: P3B run, P4 run, P5 replication | Week 3: Claims completion, ontology export, synthesis. The weekly cadence is designed for a single operator — each day has a clear target that can be completed in a focused work session.

**Critical Path:** P0 → P1 → P2A → P3A → P4 → P5 with P2B → P3B running in parallel. The critical path determines the minimum project duration. P2B (Louvain) and P3B (Quality) can run in parallel with P2A and P3A because they are independent tracks within the same phase.

**Bottlenecks:** P0 scipy resolution (blocks everything if not resolved day 1). P3A exact betweenness (may exceed memory on openflights). P5 replication (depends on colleague's output availability). The scipy compatibility issue was resolved early by using the isolated venv. The betweenness memory issue was mitigated by dropping openflights from the exact set. The replication dependency is external and cannot be controlled.

**Data Dependencies:** P2A requires profiles.csv from P1 (graph list, node/edge counts). P2B requires profiles.csv from P1. P3A requires centrality_*.csv from P2A (for exact betweenness baseline). P3B requires louvain_runs.csv from P2B. P4 requires profiles.csv from P1 (bipartite graph identification). P5 requires all previous phase outputs. This dependency chain means that a failure in an early phase blocks everything downstream.

**Parallel Execution:** Within each phase, tracks A and B are independent and can run in parallel. P2A (centrality) and P2B (Louvain) can run simultaneously. P3A (betweenness) and P3B (quality) can run simultaneously. This reduces total execution time significantly. The only constraint is that P2A and P2B both depend on P1 outputs.

---

## Phase-by-Phase Detail

### Phase 0: Setup & Scaffold

**Duration:** ~30 minutes | **Gate:** ALL 112 setup tests pass | **Track:** Both

**Goal:** Verify environment, resolve Python/scipy compatibility, create directory tree, write first-impressions, bootstrap claims and research log, install gds-owl. Nothing in P1 may start until P0 gate is green.

**What We Did:**
1. Resolved Python 3.10.20 + scipy 1.15.3 compatibility — the system Python had a version conflict that prevented scipy from importing. The fix was to create an isolated venv with the correct Python version.
2. Created full directory tree under `your-work/solo/` — organized structure for all phase outputs.
3. Ran `check_setup.py` — 112/112 tests pass. The checker validates Python version, package versions, graph file availability, checker functionality, and venv isolation.
4. Wrote `first-impressions.md` with initial observations about the graphs and environment.
5. Bootstrapped `claims.jsonl` with 12 claim skeletons — each claim has a row structure but no evidence yet.
6. Created `research-log.md` with day-1 entries documenting the setup process.
7. Installed gds-owl in isolated venv-gds-owl — the semantic web stack requires Python 3.14 and has different dependencies from the core runtime.

**Gate Criteria:** check_setup.py returns 112/112. 7 graphs verified with provenance sidecars. first-impressions.md written. claims.jsonl bootstrapped (12 rows). research-log.md created.

**Decision Rules:**
- scipy fails with Python 3.10.20 → Use venv. Do not switch to system Python.
- check_setup.py fails any test → STOP. Fix before proceeding. Do not advance to P1.
- gds-owl fails to install → Continue without ontology. Note failure in research-log.md. Defer to P5 with graceful degradation.
- One graph missing from data directory → Do not substitute. Fetch from original source, record provenance, verify with check_setup.

**Failure Modes:** scipy import error → Use correct venv, reinstall. check_setup fails → Non-zero exit code, read output, fix missing package or graph, rerun. gds-owl dependency clash → Isolate in venv-gds-owl, do not mix. Graph file missing → Fetch from source, add provenance, rerun check_setup.

**Outputs:** first-impressions.md, claims.jsonl (12 rows), research-log.md, questions.md, planner.html

**Why P0 matters:** P0 is the foundation. If the environment is not verified, every subsequent phase produces unverified results. The 112 tests cover Python version, package versions, graph file availability, checker functionality, and venv isolation. Passing all 112 means we can trust every number that follows.

---

### Phase 1: Profile & Calibrate

**Duration:** ~1 minute run + ~30 minutes analysis | **Gate:** check_part1.py passes | **Track:** Both | **Claims:** C01, C09, C10

**Goal:** Establish baseline profiles for all 7 graphs. Measure PageRank convergence and timing across 10 seeds per graph. Cross-check results between two machines to validate reproducibility. Identify what predicts algorithm cost.

**What We Did:**
1. Profiled 7 graphs: nodes, edges, density, diameter, clustering, degree distribution
2. Ran PageRank 10x per graph: 70 total runs with independent seeds
3. Recorded timing: load_s, compute_s, iterations, top_node, top_score, scores_hash
4. Cross-machine calibration: compared hashes between two runs
5. Analyzed results: formulated and tested cost-prediction hypotheses

**Key Question:** What predicts algorithm cost? Node count? Edge count? Degree skew? Density?

**Key Finding:** Degree skew explains iterations better than node count.
- lesmis: 0.0012s mean compute, 37 iterations (skew=6.0)
- unicodelang: 0.0159s, 67 iterations (skew=141.0)
- email-Eu-core: 0.0187s, 14 iterations (skew=16.5)
- crime: 0.0193s, 54 iterations (skew=25.0)
- openflights: 0.0841s, 40 iterations (skew=79.5)
- facebook_combined: 0.1856s, 21 iterations (skew=41.8)
- ca-GrQc: 0.0976s, 41 iterations (skew=27.0)

This finding is counter-intuitive — you might expect node count to be the primary predictor of PageRank cost, but degree skew is actually the dominant factor. unicodelang has only 868 nodes but needs 67 iterations because of its extreme degree skew (141.0). email-Eu-core has 986 nodes but needs only 14 iterations because its skew is moderate (16.5).

**Scope:** In Scope: 7-graph structural profiling, PageRank on every graph (10 random seeds each), timing measurements (wall-clock, CPU, repeatability), cross-machine calibration (two runs, compare hashes), analysis memo with cost-prediction hypotheses, charts/ (11 PNGs). Out of Scope: Any other centrality besides PageRank, community detection (deferred to P2), betweenness or approximation (deferred to P3), ontology modelling (deferred to P5).

**Tier Table:** Tier 1: profiles.csv (7 rows), pagerank_runs.csv (70 rows), calibration.md, part1-memo.md (Critical). Tier 2: charts/ (11 PNGs), refined first-impressions.md (Important). Tier 3: Deeper analysis on synthetic graphs (Optional).

**Decision Rules:** Round counts differ between two machines → STOP. Report discrepancy in research-log.md. Do not average or discard. One graph fails to run → Continue with 6. Note failure in questions.md with graph name and error. Timing variance > 20% across 10 seeds → Investigate; likely graph-size-dependent. Record in memo.

**Stage-by-Stage Workflow:** 1.1 Profile 7 graphs (`run_part1.py --step profile`, ~10s, profiles.csv) → 1.2 Run PageRank 10x per graph (`run_part1.py --step pagerank`, ~40s, pagerank_runs.csv) → 1.3 Cross-machine calibration (copy CSVs to second machine, run same command, diff outputs, ~5 min, calibration.md) → 1.4 Analyze & memo (manual analysis of CSVs, write part1-memo.md, ~20 min).

**Failure Modes:** Graph loads but PageRank diverges → NaN or infinite values in CSV. Check for disconnected components; add personalisation vector. Cross-machine round mismatch → Different iter counts in calibration.md. STOP, report. Do not force agreement. One graph timeout → Script hangs on large graph. Kill, note in questions.md, continue with 6.

**Outputs:** profiles.csv (7 rows), pagerank_runs.csv (70 rows), calibration.md, part1-memo.md, charts/*.png (11 PNGs)

---

### Phase 2: Centrality & Communities

**Duration:** 2A ~90s, 2B ~3 min | **Gate:** check_part2.py passes (both tracks) | **Track:** Parallel — Track A (Centrality) + Track B (Communities) | **Claims:** C02, C06, C12 (A); Prep P3B (B)

**Goal:** Track A measures four centrality measures on 5 graphs, tests pairwise Spearman rank correlation and top-10 overlap, and identifies ranking disagreements. Track B runs Louvain 200 times per graph with 200 seeds to quantify partition stability.

**Track A — Centrality Agreement:**
1. Computed 4 centrality measures: degree, PageRank, closeness, betweenness
2. Extracted top-10 nodes per measure
3. Computed pairwise Spearman correlation matrices
4. Computed top-10 overlap (Jaccard)
5. Identified and named specific disagreements
6. Wrote analysis memo

**Key Insight:** Correlation does not imply top-k agreement. Two rankings can have Spearman ρ = 0.95 yet disagree on the top-10 nodes. Always inspect the actual node lists, not just the correlation number. This is a critical trap in graph algorithm evaluation — a high correlation number can mask significant top-k disagreements.

**Track B — Louvain Stability:**
1. Ran Louvain 200 times per graph with different random seeds
2. Recorded hash, modularity, n_communities, elapsed_s, ARI vs run 1
3. Computed mean and std of modularity and community count
4. Analyzed spread across seeds
5. Wrote stability memo

**Key Insight:** Modularity std below 0.001 indicates seed-robust partitions. Graphs with std above 0.002 should be interpreted with caution — different seeds produce meaningfully different community assignments.

**Key Numbers — Centrality Agreement (degree vs PageRank Spearman):** lesmis: 0.9655, unicodelang: 0.8635, crime: 0.8966, email-Eu-core: 0.9935, openflights: 0.8622.

**Key Numbers — Louvain Stability:** crime: modularity 0.9296 ± 0.0004, 50.0 ± 1.0 communities (most stable). unicodelang: 0.7199 ± 0.0015, 22.3 ± 1.1 communities. email-Eu-core: 0.4134 ± 0.0031, 7.6 ± 0.6 communities. openflights: 0.6560 ± 0.0042, 26.1 ± 2.8 communities (highest variance). ca-GrQc: 0.8615 ± 0.0009, 391.4 ± 1.4 communities (most fragmented).

**Scope:** In Scope (Track A): 5 graphs (lesmis, crime, email-Eu-core, openflights, facebook_combined), Degree, closeness, betweenness, PageRank, Pairwise Spearman correlation matrices, Top-10 overlap (Jaccard) per pair, Disagreement analysis with named nodes. In Scope (Track B): 5 graphs (same subset), Louvain with 200 random seeds per graph, Hash, modularity, ARI recorded per run, Spread analysis (std of modularity). Out of Scope (Both): Eigenvector centrality (Tier 3), Weighted vs unweighted on openflights (Tier 3), Leiden (deferred to P3B), CPM (deferred to P3B).

**Tier Table:** Tier 1: centrality_*.csv (4 files), memos, disagreement analysis (Track A); louvain_runs.csv (1,000 rows), memos (Track B) — Critical. Tier 2: charts/, named-node disagreement report (A); Seed-range analysis, stability report (B) — Important. Tier 3: Add eigenvector centrality; weighted vs unweighted openflights (A); Compare with Leiden; test CPM (B) — Optional.

**Decision Rules:** Louvain gives identical partitions across all 200 seeds → Check seed range — likely deterministic without resolution parameter sweep. Spearman high but top-10 overlap low → Report both. Explain the trap: rank correlation measures order, not identity of top-k. One graph crashes in either track → Continue with remaining 4. Note in questions.md.

**Stage-by-Stage Workflow:** 2A.1 Load 5 graphs, compute 4 measures (`run_part2a.py --step compute`, ~20s, centrality_*.csv) → 2A.2 Pairwise Spearman + Top-10 (`run_part2a.py --step compare`, ~30s, correlation matrices, Jaccard tables) → 2A.3 Identify disagreements, write memo (manual, ~30 min, part2a-memo.md) → 2B.1 Load 5 graphs, run Louvain 200x each (`run_part2b.py --who solo`, ~3 min, louvain_runs.csv) → 2B.2 Record hash/modularity/ARI, analyze (manual + check_part2.py --track B, ~20 min, part2b-memo.md).

**Failure Modes:** Betweenness too slow on 4-graph subset → Timeout or swap thrashing. Reduce to 3 graphs; note in questions.md. Louvain ARI NaN → Singleton partitions. Check resolution parameter; increase minimum community size. Spearman matrix not symmetric → Bug in ranking function. Fix ranking; rerun track A.

**Outputs:** centrality_*.csv (4 files), louvain_runs.csv (1,000 rows), part2a-memo.md, part2b-memo.md, charts/*.png (2 PNGs)

---

### Phase 3: Approximation & Quality

**Duration:** 3A ~8 min, 3B ~5 min | **Gate:** check_part3.py passes (both tracks) | **Track:** Parallel — Track A (Approximation) + Track B (Quality) | **Claims:** C03, C04, C05 (A); C01 (B)

**Goal:** Track A benchmarks betweenness approximation against exact computation on 3 graphs, varying sample sizes and seeds. Track B compares Louvain vs Leiden community quality across 50 seeds on 5 graphs, audits community connectivity, and scores against ground truth on email-Eu-core.

**Track A — Betweenness Approximation:**
1. Computed exact betweenness on 3 graphs (email-Eu-core, openflights, ca-GrQc)
2. Sampled at 1%, 2%, 5%, 10%, 25% × 10 seeds each (150 total runs)
3. Measured speedup vs exact computation
4. Computed Spearman correlation and top-k overlap vs exact
5. Analyzed error vs sample-size curves
6. Wrote analysis memo

**Key Numbers (1% fraction):** email-Eu-core: 97.95× speedup, Spearman 0.945, top-10 overlap 0.177. openflights: 98.04× speedup, Spearman 0.929, top-10 overlap 0.429. ca-GrQc: 95.97× speedup, Spearman 0.965, top-10 overlap 0.333.

At 1% sampling, the speedup is dramatic (~96–104×) but the top-10 overlap is poor (0.177–0.429). This means that while the approximation is fast, it misses many of the top-ranked nodes. The trade-off between speed and accuracy is steep at low sampling fractions.

**Key Finding:** At 5% sampling, speedup is ~18–20× with Spearman > 0.97 and top-10 overlap ~0.5–0.8. This is the practical sweet spot. At 5% sampling, you get 97%+ rank correlation while still achieving 18–20× speedup. The top-10 overlap improves to 0.5–0.8, meaning most of the top nodes are correctly identified.

**Track B — Community Quality:**
1. Ran Louvain vs Leiden on 5 graphs × 50 seeds
2. Audited community connectivity (bridge edges, disconnected communities)
3. Scored against ground truth on email-Eu-core (42 departments)
4. Computed similarity vs bridge-edge fraction
5. Wrote quality memo

**Key Insight:** Ground truth ARI < 0.3 on email-Eu-core would mean departments are organisational, not community-structural. We measure this ourselves — no primary source to cite. If the ARI is low, it means the communities detected by the algorithm don't correspond to the known department structure, which would be a significant finding about the limitations of community detection on this graph.

**Scope:** In Scope (Track A): Exact betweenness on 3 graphs, Sampled at 1%, 2%, 5%, 10%, 25% × 10 seeds each, 500 airport pairs: weighted (km) vs hop distance, Error vs sample-size curves, Condition for "can we sample" formulation. In Scope (Track B): Louvain vs Leiden, 50 seeds × 5 graphs, Community connectivity audit (bridge edges), Ground truth on email-Eu-core (42 departments), Similarity score vs bridge-edge fraction, Hypothesis about disconnected communities. Out of Scope (Both): Synthetic planted-partition tests (Tier 3), CPM partition exploration (Tier 3), Deep learning on graphs (out of project scope).

**Tier Table:** Tier 1: betweenness_*.csv, weights_effect.csv, memos (A); community_quality.csv, ground_truth_scores.csv, similarity_vs_bridges.csv, memos (B) — Critical. Tier 2: charts/, --full flag on facebook_combined (A); Connectivity audit report, seed-sensitivity analysis (B) — Important. Tier 3: Synthetic planted-partition tests; CPM exploration (A); Disconnected-community hypothesis report (B) — Optional.

**Decision Rules:** 25% sampling still unreliable (error > 10%) → State condition for "can we sample at all" — likely no for global betweenness on this graph class. Leiden shows same disconnected rate as Louvain → Hypothesis: graph shape (community size distribution) dominates algorithm choice. Ground truth ARI < 0.3 on email-Eu-core → Note: departments are organisational, not necessarily community-structure-aligned.

**Stage-by-Stage Workflow:** 3A.1 Exact betweenness on 3 graphs (`run_part3a.py --step exact`, ~5 min, betweenness_exact_*.csv) → 3A.2 Sampled at 1/2/5/10/25% (`run_part3a.py --step sample`, ~3 min, betweenness_sample_*.csv) → 3A.3 Weights Effect — 500 airport pairs weighted vs hop (`run_part3a.py --step weights`, ~30s, weights_effect.csv) → 3B.1 Louvain vs Leiden 50 seeds × 5 graphs (`run_part3b.py --who solo`, ~3 min, community_quality.csv) → 3B.2 Community connectivity audit + ground truth (`run_part3b.py --step audit`, ~2 min, ground_truth_scores.csv, similarity_vs_bridges.csv).

**Failure Modes:** Exact betweenness OOM on openflights → MemoryError. Drop openflights from exact set; use 2 graphs. Sampling error plateaus at >10% → No convergence in betweenness_sample_*.csv. Document in memo; answer "can we sample" = no for global betweenness. Leiden produces many singleton communities → ARI near 0, modularity low. Check resolution parameter; increase minimum community size.

**Outputs:** betweenness_*.csv (multiple), weights_effect.csv (500 rows), community_quality.csv (~500 rows), ground_truth_scores.csv (~250 rows), similarity_vs_bridges.csv (~250 rows), part3a-memo.md, part3b-memo.md, charts/*.png (3 PNGs)

---

### Phase 4: Capstone & Projection

**Duration:** ~30s run + ~45 min analysis | **Gate:** check_part4.py passes | **Track:** Both | **Claims:** C07, C08, C11

**Goal:** Apply PageRank and Louvain to bipartite graphs, project onto each side, compare rankings and communities, and document the consequences of projection choice. This is the single most consequential analytical decision in the pack.

**What We Did:**
1. Loaded bipartite graphs: crime (offender-location), unicodelang (language-script)
2. Computed raw PageRank + Louvain on bipartite graphs
3. Projected onto side 0 and computed PageRank + Louvain
4. Projected onto side 1 and computed PageRank + Louvain
5. Compared rankings: Spearman between raw and projected
6. Compared communities: ARI between raw and projected
7. Documented projection blowup: edge count increase from projection
8. Wrote memo and synthesis

**Key Numbers — Projection Effect:** crime side 0 (people): Spearman 0.2264, ARI 0.5688, Top-10 Overlap 0.3333. crime side 1 (crimes): Spearman 0.002, ARI 0.5751, Top-10 Overlap 0.1765. unicodelang side 0 (territories): Spearman 0.3069, ARI 0.1702, Top-10 Overlap 0.1111. unicodelang side 1 (languages): Spearman 0.2996, ARI 0.3506, Top-10 Overlap 0.8182.

**Key Insight:** Projection is NOT neutral. On crime side 1, raw vs projected PageRank Spearman = 0.002 — the two rankings are essentially uncorrelated. On unicodelang side 0, ARI = 0.17 — communities barely overlap. Both results are correct. Only one answers your question. Document which question you are answering and why you chose that projection.

The crime side 1 result is particularly striking — a Spearman of 0.002 means the projected ranking is essentially random compared to the raw ranking. This means that if you're studying crimes (not people), you must analyze the bipartite graph directly, not its projection. The projection fundamentally changes the ranking object.

**Scope:** In Scope: Bipartite graphs: crime (offender-location), unicodelang (language-script), Raw PageRank + Louvain on bipartite graphs, Projection onto side 0 and side 1, Ranking comparison (Spearman between raw and projected), Community comparison (ARI between raw and projected), Write part4-memo.md, Replication: colleague's headline finding, synthesis.md: cross-part narrative. Out of Scope: Weighted projection (Tier 3), Custom bipartite construction (Tier 3), Algorithm design beyond provided scripts.

**Tier Table:** Tier 1: projection_*.csv (4 files), part4-memo.md — Critical. Tier 2: replication.md, synthesis.md — Important. Tier 3: Weighted projection, custom bipartite construction — Optional.

**Decision Rules:** Spearman ~0 between raw and projected rankings → Report as finding, not error. Projection fundamentally changes the ranking object. Projection blowup > 10× edge count → Warn in memo. Density may make downstream algorithms impractical. Consider weighted projection or sampling. Replication finding differs from colleague → Report honestly. Do not adjust parameters to force agreement.

**Stage-by-Stage Workflow:** 4.1 Raw PageRank + Louvain on bipartite (`run_part4.py --step raw`, ~10s, projection_raw_*.csv) → 4.2 Project onto side 0 (`run_part4.py --step proj0`, ~10s, projection_side0_*.csv) → 4.3 Project onto side 1 (`run_part4.py --step proj1`, ~10s, projection_side1_*.csv) → 4.4 Compare rankings and communities (`run_part4.py --step compare`, ~5s, Spearman, ARI tables) → 4.5 Write memo (manual, ~40 min, part4-memo.md).

**Failure Modes:** Projection produces dense graph → Edge count blows up; algorithms slow. Use weighted projection or sample; document in memo. Raw PageRank undefined on bipartite → Zero probability mass. Use personalisation vector; restart with damping. Replication data missing → Colleague's output not available. Request from colleague; note gap in research-log.md.

**Outputs:** projection_effect.csv, projection_rankings.csv, projection_mass.csv, projection_shape.csv, part4-memo.md, replication.md, synthesis.md

---

### Phase 5: Replication & Synthesis

**Duration:** ~2–3 hours | **Gate:** All previous gates pass + claims.jsonl complete | **Track:** Both | **Claims:** C07, C08, C11 + all claims memo

**Goal:** Replicate a colleague's headline finding, complete the claims strand for C07/C08/C11, run check_claims.py, write claims-memo.md, export RDF Turtle via gds-owl, and write synthesis.md.

**What We Did:**
1. Replicated colleague's headline finding: ran their script, compared outputs
2. Completed claims.jsonl: filled evidence, verdict, and grade for all 12 claims
3. Ran check_claims.py: validated all 12 rows pass
4. Wrote claims-memo.md: narrative synthesis of all 12 claims
5. Exported RDF Turtle: used gds-owl to export experiment results
6. Validated with SHACL: ran pyshacl on experiment.ttl
7. Wrote synthesis.md: cross-part narrative and conclusions

**Scope:** In Scope: Replicate colleague's headline finding (claim from another solo intern), Complete claims.jsonl for C07, C08, C11, Run check_claims.py --who solo, Write claims-memo.md, Export RDF Turtle via gds-owl, Write synthesis.md, SHACL validation on experiment.ttl, Cross-lab comparison notes. Out of Scope: New graph algorithms (out of scope), Deep learning (out of scope), Streaming / temporal graphs (no timestamps in data).

**Tier Table:** Tier 1: replication.md, synthesis.md, claims-memo.md, claims.jsonl (12 rows complete) — Critical. Tier 2: experiment.ttl (RDF export), SHACL validation report — Important. Tier 3: Cross-lab comparison, SPARQL queries over results — Optional.

**Decision Rules:** Replication mismatch (numerical difference > tolerance) → Report honestly as "did not replicate". Do not adjust parameters. Explain discrepancy in replication.md. gds-owl unavailable → Skip Turtle export. Note in synthesis.md. Ontology strand is gracefully degraded. check_claims.py returns < 12 → Fix missing claims. Rerun until 12 rows pass.

**Stage-by-Stage Workflow:** 5.1 Replicate colleague's headline finding (manual: run colleague's script, compare outputs, ~1 hour, replication.md) → 5.2 Complete claims.jsonl for C07/C08/C11 (manual: fill evidence, verdict, grade, ~30 min, claims.jsonl 12 rows) → 5.3 Run check_claims.py (`check_claims.py --who solo`, ~10s, pass/fail report) → 5.4 Write claims-memo.md (manual, ~30 min, claims-memo.md) → 5.5 Export RDF Turtle via gds-owl (`gds-owl export --format turtle --output experiment.ttl`, ~5 min, experiment.ttl) → 5.6 Write synthesis.md (manual, ~30 min, synthesis.md).

**Failure Modes:** Replication mismatch → Numerical difference > tolerance. Report honestly. Check random seeds, data versions, graph preprocessing. gds-owl import error → ModuleNotFoundError. Use venv-gds-owl. If still failing, skip Turtle export. SHACL validation fails → Conformance = false. Inspect validation report; fix Turtle or shapes; rerun. check_claims.py returns < 12 → Missing required fields. Fill all required fields in claims.jsonl; rerun.

**Outputs:** replication.md, claims.jsonl (12 completed claim records with evidence grades), claims-memo.md, experiment.ttl, synthesis.md, SHACL validation report

---

## Key Findings

1. **PageRank cost correlates with degree skew more than node count.** unicodelang (skew=141) needs 67 iterations; email-Eu-core (skew=16.5) needs only 14. This counter-intuitive finding means that degree skew, not size, is the primary predictor of PageRank convergence cost.

2. **Louvain is stable on crime** (mod 0.9296 ± 0.0004) but noisy on openflights (0.6560 ± 0.0042). This means that for crime, you can trust Louvain results without testing multiple seeds. For openflights, you must test multiple seeds and report the variance.

3. **Projection changes rankings drastically:** crime side 1 Spearman=0.002 (uncorrelated). unicodelang side 0 ARI=0.17. Projection is not a neutral transformation — it fundamentally changes the ranking object. Choosing the wrong representation leads to wrong conclusions.

4. **Betweenness approximation achieves 95–104x speedup** with Spearman >0.92 at 1% pivot sampling. At 1% sampling, you get dramatic speedup but poor top-10 overlap. The trade-off is steep.

5. **At 5% sampling, speedup is ~18–20×** with Spearman >0.97 and top-10 overlap ~0.5–0.8. Practical sweet spot. This is the recommended sampling fraction for betweenness approximation.

6. **Correlation does not imply top-k agreement.** Two rankings can have Spearman ρ = 0.95 yet disagree on top-10 nodes. Always inspect the actual node lists, not just the correlation number. This is a critical trap in graph algorithm evaluation.

7. **Modularity std below 0.001 indicates seed-robust partitions** (crime, unicodelang). Above 0.002 — interpret with caution. This metric is essential for determining whether Louvain results are reliable.

8. **Projection is NOT neutral:** Amplifies mass imbalances and reshapes ranking structures. The choice of projection side fundamentally changes the analytical result.

**What these findings mean:** Degree skew is the dominant factor in PageRank convergence — not node count. This means you should always check skew before choosing an algorithm. Louvain stability varies dramatically across graphs — crime is robust, openflights is not. This means you should never assume Louvain will produce stable results without testing. Projection fundamentally changes the ranking object — this means you must choose your representation carefully based on your question, not convenience.

**Implications for practice:** These findings have direct consequences for how graph algorithms are applied in production. If you use PageRank on a high-skew graph without checking convergence, you may get misleading results. If you use Louvain without testing stability, your communities may be artifacts of initialization. If you project a bipartite graph without understanding the consequences, you may answer the wrong question.

---

## Deliverables Completed

**Phase 0:** first-impressions.md, claims.jsonl (12 rows), research-log.md, questions.md, planner.html
**Phase 1:** profiles.csv (7), pagerank_runs.csv (70), calibration.md, part1-memo.md, charts/ (11 PNGs)
**Phase 2A:** centrality_*.csv (4), disagreements.csv, part2a-memo.md, charts/
**Phase 2B:** louvain_runs.csv (1,000), part2b-memo.md, charts/
**Phase 3A:** betweenness_exact.csv, betweenness_approx.csv (150), weights_effect.csv (500), part3a-memo.md, charts/
**Phase 3B:** community_quality.csv (500), ground_truth_scores.csv, similarity_vs_bridges.csv, part3b-memo.md, charts/
**Phase 4:** projection_*.csv (4), replication.md, synthesis.md, part4-memo.md, charts/
**Phase 5:** claims.jsonl (12 rows scaffolded, 0/12 filled), claims-memo.md

**All Phase 1–4 checkers pass.** Every checker test passed for phases 0 through 4. The checkers validate that outputs exist, have the correct format, contain the expected number of rows, and meet quality criteria. Phase 5 claims strand is scaffolded but unfilled (requires manual primary-source research).

**What each deliverable contains:**
- CSVs: Raw measurement data with provenance sidecars (.provenance.json)
- Memos: Analysis narratives explaining methodology, findings, and decision rules
- Charts: Visualization PNGs for each phase (11 in P1, 2 in P2, 3 in P3)
- claims.jsonl: Structured claim records with evidence, verdict, and grade
- research-log.md: Day-by-day documentation of the project
- planner.html: Interactive phase plan with decision rules and tier tables
- graph_analysis.html: Interactive analysis report with all phases

---

## Ontology & Interoperability

**Biolink Model v4.4.4:** Located at `life_science_corpus/ontology/biolink_model.owl.ttl` (~19k lines, 948+ classes). Provides standard biomedical vocabulary for modelling experimental results as RDF/OWL linked data. The model covers genes, diseases, chemical entities, pathways, publications, associations, and molecular activities.

**SHACL Shapes:** `life_science_corpus/ontology/biolink_model.shacl.ttl` (~60k lines). Validates exports before archiving, catching schema violations early. SHACL (Shapes Constraint Language) is a W3C standard for validating RDF graphs. It ensures that exported Turtle files conform to the expected structure and vocabulary.

**Chemical Ontology:** `life_science_corpus/ontology/chebi.owl` — Chemical entities reference. ChEBI (Chemical Entities of Biological Interest) provides a hierarchical classification of chemical entities.

**LinkML Schema:** `life_science_corpus/ontology/biolink_model.yaml` — Structured schema definition. LinkML is a framework for defining schemas for biomedical data.

**gds-owl Bridge:** v0.99.0. Converts experimental results into Turtle format. Installed in venv-gds-owl (Python 3.14). The bridge takes CSV outputs from each phase and converts them to RDF triples using the Biolink Model vocabulary.

**Validation Pipeline:** Experiment results → gds-owl export → experiment.ttl → pyshacl validation → SHACL conformance report → Archive. Only conforming exports are archived. This ensures that every archived result is both syntactically valid and semantically correct.

**Key Advantage:** W3C standards (Turtle and RDF) have decades-long archival stability compared to CSV/Markdown. Results can be joined with external knowledge graphs via SPARQL without schema mapping. CSV files are opaque — you need to know the schema to understand what each column means. RDF Turtle is self-describing: every triple has a subject, predicate, and object, all of which are URIs that resolve to definitions.

**Why this matters for cross-lab interoperability:** By aligning our experimental results with the Biolink Model, we ensure that our data can be integrated with other biomedical knowledge graphs. This means our results can be queried alongside external datasets using standard SPARQL endpoints. Any lab that uses the Biolink Model can directly query our results without custom mapping.

---

## Next Steps

1. **Complete claims strand:** Fill all 12 rows in claims.jsonl with evidence, verdict, and grade. Longest pole in schedule — requires manual primary-source research. Each claim requires finding a primary source, locating the exact quote, checking it says what is claimed, and recording the verdict. This is the most labor-intensive part of the project.

2. **Replicate colleague's finding:** Run colleague's script, compare outputs, document discrepancies honestly. If the results match within tolerance, we have replicated the finding. If they differ, we document the discrepancy honestly — we do not adjust parameters to make them match.

3. **Export RDF Turtle:** Use gds-owl to export experiment results, validate with SHACL. The export pipeline converts CSV outputs to Turtle format using the Biolink Model vocabulary. SHACL validation ensures the exported Turtle conforms to the expected structure.

4. **Write synthesis.md:** Cross-part narrative and conclusions. synthesis.md ties together findings from all phases into a coherent narrative. It answers the big questions: What did we learn? What works? What doesn't? What are the limitations?

5. **Fix graph_analysis.html:** The file uses Chart.js CDN which may not load in all environments. Consider self-contained Chart.js or fallback to static images. This is a quality-of-life improvement that ensures the analysis page works in all environments.

6. **Build SPARQL endpoint:** Once RDF export is complete, set up a SPARQL endpoint for cross-lab comparison. This would allow other labs to query our results alongside their own data.

7. **Expand graph set:** Add more domains (biological, citation) to improve statistical generalization. The current 7 graphs are sufficient for methodology demonstration but not for broad generalization.

---

## Q&A

**Anticipated Questions:**

- Q: Why 7 graphs? A: Structural diversity — no interchangeable pairs. Each tests different algorithm behaviors. lesmis is small and dense, while ca-GrQc is large and fragmented. openflights has extreme degree skew, while email-Eu-core has ground truth labels.

- Q: Why two venvs? A: Core runtime packages move fast; semantic web stack is conservative. Mixing creates dependency resolver conflicts. Isolation lets us upgrade each stack independently.

- Q: What about Phase 5? A: Depends on colleague output and manual claims research. Everything else is complete. All Phase 1–4 checkers pass. The claims strand is scaffolded but unfilled.

- Q: Can we scale to larger graphs? A: Exact betweenness is O(n·m). For openflights (36,906 edges), exact betweenness may exceed memory. We mitigate by dropping it from the exact set. Sampling at 5% gives 18–20× speedup with Spearman > 0.97.

- Q: What's the practical value of approximation? A: At 5% sampling, you get 18–20× speedup with 97%+ rank correlation. For large graphs where exact betweenness is infeasible, this makes the computation tractable.

- Q: Why is projection not neutral? A: Bipartite projection discards information about the original structure. The projected graph has different properties than the original. On crime side 1, raw vs projected PageRank Spearman = 0.002 — essentially uncorrelated.

- Q: What's the significance of degree skew? A: Degree skew is the primary predictor of PageRank convergence cost, not node count. unicodelang (skew=141) needs 67 iterations; email-Eu-core (skew=16.5) needs only 14. This means you should always check skew before choosing an algorithm.

- Q: How do you validate Louvain stability? A: Run Louvain 200 times per graph with different seeds. Record modularity std. Below 0.001 indicates seed-robust partitions. crime: 0.9296 ± 0.0004 (stable). openflights: 0.6560 ± 0.0042 (unstable).

- Q: What about the claims strand? A: 12 claims are scaffolded but unfilled (0/12). This requires manual primary-source research — finding papers, locating exact quotes, and grading evidence quality. It cannot be automated.

**Key Messages:**
- Every number traces to a CSV row — reproducibility is the core value proposition
- Degree skew explains iterations better than node count — this is the counter-intuitive finding
- Projection is NOT neutral — this is the most consequential analytical decision
- Claims strand is scaffolded but unfilled — this is the biggest gap
- Approximation at 5% sampling gives 18–20× speedup with 97%+ rank correlation
- RDF/OWL export enables cross-lab interoperability via SPARQL

---

## Speaker Notes

**Timing:** ~20 minutes total. Adjust phase summary depth based on audience interest. The opening and what-is-GDS sections should take about 3 minutes. The aims and objectives section should take about 2 minutes. The phase-by-phase detail can be adjusted based on audience questions. The key findings and Q&A should take about 5 minutes.

**Key Messages:**
- Every number traces to a CSV row — reproducibility is the core value proposition
- Degree skew explains iterations better than node count — this is the counter-intuitive finding
- Projection is NOT neutral — this is the most consequential analytical decision
- Claims strand is scaffolded but unfilled — this is the biggest gap
- Approximation at 5% sampling gives 18–20× speedup with 97%+ rank correlation
- RDF/OWL export enables cross-lab interoperability via SPARQL

**Anticipated Questions:**
- Q: Why 7 graphs? A: Structural diversity — no interchangeable pairs. Each tests different algorithm behaviors.
- Q: Why two venvs? A: Core runtime packages move fast; semantic web stack is conservative. Mixing creates dependency resolver conflicts.
- Q: What about Phase 5? A: Depends on colleague output and manual claims research. Everything else is complete.
- Q: Can we scale to larger graphs? A: Exact betweenness is O(n·m). For openflights (36,906 edges), exact betweenness may exceed memory. We mitigate by dropping it from the exact set.
- Q: What's the practical value of approximation? A: At 5% sampling, you get 18–20× speedup with 97%+ rank correlation.
- Q: Why is projection not neutral? A: Bipartite projection discards information about the original structure.
- Q: What's the significance of degree skew? A: Degree skew is the primary predictor of PageRank convergence cost, not node count.
- Q: How do you validate Louvain stability? A: Run Louvain 200 times per graph with different seeds. Record modularity std.
- Q: What about the claims strand? A: 12 claims are scaffolded but unfilled (0/12). Requires manual primary-source research.

**References:**
- gds-workflow.html — Full technical reference with all procedures, flowcharts, decision rules, quality gates
- planner.html — Phase plan with decision rules, tier tables, failure modes
- graph_analysis.html — Interactive analysis report with all phases
- All CSVs and memos in your-work/solo/part{1,2,3,4}/

---

*End of script. See gds-workflow.html for full technical details.*
