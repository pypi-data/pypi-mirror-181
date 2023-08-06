#!/usr/bin/env python3

import argparse
import json

from pkgparser.pypackage.pypackage import PyPackage
from pkgparser.bin.parameters import param_package_name, param_output

def main(package_name: str = None, output: str = None):
    """
    Parse documentation from Python package and generate Markdown files for each class/function.

    Args:
        output (string): directory path for generated artifacts
        package_name (string): Name of package to parse
    """

    result = None

    # parse arguments
    opt = parse_args()

    # get params
    pn = package_name if package_name else opt.package_name
    po = output if output else opt.output

    # check for params
    if pn:

        # parse package
        p = PyPackage(package_name=pn)

        # loop through classes
        for c in p.classes:

            # put the git url on each class for rendering templates
            c.url_git = p.url_git

            # put the git url on each method for rendering templates
            for m in c.methods:
                m.url_git = p.url_git

        # put the git url on each function for rendering templates
        for f in p.functions:
            f.url_git = p.url_git

    else:

        raise AttributeError("Missing package name to parse into documentation. Pass with --package-name via console script or package_name via class instantiation.")

def parse_args():
    """
    Parse user input.

    Returns:
        A Namespace with attributes for each provided argument.
    """

    # create arguments
    parser = argparse.ArgumentParser()

    # define optional values
    param_package_name(parser)
    param_output(parser)

    # parse user input
    args, unknown = parser.parse_known_args()

    return args

if __name__ == "__main__":
    main()
