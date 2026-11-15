# Start here

Welcome. This folder is everything you need for this project.

You do not need any accounts, API keys, servers or internet access after setup.
Everything runs offline on your own laptop. You need Python 3.10+, a text editor,
and about fifteen minutes to install some libraries.

Read this page top to bottom before anything else. Ten minutes.

---

## 1. What you are doing, in one paragraph

Graphs — things and the connections between them — can be asked a kind of
question that ordinary databases cannot answer. Not "who does this person report
to", which is written down somewhere, but "if one person left, whose departure
would cut the most teams off from each other", which is written down nowhere and
exists only in the shape of the whole network. A family of algorithms computes
answers to that second kind of question. **You will run those algorithms on real
public data and find out how well they actually work** —
where they agree, where they disagree, how repeatable they are, how much they
cost, and where they confidently return something that is not true.

That last part is most of the value. Plenty of material describes what these
algorithms are supposed to do. Far less measures what they actually do.

## 2. There are two of you, and that is deliberate

You will work through four parts. Some you both do; some you split.

| | What happens |
|---|---|
| **Part 1** | You both run the **same** experiments, on your **own** machines, and compare |
| **Parts 2–3** | You split: one of you takes centrality and paths, the other communities and similarity |
| **Part 4** | Back together for a shared capstone, plus each of you re-runs the other's headline result |

Part 1 is not busywork or duplicated effort. Two people running identical code on
two different laptops is a genuine experiment, and its result — *which numbers
survive a change of hardware and which do not* — is something neither of you can
discover alone.

**Do the parts strictly in order, and do not read ahead.** You have all four in
front of you, which makes that a matter of discipline rather than a fact of
delivery — so here is why it matters.

The parts build on each other. Part 2 tells you how much an algorithm varies with
itself, and Part 3 cannot be interpreted without that number. More importantly,
two of the later briefs state published claims that you are then asked to
measure. If you read those first, you will know what you are "supposed" to find
before you find it, and neither of us will ever be able to tell whether your
result was independent.

That is not a rule we can enforce. It is just the difference between a
measurement and a confirmation.

**Running alongside all four parts** there is a second, smaller task: verifying
twelve widely-cited claims about graph algorithms against their original sources.
A small slice alongside each part. It needs no code at all, and it is
deliberately interleaved so you switch between measuring things and reading
carefully. See [`06-claims/BRIEF.md`](06-claims/BRIEF.md) — start it at the end
of Part 1, not all at the end.

If a part stalls — a run fails, you are waiting on your colleague — there are six
self-contained spare experiments in [`05-bench/`](05-bench/README.md). They are
for when you are **blocked**, not for when you finish early; if you finish early,
each brief tells you how to go deeper instead.

## 3. Read these first, in order

Do these in order. Do not skip to the experiments.

1. **This page.** You are on it.
2. **[02-setup/SETUP.md](02-setup/SETUP.md)** — install and verify. ~15 min.
   Do this early; if something is going to go wrong, you want to know now.
3. **[01-context/graphs-from-zero.md](01-context/graphs-from-zero.md)** — what a
   graph is, assuming you have never seen one. Read it with a terminal open and
   run the snippets. ~25 min.
4. **[01-context/the-six-families.md](01-context/the-six-families.md)** — what you
   can actually compute, and the traps. ~40 min.
5. **[01-context/how-we-work.md](01-context/how-we-work.md)** — the shortest
   document here and the one most worth taking seriously. ~10 min.
6. **[01-context/glossary.md](01-context/glossary.md)** — skim, then keep it open.
7. **[03-data/README.md](03-data/README.md)** — the seven graphs you will be
   working with. ~10 min.

**Plus one thing you must do before any of it sinks in** — see §4.

Then start your Part 1 brief.

## 4. The ten-minute task that has to happen first

**As you read documents 3–6 above, keep a file open and note down every single
thing that confuses you.** Every term used before it is defined, every sentence
you had to read twice, every point where you thought "why would anyone do that".

Save it as `your-work/<your-name>/first-impressions.md`. Rough notes are fine —
it should take you ten minutes in total.

This is the only task in the whole pack that becomes **impossible** later. Once
you understand this material you will not be able to remember what was opaque
about it; the knowledge overwrites the memory of not having it. Nobody who
already knows this subject can tell us where the explanations fail. You can, but
only before you learn it.

Do not tidy it up. Do not resolve the confusions first. Write them down while
they are still confusing.

## 5. Where your work goes

Everything you produce goes in **`your-work/<your-name>/`**. Nothing else in this
pack should be edited.

If you think something here is wrong — a number that does not reproduce, an
explanation that contradicts itself, a script that misbehaves — **that is a
finding, and we want it.** Write it in your questions file rather than quietly
fixing it. Finding errors in this pack is genuinely welcome; several exist that
we do not know about yet.

## 6. Four habits

**Keep a log as you go.** Three lines per working session: what you did, what you
found, what blocked you. Start from
[04-templates/research-log-template.md](04-templates/research-log-template.md).
Five minutes, and it is what makes your work reviewable by someone who was not
watching.

**Keep a running questions file.** Start from
[04-templates/questions-template.md](04-templates/questions-template.md). Write
down anything unclear the moment it happens, *even if you resolve it yourself an
hour later*. The ones you resolved yourself are often the most useful, because
they are the gaps in this pack.

**Never guess in a deliverable.** "I could not determine this; here is what I
checked and why it was inconclusive" is a complete, useful answer. A confident
wrong number is not, because somebody will build on it.

**Ask early.** If you are stuck and going in circles, ask. Being stuck quietly is
the only genuinely expensive mistake available to you here — everything else is
recoverable.

## 7. What is in this folder

```
00-base/
├── START_HERE.md            you are here
├── 01-context/              what this is, and how we work
│   ├── graphs-from-zero.md     graphs assuming zero background
│   ├── the-six-families.md     what you can compute, and the traps
│   ├── how-we-work.md          the measurement discipline - read properly
│   └── glossary.md             every term, defined
├── 02-setup/                install and verify
├── 03-data/                 the seven graphs + a generator, and their provenance
├── 04-templates/            start your deliverables from these
├── 05-bench/                extra experiments, for when something stalls
├── 06-claims/               the running claim-verification task
├── gdslab/                  the toolkit you will use
├── tests/                   the toolkit's own tests
└── your-work/               everything you produce
    ├── intern-A/
    └── intern-B/
```

## 8. A word about the toolkit

`gdslab` exists so you spend your time measuring things rather than plumbing. It loads the graphs, times things properly, and writes results in a
consistent shape.

One design decision is worth knowing about, because it will shape how you work:

> **The harness writes one row per run. It never writes a summary.**

If you run something two hundred times you get two hundred rows, and you compute
the average yourself afterwards. This is deliberate. If the tool wrote summaries,
a single run would look identical in the output file to two hundred runs, and
nobody reading your results later — including you — could tell which they were
looking at. Writing the rows makes the sample size impossible to lose.

You are welcome to read the toolkit's source. It is short, and if you find a bug
in it that is a genuinely good outcome.

---

**Next:** [02-setup/SETUP.md](02-setup/SETUP.md)
