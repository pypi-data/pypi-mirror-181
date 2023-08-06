from typing import List

from .FileData import FileData
from .utils import file_names_from_regex, sequence

class DataSet:
    def __init__(self, data: List[FileData] = None):
        self.data = data if data is not None else []

    # define slicing of DataSet
    def __getitem__(self, subscript):
        if isinstance(subscript, slice):
            return DataSet(self.data[subscript.start:subscript.stop:subscript.step])
        else:
            return self.data[subscript]

    def clear(self):
        self.data = []

    def map(self, func):
        for file_data in self.data:
            func(file_data)

    def sequence(self, funcs):
        self.map(sequence(funcs))

    @classmethod
    def from_files(cls, file_names, name_format="", dir="", **args):
        """
        Creates a DataSet instance from a list of files.
        """
        return cls([FileData.from_file(name, name_format, dir, **args) for name in file_names])

    @classmethod
    def from_regex(cls, regex="*", dir="", name_format="", **args):
        """
        Creates a DataSet instance from a list of files that match the given regex.
        """
        return cls.from_files(file_names_from_regex(regex, dir), name_format, dir, **args)