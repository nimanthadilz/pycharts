import unittest
from matplotlib.figure import Figure
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

    def test_get_figure(self):
        self.assertTrue(isinstance(self.treemap.get_figure(), Figure))

    def test_convert_data(self):
        expected_data = (
                            "Documents", 
                            (
                                (
                                    "School",
                                    (
                                        ("Assignment",
                                            100
                                        ),
                                    )
                                ),
                                (
                                    "Personal",
                                    (
                                        (
                                            "CV",
                                            200
                                        ),
                                    )
                                )
                            )
        )
        converted_data = self.treemap._Treemap__convert_data()
        pp = pprint.PrettyPrinter()
        pp.pprint(converted_data)
        self.assertEqual(converted_data, expected_data)
    

if __name__ == "__main__":
    unittest.main()

