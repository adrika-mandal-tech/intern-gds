# B3 — Can Louvain see small communities at all?

**Output:** `your-work/<your-name>/bench/B3/`

---

## The question

Modularity-based community detection has a known structural limitation called the
**resolution limit**: below a certain size, communities cannot be found — not
because the algorithm is not clever enough, but because merging them *increases*
the modularity score. The algorithm is working perfectly and returning the wrong
answer, because the objective it optimises does not want the right one.

> **Plant small communities in a graph where you know the truth. Does Louvain
> find them?**

This is one of the two bench experiments most likely to produce something we did
not already know, because it is easy to state and rarely measured.

## Method

`03-data/make_synthetic.py` gives you `planted_partition(groups, per_group,
p_in, p_out, seed)` and returns the true grouping alongside the graph.

The experiment: hold the total node count roughly constant and vary how the
nodes are divided up.

- 4 groups of 100
- 10 groups of 40
- 25 groups of 16
- 50 groups of 8
- 100 groups of 4

For each: run Louvain (many seeds — you know from Part 2B that one run tells you
nothing), and score against the planted truth with ARI and NMI. Also record how
many communities it found against how many you planted.

## Questions to answer

1. **At what group size does recovery break down?** Give the number, with the ARI
   at each step.
2. When it fails, **how does it fail?** Does it merge small groups into bigger
   ones, split them, or scatter them? Compare `n_communities` found against
   planted — that one comparison tells you which.
3. **Does the modularity of the wrong answer exceed the modularity of the true
   grouping?** This is the crux. Compute modularity of the planted truth and of
   Louvain's output, and put them side by side.

   If Louvain's answer scores *higher* than the truth, then the algorithm did not
   fail — **the objective did**, and no amount of running it better would help.
   That is a genuinely different kind of bug and it is worth stating carefully.
4. Does Leiden do better? It has the same objective, so predict first.
5. Does raising `p_in` (making the small groups denser and more obvious) rescue
   them, or is size the binding constraint regardless?

## Why it matters

If small communities cannot be recovered, then any system that groups things and
then describes each group will silently never mention the small ones. They do not
appear as an error. They appear as an absence, which is much harder to notice.

## A caution

Keep `p_in` and `p_out` fixed while you vary group size, or you are changing two
things at once and cannot attribute the result to either. If you do decide to
vary both, do it as a second sweep, not the same one.
