import unittest
from chart.icicle import Icicle
from matplotlib.figure import Figure

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

    def test_get_figure(self):
        self.assertTrue(isinstance(self.icicle.get_figure(), Figure))

    def test_calculate_color(self):
        self.assertEqual(self.icicle._Icicle__calculate_color(1280), 'white', "Should equal to white")

    def test_duplicate_object(self):
        dup_data = self.icicle._Icicle__duplicate_object(self.data)
        self.assertEqual(dup_data,self.data)

    def test_calculate_color_middle_value(self):
        self.min = 100
        self.max = 500
        self.assertEqual(self.icicle._Icicle__calculate_index(0.9,0.4,200), 0.65, "Should equal to 0.65")

    def test_calculate_color_min_value(self):
        self.min = 100
        self.max = 500
        self.assertEqual(self.icicle._Icicle__calculate_index(0.9, 0.4, 100), 0.4, "Should equal to 0.4")

    def test_calculate_color_max_value(self):
        self.min = 100
        self.max = 500
        self.assertEqual(self.icicle._Icicle__calculate_index(0.9, 0.4, 500), 1.4, "Should equal to 0.9")

if __name__ == "__main__":
    unittest.main()
