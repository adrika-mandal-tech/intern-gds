# How we work

Ten minutes, and the most important page in this folder.

These are not abstract values. Every rule below is here because ignoring it
produced a wrong number, and most of the stories come from **building this
pack** — they happened while assembling the very files you are about to use.

---

## 1. Evidence before assertions

**Never claim something is done, working, or verified until you have run the
check and read the output.**

Not "this should work". Not "I checked it carefully". Run it, read what came
back, then say what you found.

> While preparing the seven graphs in this pack, three of them came out with
> different node and edge counts from the numbers published on their source
> pages. Every one had an innocent explanation. Every one *also* had to be
> reconciled to the exact number before it could be shipped, because "probably
> self-loops" is not a reconciliation — it is a guess wearing a lab coat.
>
> They turned out to be: 642 self-loops in one, a file listing every edge twice
> in another, and 29,864 duplicate airline routes in the third. The arithmetic
> now matches exactly, and it is written down in
> [`03-data/README.md`](../03-data/README.md) so you can check it rather than
> believe it.

The habit is: when a number surprises you, do not explain it. **Reconcile it.**
An explanation that does not produce the exact number is not an explanation.

## 2. A number that never moves isn't measuring anything

Before you trust a measurement, ask: **what would make this number go down?**

> Two graphs in this pack report a clustering coefficient of exactly 0.000. It
> is tempting to note it and move on. But clustering counts triangles, and both
> graphs are bipartite, and a bipartite graph **cannot contain a triangle** —
> every edge crosses between the two sides, so you can never get back to where
> you started in three steps.
>
> Zero was the only value that metric could ever have returned on that data. It
> was not measuring those graphs. It was reporting a property of arithmetic.

If you cannot describe the result that would have made your number come out
differently, you have not got a measurement — you have got a reassuring number.

## 3. Time the right thing, and warm up first

> The first call to `pagerank` on a 77-node graph took **0.3239 seconds**. The
> next three took **0.0012 seconds**. That is a factor of **270**, on a graph
> small enough to draw by hand.
>
> Nothing about the algorithm changed. The first call paid for imports and
> lazily-built internals. Timing it would have measured Python's start-up costs
> and called them PageRank.

So: `gdslab.runs.timed()` discards a warm-up call by default. Use it. And time
**loading** separately from **computing** — they scale differently, are caused
by different things, and if you report one number you will not know which one to
fix.

## 4. Report ratios, not absolute times

Your laptop and your colleague's laptop are different machines. So:

- **"86 seconds"** tells the reader nothing unless they know your hardware.
- **"twice as long as `ca-GrQc`, on the same machine"** survives being read by
  anybody, on any machine, next year.

Always state absolute times *with* the machine, and always give the ratio too.
Every results file this pack writes carries a `.provenance.json` sidecar naming
the platform, CPU count, RAM and library versions, precisely so that a timing can
still be interpreted six months later.

Part 1 makes this concrete: you and your colleague will run identical code on
different machines and compare what survives.

## 5. Describe the graph, not just its size

> `ca-GrQc` has 5,241 nodes. `facebook_combined` has 4,039 — twenty-three
> percent fewer. Exact betweenness takes **41.4 s** on the bigger one and
> **85.7 s** on the smaller one.

"How big is your graph" is very nearly a meaningless question. Report the shape:
edge count, degree spread, how many components. A statement like "this handles
graphs of five thousand nodes" is not a claim anyone can check.

## 6. Never compare educated guesses by equality

Community detection, and a good deal else, uses heuristics seeded with
randomness. **Two runs on identical input can legitimately return different
answers.**

So a test of the form "did we get the same grouping?" will fail for reasons that
have nothing to do with correctness. Compare the **quality score** instead, over
many runs, and report the distribution.

> A different grouping is not a worse grouping. If you want to claim one is
> worse, you have to measure how much worse and say over how many runs.

## 7. Establish repeatability before comparing anything

If you have not first established that a thing gives a stable answer, then
comparing two of them is comparing two coin flips.

This is the entire reason Part 2B comes before Part 3B. You find out how much a
single algorithm varies with itself *before* you try to say anything about how it
compares to another one.

## 8. A sample of one is not a rate

"Louvain produced a disconnected community" is an anecdote. **"Across 50 runs on
5 graphs, 3.2% of communities were internally disconnected"** is a finding.

Every rate you report needs its sample size attached, in the same sentence. The
part checkers look for this, crudely, and will nag you if a memo states a
percentage with no `n=` anywhere in it.

This cuts both ways. If you only ran it once, say "one run" — do not round it up
into language that implies more.

## 9. Record *why*, not just *what*

When you make a judgement call, write the reasoning next to the answer.

Three weeks later nobody can reconstruct why you excluded that graph, or chose
that threshold, and the result becomes unusable — you cannot check reasoning you
cannot see.

This applies double to **negative** results. "We tested for X and did not find
it, here is the rate and the sample size" is genuinely useful and stops the next
person spending a day rediscovering it. Write it up with the same care as a
positive result.

## 10. "I don't know" is a complete and acceptable answer

There is no penalty here for not knowing. There is a real penalty for guessing
and presenting it as fact, because somebody downstream will build on it.

The good form is:

> *"I could not determine X. I checked A, B and C. A was inconclusive because…,
> B and C did not cover it. What I would try next is D."*

That is a useful deliverable. "Probably around 60%" is not.

## 11. Break it, and confirm your check notices

**A test that has never been seen to fail is not evidence.**

Before you trust a check — one of ours or one you wrote — deliberately feed it
something wrong and confirm it complains. Every checker in this pack was built
that way; the tests in `tests/test_check.py` are written in pairs, one proving
each check passes good input and one proving it *fails* bad input.

Do the same with your own analysis scripts. If your code reports "0 disconnected
communities", hand it a deliberately disconnected community and make sure it says
1. Otherwise you have not learned that there are none; you have learned nothing
at all.

## 12. What good work looks like here

- It says what was measured, on what data, with what sample size.
- Its claims can be checked by someone else without asking you questions.
- It records the judgement calls and the reasoning behind them.
- It reports what did not work as clearly as what did.
- It says "I don't know" where that is the truth.

None of that requires seniority or prior knowledge of graphs. It is just
discipline, and it is most of the job.

---

## A note on the two of you

You are working alongside each other, and you will talk. That is fine and we are
not going to pretend otherwise.

But it does mean one thing: when you compare results at the end of a part, you
are **not** independent observers who happened to agree. You are two people who
have been discussing method all week. That is still worth something — running the
same protocol on two machines catches real problems — but it is a weaker claim
than blind agreement, and the honest thing is to say so.

So whenever you compare notes, record it: what did you discuss, and when? A
sentence is enough. It costs you nothing and it lets a reader weight your
agreement correctly.

---

**Next:** [glossary.md](glossary.md), then your part brief.
