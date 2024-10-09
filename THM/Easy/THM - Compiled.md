```bash
# PLATFORM          . THM
# CTF NAME          . Compiled
# DESCRIPTION       . Strings can only help you so far.
# DIFFICULTY        . Easy
# CTF LINK          . https://tryhackme.com/room/compiled
```

```bash
cat Compiled.Compiled

H�Ǹ��������H�H��Password: DoYouEven%sCTF__dso_handle_initCorrect!Try again!,
```

- The binary exits and outputs `Try again!` when the incorrect password is inputted.

- Here's the decompiled `main` function by Ghidra.

```
undefined8 main(void)

{
  int iVar1;
  char local_28 [32];
  
  fwrite("Password: ",1,10,stdout);
  __isoc99_scanf("DoYouEven%sCTF",local_28);
  iVar1 = strcmp(local_28,"__dso_handle");
  if ((-1 < iVar1) && (iVar1 = strcmp(local_28,"__dso_handle"), iVar1 < 1)) {
    printf("Try again!");
    return 0;
  }
  iVar1 = strcmp(local_28,"_init");
  if (iVar1 == 0) {
    printf("Correct!");
  }
  else {
    printf("Try again!");
  }
  return 0;
}
```

- If we use `DoYouEven` as a password, we see a strange behaviour. 
- The program is not exiting, but it is not showing anything either.

- This is because we're somewhere after the `first if` and it waits for our input to check for `the second if`.

- In this case, we see that `strcmp` is used to check if the input is `_init`. 

- We're able to solve this challenge by first introducing `DoYouEven` and then `_init`. 

- The flag is `DoYouEven_init`.

