import os

from setuptools import setup, find_packages

setup(
    name="pkgparser",
    description="Python package for parsing metadata from classes and functions in a python package.",
    long_description=open(os.path.join(os.getcwd(), "README.md")).read().strip(),
    license="MIT",
    long_description_content_type="text/markdown",
    version=open(os.path.join(os.getcwd(), "VERSION")).read().strip(),
    url="https://gitlab.com/lgensinger/pkgparser",
    install_requires=[d.strip() for d in open(os.path.join(os.getcwd(), "requirements.txt")).readlines()],
    extras_require={
        "render": [d.strip() for d in open(os.path.join(os.getcwd(), "requirements-render.txt")).readlines()],
        "test": [d.strip() for d in open(os.path.join(os.getcwd(), "requirements-test.txt")).readlines()]
    },
    packages=find_packages(),
    include_package_data=True,
    entry_points={
        "console_scripts": [
            "generate-package-docs=pkgparser.bin.generate_package_docs:main",
            "parse-docs=pkgparser.bin.parse_docs:main"
        ],
    }
)
