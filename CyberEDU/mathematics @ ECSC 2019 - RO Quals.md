- the `math.out` binary is sent to us

![[Pasted image 20231212171846.png]]

- After inputting a random pin, the program exits.

- So let's take a look at the source code in `ghidra`

- Below is the main function

```c

undefined8 main(void)

{
  int iVar1;
  int iVar2;
  int iVar3;
  int iVar4;
  int iVar5;
  int iVar6;
  int iVar7;
  int iVar8;
  basic_ostream *pbVar9;
  long in_FS_OFFSET;
  int local_28;
  int local_24;
  long local_20;
  
  local_20 = *(long *)(in_FS_OFFSET + 0x28);
  iVar1 = tryharder(8);
  iVar2 = eadsvfbdgw(0xf);
  iVar3 = eadsvfbdgw(7);
  iVar3 = eadsvfbdgw(iVar3);
  iVar4 = eadsvfbdgw(8);
  iVar4 = eadsvfbdgw(iVar4);
  iVar5 = eadsvfbdgw(8);
  iVar5 = eadsvfbdgw(iVar5);
  iVar6 = asberwefreqw(4);
  iVar7 = asberwefreqw(1);
  iVar7 = asberwefreqw(iVar7);
  iVar7 = eadsvfbdgw(iVar7);
  iVar8 = eadsvfbdgw(5);
  iVar8 = eadsvfbdgw(iVar8);
  local_24 = tryharder(0xb);
  local_24 = local_24 + iVar1 + iVar2 + iVar3 + iVar4 + iVar5 + iVar6 + iVar7 + iVar8;
  local_24 = tryharder(local_24 + -1);
  pbVar9 = std::operator<<((basic_ostream *)std::cout,"Enter the pin for the flag here:");
  std::basic_ostream<char,std::char_traits<char>>::operator<<
            ((basic_ostream<char,std::char_traits<char>> *)pbVar9,
             std::endl<char,std::char_traits<char>>);
  std::basic_istream<char,std::char_traits<char>>::operator>>
            ((basic_istream<char,std::char_traits<char>> *)std::cin,&local_28);
  if (local_24 == local_28) {
    pbVar9 = std::operator<<((basic_ostream *)std::cout,"ECSC{sha256(<your number>)}");
    std::basic_ostream<char,std::char_traits<char>>::operator<<
              ((basic_ostream<char,std::char_traits<char>> *)pbVar9,
               std::endl<char,std::char_traits<char>>);
  }
  if (local_20 != *(long *)(in_FS_OFFSET + 0x28)) {
                    /* WARNING: Subroutine does not return */
    __stack_chk_fail();
  }
  return 0;
}
```

- Take a look at `iVar1` through `iVar8` after they're declared. The initialization of these variables is being made by calling some functions.

```c

/* asberwefreqw(int) */

int asberwefreqw(int param_1)

{
  int iVar1;
  
  if (param_1 < 2) {
    iVar1 = 1;
  }
  else {
    iVar1 = asberwefreqw(param_1 + -1);
    iVar1 = iVar1 * param_1;
  }
  return iVar1;
}
```

```c

/* eadsvfbdgw(int) */

int eadsvfbdgw(int param_1)

{
  int iVar1;
  int iVar2;
  
  if (1 < param_1) {
    iVar1 = eadsvfbdgw(param_1 + -1);
    iVar2 = eadsvfbdgw(param_1 + -2);
    param_1 = iVar2 + iVar1;
  }
  return param_1;
}
```

```c

/* ecscisfun(int) */

int ecscisfun(int param_1)

{
  int iVar1;
  
  if (param_1 < 2) {
    iVar1 = 1;
  }
  else {
    iVar1 = tryharder(param_1 + -1);
    iVar1 = iVar1 + param_1 * 2 + 0x539;
  }
  return iVar1;
}
```

```c

/* tryharder(int) */

int tryharder(int param_1)

{
  int iVar1;
  
  if (param_1 < 2) {
    iVar1 = 1;
  }
  else {
    iVar1 = ecscisfun(param_1 + -1);
    iVar1 = iVar1 + (param_1 + 200) * 2;
  }
  return iVar1;
}
```

- Back to the main, let's have a bit of understanding about what the code does

```c
local_20 = *(long *)(in_FS_OFFSET + 0x28);


if (local_20 != *(long *)(in_FS_OFFSET + 0x28)) 
{ 
	/* WARNING: Subroutine does not return */
	__stack_chk_fail();
}
```

- this seems to be some sort of protection to make sure the heap integrity is not compromised ; it helps preventing vulnerabilities like buffer overflow, most probably.

```c
	  iVar1 = tryharder(8);
  iVar2 = eadsvfbdgw(0xf);
  iVar3 = eadsvfbdgw(7);
  iVar3 = eadsvfbdgw(iVar3);
  iVar4 = eadsvfbdgw(8);
  iVar4 = eadsvfbdgw(iVar4);
  iVar5 = eadsvfbdgw(8);
  iVar5 = eadsvfbdgw(iVar5);
  iVar6 = asberwefreqw(4);
  iVar7 = asberwefreqw(1);
  iVar7 = asberwefreqw(iVar7);
  iVar7 = eadsvfbdgw(iVar7);
  iVar8 = eadsvfbdgw(5);
  iVar8 = eadsvfbdgw(iVar8);
  local_24 = tryharder(0xb);
  local_24 = local_24 + iVar1 + iVar2 + iVar3 + iVar4 + iVar5 + iVar6 + iVar7 + iVar8;
  local_24 = tryharder(local_24 + -1);
```

- Here are the variables I was talking about in the beginning. To find the values, we must calculate each of them based on the argument value and what is each function doing.

- Then, at the end, we need to get the value of `local_24`. 

- This is then compared to `local_28` - this is the variable that is storing our input

```c
if (local_24 == local_28) {
    pbVar9 = std::operator<<((basic_ostream *)std::cout,"ECSC{sha256(<your number>)}");
    std::basic_ostream<char,std::char_traits<char>>::operator<<
              ((basic_ostream<char,std::char_traits<char>> *)pbVar9,
               std::endl<char,std::char_traits<char>>);
  }
```

- if these 2 are equal, then the flag is outputted. kind of. we should convert the number in sha256, but you got the idea.

- Since we already have the functions, let's skip the input thing and make a quick c program to calculate `local_24` for us, based on the functions found in the ghidra decompilation. 

```c
#include <stdio.h>

int tryharder(int);
int ecscisfun(int);
int eadsvfbdgw(int);
int asberwefreqw(int);

int main() {
  int iVar1, iVar2, iVar3, iVar4, iVar5, iVar6, iVar7, iVar8, local_24;
  
  iVar1 = tryharder(8);
  iVar2 = eadsvfbdgw(0xf);
  iVar3 = eadsvfbdgw(7);
  iVar3 = eadsvfbdgw(iVar3);
  iVar4 = eadsvfbdgw(8);
  iVar4 = eadsvfbdgw(iVar4);
  iVar5 = eadsvfbdgw(8);
  iVar5 = eadsvfbdgw(iVar5);
  iVar6 = asberwefreqw(4);
  iVar7 = asberwefreqw(1);
  iVar7 = asberwefreqw(iVar7);
  iVar7 = eadsvfbdgw(iVar7);
  iVar8 = eadsvfbdgw(5);
  iVar8 = eadsvfbdgw(iVar8);
  local_24 = tryharder(0xb);
  local_24 = local_24 + iVar1 + iVar2 + iVar3 + iVar4 + iVar5 + iVar6 + iVar7 + iVar8;
  local_24 = tryharder(local_24 - 1);

  printf("iVar1: %d\n", iVar1);
  printf("iVar2: %d\n", iVar2);
  printf("iVar3: %d\n", iVar3);
  printf("iVar4: %d\n", iVar4);
  printf("iVar5: %d\n", iVar5);
  printf("iVar6: %d\n", iVar6);
  printf("iVar7: %d\n", iVar7);
  printf("iVar8: %d\n", iVar8);
  printf("local_24: %d\n", local_24);

  return 0;
}

int tryharder(int param_1) {
  int iVar1;
  
  if (param_1 < 2) {
    iVar1 = 1;
  }
  else {
    iVar1 = ecscisfun(param_1 - 1);
    iVar1 = iVar1 + (param_1 + 200) * 2;
  }
  return iVar1;
}

int ecscisfun(int param_1) {
  int iVar1;
  
  if (param_1 < 2) {
    iVar1 = 1;
  }
  else {
    iVar1 = tryharder(param_1 - 1);
    iVar1 = iVar1 + param_1 * 2 + 0x539;
  }
  return iVar1;
}

int eadsvfbdgw(int param_1) {
  int iVar1, iVar2;
  
  if (1 < param_1) {
    iVar1 = eadsvfbdgw(param_1 - 1);
    iVar2 = eadsvfbdgw(param_1 - 2);
    param_1 = iVar2 + iVar1;
  }
  return param_1;
}

int asberwefreqw(int param_1) {
  int iVar1;
  
  if (param_1 < 2) {
    iVar1 = 1;
  }
  else {
    iVar1 = asberwefreqw(param_1 - 1);
    iVar1 = iVar1 * param_1;
  }
  return iVar1;
}
```

```
gcc -o FLAG solve.c
```

```
./FLAG
```

```
iVar1: 5682
iVar2: 610
iVar3: 233
iVar4: 10946
iVar5: 10946
iVar6: 24
iVar7: 1
iVar8: 5
local_24: 1{redacted}5
```

```
echo -n <local24_value> | sha256sum
```

- The flag is `ECSC{value_from_command_above}`.

