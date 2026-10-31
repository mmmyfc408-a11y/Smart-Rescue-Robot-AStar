"""Run: python -m unittest discover -s tests -v"""
import unittest
from algorithm import EMPTY, WALL, DANGER, astar, manhattan


class AStarTests(unittest.TestCase):
    def test_shortest_path(self):
        result = astar([[0, 0, 0], [0, 1, 0], [0, 0, 0]], (0, 0), (2, 2))
        self.assertEqual(result["cost"], 4)
        self.assertEqual(len(result["path"]), 5)
        self.assertGreater(result["explored"], 0)

    def test_avoids_expensive_danger(self):
        result = astar([[0, 2, 0], [0, 0, 0]], (0, 0), (0, 2))
        self.assertEqual(result["cost"], 4)
        self.assertNotIn((0, 1), result["path"])

    def test_no_route(self):
        result = astar([[0, 1, 0], [1, 1, 1], [0, 1, 0]], (0, 0), (2, 2))
        self.assertIsNone(result["path"])
        self.assertIsNone(result["cost"])

    def test_same_start_goal(self):
        result = astar([[EMPTY]], (0, 0), (0, 0))
        self.assertEqual(result["cost"], 0)
        self.assertEqual(result["path"], [(0, 0)])

    def test_blocked_goal(self):
        self.assertIsNone(astar([[0, WALL]], (0, 0), (0, 1))["path"])

    def test_bad_shape(self):
        with self.assertRaises(ValueError):
            astar([[0], [0, 0]], (0, 0), (1, 1))

    def test_heuristic(self):
        self.assertEqual(manhattan((1, 2), (4, 6)), 7)


if __name__ == "__main__":
    unittest.main()
