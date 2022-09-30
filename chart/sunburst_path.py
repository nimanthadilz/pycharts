from typing import Dict, Iterable

class Path(tuple):
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