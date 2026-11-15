# What you can compute on a graph

About forty minutes. Every number here comes from a graph in this pack, and the
code to reproduce it is included.

---

## 1. The one distinction that matters

Picture a company directory. Ask **"who does Priya report to?"** — the answer is
sitting in Priya's record. You look it up. Every database ever built does this.

Now ask: **"if one person resigned tomorrow, whose leaving would cut the most
teams off from each other?"**

That answer is in nobody's record. It is not written down anywhere. It exists
only in the *shape* of the whole organisation, and the only way to get it is to
work across everybody at once.

That second kind of question is what this field is for.

| | A lookup | A computation |
|---|---|---|
| Where's the answer? | stored in a record | nowhere — it emerges from the structure |
| How do you get it? | read the record | examine every connection, often repeatedly |
| Reading less data | helps enormously | does not help at all |
| Is it still true tomorrow? | until someone edits it | **one new edge can change every score** |

That last row catches people out. A stored fact stays true until somebody changes
it. A computed score is only true *as of a particular shape of the graph* — add
one edge and, in principle, every number you computed is stale.

## 2. The smallest possible demonstration

Eight nodes. Two tight groups of four, joined by exactly one edge.

```
    A───B          E───F
    │╲ ╱│          │╲ ╱│
    │ ╳ │          │ ╳ │
    │╱ ╲│          │╱ ╲│
    D───C ──────── G───H
          the only
           bridge      (C and E are the bridge ends)
```

```python
import sys; sys.path.insert(0, "03-data")
import networkx as nx
from make_synthetic import bridge_graph

G, _ = bridge_graph()
deg = dict(G.degree())
clo = nx.closeness_centrality(G)
bet = nx.betweenness_centrality(G, normalized=False)
for n in sorted(G):
    print(n, deg[n], round(clo[n], 3), bet[n])
```

| Node | Degree | Closeness | Betweenness |
|---|---|---|---|
| A, B, D, F, G, H | 3 | 0.500 | **0.00** |
| C | 4 | 0.700 | **12.00** |
| E | 4 | 0.700 | **12.00** |

**Read that table twice.**

Counting connections — the thing any database can do — says C has 4 where the
others have 3. Thirty-three percent more. A difference you would shrug at.

Counting how much traffic must pass *through* each node says C carries
**every single route** between the two halves, and six of the eight nodes carry
**none at all**. Twelve versus zero. Remove C and the network falls in two.

Same graph. Same eight nodes. One measure sees almost nothing; the other locates
the exact point of failure. That is the entire argument for this field, and it
fits on a napkin.

## 3. "Most important" is not a question

It has at least four different answers, and they are answers to different
questions:

| Measure | The question it actually answers | Cost |
|---|---|---|
| **Degree** | who has the most connections? | free |
| **PageRank** | who is endorsed by others who are themselves endorsed? | cheap |
| **Closeness** | who is nearest to everyone else on average? | expensive |
| **Betweenness** | who sits on the most routes between other people? | very expensive |

Nobody should ever say "the most central node" without saying which. Part 2A asks
you to measure how much these four actually disagree on real graphs — and whether
the cheap one can stand in for the expensive one.

### PageRank, in plain terms

Imagine importance as water. Every node pours its water equally down its outgoing
edges each round. Popular nodes receive more, so next round they pour more.
Repeat until the levels stop moving.

One refinement makes it work: each round a small share of all the water — 15%
conventionally — is collected up and sprinkled evenly over everything. Without
that, water drains into dead ends and pools in loops forever. That 15% is not a
tuning knob; it is what makes the maths valid.

**Two warnings.**

PageRank on an *undirected* graph tells you very little that degree does not.
It needs direction to mean anything. (Bench experiment B5 asks you to check
whether that is actually true.)

And the number of rounds it takes depends on the graph's *shape*, not its size.
You cannot predict the cost from the input size, which is unlike almost every
database operation you have ever met. Part 1 is about this.

### The cost warning that matters

**Betweenness is the most expensive measure in common use.** It effectively
traces routes between every pair of nodes. On this pack's graphs, exact
betweenness takes about 1 second on the small ones and **86 seconds** on
`facebook_combined`.

And here is the thing worth remembering — measured on the reference machine:

| Graph | Nodes | Edges | Exact betweenness |
|---|---|---|---|
| `ca-GrQc` | **5,241** | 14,484 | 41.4 s |
| `facebook_combined` | **4,039** | 88,234 | **85.7 s** |

`ca-GrQc` has 30% *more* nodes and takes *half* as long. If you had budgeted from
node count you would have been wrong by a factor of two, in the wrong direction.

## 4. The six families

Every algorithm you will meet — there are roughly fifty-five in a mature library
— answers one of six questions. Learn the six and the fifty-five become lookups.

| Family | The question | Examples |
|---|---|---|
| **Centrality** | which things matter most? | PageRank, betweenness, closeness, degree |
| **Community detection** | which things belong together? | Louvain, Leiden, label propagation |
| **Similarity** | which things resemble each other? | node similarity, k-nearest-neighbours |
| **Path finding** | what is the best route? | Dijkstra, A*, breadth-first search |
| **Embeddings** | how do I feed a graph to a machine-learning model? | FastRP, GraphSAGE, node2vec |
| **Link prediction** | which connection is missing? | Adamic-Adar, common neighbours |

This pack works on the first four. Embeddings and link prediction get a mention
and one optional bench experiment; they need training data and a different set of
habits.

## 5. Community detection — finding groups nobody labelled

Nobody tagged these nodes as belonging to groups. The algorithm finds them by
looking for clumps: sets of nodes far more connected to each other than to
everything else.

The score for "is this a good grouping" is called **modularity** — how much more
connected each group is internally than you would expect if all the edges had
been thrown down at random.

On the eight-node bridge graph:

| Proposed grouping | Modularity | Verdict |
|---|---|---|
| The two natural clumps | **+0.4231** | best |
| Everything in one group | 0.0000 | no better than random |
| Every node on its own | −0.1272 | worse than random |

Notice that both lazy answers score zero or below *automatically*. Lumping
everything together maximises the "connected internally" term, but the "expected
by chance" term rises to match it exactly, and they cancel. That self-correction
is why the measure does not need anybody to tell it how many groups to look for.

### Louvain, Leiden, and the difference

**Louvain** repeatedly moves each node into whichever neighbouring group most
improves modularity, then collapses each group into a single node and repeats.

**Leiden** adds one step: before collapsing, it checks that each group is
actually *connected inside*, and splits any group that is not.

That extra step exists because of a real defect. Louvain can return a "group"
whose members cannot reach each other **without leaving the group** — nodes
reported as belonging together with no path between them inside their own
community. The paper introducing Leiden measured Louvain producing up to 25%
badly-connected groups and up to 16% internally disconnected ones.

**Part 3B asks you to test that on real graphs.** Not to confirm it — to measure
it. It may not hold on these graphs, and "we measured it and found a much lower
rate than published, here is the number and the sample size" is a completely
good result.

### Two runs may not agree, and that is not a bug

These algorithms make educated guesses. Finding the genuinely best grouping is a
problem with no known efficient exact solution, so every practical tool uses a
heuristic seeded with randomness.

**So two runs on identical data can return different groupings.** Part 2B asks
you to measure how often, and how much the quality varies when it happens.

The rule that follows is important enough to state on its own:

> **Never compare two groupings by asking whether they are equal.**
> A different grouping is not a worse grouping. Compare their modularity.

## 6. Similarity — and the most instructive zero in this document

Similarity here means **"shares neighbours"**, not "means something similar". Two
people are similar if they know many of the same people. Nothing about the nodes
themselves is examined.

Back to the eight-node graph, using Jaccard overlap of neighbourhoods:

| Pair | Shared neighbours | Similarity |
|---|---|---|
| A and B — same tight group | 2 | 0.500 |
| A and E — opposite halves | 1 | 0.167 |
| **C and E — the two bridge ends** | **0** | **0.000** |

C and E are **directly connected to each other**. Theirs is the single most
important relationship in the entire graph — the only thing holding the two
halves together. Remove it and the network splits.

Their structural similarity is **exactly zero**, because they share no
neighbours at all.

This is not a bug to be fixed. It is what the measure means. But it has a sharp
consequence: if you use similarity to suggest "related things", it will
systematically miss precisely the relationships that matter most — the ones that
bridge otherwise separate parts of your graph. Part 3B measures how often that
happens on real data.

**Cost trap.** Comparing every pair is quadratic. Ten thousand nodes means fifty
million comparisons; a million nodes is out of reach entirely. Usable
implementations only compare nodes that already share at least one neighbour.

## 7. Projection — the idea everything rests on

If you take one thing from this document, take this one.

**You almost never want to analyse everything.** You want "just the people, and
just the works-with relationships". Or "just this one department". A
**projection** is that selection: a temporary working copy holding only the slice
you care about.

And it is not merely a filter — **a projection can create connections that do not
exist in the stored data.**

Take the `crime` graph: 829 people and 551 crimes, edges only between them. You
cannot ask "which person is most central among people", because no two people are
connected at all. So you *derive* a graph: connect two people when they were
involved in the same crime.

```python
from networkx.algorithms import bipartite
from gdslab import loaders

G = loaders.load("crime")
sides = loaders.sides("crime")
people = [n for n in G if sides[n] == 0]

P = bipartite.projected_graph(G, people)
print(G.number_of_edges(), "->", P.number_of_edges())   # 1476 -> 2253
```

Those 2,253 person-to-person edges appear in no data file anywhere. They are
derived, they are exactly what makes the question answerable — and they are your
choice, not the data's.

**And projection can explode.** Same operation on `unicodelang`:

| Graph | Original edges | Projected edges | Blow-up |
|---|---|---|---|
| `crime` → people | 1,476 | 2,253 | 1.5× |
| `unicodelang` → territories | 1,255 | **12,552** | **10.0×** |

Why the difference? **The blow-up is driven by the degree of the side you are
projecting *away*, and it is quadratic in that degree.**

A node on the away-side with degree *d* connects all *d* of its neighbours to
each other — that is *d*(*d*−1)/2 edges from one node.

- Projecting `crime` onto people collapses the **crimes**. The largest crime
  involved 18 people, so it contributes 18×17÷2 = **153** edges.
- Projecting `unicodelang` onto territories collapses the **languages**. The most
  widespread language is spoken in 141 territories, so it contributes
  141×140÷2 = **9,870** edges — on its own, nearly eight times the entire
  original graph.

That single node is most of the 10× blow-up. Which is the practical lesson: to
predict whether a projection will explode, do not look at how many edges you
have. Look at the *maximum degree on the side you are about to collapse*.

Part 4 is entirely about what projection does to your answers.

## 8. Where the answer goes

The same algorithm can be run five different ways, and choosing wrongly is how
people accidentally write a billion rows into a database:

| Mode | What it does | When |
|---|---|---|
| **estimate** | reports how much memory it would need, runs nothing | always, before anything large |
| **stats** | summary numbers only — how many groups, what score range | cheaply tuning settings |
| **stream** | returns rows to the caller, stores nothing | exploring |
| **mutate** | writes into the working copy only | chaining one algorithm into another |
| **write** | saves into the database | results an application will query |

The one people skip is **estimate**, and it is the one that saves you. Its whole
purpose is turning an out-of-memory crash into a sentence: *"this needs 40 GB,
you have 8, narrow your selection."*

Notice also that "return one row per node" is not a safe default. On a large
graph it is not slow — it is impossible.

## 9. What this pack does and does not cover

**Covered:** centrality, community detection, similarity, path finding,
projection, and how to measure any of it honestly.

**Not covered:** embeddings and graph machine learning. They need training data,
a model lifecycle and usually a GPU, and they are validated statistically rather
than by re-computation — a different discipline. Mentioned so you know the shape
of the field, not so you can skip them silently.

**One honest limit on the whole field.** Graphs do not beat ordinary search at
everything. On simple factual lookups they add very little and cost considerably
more to build. The gain appears on questions needing several connected steps.
Anyone telling you graphs are always better is selling something — and one of
your claim-verification rows asks you to check that specific claim.

---

## Check yourself

You should be able to answer these without looking back. If you cannot, reread
the section rather than pressing on.

1. Why is "which node is most central?" not a well-formed question?
2. Two runs of Louvain give different groupings. Is that a bug?
3. C and E are the most important pair in the bridge graph and their similarity
   is 0.000. Why, and is it wrong?
4. `ca-GrQc` has more nodes than `facebook_combined` but betweenness runs twice
   as fast on it. Why?
5. Projecting `unicodelang` turns 1,255 edges into 12,552. What controls that
   number?

---

**Next:** [how-we-work.md](how-we-work.md) — the shortest document here and the
one most worth taking seriously.
