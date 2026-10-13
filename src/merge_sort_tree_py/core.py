from __future__ import annotations

from bisect import bisect_left, bisect_right
from typing import List, Sequence


class MergeSortTree:
    """
    A merge sort tree over a fixed sequence of integers.

    The tree stores, at each node, the sorted slice of the underlying array
    corresponding to that node's segment. Building the tree is O(n log n) in
    time and space, and each query visits O(log n) nodes performing a
    binary search inside each, so queries are O(log^2 n).

    Design choice: the tree is immutable after construction. This keeps the
    queries lock-free and lets us pre-sort each segment once, which is where
    the data structure's value comes from. If you need point updates, a
    merge sort tree is the wrong structure — use a BIT or a segment tree of
    balanced BSTs instead.
    """

    def __init__(self, data: Sequence[int]):
        # We snapshot the input defensively. A caller mutating the list they
        # passed in would otherwise silently invalidate our segment mapping.
        self._data: List[int] = list(data)
        self._n: int = len(self._data)
        self._tree: List[List[int]] = []
        if self._n > 0:
            size = 1
            while size < self._n:
                size <<= 1
            self._tree = [[] for _ in range(2 * size)]
            self._size = size
            self._build(1, 0, size)
        else:
            self._size = 1
            self._tree = [[], []]

    def _build(self, node: int, left: int, right: int) -> None:
        mid = (left + right) >> 1
        if right - left == 1:
            self._tree[node] = [self._data[left]] if left < self._n else []
            return
        self._build(node * 2, left, mid)
        self._build(node * 2 + 1, mid, right)
        # Merge two already-sorted children. Python's sort is timsort, which
        # recognises the two-run input and degrades to a linear merge; doing
        # the merge by hand gains little and risks bugs at the boundaries.
        self._tree[node] = sorted(self._tree[node * 2] + self._tree[node * 2 + 1])

    def count_leq(self, lo: int, hi: int, value: int) -> int:
        """Count elements in data[lo:hi] that are <= value. Range is half-open."""
        if lo < 0:
            lo = 0
        if hi > self._n:
            hi = self._n
        if lo >= hi:
            return 0
        return self._query_leq(1, 0, self._size, lo, hi, value)

    def count_less(self, lo: int, hi: int, value: int) -> int:
        """Count elements in data[lo:hi] that are < value. Range is half-open."""
        if lo < 0:
            lo = 0
        if hi > self._n:
            hi = self._n
        if lo >= hi:
            return 0
        return self._query_less(1, 0, self._size, lo, hi, value)

    def count_eq(self, lo: int, hi: int, value: int) -> int:
        """Count elements in data[lo:hi] that are == value. Range is half-open."""
        return self.count_leq(lo, hi, value) - self.count_less(lo, hi, value)

    def _query_leq(self, node: int, left: int, right: int,
                   lo: int, hi: int, value: int) -> int:
        if lo <= left and right <= hi:
            # bisect_right returns the count of elements <= value in a sorted
            # list, which is exactly what we want.
            return bisect_right(self._tree[node], value)
        mid = (left + right) >> 1
        total = 0
        if lo < mid:
            total += self._query_leq(node * 2, left, mid, lo, hi, value)
        if hi > mid:
            total += self._query_leq(node * 2 + 1, mid, right, lo, hi, value)
        return total

    def _query_less(self, node: int, left: int, right: int,
                    lo: int, hi: int, value: int) -> int:
        if lo <= left and right <= hi:
            return bisect_left(self._tree[node], value)
        mid = (left + right) >> 1
        total = 0
        if lo < mid:
            total += self._query_less(node * 2, left, mid, lo, hi, value)
        if hi > mid:
            total += self._query_less(node * 2 + 1, mid, right, lo, hi, value)
        return total

    def __len__(self) -> int:
        return self._n


def count_leq(tree: MergeSortTree, lo: int, hi: int, value: int) -> int:
    """Functional wrapper around MergeSortTree.count_leq."""
    return tree.count_leq(lo, hi, value)


def count_less(tree: MergeSortTree, lo: int, hi: int, value: int) -> int:
    """Functional wrapper around MergeSortTree.count_less."""
    return tree.count_less(lo, hi, value)


def count_eq(tree: MergeSortTree, lo: int, hi: int, value: int) -> int:
    """Functional wrapper around MergeSortTree.count_eq."""
    return tree.count_eq(lo, hi, value)
