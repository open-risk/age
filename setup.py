from owlready2 import *


def main():
    print("Hello from AGE!")
    world = World(backend="sqlite", filename="./djangology/db.sqlite3", dbname="owlready2_quadstore")
    world.save()


if __name__ == "__main__":
    main()
