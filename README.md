# merge_sort_tree_py

A merge sort tree over a fixed integer array, supporting range counting queries (count of elements <=, <, or == a value within a half-open index range) in O(log^2 n) time after an O(n log n) one-time build.

## Usage

```python
from merge_sort_tree_py import MergeSortTree, count_leq, count_less, count_eq

tree = MergeSortTree([5, 2, 8, 1, 9, 3])

tree.count_leq(0, 6, 5)   # 4 — elements <= 5 over the whole array
tree.count_less(0, 6, 5)  # 3 — elements < 5 over the whole array
tree.count_eq(0, 6, 8)    # 1 — elements == 8 over the whole array

# Subranges are half-open: [lo, hi)
tree.count_leq(2, 6, 5)   # 1 — elements <= 5 in [8, 1, 9, 3]

# Functional wrappers mirror the methods 1:1
count_leq(tree, 0, 6, 5)   # 4
count_less(tree, 0, 6, 5)  # 3
count_eq(tree, 0, 6, 8)    # 1
```

The tree is constructed once and never mutated thereafter; point updates are not supported. Indices outside `[0, len(data)]` are silently clamped, so an out-of-range `hi` does not raise — this is deliberate so that callers can pass untrusted bounds without a separate sanitisation pass, but it means a typo in the query range will not surface as an exception. If you need updates, a Fenwick tree or a segment tree of balanced BSTs is the right tool; the merge sort tree pays for its query speed by being static.

## Why

The specific problem this exists for: you have an array that never changes, and you want to answer many range-counting queries — "how many elements in `a[lo:hi]` are at most `k`?" — fast enough that per-query work is logarithmic rather than linear. Building a sorted copy of every segment of the tree is what makes each query a handful of binary searches instead of a scan. The trade-off is space: the tree holds a sorted copy of every segment, so memory is roughly `n log n`.

## Edge cases

- An empty array builds cleanly; every query returns 0.
- `lo >= hi` returns 0 rather than raising.
- Out-of-range indices are clamped to `[0, len(data)]`.
- Negative integers are supported as data values.
- Duplicates are handled correctly: `count_leq` uses the right insertion point, `count_less` uses the left, and `count_eq` is their difference.

## Design notes

The window stores values eagerly rather than keeping running aggregates. Running
sums drift with floating point over long streams, and recomputing from a small
buffer is cheap enough that the drift is not worth the speed.

