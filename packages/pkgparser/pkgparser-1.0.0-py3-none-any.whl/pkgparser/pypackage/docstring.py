import re

from pkgparser import configuration

class DocString:
    """
    DocString is a representation of a Python Function DocString.
    """

    def __init__(self, content: str = None):
        self.raw = content

        # pull lines from blob and remove empties
        self.lines = self.extract_lines(content)

        # infer style
        self.style = self.determine_style(self.raw)
        self.is_multiline = self.style in ["google", "numpydoc"]

        # for multi-line styles determine sections
        self.sections = self.determine_section(self.lines) if self.is_multiline else None

        # extract attributes
        self.urls = None
        self.attributes = self.extract_attributes(self.lines)
        self.description = self.extract_description(self.lines)
        self.raises = self.extract_raises(self.lines)
        self.returns = self.extract_returns(self.lines)

    def determine_section(self, lines: list) -> dict:
        """
        Determine start and end lines for a given docstring section so multi-line style docstrings can be correlated to section key.

        Args:
            lines (list): strings of doctring content segments

        Returns:
            A dictionary where eacy key is a docstring section and corresponding values are (start, ending) line indicies relative to extracted lines not the original docstring.
        """

        result = None

        if self.style == "google":

            # get section delimeter indicies
            sdi = [i for i, d in enumerate(lines) if re.match(re.compile("^[A-Z][a-z]+\:$"), d)]

            # determine start/end of sections
            result = {
                lines[d].strip(":").lower(): (
                    d + 1,
                    sdi[i + 1] - 1 if d != sdi[-1] else len(lines) - 1
                ) for i, d in enumerate(sdi)
            }

        if self.style == "numpydoc":

            # get section delimeter indicies
            sdi = [i for i, d in enumerate(lines) if re.search(re.compile(r"^-+$"), d)]

            # determine start/end of sections
            result = {
                lines[d - 1].strip(":").lower(): (
                    d + 1,
                    sdi[i + 1] - 2 if d != sdi[-1] else len(lines) - 1
                ) for i, d in enumerate(sdi)
            }

        return result

    def determine_style(self, docstring: str = None) -> dict:
        """
        Determine the docstring style.

        Args:
            docstring (string): Python Function text blob

        Returns:
            An enum string representing a docstring type: Epytext, reST, Google, Numpydoc.
        """

        result = None

        # get lines of blob
        lines = self.extract_lines(docstring)

        # Epytext
        is_epytext = any([re.match(configuration.EPYTEXT, d) for d in lines])
        if is_epytext: result = "epytext"

        # Google
        is_google = any([re.match(configuration.GOOGLE, d) for d in lines])
        if is_google: result = "google"

        # Numpydoc
        is_numpydoc = any([re.match(configuration.NUMPYDOC, d.lower()) for d in lines])
        if is_numpydoc: result = "numpydoc"

        # reST
        is_reST = any([re.match(configuration.REST, d) for d in lines])
        if is_reST: result = "rest"

        return result

    def extract_attributes(self, lines: list) -> str:
        """
        Extract params, parameters, and args key/values.

        Args:
            lines (list): strings of doctring content segments

        Returns:
            A dictionary with key/value pairs where each key is a named value for the attribute and corresponding value is the documented value.
        """

        result = None

        # multiline style
        if self.is_multiline:

            if self.style == "google":
                result = dict() if result is None else result

                # loop through section valusets
                for valueset in self.sections:

                    # skip returns/raises
                    if valueset not in ["raises", "returns"]:

                        # set up result list
                        result[valueset] = list()

                        # loop through lines in valueset
                        for line in self.lines[self.sections[valueset][0]:self.sections[valueset][1] + 1]:

                            # split off key/value
                            tokens = [d.strip() for d in line.split(":")]

                            # determine if line contains datatype
                            has_datatype = [d for d in tokens if len(re.compile("\([a-z]+\)").findall(d)) > 0]

                            if has_datatype:

                                # loop through tokens
                                for t in tokens:

                                    # datatype matches
                                    dt_matches = re.compile("\([a-z]+\)").findall(t)

                                    # check if datatype is included with key
                                    if dt_matches:

                                        # update result
                                        result[valueset].append({
                                            "data_type": dt_matches[0].strip("(").strip(")").strip(),
                                            "key": t.split("(")[0].strip(),
                                            "value": line.split(":")[-1].strip()
                                        })

                            else:

                                # update result
                                result[valueset].append({
                                    "data_type": None,
                                    "key": line.split(":")[0].strip() if valueset == "Args" else None,
                                    "value": line.split(":")[-1].strip() if valueset == "Args" else line
                                })

            if self.style == "numpydoc":
                result = dict() if result is None else result

                # loop through section valusets
                for valueset in self.sections:

                    # skip returns/raises
                    if valueset not in ["raises", "returns"]:

                        # set up result list
                        result[valueset] = list()

                        # get section lines
                        section_lines = self.lines[self.sections[valueset][0]:self.sections[valueset][1] + 1]

                        # get all keys in sections
                        keys = [d for d in section_lines if re.search(re.compile(r".\s:\s.|\s:$"), d)]

                        # loop through keys
                        for i, key in enumerate(keys):

                            # determine if datatype provided
                            has_datatype = len([d.strip() for d in key.split(":") if d.strip() != ""]) > 1

                            # determine if attribute is multiline
                            value_start_index = section_lines.index(key) + 1
                            value_end_index = section_lines.index(keys[i + 1]) - 1 if i < len(keys) - 1 else -1
                            value_is_multiline = value_start_index < value_end_index

                            # adjust start/end
                            value_end_index_adjusted = len(section_lines) if value_end_index == -1 else value_end_index + 1

                            # update results
                            result[valueset].append({
                                "data_type": key.split(":")[-1].strip() if has_datatype else None,
                                "key": key.split(":")[0].strip() if has_datatype else key.strip(":"),
                                "value": " ".join([d for d in section_lines[value_start_index:value_end_index_adjusted]])
                            })

        else:

            # loop through lines
            for i, line in enumerate(lines):

                # check for return statement
                if not re.match(configuration.RAISES, line) and not re.match(configuration.RETURNS, line) and re.match(configuration.ATTRIBUTES, line):

                    # set up result list
                    result = dict() if result is None else result

                    # extract attributes from various styles
                    if self.style == "epytext":

                        key = "params"

                        # get line content
                        text = line.split("@param")[-1].lstrip(":").strip()

                        # split into key/value
                        tokens = [d.strip() for d in text.split(":")]

                        # add valueset key if needed
                        result[key] = list() if key not in result.keys() else result[key]

                        # update result
                        result[key].append({
                            "data_type": None,
                            "key": tokens[0],
                            "value": tokens[-1]
                        })

                    if self.style == "rest":

                        key = "params"

                        # get line content
                        text = line.split(":param ")[-1].lstrip(":").strip()

                        # split into key value
                        tokens = [d.strip() for d in text.split(":")]

                        # add valueset key if needed
                        result[key] = list() if key not in result.keys() else result[key]

                        # update result
                        result[key].append({
                            "data_type": None,
                            "key": tokens[0],
                            "value": tokens[-1]
                        })

        return result

    def extract_description(self, lines: list) -> str:
        """
        Extract any text that does not fall into raises, returns, or attributes and precedes the first section.

        Args:
            lines (list):

        Returns:
            A string representing python object description.
        """

        # determine line index where named sections start
        indicies = [self.sections[k][0] - 2 if k.lower() == "parameters" else self.sections[k][0] - 1 for k in self.sections] if self.is_multiline else [i for i, d in enumerate(lines) if re.match(re.compile("^(@|:)"), d)]

        # get ending section
        # smallest index since that is where first section begins
        sections_start = min(indicies) if len(indicies) > 0 else None

        # update result
        descriptions = self.lines[0:sections_start] if sections_start else list()

        # get indicies of descriptions that look like documented endpoints
        indicies = [(i, d) for i, d in enumerate(descriptions) if re.match(re.compile("^/"), d)]

        # update self with urls
        self.urls = [d[1] for d in indicies]

        # only keep descriptions which don't look like documented endpoints
        result = [d for i, d in enumerate(descriptions) if i not in [x[0] for x in indicies]]

        return " ".join(result)

    def extract_lines(self, docstring: str = None) -> list:
        """
        Extract lines of docstring which are not empty.

        Args:
            docstring (string): Python Function text blob

        Returns:
            A list of strings where each is a line of content from a docstring.
        """

        return [d.strip() for d in docstring.split("\n") if d.strip() is not str()] if docstring else list()

    def extract_raises(self, lines: list) -> str:
        """
        Extract raises documentation value.

        Args:
            lines (list): strings of doctring content segments

        Returns:
            A string representing the function's documented return description.
        """

        result = None

        # multi-line styles
        if self.is_multiline:

            if self.style == "google" and "Raises" in self.sections:
                # get key/values in section
                section = self.sections["Raises"]

                # split into key/value
                section_lines = "&&&".join(self.lines[section[0]:section[1] + 1]).split("&&&")

                # construct value
                result = { d.split(":")[0].strip(): d.split(":")[-1].strip() for d in section_lines }

            if self.style == "numpydoc" and "Raises" in self.sections:
                # get key/values in section
                section = self.sections["Raises"]

                # split into key/value
                section_lines = "&&&".join(self.lines[section[0]:section[1] + 1]).split("&&&")

                # construct value
                result = {
                    k: section_lines[section_lines.index(k) + 1]
                    for k in [d for i,d in enumerate(section_lines) if i % 2 == 0]
                }

        else:

            # loop through lines
            for i, line in enumerate(lines):

                # check for return statement
                if re.match(configuration.RAISES, line):

                    # extract raise statement from various styles
                    if self.style == "epytext":
                        result = dict() if result is None else result

                        # get line content
                        text = line.split("@raise")[-1].lstrip(":").strip()

                        # split into key/value
                        tokens = [d.strip() for d in text.split(":")]

                        # update result
                        result[tokens[0]] = tokens[-1]

                    if self.style == "rest":
                        result = dict() if result is None else result

                        # get line content
                        text = line.split(":raises ")[-1].lstrip(":").strip()

                        # split into key value
                        tokens = [d.strip() for d in text.split(":")]

                        # update result
                        result[tokens[0]] = tokens[-1]

        return result

    def extract_returns(self, lines: list) -> str:
        """
        Extract return documentation value.

        Args:
            lines (list): strings of doctring content segments

        Returns:
            A string representing the function's documented return description.
        """

        result = None

        # loop through lines
        for i, line in enumerate(lines):

            # check for return statement
            if re.match(configuration.RETURNS, line):

                # extract return statement from various styles
                if self.style == "epytext":

                    # get single line value
                    result = line.split("@return")[-1].lstrip(":").strip()

                if self.style == "google" and "returns" in self.sections:

                    # get key/values in section
                    section = self.sections["returns"]

                    # construct value
                    result = " ".join(self.lines[section[0]:section[1] + 1])

                if self.style == "numpydoc" and "returns" in self.sections:

                    # get key/values in section
                    section = self.sections["returns"]

                    # construct value
                    result = "; ".join([d for i,d in enumerate(self.lines[section[0]:section[1] + 1]) if i % 2 != 0])

                if self.style == "rest":

                    # get single line value
                    result = line.split(":returns")[-1].lstrip(":").strip()

        return result
