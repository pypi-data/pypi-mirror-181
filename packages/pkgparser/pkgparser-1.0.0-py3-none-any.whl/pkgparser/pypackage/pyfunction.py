from pkgparser import configuration
from pkgparser.pypackage.pyobject import PyObject
from pkgparser.utilities.package import associate_method_params

class PyFunction(PyObject):
    """
    PyFunction is a representation of a Python Function.
    """

    def __init__(self, function_path, directory_path, function=None, is_method=False, is_init=False):
        """
        Args:
            function (object): Python Function
            function_path (string): full path to function from package
            is_init (boolean): TRUE if function is an init method on a class object
            is_method (boolean): TRUE if function is a method on a class object
        """
        self.is_method = is_method

        # parse paths
        submodules = function_path.split(".")
        import_path = ".".join(submodules[0:-2]) if is_init else ".".join(submodules[0:-1])
        self.function_name = submodules[-1]

        # import function
        self.pyobject = function if is_method else getattr(__import__(import_path, fromlist=[self.function_name]), self.function_name)

        # get parent object path
        parent_object_path = ".".join(function_path.split(".")[0:-1]) if is_method else function_path

        # initialize inheritance
        super(PyFunction, self).__init__(
            object=self.pyobject,
            object_path=parent_object_path,
            directory_path=directory_path
        )

        # associate values defined in code to
        # values documented in docstrings
        associate_method_params(self.pyobject, self)
