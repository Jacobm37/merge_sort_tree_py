import unittest

from merge_sort_tree_py import MergeSortTree, count_leq, count_less, count_eq


class TestConstruction(unittest.TestCase):
    def test_empty_array(self):
        tree = MergeSortTree([])
        self.assertEqual(len(tree), 0)
        self.assertEqual(tree.count_leq(0, 0, 5), 0)
        self.assertEqual(tree.count_less(0, 0, 5), 0)
        self.assertEqual(tree.count_eq(0, 0, 5), 0)

    def test_single_element(self):
        tree = MergeSortTree([7])
        self.assertEqual(tree.count_leq(0, 1, 10), 1)
        self.assertEqual(tree.count_leq(0, 1, 7), 1)
        self.assertEqual(tree.count_leq(0, 1, 6), 0)
        self.assertEqual(tree.count_less(0, 1, 7), 0)
        self.assertEqual(tree.count_less(0, 1, 8), 1)
        self.assertEqual(tree.count_eq(0, 1, 7), 1)
        self.assertEqual(tree.count_eq(0, 1, 8), 0)

    def test_input_list_is_not_mutated(self):
        data = [5, 3, 1, 4, 2]
        MergeSortTree(data)
        self.assertEqual(data, [5, 3, 1, 4, 2])


class TestQueries(unittest.TestCase):
    def test_basic_count_leq(self):
        tree = MergeSortTree([5, 2, 8, 1, 9, 3])
        self.assertEqual(tree.count_leq(0, 6, 5), 4)
        self.assertEqual(tree.count_leq(0, 6, 100), 6)
        self.assertEqual(tree.count_leq(0, 6, 0), 0)

    def test_count_less_strict(self):
        tree = MergeSortTree([5, 2, 8, 1, 9, 3])
        self.assertEqual(tree.count_less(0, 6, 5), 3)
        self.assertEqual(tree.count_less(0, 6, 1), 0)
        self.assertEqual(tree.count_less(0, 6, 100), 6)

    def test_count_eq_with_duplicates(self):
        tree = MergeSortTree([3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5])
        self.assertEqual(tree.count_eq(0, 11, 5), 3)
        self.assertEqual(tree.count_eq(0, 11, 1), 2)
        self.assertEqual(tree.count_eq(0, 11, 7), 0)

    def test_subrange_query(self):
        tree = MergeSortTree([3, 1, 4, 1, 5, 9, 2, 6])
        self.assertEqual(tree.count_leq(2, 6, 4), 2)
        self.assertEqual(tree.count_eq(2, 6, 1), 1)
        self.assertEqual(tree.count_less(2, 6, 9), 3)

    def test_full_range_leq(self):
        tree = MergeSortTree([1, 2, 3, 4, 5])
        self.assertEqual(tree.count_leq(0, 5, 3), 3)

    def test_single_index_range(self):
        tree = MergeSortTree([10, 20, 30])
        self.assertEqual(tree.count_leq(1, 2, 25), 1)
        self.assertEqual(tree.count_leq(1, 2, 20), 1)
        self.assertEqual(tree.count_leq(1, 2, 15), 0)

    def test_query_boundary_at_end(self):
        tree = MergeSortTree([1, 2, 3, 4, 5])
        self.assertEqual(tree.count_leq(4, 5, 5), 1)
        self.assertEqual(tree.count_leq(4, 5, 4), 0)

    def test_negative_values(self):
        tree = MergeSortTree([-5, -1, -3, 0, -2, 4])
        self.assertEqual(tree.count_leq(0, 6, 0), 5)
        self.assertEqual(tree.count_less(0, 6, 0), 4)
        self.assertEqual(tree.count_eq(0, 6, -3), 1)


class TestEdgeCases(unittest.TestCase):
    def test_empty_range_returns_zero(self):
        tree = MergeSortTree([1, 2, 3])
        self.assertEqual(tree.count_leq(1, 1, 5), 0)
        self.assertEqual(tree.count_less(1, 1, 5), 0)
        self.assertEqual(tree.count_eq(1, 1, 5), 0)

    def test_out_of_range_indices_clamped(self):
        tree = MergeSortTree([1, 2, 3, 4])
        self.assertEqual(tree.count_leq(-5, 100, 3), 3)
        self.assertEqual(tree.count_less(-5, 100, 2), 1)

    def test_lo_greater_than_hi(self):
        tree = MergeSortTree([1, 2, 3])
        self.assertEqual(tree.count_leq(2, 1, 5), 0)
        self.assertEqual(tree.count_less(2, 1, 5), 0)
        self.assertEqual(tree.count_eq(2, 1, 5), 0)

    def test_lo_equals_hi_clamped(self):
        tree = MergeSortTree([1, 2, 3])
        self.assertEqual(tree.count_leq(3, 3, 5), 0)


class TestFunctionalWrappers(unittest.TestCase):
    def test_count_leq_function(self):
        tree = MergeSortTree([5, 3, 1, 4, 2])
        self.assertEqual(count_leq(tree, 0, 5, 3), 3)

    def test_count_less_function(self):
        tree = MergeSortTree([5, 3, 1, 4, 2])
        self.assertEqual(count_less(tree, 0, 5, 3), 2)

    def test_count_eq_function(self):
        tree = MergeSortTree([5, 3, 1, 4, 2])
        self.assertEqual(count_eq(tree, 0, 5, 3), 1)


if __name__ == "__main__":
    unittest.main()
