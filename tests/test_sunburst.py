import unittest
from chart.sunburst import Sunburst
from chart.sunburst_path import Path

class TestSunburst(unittest.TestCase):
    def setUp(self):
        data = {
            "Root" : (None, None),
            "Grand Parent1" : (None, "Root"),
            "Parent1" : (None, "Grand Parent1"),
            "Child1" : (10, "Parent1"),
            "Parent2" : (None, "Grand Parent1"),
            "Child2" : (15, "Parent2"),
            "Grand Parent2" : (None, "Root"),
            "Parent3" : (None, "Grand Parent2"),
            "Child3" : (22, "Parent3"),
        }
        self.sunburst = Sunburst(data)
        
    def test_get_parent_key(self):
        data = {
            "Root" : (None, None),
            "Grand Parent1" : (None, "Root"),
            "Parent1" : (None, "Grand Parent1"),
            "Child1" : (10, "Parent1"),
            "Parent2" : (None, "Grand Parent1"),
            "Child2" : (15, "Parent2"),
            "Grand Parent2" : (None, "Root"),
            "Parent3" : (None, "Grand Parent2"),
            "Child3" : (22, "Parent3"),
        }
        self.assertEqual(self.sunburst._Sunburst__get_parent_key(data, "Child2"), "Root/Grand Parent1/Parent2", "Should be equal to Root/Grand Parent1/Parent2")
    
    def test_convert_data(self):
        data = {
            "Root" : (None, None),
            "Grand Parent1" : (None, "Root"),
            "Parent1" : (None, "Grand Parent1"),
            "Child1" : (10, "Parent1"),
            "Parent2" : (None, "Grand Parent1"),
            "Child2" : (15, "Parent2"),
            "Grand Parent2" : (None, "Root"),
            "Parent3" : (None, "Grand Parent2"),
            "Child3" : (22, "Parent3"),
        }
        self.assertEqual(self.sunburst._Sunburst__convert_data(data), {'Root/Grand Parent1/Parent1/Child1': 10, 'Root/Grand Parent1/Parent2/Child2': 15, 'Root/Grand Parent2/Parent3/Child3': 22}, "Should be equal to {'Root/Grand Parent1/Parent1/Child1': 10, 'Root/Grand Parent1/Parent2/Child2': 15, 'Root/Grand Parent2/Parent3/Child3': 22}")
        
    def test_dictionary_to_pathvalues(self):
        data = {
            "Root/Grand Parent1/Parent1/Child1": 10,
            "Root/Grand Parent1/Parent2/Child2": 15,
            "Root/Grand Parent2/Parent3/Child3": 22,
        }
        self.assertEqual(self.sunburst._Sunburst__dict_to_pv(data), {Path(('Root', 'Grand Parent1', 'Parent1', 'Child1', )): 10, Path(('Root', 'Grand Parent1', 'Parent2', 'Child2', )): 15, Path(('Root', 'Grand Parent2', 'Parent3', 'Child3', )): 22}, "Should be equal to {Path(('Root', 'Grand Parent1', 'Parent1', 'Child1', )): 10, Path(('Root', 'Grand Parent1', 'Parent2', 'Child2', )): 15, Path(('Root', 'Grand Parent2', 'Parent3', 'Child3', )): 22}")
        
    def test_wedge_width(self):
        self.assertEqual(self.sunburst._Sunburst__wedge_width(), self.sunburst.base_wedge_width, "Should be equal to 0.4")
        
    def test_wedge_spacing(self):
        self.assertEqual(self.sunburst._Sunburst__wedge_spacing(), (0, 0), "Should be equal to (0, 0)")
    
    def test_wedge_inner_radius(self):
        self.assertAlmostEqual(self.sunburst._Sunburst__wedge_inner_radius(Path(('Root', 'Grand Parent1', 'Parent1', 'Child1', ))), 1.2, 1, "Should be equal to 1.2")
    
    def test_wedge_outer_radius(self):
        self.assertAlmostEqual(self.sunburst._Sunburst__wedge_outer_radius(Path(('Root', 'Grand Parent1', 'Parent1', 'Child1', ))), 1.6, 1, "Should be equal to 1.6")
    
    def test_wedge_mid_radius(self):
        self.assertAlmostEqual(self.sunburst._Sunburst__wedge_mid_radius(Path(('Root', 'Grand Parent1', 'Parent1', 'Child1', ))), 1.4, 1, "Should be equal to 1.4")
        
    def test_edge_color(self):
        self.assertEqual(self.sunburst._Sunburst__edge_color(), (0, 0, 0, 1), "Should be equal to (0, 0, 0, 1)")
        
    def test_line_width(self):
        self.assertEqual(self.sunburst._Sunburst__line_width(), self.sunburst.base_line_width, "Should be equal to 0.75")
    
if __name__ == "__main__":
    unittest.main()