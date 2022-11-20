import unittest
from input_parser import Parser
from exceptions import ParseError
from parameterized import parameterized

class TestParser(unittest.TestCase):
    def setUp(self):
        self.parser = Parser()

    @parameterized.expand([
        ("tests/fixtures/test_invalid_col_names.csv"),
        ("tests/fixtures/test_invalid_num_of_cols.csv"),
        ("tests/fixtures/test_duplicate_rows.csv"),
        ("tests/fixtures/test_invalid_row.csv")
    ])
    def test_invalid_data_files(self, path):
        file_obj = open(path, "r")
        self.assertRaises(ParseError, self.parser.parse, file_obj)
        file_obj.close()

    @parameterized.expand([
        ("tests/fixtures/test_valid_data_1.csv")
    ])

    def test_valid_data_files(self, path):
        file_obj = open(path, "r")
        self.assertTrue(ParseError, self.parser.parse(file_obj))
        file_obj.close()

if __name__ == "__main__":
    unittest.main()

