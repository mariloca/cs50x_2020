import cs50


def main():
    number = int(get_creditcard())
    card = number
    # if card < pow(10, 13) or card >= pow(10, 16):
    #     print("INVALID")
    checksum = 0
    while card:
        pair = card % 100  # last two digit of the card
        p_digit = pair // 10
        a_digit = pair % 10
        p_digit *= 2
        if p_digit // 10 > 0:  # if true then add each digit to the sum
            pairsum = p_digit // 10 + p_digit % 10
            checksum = checksum + pairsum + a_digit
        else:
            pairsum = p_digit
            checksum = checksum + pairsum + a_digit
        card = card // 100
    if checksum % 10 == 0:  # check which company
        if number // pow(10, 13) == 34 or number // pow(10, 13) == 37:
            print("AMEX")
        elif 51 <= number // pow(10, 14) and number // pow(10, 14) <= 55:
            print("MASTERCARD")
        elif number // pow(10, 12) == 4 or number // pow(10, 15) == 4:
            print("VISA")
    else:
        print("INVALID")


def get_creditcard():
    while True:
        number = cs50.get_string("Enter credit card number:")
        if number.isnumeric() == True:
            break
    return number


main()