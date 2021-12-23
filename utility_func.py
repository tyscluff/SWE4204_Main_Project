# This just has helper functions that i've written


def strip_tuple(tuple):
    """This will take in a tuple and strip it to a normal string"""
    tuple_str = str(tuple)
    stripped1 = tuple_str.strip(")")
    stripped2 = stripped1.strip("(")
    stripped3 = stripped2.strip(",")
    stripped4 = stripped3.strip("'")

    return stripped4
