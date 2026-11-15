# Glossary

Skim it once, then keep it open while you work. Terms are grouped by what they
are about, not alphabetically — you will usually be looking for "that thing about
communities" rather than for a specific word.

---

## The graph itself

**Node** (also *vertex*) — a thing. A person, an airport, a character, a word.

**Edge** — a connection between two nodes.

**Neighbour** — a node one edge away.

**Degree** — how many neighbours a node has. For a directed graph, *in-degree*
counts arrows pointing at it and *out-degree* counts arrows leaving it.

**Degree skew** — in this pack, `max degree ÷ median degree`. How many times more
connected the busiest node is than a typical one. A crude but useful measure of
how lopsided a graph is. Not standard terminology; we use it because it predicts
cost better than node count does.

**Directed / undirected** — whether edges have a direction. Emails are directed
(you emailing me is not me emailing you); appearing in a scene together is not.

**Weighted** — edges carry a number. **Always ask what the number means**: a
*cost* (bigger = further, worse) or a *strength* (bigger = closer, better). They
are opposites and no algorithm can tell them apart.

**Path** — a sequence of edges leading from one node to another.

**Shortest path** — fewest edges, or lowest total cost if weighted. These are
different questions with different answers.

**Distance** — the length of the shortest path between two nodes.

**Component** — a set of nodes that can all reach each other, with no path to
anything outside it. A graph in several components has pairs of nodes with no
route between them at all, which makes "average distance" undefined.

**Density** — the fraction of all possible edges that actually exist. Real graphs
are usually far sparser than people expect.

**Clustering coefficient** — do your neighbours know each other? The fraction of
connected triples that close into a triangle.

**Bipartite** — the graph has two kinds of node and every edge crosses between
the kinds. People↔crimes, actors↔films, things↔the documents mentioning them.
A bipartite graph has clustering exactly zero, because a triangle is impossible.

**Self-loop** — an edge from a node to itself. Usually dropped before analysis;
all of this pack's graphs have had them removed.

**Multigraph** — more than one edge allowed between the same pair. `openflights`
was one before normalisation (several airlines, same route).

---

## Centrality — which nodes matter

**Centrality** — any measure of a node's importance. There is no single one, and
"most central" is not a well-formed question without saying which.

**Degree centrality** — count the connections. Nearly free. Often misleading on
its own.

**PageRank** — importance flows along edges; you are important if important
things point at you. Needs direction to mean much. Converges by iterating until
scores stop moving.

**Damping factor** — the ~0.85 in PageRank: the chance of following an edge
rather than jumping somewhere random. The 15% jump is what guarantees the maths
has a unique answer. Not a tuning knob.

**Closeness centrality** — how near a node is to everyone else on average.
Expensive, and ill-defined on a disconnected graph.

**Betweenness centrality** — how many shortest routes between other pairs pass
through this node. The most expensive measure in common use, and the one that
finds single points of failure.

**Edge betweenness** — the same idea for edges rather than nodes. Finds bridges.

**Convergence / iterations** — iterative algorithms stop when the answer stops
changing much. The *number of rounds* depends on the graph's shape, not its size,
which is why you cannot predict cost from input size.

---

## Communities — which nodes group together

**Community detection** — finding groups of nodes more connected to each other
than to the rest. Nobody labelled them; the algorithm infers them.

**Modularity** — the score for how good a grouping is: how much more connected
each group is internally than chance would predict. Ranges roughly −0.5 to +1.
Zero means "no better than random".

**Resolution** — a knob controlling how big the groups come out. Related to the
*resolution limit*: modularity-based methods are structurally unable to find
communities below a certain size, no matter how obvious those communities are.

**Louvain** — the standard fast community algorithm. Repeatedly moves nodes to
whichever neighbouring group improves modularity, then collapses and repeats.

**Leiden** — Louvain plus a refinement step that checks each group is actually
connected inside, and splits it if not. Exists specifically to fix a Louvain
defect.

**Internally disconnected community** — a group whose members cannot reach each
other *without leaving the group*. Reported as belonging together with no path
between them inside their own community. The failure Leiden was invented to
prevent.

**Badly connected community** — connected, but only just: some member hangs off
the rest of its own community by a single edge.

**Label propagation** — a cheaper alternative: everybody repeatedly adopts
whichever group is most common among their neighbours. No scoring function at
all. Fast and cheap to update, lower quality.

**Ground truth** — the *actually correct* grouping, known independently of any
algorithm. Rare and precious. Only `email-Eu-core` has it here (42 real
departments), and it is the only graph where you can measure whether an algorithm
is **right** rather than merely whether two algorithms **agree**.

**ARI** (Adjusted Rand Index) — how much two groupings agree. 1.0 identical, ~0.0
no better than chance. Ignores what the groups are *called*, which is what you
want.

**NMI** (Normalised Mutual Information) — another agreement measure between
groupings, on a 0–1 scale.

**Partition** — one complete grouping of every node. **Partition hash** — a
fingerprint of a partition, for counting how many *distinct* outcomes appeared
across many runs. Use it for counting, never for judging quality.

---

## Similarity and prediction

**Node similarity** — how alike two nodes are *by the company they keep*. Two
nodes are similar when they share many neighbours. Says nothing about what the
nodes mean.

**Jaccard similarity** — shared neighbours ÷ total distinct neighbours. 1.0
identical neighbourhoods, 0.0 none in common.

**Link prediction** — guessing which edges *ought* to exist but do not. Acts on
what the graph is missing rather than what it contains.

**Adamic-Adar** — the standard simple link-prediction method: weights rare shared
neighbours more heavily than common ones. Two people who both know an obscure
acquaintance are far more likely connected than two who both know a celebrity.

**Temporal split vs random split** — how you divide data into train and test. A
*random* split lets the model see the future and inflates its score
spectacularly; a *time-based* split does not. Getting this wrong is the classic
way to report a great result that collapses in production.

---

## Doing the work

**Projection** — selecting a slice of a graph to analyse, and possibly deriving
new edges in the process. Projecting a bipartite people↔crimes graph onto people
creates person-to-person edges that exist in no data file. **The single most
consequential choice you make**, because it determines what any algorithm can
possibly see.

**One-mode projection** — the specific case of collapsing a bipartite graph onto
one of its two sides.

**Rank sink** — what happens when you run PageRank on a bipartite graph without
thinking: score piles up on one side simply because arrows point that way. The
numbers look authoritative and mean nothing.

**Execution mode** — how you want the answer back: `estimate` (how much memory
would this need?), `stats` (summary only), `stream` (return rows), `mutate` (keep
it in the working copy), `write` (save it). Choosing wrongly is how people
accidentally write a billion rows somewhere.

**Seed** — the number that fixes an algorithm's randomness. Same seed, same
answer. Different seeds are how you measure how much an algorithm varies with
itself — which is why every run in this pack records the seed it used.

**Provenance** — the record of *how* a number was produced: which machine, which
library versions, which seed, when. Every results file here gets a
`.provenance.json` sidecar automatically. A timing without provenance cannot be
interpreted by anybody, including you, three weeks later.

**Warm-up** — discarding the first call before timing, because the first call
pays for imports and lazily-built internals. Measured here at 270× the cost of
subsequent calls.

**Sample size** — how many runs a number is based on. Attach it to every rate you
state. A result from one run is an anecdote.

---

## Things that are easy to confuse

| These sound alike | But |
|---|---|
| similarity vs. connection | The two most important nodes in the bridge graph are directly connected and have similarity **0.000** |
| "the same size" vs. "the same shape" | 4,039 nodes took twice as long as 5,241 nodes |
| agreement vs. correctness | Two algorithms can agree and both be wrong |
| a different answer vs. a worse answer | Two Louvain runs differing is expected, not a bug |
| the checker passed vs. the finding is right | A checker sees whether evidence is *present*, never whether it is *true* |
| weight as cost vs. weight as strength | Opposites. Nothing will warn you |
