Observe the following piece of code starting at line `100`:

```c
if (strstr(player_turn, loses[computer_turn])) {
    puts("You win! Play again?");
    return true;
  } else {
    puts("Seems like you didn't win this time. Play again?");
    return false;
  }
```



With `computer_turn` being a random `int` ranging inclusively from 0 to 2, here is the contents of the `loses` array:

```c
char* loses[3] = {"paper", "scissors", "rock"};
```



With these two pieces of code, we can already see the vulnerability. The above `if` statement uses the `strstr()` function to check if the winning hand was played by looking for a **substring**. So, if our user input contains *all three* possible plays, the desired substring will always be found, and the user will always win.



So, to obtain the flag, simply enter `rockpaperscisscors` each round.
