import inspect

def associate_method_params(python_function, _self):
    """
    Extract Python Method parameters with default values as defined in code and associate them to already parsed docstring values.

    Args:
        _self (Object): Python self object
        python_function (Object): Python object
    """
    
    # load function as signature
    signature = inspect.signature(python_function)

    # pull function param defaults
    params = { k: v.default if not v.default == inspect._empty else str() for k, v in signature.parameters.items() }

    # extract raw text lines of python object declaration which uses configuration or os.environ values
    # because those can be secrets we need to mask them somehow when we render markdown
    # and using inspect we can't know which variable values came from a configuration or environmental variable
    class_lines = {
        _self.object_path: {
            x.strip("):").strip().split("=")[0]: x.strip("):").strip().split("=")[1]
            for x in d.split(",") if "configuration" in x
        }
        for d in _self.rawfile if d.startswith("class") and "configuration" in d or "=os.environ" in d
    }

    def_lines = {
        _self.object_path: {
            x.strip("):").strip().split("=")[0]: x.strip("):").strip().split("=")[1]
            for x in d.split(",") if "configuration" in x
        }
        for d in _self.rawfile if d.startswith("def") and "configuration" in d or "=os.environ" in d
    }

    # attach to self
    _self.config_params = {**class_lines, **def_lines}

    # loop through attribute sets
    for key in extract_class_attrs(_self):

        # only check attributes that are lists
        if isinstance(getattr(_self, key), list):

            # loop through individual pairs
            for d in getattr(_self, key):

                # take only dictionaries of values
                if isinstance(d, dict) and "values" in d:

                    # loop through values of the pairset
                    for v in d["values"]:

                        # check if the key matches a param of this function
                        if v["key"] in list(params.keys()):

                            # have to determine if we need to mask params
                            # that are populated from the environment
                            config_param_key = _self.object_path
                            is_class_or_method_in_config_params = config_param_key in _self.config_params

                            # update default value
                            v["default"] = _self.config_params[config_param_key][v["key"]] if is_class_or_method_in_config_params and v["key"] in _self.config_params[config_param_key] else params[v["key"]]

                            # since there is a default defined it isn't required so update
                            v["required"] = v["default"] == str()

def extract_class_attrs(python_class):
    """
    Extract Python Class attributes and convert to dictionary key/value map.

    Args:
        python_class (Class): Python Class object

    Returns:
        A dictionary of key/value pairs where each key is a Python Class attribute and corresponding value is the value.
    """

    # pull class attributes
    attrs = inspect.getmembers(python_class, lambda a:not(inspect.isroutine(a)))

    # filter out python built-ins
    attrs_filtered = [a for a in attrs if not(a[0].startswith('__') and a[0].endswith('__'))]

    d = dict()

    # loop through attributes
    for attr in attrs_filtered:

        # put into dictionary
        d[attr[0]] = attr[1]

    return d
