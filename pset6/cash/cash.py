from cs50 import get_float


def main():
    arr = [25, 10, 5, 1]
    # prepare change in the loop
    change = round(get_change() * 100)
    coins = 0
    # loop thru the list
    for i in range(len(arr)):
        # quotient of change // arr[i] is numbers of coins
        coins = coins + change // arr[i]
        # prepare change for next loop round
        change = change % arr[i]
    print(coins)


def get_change():
    while True:
        c = get_float("Enter the change: ")
        if c > 0:
            break
    return c


main()