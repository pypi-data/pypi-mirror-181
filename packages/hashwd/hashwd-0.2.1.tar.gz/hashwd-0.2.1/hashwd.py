    #import the necessary modules
import random
import pyperclip
import argparse

    # function to generate a random password
def generate_password(dictionary, num_words=4, num_numbers=2, num_symbols=2):
    with open(dictionary, "r") as file:
        words = file.read().splitlines()
    
    password_words = random.sample(words, k=num_words)
    password_words = [word for word in password_words if len(word) >= 5]

    # choose a random word to capitalize
    random_index = random.randint(0, len(password_words) - 1)
    password_words[random_index] = password_words[random_index].capitalize()

    password = " ".join(password_words)

    # add the specified number of random numbers to the password
    numbers = random.sample(range(0, 9), k=num_numbers)

    # add the specified number of random basic symbols to the password
    symbols = random.sample(["!", "@", "#", "_", "-", "?", "(", ")", "[", "]"], k=num_symbols)

    # randomly place the numbers and symbols at the beginning or end of the password
    if random.random() < 0.5:
        password = "".join([str(num) for num in numbers]) + password + "".join(symbols)
    else:
        password += "".join([str(num) for num in numbers]) + "".join(symbols)

    return password
    
def clear_clipboard():
    # clear the clipboard
    pyperclip.copy("")
    
if __name__ == "__main__":
    # use argparse to handle command line arguments
    parser = argparse.ArgumentParser(description="Generate a strong, random password using a list of words and optional numbers and symbols.", epilog="Use 'hashwd clear' to clear the clipboard.")
    parser.add_argument("-d", "--default", action="store_true", help="use default values for number of words, numbers, and symbols")
    parser.add_argument("-w", "--words", type=int, help="number of words in the password (1-12)")
    parser.add_argument("-n", "--numbers", type=int, help="number of numbers in the password (1-12)")
    parser.add_argument("-s", "--symbols", type=int, help="number of symbols in the password (1-12)")
    parser.add_argument("-c", "--copy", action="store_true", help="copy the password to the clipboard")
    parser.add_argument("-S", "--show", action="store_true", help="print the password to the console")
    parser.add_argument("-p", "--prompt", action="store_true", help="prompt the user to input the values for number of words, numbers, and symbols")
    parser.add_argument("command", choices=["clear", "generate"], help="specify whether to clear the clipboard or generate a new password")
    args = parser.parse_args()

    # if the clear flag is set, clear the clipboard and exit
    if args.command == "clear":
        clear_clipboard()
        exit()
    # set default values for the number of words, numbers, and symbols
    num_words = 4
    num_numbers = 2
    num_symbols = 2

    # if the user specifies a custom value for any of the arguments, use it instead of the default value
    if args.words:
        num_words = args.words
    if args.numbers:
        num_numbers = args.numbers
    if args.symbols:
        num_symbols = args.symbols

    # if the prompt flag is set, prompt the user to specify the values for the number of words, numbers, and symbols
    if args.prompt:
        while True:
            try:
                num_words = int(input("How many words? (1-99): "))
                if 1 <= num_words <= 99:
                    break
                else:
                    print("Please enter a number between 1 and 99.")
            except ValueError:
                print("Invalid Input. Please enter a valid number.")
        while True:
            try:
                num_numbers = int(input("How many numbers? (1-9): "))
                if 1 <= num_numbers <= 9:
                    break
                else:
                    print("Please enter a number between 1 and 9.")
            except ValueError:
                print("Invalid input. Please enter a valid number.")
        while True:
            try:
                num_symbols = int(input("How many symbols? (1-9): "))
                if 1 <= num_symbols <= 9:
                    break
                else:
                    print("Please enter a number between 1 and 9.")
            except ValueError:
                print("Invalid input. Please enter a valid number.")

    password = generate_password("dictionary.txt", num_words, num_numbers, num_symbols)

    # copy the password to the clipboard
    if args.copy:
        pyperclip.copy(password)
        print("Password copied. Use 'hashwd clear' to clear the clipboard.")
    # print the password to the terminal if the print flag is set
    if args.show:
        print(password)