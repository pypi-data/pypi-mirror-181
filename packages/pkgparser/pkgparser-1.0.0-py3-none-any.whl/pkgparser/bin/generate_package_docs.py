#!/usr/bin/env python3

import argparse
import json

from mkdpdf.documentation.documentation import Documentation

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

            # initialize
            r = Documentation(
                directory_name_templates="class",
                directory_path_output=po,
                filename=c.object_path.replace(".", "-"),
                format="md"
            )

            # put the git url on each class for rendering templates
            c.url_git = p.url_git

            # put the git url on each method for rendering templates
            for m in c.methods:
                m.url_git = p.url_git

            # generate markdown
            cc = r.generate(
                header={
                    "CLASS_NAME": c.class_name,
                    "PACKAGE_DESCRIPTION": p.description,
                    "PACKAGE_NAME": p.name,
                    "PACKAGE_VERSION": p.version,
                    "URL_GIT": p.url_git,
                    "URL_RELEASE": p.url_release
                },
                main={
                    "CLASS_DESCRIPTION": c.docstring.description,
                    "CLASS_IMPORT": ".".join(c.object_path.split(".")[0:-1]),
                    "CLASS_NAME": c.class_name,
                    "SUBTEMPLATE_INIT": c,
                    "SUBTEMPLATE_FUNCTIONS": c.methods
                }
            )

            # write to file system
            r.render(cc, r.file_path)

        # initialize for functions
        r = Documentation(
            directory_name_templates="functions",
            directory_path_output=po,
            filename="functions",
            format="md"
        )

        # put the git url on each function for rendering templates
        for f in p.functions:
            f.url_git = p.url_git

        # render markdown
        cf = r.generate(
            header={
                "PACKAGE_DESCRIPTION": p.description,
                "PACKAGE_NAME": p.name,
                "PACKAGE_VERSION": p.version,
                "URL_GIT": p.url_git,
                "URL_RELEASE": p.url_release
            },
            main={
                "SUBTEMPLATE_FUNCTIONS": p.functions
            }
        )

        # write to file system
        r.render(cf, r.file_path)

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
