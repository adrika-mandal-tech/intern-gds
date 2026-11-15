# B4 — How much does the wrong train/test split inflate a score?

**Output:** `your-work/<your-name>/bench/B4/`

---

## The question

Link prediction guesses which edges *ought* to exist but do not. To test it you
hide some edges, predict them back, and score how many you recovered.

**How you choose which edges to hide decides your score**, and the standard
mistake is severe: split randomly and the model gets to see the future, scores
beautifully, and then collapses when deployed.

> **Measure the inflation. How much better does a random split look than an
> honest one?**

## The complication, and what to do about it

None of the graphs in this pack carry timestamps, so you cannot do a true
temporal split. **Do not pretend otherwise.** Instead, use a structural
substitute and be explicit that it is one:

**Option 1 — degree-biased split.** Hide edges attached to high-degree nodes with
higher probability. This mimics the real situation where new edges attach
preferentially to already-popular nodes.

**Option 2 — component-aware split.** Hide edges whose removal would isolate a
node, versus edges whose removal would not. Random splitting quietly creates
isolated nodes that no method can score.

**Option 3 — hide a whole neighbourhood.** Remove all edges of a randomly chosen
set of nodes, rather than scattered individual edges. This is the closest
structural analogue of "these nodes arrived later".

Option 3 is the most interesting. Pick one, or do two and compare.

## Method

1. Take a graph — `ca-GrQc` and `facebook_combined` are good, different shapes.
2. Hide 10% of edges, two ways: uniformly at random, and by your chosen
   structural rule.
3. Score the same predictor both ways. Adamic-Adar is the standard
   (`nx.adamic_adar_index`); common neighbours is a good simpler baseline.
4. Sample negatives properly — non-edges, as many as positives. **Say how you
   sampled them**, because this choice moves the score as much as the split does.
5. Report precision-at-k, or AUC, or both. Say which and why.
6. Repeat with several seeds. One split is one sample.

## Questions to answer

1. **How much higher is the random-split score?** Give both numbers with their
   spread across seeds.
2. Is the gap the same on both graphs? If not, what differs?
3. **Does the ranking of methods change**, or only the absolute scores? This is
   the practically important one: if random splitting inflates everything
   equally, comparisons between methods survive it. If it inflates some methods
   more than others, published comparisons are unsafe.
4. Your split is a structural substitute for a temporal one. **What would you
   expect a true temporal split to show, and why?** Argue it; do not guess it.
5. What is the smallest change to a typical evaluation that would prevent this
   mistake?

## The trap

It is easy to accidentally leave the hidden edges in the graph you compute
predictions from. Then you are predicting edges you can see, and you will score
close to perfect.

**Check for this explicitly.** If your score is startlingly high, that is the
first thing to suspect — and finding it in your own code is exactly the kind of
thing worth writing up rather than quietly fixing.
