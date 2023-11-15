def get_obj_name(obj: object):
    """
    Get the name of the object if it is known by the program.

    :param obj: any python object.
    :return: the name of the object if the object is known by the program,
        None otherwise.
    """
    if isinstance(obj, list):
        return "List"
    if isinstance(obj, tuple):
        return "Tuple"
    if isinstance(obj, dict):
        return "Dict"
    if isinstance(obj, set):
        return "Set"
    if isinstance(obj, str):
        if obj == "Brian":
            return "Brian is in the kitchen"
        return "Str"


def all_thing_is_obj(obj: object):
    """
    Print the type of obj if it is known by the program.

    :param obj: any python object.
    :return: 42.
    """
    if (name := get_obj_name(obj)) is None:
        print("Type not found")
    else:
        print(f"{name}: {type(obj)}")
    return 42


__all__ = "all_thing_is_obj",
