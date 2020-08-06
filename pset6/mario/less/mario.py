from cs50 import get_int


def main():
    h = get_height()
    for i in range(1, h+1):
        print(" " * (h-i), end="")
        print("#" * i)
        '''
        #another approach
        for m in range(h-i):
            print(" ", end="")
        for n in range(i):
            print("#", end="")
        print()
        '''


def get_height():
    while True:
        n = get_int("Height:")
        if 0 < n < 9:
            break
    return n


main()