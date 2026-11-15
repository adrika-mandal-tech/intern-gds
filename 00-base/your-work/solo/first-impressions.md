# First Impressions — solo

*Written before understanding the full project. Ten minutes total.*

---

## Confusions, Opacities, "Why would anyone do that?"

### 1. Term used before definition
- "Modularity" looked important, but I did not yet know whether it was a quality score, a community metric, or a design choice.
- "Bridge edges" and "fragile communities" were unfamiliar terms at first glance.

### 2. Sentence read twice
- The phrase about Louvain/Leiden differences needed a second pass because it sounded like a general claim but was really a measured result on specific graphs.
- The projection discussion also needed rereading because the same graph could look very different after a bipartite-to-unipartite transformation.

### 3. "Why would anyone do that?" moments
- Projection was the biggest one: turning a bipartite graph into a single-mode graph changes the meaning of the data, and it is not obvious that this should be done without caution.
- Comparing multiple centrality measures also felt odd at first because each metric answers a different question, yet they were being ranked against one another.

### 4. Concepts that seem backwards
- It was surprising that a graph could have a strong community score while still being poor for downstream interpretation.
- I initially assumed larger graphs would always be harder, but the real story was more about structure and degree skew than raw node count.

### 5. Assumptions I'm making that might be wrong
- I assumed the benchmark would be dominated by size effects; after reading more closely, structure and skew matter at least as much.
- I assumed community detection quality was a single fixed number, but the project shows that different metrics can disagree even when the same partition is used.

---

**Time spent:** ~10 minutes  
**Date:** 2026-08-24