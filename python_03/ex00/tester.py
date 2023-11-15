from S1E9 import Stark


def print_doc(*args: object):
    """
    Print the docstring of the given objects separated by newlines.

    :param args: the objects to print the docstring of.
    """
    output = ""
    for arg in args:
        if arg.__doc__ is None:
            print(f"Missing docstring for {arg}")
            continue
        output += arg.__doc__.strip() + "\n"
    print(output, end="")


Ned = Stark("Ned")
print(Ned.__dict__)
print(Ned.is_alive)
Ned.die()
print(Ned.is_alive)
print_doc(Ned, Ned.__init__, Ned.die)
print("---")
Lyanna = Stark("Lyanna", False)
print(Lyanna.__dict__)
