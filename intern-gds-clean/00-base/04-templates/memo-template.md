# Part N — <the question you were answering>

**Who:** <your name>
**Machine:** <platform, CPU count, RAM — from your provenance sidecar>
**Dates:** <start> to <end>
**Results files:** <list every CSV this memo draws on>

---

## 1. What I did

What you actually ran, in a few sentences. Enough that someone could repeat it
without asking you anything. Name the graphs, the number of runs, the seeds.

If you deviated from the brief in any way, say so here and say why. Deviating is
allowed. Deviating silently is not.

## 2. What I found

The findings themselves. One subsection per finding.

For each one:

- **State the number, with its sample size in the same sentence.**
  "Across 50 runs on 5 graphs, 3.2% of communities were internally disconnected"
  — not "communities are sometimes disconnected".
- Say which graphs it holds on, and which it does not.
- If it varies a lot between graphs, that variation *is* the finding — report the
  spread, do not average it away.

Include the chart if a chart helps. Do not include a chart that merely decorates
a number already in a sentence.

## 3. What surprised me

Anything that came out differently from what you expected, including things you
expected from the context documents. This section is often where the real result
is.

If nothing surprised you, say that — but check first whether that is because you
did not have an expectation written down beforehand.

## 4. What I could not determine

The honest list. For each:

- what you were trying to find out
- what you tried
- why it was inconclusive
- what you would try next

**This is a real section, not an apology.** A clearly-described dead end saves
the next person the day you spent on it.

## 5. Judgement calls

Every point where you had to decide something the brief did not settle: which
threshold, which graphs to exclude, how to handle a tie, what to do about an
outlier.

For each: what you chose, and **why**. Three weeks from now this section is what
makes the rest of the memo checkable.

## 6. Sample sizes and caveats

A short table is ideal:

| Claim | Graphs | Runs | Caveat |
|---|---|---|---|
| | | | |

Then anything a reader should know before quoting you. Small samples, one graph
behaving oddly, a result that only held on synthetic data, anything you ran once
rather than many times.

## 7. Collaboration record

You two work alongside each other, so this is not an accusation — it is
information a reader needs to weight your results correctly.

- What did you discuss with your colleague about this part, and roughly when?
- Did you see any of their numbers before finalising yours?
- Did you share code, or only method?

A few sentences. "We discussed the approach on day 2 and did not compare numbers
until both memos were written" is a perfectly good answer, and so is "we debugged
the runner together and our results are not independent".

---

## Before you submit

- [ ] Every rate has a sample size **in the same sentence**
- [ ] Every number in this memo can be traced to a row in a results CSV
- [ ] The checker for this part passes
- [ ] Nothing here says "the checker passed" as though it meant "this is correct"
- [ ] Section 4 is filled in honestly, including if it is empty and why
- [ ] Your research log covers every day of this part
