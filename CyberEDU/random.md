# Random

This time, we're given what seems to be a binary file that we need to reverse engineer.  

But first, let's interact with the service we're given.  

We can use `netcat` to connect to remote service.  

\
The service generates us a random number or outputs `wrong option` if anything else than `1` is sent as input.  

![Screenshot_20230531_113950](https://github.com/leftermv/ctf_writeups/assets/92045728/13572fa5-21d1-49c5-a8fa-a9c2a08231a2)

Below, I've opened the file we're given in `ghidra`.  

![Screenshot_20230531_113841](https://github.com/leftermv/ctf_writeups/assets/92045728/1c08b75d-f5ab-4abb-bb86-c69b76317f62)

The program seems to generate and print a random number by calling the `rand()` function when value `1` is used as input.  

Otherwise, it prints `wrong option` on the screen.  

But in between this `if-else`, we have a `else-if` condition that compares our input with `0x539`.  

If the values are equal, we see that the `FLAG` environment table is retrieved and printed.  

As a reference, I have highlighted this in the image above.  0x539 in hexa is 1337 in decimal.  

When we introduce this value as input, we receive the flag.  

FLAG : flag{l3{REDATCTED}ag}


