from S1E7 import Baratheon, Lannister
from S1E9 import Character, Stark


def print_doc(*args: object):
    """
    Print the docstring of the given objects separated by newlines,
    or else print "Missing docstring for {object}".

    :param args: the objects to print the docstring of.
    """
    output = ""
    for arg in args:
        if arg.__doc__ is None:
            print(f"Missing docstring for {arg}")
            continue
        output += arg.__doc__.strip() + "\n"
    print(output, end="")


Robert = Baratheon("Robert")
print(Robert.__dict__)
print(Robert.__str__)
print(Robert.__repr__)
print(Robert.is_alive)
Robert.die()
print(Robert.is_alive)
print_doc(Robert)
print("---")
Cersei = Lannister("Cersei")
print(Cersei.__dict__)
print(Cersei.__str__)
print(Cersei.is_alive)
print("---")
Jaine = Lannister.create_lannister("Jaine", True)
print(
    f"Name : {Jaine.first_name, type(Jaine).__name__}, "
    f"Alive : {Jaine.is_alive}"
)

characters: list[Character] = [
    Stark("Bran"),
    Stark("Arya", is_alive=False),
    Lannister("Cersei"),
    Lannister("Jaime"),
    Lannister("Tyrion", is_alive=False),
    Baratheon("Robert"),
    Baratheon("Joffrey"),
]

clones = [c.create_character(f"{c.first_name}_clone", c.is_alive) for c in characters]

print("---")
for c in characters:
    print(c)
print("---")
for c in clones:
    print(c)
