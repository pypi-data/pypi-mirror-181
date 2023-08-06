import inspect
import pkgutil

try:
    from importlib import metadata
    from importlib import resources
except ImportError: # for Python<3.8
    import importlib.metadata as metadata
    import importlib_resources as resources

from pkgparser.pypackage.pyclass import PyClass
from pkgparser.pypackage.pyfunction import PyFunction

class PyPackage:
    """
    PyPackage is a Python Package (top-level module).
    """

    def __init__(self, package_name):
        """
        Args:
            package_name (string): name of package
        """

        # get metadata
        md = metadata.metadata(package_name)

        # update self
        self.description = md["Summary"]
        self.directory_path = str(resources.files(package_name)).rstrip(package_name).rstrip("/")
        self.name = package_name
        self.url_git = md["Home-page"]
        self.url_release = "http://releaseurl"
        self.version = md["Version"]

        # import top-level module (package)
        self.module = __import__(self.name)
        self.path = getattr(self.module, "__path__", None)

        # extract data about package
        self.classes = [
            PyClass(
                class_path=d,
                directory_path=self.directory_path
            )
            for d in self.walk(inspect.isclass)
        ]

        self.functions = sorted([
            PyFunction(
                directory_path=self.directory_path,
                function_path=d
            )
            for d in self.walk(inspect.isfunction)
        ], key=lambda d: d.function_name)

    def walk(self, inspection_object: inspect) -> list:
        """
        Walk modules of a package.

        Args:
            inspection_object (enum): type of object to extract from another python object

        Returns:
            A list of strings where each represents a python object full object path, i.e. mypackage.submodule.module.method_name.
        """

        result = None

        # if module is a package
        if self.path:

            # update result
            result = list()

            # walk the submodules
            for importer, module_name, ispkg in pkgutil.walk_packages(self.path, prefix="%s." % self.name.split(".")[0]):

                # load module
                module = importer.find_module(module_name).load_module(module_name)

                # get class-less methods
                all_methods = [t for t in inspect.getmembers(module, inspection_object)]

                # filter to objects specific to this package
                # i.e. this will filter out dependency packages which happen to be declared as an import
                result += [
                    "%s.%s" % (
                        d[1].__module__,
                        d[0]
                    )
                    for d in all_methods if d[1].__module__.startswith(self.name)
                ]

        # not a python package
        else:
            pass

        return list(set(result)) if result else result
