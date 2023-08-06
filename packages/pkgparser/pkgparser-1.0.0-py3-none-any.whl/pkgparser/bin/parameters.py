from pkgparser import configuration

def param_output(parser):
    """
    Add output directory parameter.
    """

    parser.add_argument("--output",
        type=str,
        default=configuration.DIRECTORY_PATH_OUTPUT,
        help="Directory path to output files to."
    )

def param_package_name(parser):
    """
    Add package-name parameter.
    """

    parser.add_argument("--package-name",
        type=str,
        help="Name of Python package."
    )

def param_return_data(parser):
    """
    Add return-data parameter.
    """

    parser.add_argument("--return-data",
        action="store_true",
        default=False,
        help="Whether or not to return user data object."
    )
