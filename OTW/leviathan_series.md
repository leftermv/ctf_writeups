###### SSH Credentials
> User: leviathan0  
> Password: leviathan0  
> Address: leviathan.labs.overthewire.org   
> Port: 2223  

### Leviathan 0
###### There is no information for this level, intentionally.  

**cat** .backup/bookmarks.hmtl | **grep** levi
```
This will be fixed later, the password for leviathan1 is rioGegei8m" ADD_DATE="1155384634" 
LAST_CHARSET="ISO-8859-1" ID="rdf:#$2wIU71">password to leviathan1</A>
```
 > rioGegei8m
##

### Leviathan 1
###### There is no information for this level, intentionally.

It seems that the **check** binary requires a password to run.  
Once we look at the source code, we can somehow guess some things.  
* �[�password: /bin/shWrong password, Good Bye ..   

The live above could indicate that if the password is right, a shell is spawned. Otherwise, a message is shown to the user.  
However, by looking more careful we can see some words hidden in the unknown characters.  
* �sex
* �secrf
* �god
* �love�

The spaces in between could be the words the, making the sentence **Sex is the secret the god love**.   
However, I don't have any clue if that is the right sentence.  

Using **sex** as a password on its own seems to let us run the script and spawn a shell.  
**Note**: Since Python is installed on the machine, we can use ```python3 -c 'import pty;pty.spawn("/bin/bash")'``` to spawn a bash shell.

**whoami** returns us the leviathan2 user, meaning that we have access to read from /etc/leviathan_pass/leviathan2 file.
> ougahZi8Ta
##

### Leviathan 2
###### There is no information for this level, intentionally.

Use the **ltrace** command to trace library calls of the **printfile** binary.

If we read a file that we don't have **access()** to  
```
leviathan2@leviathan:/tmp/blabla$ ltrace ~/printfile /etc/leviathan_pass/leviathan3
__libc_start_main(0x804852b, 2, 0xffffd734, 0x8048610 <unfinished ...>
access("/etc/leviathan_pass/leviathan3", 4)                             = -1
puts("You cant have that file..."You cant have that file...
)                                      = 27
+++ exited (status 1) +++
```

If we read a file that we have **access()** to  
```
leviathan2@leviathan:/tmp/blabla$ ltrace ./printfile test
__libc_start_main(0x804852b, 2, 0xffffd774, 0x8048610 <unfinished ...>
access("test", 4) = 0
snprintf("/bin/cat test", 511, "/bin/cat %s", "test") = 13
geteuid() = 12002
geteuid() = 12002
setreuid(12002, 12002) = 0
system("/bin/cat test"test
 <no return ...>
--- SIGCHLD (Child exited) ---
<... system resumed> ) = 0
+++ exited (status 0) +++

```

When we read a file, the binary first checks if we have **access()** to that file.  
It reads the effective user id (geteuid()) to check the permissions of the file.  
Then, it sets the real and effective user id to 12002, both for user and group.  
Finally, it reads from the file **IF** the user leviathan2 have access to read from that file.  

By playing around with the binary, I found out that if we have a file with spaces in its name we 
can trick the binary to think that both parts of the file names are different files.

We can create a symbolic link file that points to the password file.  
**ln** -s /etc/leviathan_pass/leviathhan3 test

Then, we can create a file that has a space in its name.  
**touch** "test file"

By using the binary with the files we created, we can output the password before the error triggers.  
**~/printfile** test\ file (both test and test file should be in a tmp directory).

>Ahdiemoo1j  
>/bin/cat: file: No such file or directory
##

### Leviathan 3
###### There is no information for this level, intentionally.
**ltrace** ./level3 
```
__libc_start_main(0x8048618, 1, 0xffffd794, 0x80486d0 <unfinished ...>
strcmp("h0no33", "kakaka") = -1
printf("Enter the password> ")= 20
fgets(Enter the password> test
"test\n", 256, 0xf7fc55a0) = 0xffffd5a0
strcmp("test\n", "snlprintf\n") = 1
puts("bzzzzzzzzap. WRONG"bzzzzzzzzap. WRONG
) = 19
+++ exited (status 0) +++
```
We see that the password we entered is compared with the string **snlprintf**.  

**./level3** snlprintf  
```
leviathan3@leviathan:~$ ./level3 
Enter the password> snlprintf
[You've got shell]!
$ cat /etc/leviathan_pass/leviathan4
vuH0coox6m
```

> vuH0coox6m
##

### Leviathan 4
###### There is no information for this level, intentionally.
The **bin** binary inside ~./trash/ outputs 11 blocks of 8bits each.
```
01010100 01101001 01110100 01101000 00110100 01100011 01101111 01101011 01100101 01101001 00001010 
```

By translating from Binary to ASCII text, we get the next level's password.  
> Tith4cokei
##

### Leviathan 5
###### There is no information for this level, intentionally.
**./leviathan5** 
> cat: /tmp/file.log: No such file or directory
**ln** -s /etc/leviathan_pass/leviathan6 /tmp/file.log
**./leviathan5**
> UgaoFee4li
##

### Leviathan 6
###### There is no information for this level, intentionally.

**./leviathan6**
> usage: ./leviathan6 <4 digit code>  

```for i in {0..9999}; do ~/leviathan6 $i; done;```  
After some time, we get a shell as leviathan7.
```
$ whoami
leviathan7
$ cat /etc/leviathan_pass/leviathan7
ahy7MaeBo9
```

> ahy7MaeBo9
##

### Leviathan 7 - Doesn't exist yet.

