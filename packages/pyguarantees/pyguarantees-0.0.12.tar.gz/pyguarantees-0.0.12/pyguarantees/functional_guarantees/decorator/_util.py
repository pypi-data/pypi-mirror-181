def ismethod(fct) -> bool:
    """
    The `inspect.ismethod` function doesn't work on a method when called
     from inside the decorator of that method; it always returns `False`.

    Instead, use the `inspect.getmembers` function to distinguish between
     functions and methods so that `self` and `class` can be ignored
     where appropriate.
    """
    qualname = fct.__qualname__.split(".")

    # The __qualname__ of a method is always in the form
    #   *classname*.*...*.*methodname*;
    #   Functions, on the other hand, are always in the form *functionname*
    if len(qualname) == 1:
        return False

    # Functions defined within methods are of the form
    #   *classname*.*...*.<locals>.*fname*
    if qualname[-2] == "<locals>":
        return False

    return True
