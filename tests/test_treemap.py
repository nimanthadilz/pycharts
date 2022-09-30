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
        self.assertEqual(converted_data, expected_data)

    def test_calculate_node_value_1(self):
        key_list = ["Documents", "School", "Assignment", "Personal", "CV"]
        return_value = self.treemap._Treemap__calculate_node_value("CV", key_list)
        self.assertEqual(return_value, 200)
    
    def test_calculate_node_value_2(self):
        key_list = ["Documents", "School", "Assignment", "Personal", "CV"]
        return_value = self.treemap._Treemap__calculate_node_value("School", key_list)
        self.assertEqual(return_value, (("Assignment", 100),))

    def test_get_node_name(self):
        self.assertEqual(self.treemap._Treemap__get_node_name(("Cecil", 20)), "Cecil")

    def test_get_node_value_1(self):
        self.assertEqual(self.treemap._Treemap__get_node_value(("Cecil", 20, None)), 20)

    def test_get_node_value_2(self):
        self.assertEqual(self.treemap._Treemap__get_node_value(("Cecil", (("A", 3), ("B", 5)), 8)), 8)
if __name__ == "__main__":
    unittest.main()

