# B5 — On an undirected graph, is PageRank worth running?

**Output:** `your-work/<your-name>/bench/B5/`

---

## The question

There is a claim, repeated in this pack's own context documents, that

> *"PageRank on an undirected graph tells you nothing that counting connections
> does not."*

It is stated confidently and it is exactly the kind of claim that gets passed
along without being checked.

> **Check it.**

This is one of the two bench experiments most likely to change something we
believe, because a claim in the teaching material is on the line.

## Why it might be true

On an undirected graph, every edge points both ways. There is a known result that
for a connected undirected graph, a random walk's long-run probability of being
at a node is exactly proportional to that node's degree. PageRank is a damped
random walk, so it ought to land close to degree.

**"Ought to land close to" is not "tells you nothing".** That gap is the
experiment.

## Method

1. Take every graph in the pack, undirected (convert the directed ones).
2. Compute degree and PageRank.
3. Compare properly: Spearman correlation, top-10 and top-50 overlap, and — the
   informative one — **which nodes disagree most, and by how much.**
4. Then do it on the *directed* versions of `email-Eu-core` and `openflights`.
   The claim is specifically about undirected graphs; the contrast is the control.
5. Vary the damping factor. At `alpha` near 0, PageRank should collapse towards
   uniform. At `alpha` near 1, towards the pure random-walk result. **Where in
   that range does it stop resembling degree, if anywhere?**

## Questions to answer

1. **How close is "close"?** Give the correlation, per graph, undirected.
2. Is any node ranked substantially differently by the two? Name it and explain
   why.
3. **Does the claim hold on disconnected graphs?** The theoretical result assumes
   connectivity, and `ca-GrQc` has 354 components. Predict, then measure. This is
   where the claim is most likely to break and it is worth going at properly.
4. How much does the directed case differ? Quantify it.
5. **Verdict:** is the claim in the context document correct, correct-with-
   conditions, or wrong? If it needs conditions, write the sentence that should
   replace it.

## What to do if you find it is wrong

Put it in `questions.md`, tell us, and say what the corrected version should be.

Finding an error in the teaching material is a genuinely good outcome — better
than confirming it. The claim was written into this pack because it appears in
the literature, not because anybody here measured it on these graphs. You would
be the first.
