"""gdslab - the shared toolkit for this pack.

Five modules, each with one job:

    loaders   get a graph out of 03-data/, with its checksum verified
    profile   describe a graph's shape
    runs      the measurement harness - warms up, times, records one row per run
    stats     compare two results (rankings, partitions, communities)
    plots     draw the charts
    check     the validation helpers the per-part checkers are built from

Everything you measure should go through `runs`, because it is what writes the
provenance record - which machine, which library versions, which seed. A number
without that record cannot be checked by anybody else later, including you.
"""

__all__ = ["loaders", "profile", "runs", "stats", "plots", "check"]
