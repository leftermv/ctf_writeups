```bash
# PLATFORM          . THM
# CTF NAME          . Reversing ELF
# DESCRIPTION       . Room for beginner Reverse Engineering CTF players
# DIFFICULTY        . Easy
# CTF LINK          . https://tryhackme.com/room/reverselfiles
```

> crackme1

- All we need to do is to run the binary.

```
chmod +x crackme1
./crackme1
```

> crackme2

- A simple `strings` on the `crackme2` binary will reveal the password

```
t$,U
[^_]
Usage: %s password
su{redacted}rd
Access denied.
Access granted.
;*2$"(
```

```
chmod +x crackme2
./crackme2 [password]
```

> crackme3 

- Again, a simple `strings` or `cat` will reveal a base64 text that is the flag encoded.

```
Usage: %s PASSWORD
malloc failed
ZjByX{redacted}NQ==
Correct password!
Come on, even my aunt Mildred got this one!
ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/
;*2$"8
GCC: (Ubuntu/Linaro 4.6.3-1ubuntu5) 4.6.3
```

> crackme4

- `strings` is not working anymore, as we can find out by using... `strings`. ( or by running the binary)

```
This time the string is hidden and we used strcmp
```

- A simple `ltrace ./crackme4 test` will reveal the password.

> crackme5 

- Again, `ltrace` is enough to solve this.

```
ltrace ./crackme5
```

- When asked for input, input something simple, such as `test`.

- We're shown the `strncmp` function. The flag is there.

> crackme6

- For this one, `ltrace` is not helping us anymore.

- I fired up `ghidra` and analyzed the source code

- We see a function called `my_secure_test`

```
undefined8 my_secure_test(char *param_1)

{
  undefined8 uVar1;
  
  if ((*param_1 == '\0') || (*param_1 != '1')) {
    uVar1 = 0xffffffff;
  }
  else if ((param_1[1] == '\0') || (param_1[1] != '3')) {
    uVar1 = 0xffffffff;
  }
  else if ((param_1[2] == '\0') || (param_1[2] != '3')) {
    uVar1 = 0xffffffff;
  }
  else if ((param_1[3] == '\0') || (param_1[3] != '7')) {
    uVar1 = 0xffffffff;
  }
  else if ((param_1[4] == '\0') || (param_1[4] != '_')) {
    uVar1 = 0xffffffff;
  }
  else if ((param_1[5] == '\0') || (param_1[5] != 'p')) {
    uVar1 = 0xffffffff;
  }
  else if ((param_1[6] == '\0') || (param_1[6] != 'w')) {
    uVar1 = 0xffffffff;
  }
  else if ((param_1[7] == '\0') || (param_1[7] != 'd')) {
    uVar1 = 0xffffffff;
  }
  else if (param_1[8] == '\0') {
    uVar1 = 0;
  }
  else {
    uVar1 = 0xffffffff;
  }
  return uVar1;
}
```

- We're comparing each character of the parameter_1 (our input) to see if it's not the null character `\0` and if it's equal to  `1,3,3,7, _, p, w and d` characters. That's the password.

> crackme7

- By analyzing the `main` function, we can see that the menu has a secret entry.

```
undefined4 main(void)

{
  int iVar1;
  undefined4 *puVar2;
  byte bVar3;
  undefined4 inputted_name [25];
  int local_1c;
  int local_18;
  int input_menu;
  undefined *local_10;
  
  bVar3 = 0;
  local_10 = &stack0x00000004;
  while( true ) {
    while( true ) {
      puts("Menu:\n\n[1] Say hello\n[2] Add numbers\n[3] Quit");
      printf("\n[>] ");
      iVar1 = __isoc99_scanf(&DAT_08048814,&input_menu);
      if (iVar1 != 1) {
        puts("Unknown input!");
        return 1;
      }
      if (input_menu != 1) break;
      printf("What is your name? ");
      puVar2 = inputted_name;
      for (iVar1 = 0x19; iVar1 != 0; iVar1 = iVar1 + -1) {
        *puVar2 = 0;
        puVar2 = puVar2 + (uint)bVar3 * -2 + 1;
      }
      iVar1 = __isoc99_scanf(&DAT_0804883a,inputted_name);
      if (iVar1 != 1) {
        puts("Unable to read name!");
        return 1;
      }
      printf("Hello, %s!\n",inputted_name);
    }
    if (input_menu != 2) {
      if (input_menu == 3) {
        puts("Goodbye!");
      }
      else if (input_menu == 0x7a69) {
        puts("Wow such h4x0r!");
        giveFlag();
      }
      else {
        printf("Unknown choice: %d\n",input_menu);
      }
      return 0;
    }
    printf("Enter first number: ");
    iVar1 = __isoc99_scanf(&DAT_08048875,&local_18);
    if (iVar1 != 1) break;
    printf("Enter second number: ");
    iVar1 = __isoc99_scanf(&DAT_08048875,&local_1c);
    if (iVar1 != 1) {
      puts("Unable to read number!");
      return 1;
    }
    printf("%d + %d = %d\n",local_18,local_1c,local_18 + local_1c);
  }
  puts("Unable to read number!");
  return 1;
}
```

**NOTE**: i used the `rename variable` function in `Ghidra` for `input_menu`. It was called `local_14` before, I think.


- However, the logic of the program is as follows

- if input is 1, ask for a string input and output `hello` + string. 
- If input is 2, ask for 2 integers and add them.
- If input is 3, quit the program.

- But, here's the catch. There's another if that verifies the value inputted in the menu.

```
      else if (input_menu == 0x7a69) {
        puts("Wow such h4x0r!");
        giveFlag();
      }
```

- `0x7a69` is the equivalent of `zi` in ASCII. But the input required is int, right? The decimal equivalent is 31337. 

- This input will call the `giveFlag` function and print it.


> crackme8

- This is simialr to `crackme7`, as it requires to analyze the `main` function in ghidra.

```

{
  undefined4 uVar1;
  int iVar2;
  
  if (param_1 == 2) {
    iVar2 = atoi((char *)param_2[1]);
    if (iVar2 == -0x35010ff3) {
      puts("Access granted.");
      giveFlag();
      uVar1 = 0;
    }
    else {
      puts("Access denied.");
      uVar1 = 1;
    }
  }
  else {
    printf("Usage: %s password\n",*param_2);
    uVar1 = 1;
  }
  return uVar1;
}
```

- we see that `iVar2` is compared to `-03x35010ff3` hex value, which is `-889262067` in decimal. That's the password to the binary.


