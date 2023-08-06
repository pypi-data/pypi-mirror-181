#!/usr/bin/env python3

import argparse
import json

from pkgparser.pypackage.pypackage import PyPackage
from pkgparser.bin.parameters import param_package_name, param_return_data
from pkgparser.utilities.package import extract_class_attrs

def main(return_data: bool = False) -> dict:
    """
    Parse documentation from Python package.

    Args:
        return_data (bool): TRUE if data should be returned

    Returns:
        A dictionary of key/values representing the metadata of a Python package.
    """

    result = None

    # parse arguments
    opt = parse_args()

    # parse package
    p = PyPackage(package_name=opt.package_name)

    # get attributes
    result = extract_class_attrs(p)
    pac = result["classes"]
    paf = result["functions"]

    # cleanup
    del result["classes"]
    del result["functions"]
    del result["module"]

    result["classes"] = list()
    result["functions"] = list()

    # parse classes
    for c in pac:

        # get attributes
        ca = extract_class_attrs(c)
        cam = ca["methods"]

        # cleanup
        del ca["init"]
        del ca["methods"]
        del ca["pyobject"]
        del ca["rawfile"]

        ca["methods"] = list()

        for m in cam:

            # get attributes
            ma = extract_class_attrs(m)

            # cleanup
            del ma["rawfile"]

            # update class attr
            ca["methods"].append(ma)

        # update result
        result["classes"].append(ca)

    # parse functions
    for f in paf:

        # get attributes
        fa = extract_class_attrs(f)

        # cleanup
        del fa["rawfile"]

        # update result
        result["functions"].append(fa)

    # only return data when requested
    # this ensures console scripts do not break when output is evaluated as error 1 code
    if opt.return_data or return_data:
        return result

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
    param_return_data(parser)

    # parse user input
    args, unknown = parser.parse_known_args()

    return args

if __name__ == "__main__":
    main()
