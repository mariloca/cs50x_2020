from cs50 import get_int


def main():
    h = get_height()
    # Loop row
    for i in range(1, h+1):
        print(" " * (h-i), end="")
        print("#" * i, end="")
        print("  ", end="")  # space between #
        print("#" * i, end="")
        print()


def get_height():
    while True:
        n = get_int("Height:")
        # Check n
        if 0 < n < 9:
            break
    return n


main()