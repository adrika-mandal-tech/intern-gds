# B6 — Do weights change the groups, or only the routes?

**Output:** `your-work/<your-name>/bench/B6/`

---

## The question

Part 3A measured what happens to *shortest paths* when you ignore edge weights:
90% of routes change, and some by a large factor.

Community detection also accepts weights, and every experiment in this pack ran
it **unweighted** — `loaders.load(name, weighted=False)`, deliberately, so the
comparisons were like for like.

> **Was that a free choice? Do weights change which nodes end up grouped
> together, or only which routes are shortest?**

## Method

Two graphs carry weights, and they carry **opposite kinds** of weight — which is
the most interesting thing about this experiment:

| Graph | Weight | Bigger means |
|---|---|---|
| `openflights` | distance in km | **further apart** — a cost |
| `lesmis` | shared scenes | **closer together** — a strength |

Community detection interprets a weight as *strength of connection*. So:

- On `lesmis`, feeding the weights straight in is correct.
- On `openflights`, feeding the weights straight in tells the algorithm that the
  longest flights are the strongest relationships. **Which is backwards.**

That second case is the experiment. Run it wrong on purpose, see what you get,
then work out what the right transformation would be (there is more than one
defensible answer — `1/distance`, `max - distance`, something else) and try it.

## The protocol

For each graph and each treatment (unweighted / weighted-as-is /
weighted-corrected where applicable):

- Run Louvain with many seeds. You know from Part 2B that one run is noise.
- Record: number of communities, modularity, and ARI against the **unweighted**
  grouping.
- The ARI is the headline: it says how much the membership actually moved.

## Questions to answer

1. **How much does weighting change the grouping?** Give the ARI, with its spread
   across seeds.
2. **Is that change bigger than the run-to-run variation you measured in Part
   2B?** If it is not, then weighting changed nothing you could detect, and you
   should say so. This comparison is the whole point of the experiment — without
   it you cannot tell a real effect from noise.
3. On `openflights`, how different is backwards-weighted from correctly-weighted?
   Does the wrong version look obviously wrong from the output alone, or does it
   produce plausible-looking communities?
4. That last part is the sharp question: **if you had been handed the backwards
   result with no context, would anything have told you it was wrong?**
5. Which transformation of distance-to-strength did you choose, and why? What
   would a different choice have done?

## Why it matters

Question 4 generalises well past this experiment. A cost silently treated as a
strength produces a complete, confident, well-formed answer to a question nobody
asked — and there is no error message anywhere in the pipeline. The only defence
is knowing which kind of number you have before you start.
