import inspect
import re

from pkgparser import configuration
from pkgparser.pypackage.docstring import DocString
from pkgparser.utilities.package import extract_class_attrs
class PyObject:
    """
    PyObject is a representation of a Python Class or Function.
    """

    def __init__(self, object, object_path, directory_path):
        """
        Args:
            directory_path (string): package directory path
            object (object): Python Class || Python Function
            object_path (string): class or function path
        """
        self.docstring = DocString(
            content=object.__doc__ if object.__doc__ else None
        )
        self.is_class = hasattr(self, "class_name")
        self.object_name = self.class_name if self.is_class else (self.function_name if hasattr(self, "function_name") else None)
        self.object_path = object_path
        self.object_param_label = configuration.PARAM_LABEL[self.docstring.style] if self.docstring.style else None
        self.object_params = {
            d: inspect.signature(object).parameters[d].default if not isinstance(inspect.signature(object).parameters[d].default, type) else "empty"
            for d in inspect.signature(object).parameters if d != "self"
        }
        self.object_annotations = {
            d: inspect.signature(object).parameters[d].annotation.__name__ if hasattr(inspect.signature(object).parameters[d].annotation, __name__) and inspect.signature(object).parameters[d].annotation.__name__ != "_empty" else "empty"
            for d in self.object_params
        }

        # open file
        with open("%s/%s.py" % (directory_path, "/".join(self.object_path.split(".")[0:-1])), "r") as file:

            # load raw file line content
            self.rawfile = [d.strip() for d in file.readlines() if d.strip() != str()]

            # try to find object name in file
            line_number = [i for i, d in enumerate(self.rawfile) if ("class %s" % self.object_name if self.is_class else "def %s" % self.object_name) in d]

            # extract line number for object
            self.object_line = line_number[0] if len(line_number) > 0 else None
