If we observe `vuln.c`, we can see that our `flag` is stored in the `char` array `flag`, which is displayed in the function `sigsegv_handler()`. As we can see in our `main()` function on line 31, this function is set to occur whenever the `SIGSEGV` signal is detected. In other words, this funtion executes when there is a SEGFAULT.



So, we need to execute a SEGFAULT! On purpose, for once :)



Well, how can we accomplish this? Well, a SEGFAULT occurs when our program tries to access an inaccessible part of memory. So, how can we force our program to access an inaccessible area of memory?



Let's take a look at `vuln()`. In this function, the `input` char array is copied into `buf2`, which has space allocated for 16 elements. But, if we look at line 39, we can see that our input array, `buf1`, has space allocated for 100 elements. So, if we store more than 16 elements in `buf1`, our program will attempt to copy over 16 chars into a 16-char array. This will cause a SEGFAULT!



So, we can do something as simple as the following to display our flag:

```
> ./vuln
Input: AAAAAAAAAAAAAAAAAAAA
pico_ctf{YOURFLAG}
```


