hashwd
hashwd is a command line tool that generates strong, random passwords using a list of words and optional numbers and symbols.

#Installation
To install hashwd, run the following command:
pip install hashwd

#Usage
usage: hashwd.py [-h] [-d] [-w WORDS] [-n NUMBERS] [-s SYMBOLS] [-c] [-S]
                 [-p]
                 {clear,generate}

Generate a strong, random password using a list of words and optional
numbers and symbols.

positional arguments:
  {clear,generate}      specify whether to clear the clipboard or generate
                        a new password

options:
  -h, --help            show this help message and exit
  -d, --default         use default values for number of words, numbers,
                        and symbols
  -w WORDS, --words WORDS
                        number of words in the password (1-12)
  -n NUMBERS, --numbers NUMBERS
                        number of numbers in the password (1-12)
  -s SYMBOLS, --symbols SYMBOLS
                        number of symbols in the password (1-12)
  -c, --copy            copy the password to the clipboard
  -S, --show            print the password to the console
  -p, --prompt          prompt the user to input the values for number of
                        words, numbers, and symbols

To generate a new password, run the following command:
hashwd generate

##You can customize the password by specifying the number of words, numbers, and symbols to include:
hashwd generate -w 4 -n 2 -s 2

##You can also use the -p flag to prompt the user to input the values for the number of words, numbers, and symbols:
hashwd generate -p

##To copy the generated password to the clipboard, use the -c flag:
hashwd generate -c

##To print the generated password to the console, use the -S flag:
hashwd generate -S

##To use the default values for the number of words, numbers, and symbols, use the -d flag:
hashwd generate -d

##To clear the clipboard, run the following command:
hashwd clear

#Contributing
If you would like to contribute to the hashwd project, please follow these guidelines:

	-Fork the repository and create a new branch for your changes.
	-Make your changes in the new branch.
	-Write tests to ensure that your changes are working as intended.
	-Run the tests to make sure they pass.
	-Commit your changes and push them to your fork.
	-Create a pull request to merge your changes into the main repository.
#License
hashwd is released under the GNU General Public License v3.0.

#Credits
hashwd was developed by Jordan Langland.