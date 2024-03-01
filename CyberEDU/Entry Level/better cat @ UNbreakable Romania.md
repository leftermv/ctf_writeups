
- running the `cat.elf` binary prompts for a password

- however, by using `ltrace ./cat.elf` while the program is running, we're able to see that the validation is made by the `strcmp` function ;

```
chmod +x cat.elf 
madalinux@asgard:~/workspace/ctf_workspace$ ltrace ./cat.elf 
puts("https://www.youtube.com/watch?v="...https://www.youtube.com/watch?v=oHg5SJYRHA0
)                                                                = 44
printf("The password is: ")                                                                                = 17
__isoc99_scanf(0x562134000a56, 0x7ffeb325c0a0, 0, 0The password is: 7481
)                                                       = 1
strcmp("7481", "{redacted}")                                                                                 = -57
```

**NOTE**: for you own safety, don't open that youtube link :)

- Run the program again and use the password found in the `strcmp` function as input to get the flag.
