#Python Backasswords
Thanks to Ben Kurtovic for the idea after reading his blog.

This will obfuscate any python script using Ben Kurtovic's obfuscation method.
I converted it to Python 3 and to take input from a file.

##Dependencies
*Python 3+

##Usage
```
usage: backasswords.py [-h] [-o] [-e] [-b] [-k LENGTH] [--output OUTFILE] infile

Backasswords, an obfuscation script that will hide your plain text without 
changing the functionality.

positional arguments:
infile                Input python file to be obfuscated.

optional arguments:
-h, --help            show this help message and exit
-o, --obfuscate       Enable obfuscation
-e, --encrypt         Enable self-brute-forcing encryption
-b, --bitshift        Enable bitshift obfuscation, Implies obfuscation
                      (WARNING: Takes a very long time to generate)
-k LENGTH, --key LENGTH
                      Specify encryption key length, default = 5, Irrelevant 
                      if encryption is not in use.
--output OUTFILE      Specify output file. If not given writes to stdout.
```
