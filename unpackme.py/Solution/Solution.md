Open the Python file in your text editor of choice.



Ensure you have the `cryptography` package installed using `pip install cryptography`. Without this package present in your Python installation, the program will not execute.



You will notice that a binary payload string is initialized early-on in the program. This contains our flag (and some additional code) in an encrypted state.



The important line to pay attention to is line 12: `exec(plain.decode())`



In this line, the payload is decoded, and executed as additional Python code. We can intercept this payload by simply placing the line `print(plain.decode())` anywhere after line 11. This should result in the following:

```python
pw = input('What\'s the password? ')

if pw == 'batteryhorse':
  print('picoCTF{AAA_AAAAAAAAA_AAAAAAAA}')
else:
  print('That password is incorrect.')
```

Here, you can clearly see the encrypted Python code that gets executed, as well as the flag.
