# Graphs, from zero

Assumes you have never worked with a graph. About twenty-five minutes.

Read it with a terminal open — every number below comes from a graph that ships
with this pack, and you can reproduce all of them.

---

## 1. What a graph is

A graph is **things, and connections between things**. That is the whole idea.

The things are called **nodes** (or vertices). The connections are called
**edges**. Which is which depends entirely on what you decided to build:

| Nodes | Edges |
|---|---|
| people | "knows" |
| airports | "there is a flight" |
| characters in a novel | "appear in a scene together" |
| words | "appear next to each other" |
| companies | "supplies parts to" |

That is a modelling decision, not a fact about the world, and it is the most
consequential decision in the whole field. The same underlying reality can be
turned into completely different graphs, and they will give completely different
answers. We come back to this in §9 and Part 4 is entirely about it.

Let's use the smallest graph in the pack. Open a terminal in `00-base/`:

```python
from gdslab import loaders
G = loaders.load("lesmis")
print(G)
```

```
Graph with 77 nodes and 254 edges
```

That is *Les Misérables*: 77 characters, and an edge between two of them if they
appear in a scene together.

## 2. Neighbours and degree

Two nodes joined by an edge are **neighbours**. A node's **degree** is how many
neighbours it has.

```python
names = loaders.names("lesmis")
top = sorted(G.degree(), key=lambda kv: -kv[1])[:5]
for node, d in top:
    print(names[node], d)
```

```
Valjean 36
Gavroche 22
Marius 19
Javert 17
Thenardier 16
```

Valjean shares scenes with 36 of the other 76 characters. That is a sensible
answer for the protagonist of *Les Misérables*, and noticing that it is sensible
is a real skill — most of the errors you will make in this work will be caught by
asking "is this answer even plausible?" before asking anything harder.

Degree is the cheapest thing you can know about a node. It is also, on its own,
often misleading — §3 of [the-six-families.md](the-six-families.md) shows a graph
where degree says two nodes are 33% more important than the rest and the truth is
that they are infinitely more important.

## 3. Direction

Some connections go both ways. If you appear in a scene with me, I appear in a
scene with you. That is an **undirected** graph.

Some do not. If I email you, that does not mean you emailed me. If a flight goes
London → Tokyo, there is not automatically one coming back. Those are
**directed** graphs, and each node has an **in-degree** (arrows pointing at it)
and an **out-degree** (arrows leaving it).

```python
E = loaders.load("email-Eu-core")
print(E.is_directed())          # True
print(E.number_of_edges())      # 24929
print(E.to_undirected().number_of_edges())   # 16064
```

Notice the edge count *drops* when you make it undirected: 24,929 becomes 16,064.
That is because a great many pairs emailed each other in both directions, and
those two arrows collapse into one line. **Throwing away direction throws away
information**, and some algorithms are meaningless without it — PageRank in
particular, which we come to later.

## 4. Weight

An edge can carry a number. This is where people go wrong most often, because
the number can mean two opposite things.

**A cost.** How far, how expensive, how long. Bigger is *worse*.

```python
F = loaders.load("openflights")
w = [d["weight"] for _, _, d in F.edges(data=True)]
print(min(w), max(w))     # 2.8   16087.3
```

Those are flight distances in kilometres. The shortest is 2.8 km — two airports
almost on top of each other. The longest is 16,087 km.

**A strength.** How close, how often, how much. Bigger is *better*.

```python
L = loaders.load("lesmis")
w = [d["weight"] for _, _, d in L.edges(data=True)]
print(min(w), max(w))     # 1   31
```

Those are scene counts. Two characters with weight 31 are *closely* connected.

**These are opposites, and no algorithm can tell them apart.** Ask for the
"shortest path" through `lesmis` weights and you will get the route through the
*weakest* relationships in the book, computed perfectly, returned without a
warning. The arithmetic is right and the answer is nonsense.

Whenever you see a weight, the first question is always: does bigger mean closer
or further?

## 5. Paths

A **path** is a sequence of edges taking you from one node to another. The
**shortest path** is the one with fewest edges — or, if the edges carry costs,
the one with the smallest total cost. Those are different questions:

```python
import networkx as nx
F = loaders.load("openflights").to_undirected()

def cost(p):
    return sum(F[p[i]][p[i + 1]]["weight"] for i in range(len(p) - 1))

a, b = "1702", "2745"
hops = nx.shortest_path(F, a, b)                      # fewest flights
cheap = nx.shortest_path(F, a, b, weight="weight")    # shortest distance
print(len(hops) - 1, round(cost(hops)))
print(len(cheap) - 1, round(cost(cheap)))
```

```
5 21226
5 9747
```

Look carefully at that. Both routes are **five flights**. But one covers 21,226 km
and the other 9,747 km — you fly more than twice as far for no saving in stops at
all.

The fewest-hops algorithm did not make a mistake. It was asked which route has
the fewest edges, several routes tie at five, and it returned one of them. It was
never told that some edges are 12,000 km and others are 300 km, so it could not
possibly have taken that into account.

**An algorithm given no weights does not know it is missing anything.** It
returns a confident answer, with no error and no warning, and the answer is
perfectly correct for the question it was actually asked. Part 3 measures how
often this happens and how bad it gets.

The **distance** between two nodes is the length of the shortest path between
them.

## 6. Components

Can you get from any node to any other? Often not. A **component** is a group of
nodes that can all reach each other, with no path to anything outside.

```python
import networkx as nx
C = loaders.load("ca-GrQc")
print(C.number_of_nodes(), nx.number_connected_components(C))
```

```
5241 354
```

`ca-GrQc` is a co-authorship network: an edge means two physicists wrote a paper
together. It falls into **354 separate pieces**. Most research groups have simply
never co-authored with most other research groups, so there is no chain of
collaborations linking them at all.

This matters more than it sounds. "The average distance between two nodes" is
undefined when some pairs have no path at all. Plenty of code silently ignores
that, or crashes, or quietly reports the average over only the pairs that *are*
connected — which is a different statistic wearing the same name.

## 7. Density and clustering

**Density** is what fraction of all possible edges actually exist. A graph where
everyone knows everyone has density 1.0. Real graphs are nearly always far
sparser than people expect:

| Graph | Nodes | Edges | Density |
|---|---|---|---|
| `facebook_combined` | 4,039 | 88,234 | 0.0108 |
| `ca-GrQc` | 5,241 | 14,484 | 0.0011 |

`facebook_combined` has about 1% of its possible edges. `ca-GrQc` has about one
tenth of one percent.

**Clustering** asks a different question: if A knows B and B knows C, does A know
C? Do your friends know each other? It is the fraction of such triples that close
into a triangle.

```python
from gdslab import loaders, profile
for name in ["facebook_combined", "crime"]:
    print(name, round(profile.profile_graph(loaders.load(name), name)["clustering"], 3))
```

```
facebook_combined 0.606
crime 0.0
```

Facebook is 0.606 — friends of friends really are friends, most of the time.

`crime` is **exactly zero**, and that is worth pausing on. Not "nearly zero".
Exactly. Look at §8 for why, and then notice the general lesson: when a
measurement comes back at a suspiciously clean number, the first question is not
"what does this tell me?" but **"could it have come back as anything else?"** A
metric that is structurally incapable of varying is not measuring anything.

## 8. Two-sided (bipartite) graphs

Some graphs have two kinds of thing, and every edge goes *between* the kinds,
never within:

- people ↔ crimes they were involved in
- territories ↔ languages spoken there
- actors ↔ films they appeared in
- **things extracted from documents ↔ the documents they appeared in**

That last one is why this is in the pack.

```python
G = loaders.load("crime")
sides = loaders.sides("crime")
print(sum(1 for v in sides.values() if v == 0),   # 829 people
      sum(1 for v in sides.values() if v == 1))   # 551 crimes
print(any(sides[a] == sides[b] for a, b in G.edges()))   # False
```

No edge ever connects two people directly, or two crimes directly. That is what
"bipartite" means.

**And that is why clustering is exactly zero.** A triangle needs three edges. In
a bipartite graph every edge crosses sides, so after three steps you are back on
the wrong side — you cannot close the triangle. It is not a property of these
particular crimes; it is arithmetic.

Bipartite graphs break more things than clustering. Many algorithms assume,
without ever saying so, that the nodes are all the same kind of thing. Feed them
a two-sided graph and they return confident numbers that mean nothing. Part 4 is
about exactly this.

## 9. Shape, and why it matters more than size

Here is the single most useful thing in this document.

| Graph | Nodes | Edges | Median degree | Max degree | Skew | Components |
|---|---|---|---|---|---|---|
| `facebook_combined` | 4,039 | 88,234 | 25 | 1,045 | 41.8 | 1 |
| `ca-GrQc` | 5,241 | 14,484 | 3 | 81 | 27.0 | 354 |

Those two graphs are about the same *size*. They are not remotely the same
*problem*. `ca-GrQc` has 30% more nodes and six times fewer edges, its typical
node has 3 neighbours instead of 25, and it is in 354 pieces rather than one.

**Skew** — that column — is `max degree ÷ median degree`, how many times more
connected the busiest node is than a typical one. In `facebook_combined` one
person has 1,045 friends while the median has 25. Real networks are almost always
lopsided like this, and the lopsidedness is usually what determines how expensive
an algorithm will be, because the busiest node does the most work and everything
else waits for it.

So: **"how big is your graph" is close to a meaningless question.** When someone
tells you an algorithm handles a million nodes, the correct response is to ask
what shape those nodes were in.

Part 1 asks you to test whether that is actually true, on these graphs, rather
than believe it because this document said so. It might not be. Find out.

## 10. The vocabulary, in one table

| Term | Meaning |
|---|---|
| node / vertex | a thing |
| edge | a connection between two things |
| neighbour | a node one edge away |
| degree | how many neighbours a node has |
| directed | edges have a direction (A→B ≠ B→A) |
| weighted | edges carry a number — **a cost or a strength; check which** |
| path | a sequence of edges from one node to another |
| shortest path | fewest edges, or lowest total cost — different questions |
| distance | length of the shortest path |
| component | a set of nodes that can all reach each other |
| density | fraction of possible edges that exist |
| clustering | do your neighbours know each other? |
| bipartite | two kinds of node, every edge crosses between them |
| skew | max degree ÷ median degree — how lopsided the graph is |

Fuller definitions in [glossary.md](glossary.md).

---

## Before you move on

Run these and make sure each answer makes sense to you. If one surprises you,
write it down — that is exactly the kind of note Part 1 asks for.

```python
from gdslab import loaders, profile
for name in loaders.list_graphs():
    p = profile.profile_graph(loaders.load(name), name)
    print("%-20s N=%-6d E=%-7d skew=%-6.1f components=%d"
          % (name, p["nodes"], p["edges"], p["degree_skew"], p["components"]))
```

---

**Next:** [the-six-families.md](the-six-families.md) — what you can actually
compute once you have a graph.
