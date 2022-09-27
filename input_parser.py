import csv
from pprint import pp
import pprint
from exceptions import ParseError

class Parser:
    def __init__(self):
        self.nodes = {}

    def clear_nodes(self):
        self.nodes = {}

    def parse(self, file_obj):
        csv_reader = csv.reader(file_obj, delimiter=",")
        row_count = 0
        for row in csv_reader:
            if row_count == 0:
                if not self._validate_first_row(row):
                    raise ParseError("Invalid first line: Line 1")
            else:
                if not self._validate_row(row):
                    raise ParseError(f"Invalid entry: Line {row_count + 1}")
                self._add_node(row)
            row_count += 1
        return self.nodes

    def _validate_first_row(self, first_row):
        if len(first_row) == 2 and first_row[0] == "name" and first_row[1] == "value":
            return True
        return False

    def _validate_row(self, row):
        if (
            len(row) == 2 and
            (row[1]=="" or row[1].replace(".", "").isdigit()) and
            self._validate_name(row[0])
        ):
            return True
        return False
    
    def _validate_name(self, name):
        node_names = name.split(".")
        if node_names[-1] in self.nodes:
            return False
        for name in node_names[:-1]:
            if not name in self.nodes:
                return False
        return True
    
    def _add_node(self, row):
        node_names = row[0].split(".")
        node_name = node_names[-1]
        parent_name = None
        if len(node_names) > 1:
            parent_name = node_names[-2]
        value = None if row[1]=="" else float(row[1])
        self.nodes[node_name] = (value, parent_name)
