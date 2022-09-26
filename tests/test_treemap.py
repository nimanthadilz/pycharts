import unittest
from chart.treemap import Treemap

class TestTreemap(unittest.TestCase):
    def setUp(self):
        data = {
            "Documents": (None, None),
            "School": (None, "Documents"),
            "Assignment": (100, "School"),
            "Personal": (None, "Documents"),
            "CV": (200, "Personal")
        }
        self.treemap = Treemap(data)

    def test_get_node_value(self):
        self.assertEqual(self.treemap._Treemap__get_node_value(("node1", 23)), 23, "Should equal 23")

if __name__ == "__main__":
    unittest.main()

