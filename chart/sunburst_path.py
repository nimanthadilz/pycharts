from typing import Dict, Iterable

class Path(tuple):
    """
    The class to represent the directory of a node in a hierarchical type
    
    e.g.
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
        
    path of "Root" is None because it is the root node
    path of "Grand Parent1" is 'Root'
    path of Parent1 is 'Root/Grand Parent1'
    path of ParentChild11 is 'Root/Grand Parent1/Parent1'
    """
    def __new__(cls, __iterable: Iterable[str]):
        for item in __iterable:
            assert isinstance(item, str)
        return super().__new__(cls, __iterable)
    
    def __str__(self) -> str:
        STRING_DELIM = "/"
        return STRING_DELIM.join(self)
    
    def __repr__(self) -> str:
        return "Path(({}, ))".format(
            ", ".join((string.__repr__() for string in self))
        )
        
    def __getitem__(self, key):
        result = tuple.__getitem__(tuple(self), key)
        
        if isinstance(result, tuple):
            return Path(result)
        elif isinstance(result, str):
            return Path((result,))  # do not remove ',' or it's gonna be a str

    def startswith(self, tag):
        if not isinstance(tag, Path):
            raise ValueError(
                "Expecting instance of Path " "but got {}!".format(type(tag))
            )
        if len(tag) > len(self):
            return False
        return self[: len(tag)] == tag

    def parent(self):
        return self[: len(self) - 1]

    def ancestors(self):
        return [self[:i] for i in range(len(self) + 1)]