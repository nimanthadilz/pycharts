import unittest
from chart.icicle import Icicle


class TestIciclemap(unittest.TestCase):
    def setUp(self):
        data = {
            "Documents": (None, None),
            "School": (None, "Documents"),
            "Assignment": (100, "School"),
            "Personal": (None, "Documents"),
            "CV": (200, "Personal")
        }
        self.icicle = Icicle(data)

    def test_calculate_color(self):
        self.assertEqual(self.icicle._Icicle__calculate_color(1280), '#337699d', "Should equal to #337699d")


if __name__ == "__main__":
    unittest.main()
