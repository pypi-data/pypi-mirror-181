"""
A FileData class contains the data from a file and some associated context.
"""

import pandas as pd
import parse

class FileData:
    def __init__(self, data, context):
        self.data = data
        self.context = context

    @classmethod
    def from_file(cls, file_name, name_format="", dir="", **args):
        """
        Creates a FileData instance from a file.
        """
        path = f"{dir}/{file_name}"
        # get the data from the file
        data = pd.read_csv(path, **args)
        # get the context from the file name
        parse_result = parse.parse(name_format, file_name)
        context = {"file_path": path, **parse_result.named}
        return cls(data, context)

    def update_context(self, update):
        """
        Updates the context of the FileData instance.
        """
        self.context.update(update)