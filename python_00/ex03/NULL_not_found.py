from math import isnan


def get_NULL_name(object: object):
    """
    Return the name of the object if the object is falsy,
    otherwise return None.

    :param object: any python object.
    :return: the name of the object if the object is falsy,
        otherwise return None.
    """
    if object is None:
        return "Nothing"
    if isinstance(object, float) and isnan(object):
        return "Garlic"
    if not object:
        if isinstance(object, str):
            return "Empty"
        if isinstance(object, bool):
            return "Fake"
        return "Zero"


def NULL_not_found(object: object):
    """
    Print the type of the object if the object is falsy,
    otherwise print `Type not found`.

    :param object: any python object.
    :return: 0 if the object is falsy, 1 otherwise.

    List of possible falsy values:
        - None
        - nan
        - 0/False
        - an empty string
    """
    if (name := get_NULL_name(object)) is None:
        print("Type not found")
        return 1
    print(f"{name}: {object} {type(object)}")
    return 0


__all__ = "NULL_not_found",
