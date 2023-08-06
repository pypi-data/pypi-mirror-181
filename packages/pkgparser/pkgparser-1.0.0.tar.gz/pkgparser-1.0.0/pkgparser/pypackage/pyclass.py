import inspect
import re

from pkgparser import configuration
from pkgparser.pypackage.pyfunction import PyFunction
from pkgparser.pypackage.pyobject import PyObject
from pkgparser.utilities.package import associate_method_params, extract_class_attrs

class PyClass(PyObject):
    """
    PyClass is a representation of a Python Class.
    """

    def __init__(self, class_path, directory_path):
        """
        Args:
            class_path (string): full path to class with file path and class name
            directory_path (string): python package directory path
        """

        # parse paths
        submodules = class_path.split(".")
        import_path = ".".join(submodules[0:-1])
        self.class_name = submodules[-1]

        # import class
        self.pyobject = getattr(__import__(import_path, fromlist=[self.class_name]), self.class_name)

        # initialize inheritance
        super(PyClass, self).__init__(
            object=self.pyobject,
            object_path=class_path,
            directory_path=directory_path
        )

        # get functions
        all_functions = inspect.getmembers(self.pyobject, predicate=inspect.isfunction)

        # filter out inherited methods
        functions = [d for d in all_functions if d[1].__qualname__.startswith(self.class_name)]

        # initialize
        all_class_functions = [
            PyFunction(
                directory_path=directory_path,
                function=d[1],
                function_path="%s.%s" % (class_path, d[0]),
                is_init=True if d[0] == "__init__" else False,
                is_method=True
            )
            for d in functions
        ]

        # try to get init if exists
        init_method = [d for d in all_class_functions if d.function_name == "__init__"]

        # methods
        self.init = init_method[0] if len(init_method) > 0 else None
        self.methods = sorted([d for d in all_class_functions if d.function_name != "__init__"], key=lambda d: d.function_name)
