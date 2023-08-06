import os
import re

# FILESYSTEM
DIRECTORY_PATH_OUTPUT = os.environ["DIRECTORY_PATH"] if "DIRECTORY_PATH" in os.environ else os.getcwd()

# FORMATS
EPYTEXT = re.compile("^(@param|@return)")
GOOGLE = re.compile("^(Args:|Returns:|Raises:)")
NUMPYDOC = re.compile("^(-+)")
REST = re.compile("^(:param|:returns:|:raises )")

ATTRIBUTES = re.compile("^(@param|:param )")
RAISES = re.compile("^(@raise|:raises |Raises:?)")
RETURNS = re.compile("^(@return|Returns:?|:returns)")

PARAM_LABEL = {
    "epytext": "params",
    "google": "args",
    "numpydoc": "parameters",
    "rest": "params"
}
