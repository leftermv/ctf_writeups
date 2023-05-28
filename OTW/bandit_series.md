#### The Bandit series is intended for introducing different Linux concepts to the user through a set of challenges.

#### More info can be found on their official page : https://overthewire.org/wargames/bandit/
<br/>

<sub>**NOTE**: I'LL USE {REDACTED} TO REPLACE RANDOM LENGTH OF THE PASSWORD. DO IT YOURSELF, YOU GOTTA LEARN SOMEHOW :)   </sub>


#

To complete the first level, all we have to do is to connect to the server.  
```bash
ssh bandit0@bandit.labs.overthewire.org -p 2220
```

<br />

## Bandit 0


>The password for the next level is stored in a file called readme located in the home directory.  
>Use this password to log into bandit1 using SSH.   
  
  \
  The most common way of reading a file in Linux is by using the `cat` command. 
  
  
```
cat readme
```
 
The password for bandit 1 is NH2SXQwcBd{REDACTED}MM9H66vVXjL

<br />

## Bandit 1
> The password for the next level is stored in a file called - located in the home directory
  
   \
  We can read files that contain unusual symbols by using the `./` characters.

```
cat ./-
```

 The password for bandit 2 is rRGizSaX8Mk{REDACTED}NQoXTcYZWU6lgzi

<br />

## Bandit 2  
> The password for the next level is stored in a file called spaces in this filename located in the home directory
  
   \
  You can `cat` a file containing spaces in its file filename by using quotes

```
cat "spaces in this filename"
```
<br />
 
Here are other ways to read files:  

```
cat spaces\ in\ this\ filename
cat s[tab]
cat spaces* # this would cat all files that start with spaces, be careful :) In this situation, it's ok. 
```
<br />

 And some uncommon ways (seriously, who does this for regular files?):   

```
od -c spaces\ in\ this\ filename 
0000000   a   B   Z   0   W   5   E   m   U   f   A   f   7   k   H   T
0000020   Q   e   O   w   d   8   b   a   u   F   J   2   l   A   i   G
0000040  \n
0000041

hexdump -C spaces\ in\ this\filename
00000000  61 42 5a 30 57 35 45 6d  55 66 41 66 37 6b 48 54  |aBZ0W5{REDACTED}fAf7kHT|
00000010  51 65 4f 77 64 38 62 61  75 46 4a 32 6c 41 69 47  |QeOwd8bauFJ2lAiG|
00000020  0a                                                |.|
00000021

xxd spaces\ in\ this\ filename
00000000: 6142 5a30 5735 456d 5566 4166 376b 4854  aBZ0W{REDACTED}UfAf7kHT
00000010: 5165 4f77 6438 6261 7546 4a32 6c41 6947  QeOwd8bauFJ2lAiG
00000020: 0a    

# The strings command would also work but the output is all lowercase. Not suitable for passwords.

```

 The password for bandit 3 is aBZ0W5EmUf{REDACTED}Owd8bauFJ2lAiG
 
<br />

## Bandit 3 
> The password for the next level is stored in a hidden file in the inhere directory.
  
   \
  To see hidden files or directories in Linux, we need to use the `-a` switch for the `ls` command.  
  Hidden files are preceded by a `.` in their name.  

```
ls -a inhere
```

 The password for bandit 4 is 2EW7BBsr{REDACTED}2HjW067dm8EgX26xNe
 



 
 
 
 
 
 
<br />

 ## Bandit 4
> The password for the next level is stored in the only human-readable file in the inhere directory. 
  
   \
  Technically you could just `cat` all files, check the output and see which one you understand.  But that's not very elegant.  

```
find . -type f -exec file {} +
```
  
  This command assumes that you are already in the `inhere` directory. 
  
  \
  the `.` (dot) after `find` is the path where the command will start searching.   
  `-type f` filteres just the files (since we don't care about directories).  
  `-exec file {} +` will execute the `file` command when running `find` and display the files that match the criteria.  
  
  \
  The output should be something like this. You care about the ASCII file.  
  ```
  ./-file03: data
  ./-file06: data
  ./-file08: data
  ./-file07: ASCII text
  ./-file04: data
  ./-file00: data
  ./-file01: data
  ./-file02: data
  ./-file09: Non-ISO extended-ASCII text, with no line terminators
  ./-file05: data
```
  
 The password for bandit 5 is lrIWWI6b{REDACTED}QZqUdOIYfr6eEeqR
 
 
 
 
 
 
<br />

 ## Bandit 5
> The password for the next level is stored in a file somewhere under the inhere directory and has all of the following properties:  
> human-readable  
> 1033 bytes in size  
> not executable  

  
   \
  We'll use the `find` command again. It is very powerful and allows for a wide range of customized searches.  
  
  \
  You can find (no pun intended) more about `find` using `man find`.

```
find . -size 1033c -type f -exec file {} +
```

 The password for bandit 6 is P4L4vuc{REDACTED}7Vl7jG1ApGSfjYKqJU
 
 
 
 
 
 
<br />

 ## Bandit 6
> The password for the next level is stored somewhere on the server and has all of the following properties:  
> owned by user bandit7  
> owned by group bandit6  
> 33 bytes in size  

  
   \
  Again, `find` will be our tool of choice here.  
  This time, we'll use `/` as the path, to specify that we want to search in the entire filesystem.  

```
find / -user bandit7 -group bandit6 -size 33c 2>/dev/null
```
  \
  We use `2>/dev/null` to redirect `STDERR` (standard error) to `/dev/null`.  
  In other words, we don't want error messages (such as permission denied) to be displayed on our screen.  

  \
 The password for bandit 7 is z7WtoNQU2Xfj{REDACTED}WA8u5rN4vzqu4v99S
 
 
 
 
 
 
<br />

 ## Bandit 7
> The password for the next level is stored in the file data.txt next to the word millionth
  
   \
  Instead of looking manually through the file to see if certain text exists, we can use `grep`.  
  In this case, we'll look after the string `millionth`. We know the password is on the same row.  
```
cat data.txt | grep millionth
```

 The password for bandit 8 is TESKZC0XvTe{REDACTED}9xNwm25STk5iWrBvP
 
 
 
 
 
 
<br />

 ## Bandit 8 
> The password for the next level is stored in the file data.txt and is the only line of text that occurs only once
  
   \
  We need to read the file. Then, we need to see which string is unique.  
  We have the `uniq` command to do this for us, but it ony looks for adjacent lines.  
  
  \
  As an example, if we have
  ```
  A
  A
  B
  ```
  then uniq will not display the second A.  But if the order is A/B/A, then it won't see it as duplicate.   
  
  \
   To solve this issue, we need to sort the list, so the duplicates are adjacent to each other.  
   To do this, we use the `sort` command. I've chosen to reverse sort it using `-r` switch.
   
  \
  So, we'll `cat` the file. Then, we'll `sort` it. Then we will eliminate duplicates using `uniq`.  

```
cat data.txt | sort -r | uniq -u
```

  \
  We can add an extra `uniq -c` at the end to make sure the outputted string has only one occurence in the file.  
  
  ```
  cat data.txt | sort -r | uniq -u | uniq -c
  ```

 The password for bandit 9 is EN632PlfYi{REDACTED}3XOGSlNInNE00t
 
 
 
 
 
 
<br />

 ## Bandit 9
> The password for the next level is stored in the file data.txt in one of the few human-readable strings, preceded by several ‘=’ characters.


```
cat data.txt | grep =
```

 The password for bandit 10 is G7w8LIi6J3kT{REDACTED}LgrywtEUlyyp6s
 
 
 
 
 
 
<br />

 ## Bandit 10
> The password for the next level is stored in the file data.txt, which contains base64 encoded data
  
   \
  We can use `b64` utility with `-d` switch to decode data encoded in `base64` format.  

```
base64 -d data.txt
```

 The password for bandit 11 is 6zPeziLdR{REDACTED}b6nVCKzphlXHBM
 
 
 
 
 
 
<br />

 ## Bandit 11
> The password for the next level is stored in the file data.txt, where all lowercase (a-z) and uppercase (A-Z) letters have been rotated by 13 positions
  
   \
  This is well known letter substitution cipher. Google it if you want to learn more :)  
  
  \
  The main take-away from here is that all letters are replaced by the 13th letter after it in the latin alphabet.  
  A becomes N, B becomes O and so on.  
  
  \
  The `tr` command is used to translate characters from `STDIN` and writes to `STDOUT`.  
  
```
cat data.txt | tr 'A-Za-z' 'N-ZA-Mn-za-m'
```

 The password for bandit 12 is JVNBBFSmZwKKO{REDACTED}bFXOoW8chDz5yVRv
 
 
 
 
 
 
<br />

 ## Bandit 12 
> The password for the next level is stored in the file data.txt, which is a hexdump of a file that has been repeatedly compressed. 
  
   \
  We'll use `xxd` to reverse the hexdump, when we will use the `file` utility to check the file's type.  
  
  ```
  xxd -r data.txt > reversed
  ```
  
  \
  The `file reversed` will output a gzip archive, so we have to add the `.gz` extension and unzip it.  
  
  ```
  mv reversed.bz  
  gunzip reversed.bz  
  ```
  
  \
  Use `file` again, add the correct extension, unzip, repeat.  
  
  \
  Steps:
  ```
  
  reversed  ->    gzip 
  gzip      ->    bzip2 #.bz extension, bunzip2 [file] to extract
  bzip2     ->    gzip
  gzip      ->    tar # .tar extension, tar -xf [file] to extract
  tar       ->    tar
  tar       ->    bzip2
  bzip2     ->    gzip
  gzip      ->    ASCII
  ```

 The password for bandit 13 is wbWdlBxEir4{REDACTED}8LaPhauuOo6pwRmrDw
 
 
 
 
 
 
<br />

 ## Bandit 13
> For this level, you don’t get the next password, but you get a private SSH key that can be used to log into the next level.
  
   \
  Copy the content of the file to your local machine and save it into a file.  
  
  Change the permissions to `rw` for the owner of the file using `chmod 600 [key]` command.   
  
  SSH into the next level using the command below.  

```
ssh -i /path/to/the/key bandit14@bandit.labs.overthewire.org -p 2220
```

  \
  The SSH key you'll find is similar to this format  
  ```
  -----BEGIN RSA PRIVATE KEY-----
MIIEpAIBAAKCAQEAxkkOE83W2cOT7IWhFc9aPaaQmQDdgzuXCv+ppZHa++buSkN+
gg0tcr7Fw8NLGa5+Uzec2rEg0WmeevB13AIoYp0MZyETq46t+jk9puNwZwIt9XgB
ZufGtZEwWbFWw/vVLNwOXBe4UWStGRWzgPpEeSv5Tb1VjLZIBdGphTIK22Amz6Zb
ThMsiMnyJafEwJ/T8PQO3myS91vUHEuoOMAzoUID4kN0MEZ3+XahyK0HJVq68KsV
ObefXG1vvA3GAJ29kxJaqvRfgYnqZryWN7w3CHjNU4c/2Jkp+n8L0SnxaNA+WYA7
jiPyTF0is8uzMlYQ4l1Lzh/8/MpvhCQF8r22dwIDAQABAoIBAQC6dWBjhyEOzjeA
J3j/RWmap9M5zfJ/wb2bfidNpwbB8rsJ4sZIDZQ7XuIh4LfygoAQSS+bBw3RXvzE
pvJt3SmU8hIDuLsCjL1VnBY5pY7Bju8g8aR/3FyjyNAqx/TLfzlLYfOu7i9Jet67
xAh0tONG/u8FB5I3LAI2Vp6OviwvdWeC4nOxCthldpuPKNLA8rmMMVRTKQ+7T2VS
nXmwYckKUcUgzoVSpiNZaS0zUDypdpy2+tRH3MQa5kqN1YKjvF8RC47woOYCktsD
o3FFpGNFec9Taa3Msy+DfQQhHKZFKIL3bJDONtmrVvtYK40/yeU4aZ/HA2DQzwhe
ol1AfiEhAoGBAOnVjosBkm7sblK+n4IEwPxs8sOmhPnTDUy5WGrpSCrXOmsVIBUf
laL3ZGLx3xCIwtC{REEEEDAAAAAAAAAAACTEEEEEEEEED}8njTrbRhLgbC9QrKrS
M1F2fSTxVqPtZDlDMwjNR04xHA/fKh8bXXyTMqOHNJTHHNhbh3McdURjAoGBANkU
1hqfnw7+aXncJ9bjysr1ZWbqOE5Nd8AFgfwaKuGTTVX2NsUQnCMWdOp+wFak40JH
PKWkJNdBG+ex0H9JNQsTK3X5PBMAS8AfX0GrKeuwKWA6erytVTqjOfLYcdp5+z9s
8DtVCxDuVsM+i4X8UqIGOlvGbtKEVokHPFXP1q/dAoGAcHg5YX7WEehCgCYTzpO+
xysX8ScM2qS6xuZ3MqUWAxUWkh7NGZvhe0sGy9iOdANzwKw7mUUFViaCMR/t54W1
GC83sOs3D7n5Mj8x3NdO8xFit7dT9a245TvaoYQ7KgmqpSg/ScKCw4c3eiLava+J
3btnJeSIU+8ZXq9XjPRpKwUCgYA7z6LiOQKxNeXH3qHXcnHok855maUj5fJNpPbY
iDkyZ8ySF8GlcFsky8Yw6fWCqfG3zDrohJ5l9JmEsBh7SadkwsZhvecQcS9t4vby
9/8X4jS0P8ibfcKS4nBP+dT81kkkg5Z5MohXBORA7VWx+ACohcDEkprsQ+w32xeD
qT1EvQKBgQDKm8ws2ByvSUVs9GjTilCajFqLJ0eVYzRPaY6f++Gv/UVfAPV4c+S0
kAWpXbv5tbkkzbS0eaLPTKgLzavXtQoTtKwrjpolHKIHUz6Wu+n4abfAIRFubOdN
/+aLoRQ0yBDRbdXMsZN/jvY44eM+xRLdRVyMmdPtP8belRi2E2aEzA==
-----END RSA PRIVATE KEY-----
```
 
 
 
 
 
 
<br />

 ## Bandit 14
> The password for the next level can be retrieved by submitting the password of the current level to port 30000 on localhost.
  
   \
  First, we need the password for the current user.  
  Grab it from `/etc/bandit_pass/bandit14` file.  
  
  \
  After this, we can `echo` the password to `netcat`.  

```
echo "fGrHPx402xGC{REDACTED}rXKDaxiWFTOiF0ENq" | nc localhost 30000
```

 The password for bandit 15 is jN2kgmIX{REDACTED}vhotn4Zcka6tnt
 
 
 
 
 
 
<br />

 ## Bandit 15
> The password for the next level can be retrieved by submitting the password of the current level to port 30001 on localhost using SSL encryption.
  
   \
  The steps here are the same as above, but we'll use `openssl` instead of `netcat`.  

```
echo "jN2kgmIXJ6f{REDACTED}T2avhotn4Zcka6tnt" | openssl s_client -connect localhost:30001 -ign_eof
```

 The password for bandit 16 is JQttfApK4S{REDACTED}9SXGR50qclOAil1
 
 
 
 
 
 
<br />

 ## Bandit 16
> The credentials for the next level can be retrieved by submitting the password of the current level to a port on localhost in the range 31000 to 32000.  
> First find out which of these ports have a server listening on them. Then find out which of those speak SSL and which don’t.  
> There is only 1 server that will give the next credentials, the others will simply send back to you whatever you send to it.  
  
   \
  We'll use ``nmap`` for this. It's a very known port scanner that'll help us see which ports are open for a specific target.  

```
nmap --script ssl-enum-ciphers -p31000-32000 localhost
```

\
The ``--script`` switch specifies that we want to use the `ssl-enum-ciphers` script to see which ports use `SSL`.  

\
The output here will be something similar to this.  

```
31046/tcp open  unknown
31518/tcp open  unknown
| ssl-enum-ciphers: 
|   TLSv1.2: 
|     ciphers: 
|       TLS_ECDHE_RSA_WITH_AES_128_CBC_SHA (secp256r1) - A
|       TLS_ECDHE_RSA_WITH_AES_128_CBC_SHA256 (secp256r1) - A
|       TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256 (secp256r1) - A
|       TLS_ECDHE_RSA_WITH_AES_256_CBC_SHA (secp256r1) - A
|       TLS_ECDHE_RSA_WITH_AES_256_CBC_SHA384 (secp256r1) - A
|       TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384 (secp256r1) - A
|       TLS_ECDHE_RSA_WITH_ARIA_128_GCM_SHA256 (secp256r1) - A
|       TLS_ECDHE_RSA_WITH_ARIA_256_GCM_SHA384 (secp256r1) - A
|       TLS_ECDHE_RSA_WITH_CAMELLIA_128_CBC_SHA256 (secp256r1) - A
|       TLS_ECDHE_RSA_WITH_CAMELLIA_256_CBC_SHA384 (secp256r1) - A
|       TLS_ECDHE_RSA_WITH_CHACHA20_POLY1305_SHA256 (secp256r1) - A
|       TLS_RSA_WITH_AES_128_CBC_SHA (rsa 2048) - A
|       TLS_RSA_WITH_AES_128_CBC_SHA256 (rsa 2048) - A
|       TLS_RSA_WITH_AES_128_CCM (rsa 2048) - A
|       TLS_RSA_WITH_AES_128_CCM_8 (rsa 2048) - A
|       TLS_RSA_WITH_AES_128_GCM_SHA256 (rsa 2048) - A
|       TLS_RSA_WITH_AES_256_CBC_SHA (rsa 2048) - A
|       TLS_RSA_WITH_AES_256_CBC_SHA256 (rsa 2048) - A
|       TLS_RSA_WITH_AES_256_CCM (rsa 2048) - A
|       TLS_RSA_WITH_AES_256_CCM_8 (rsa 2048) - A
|       TLS_RSA_WITH_AES_256_GCM_SHA384 (rsa 2048) - A
|       TLS_RSA_WITH_ARIA_128_GCM_SHA256 (rsa 2048) - A
|       TLS_RSA_WITH_ARIA_256_GCM_SHA384 (rsa 2048) - A
|       TLS_RSA_WITH_CAMELLIA_128_CBC_SHA (rsa 2048) - A
|       TLS_RSA_WITH_CAMELLIA_128_CBC_SHA256 (rsa 2048) - A
|       TLS_RSA_WITH_CAMELLIA_256_CBC_SHA (rsa 2048) - A
|       TLS_RSA_WITH_CAMELLIA_256_CBC_SHA256 (rsa 2048) - A
|     compressors: 
|       NULL
|     cipher preference: client
|     warnings: 
|       Weak certificate signature: SHA1
|_  least strength: A
31691/tcp open  unknown
31790/tcp open  unknown
| ssl-enum-ciphers: 
|   TLSv1.2: 
|     ciphers: 
|       TLS_ECDHE_RSA_WITH_AES_128_CBC_SHA (secp256r1) - A
|       TLS_ECDHE_RSA_WITH_AES_128_CBC_SHA256 (secp256r1) - A
|       TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256 (secp256r1) - A
|       TLS_ECDHE_RSA_WITH_AES_256_CBC_SHA (secp256r1) - A
|       TLS_ECDHE_RSA_WITH_AES_256_CBC_SHA384 (secp256r1) - A
|       TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384 (secp256r1) - A
|       TLS_ECDHE_RSA_WITH_ARIA_128_GCM_SHA256 (secp256r1) - A
|       TLS_ECDHE_RSA_WITH_ARIA_256_GCM_SHA384 (secp256r1) - A
|       TLS_ECDHE_RSA_WITH_CAMELLIA_128_CBC_SHA256 (secp256r1) - A
|       TLS_ECDHE_RSA_WITH_CAMELLIA_256_CBC_SHA384 (secp256r1) - A
|       TLS_ECDHE_RSA_WITH_CHACHA20_POLY1305_SHA256 (secp256r1) - A
|       TLS_RSA_WITH_AES_128_CBC_SHA (rsa 2048) - A
|       TLS_RSA_WITH_AES_128_CBC_SHA256 (rsa 2048) - A
|       TLS_RSA_WITH_AES_128_CCM (rsa 2048) - A
|       TLS_RSA_WITH_AES_128_CCM_8 (rsa 2048) - A
|       TLS_RSA_WITH_AES_128_GCM_SHA256 (rsa 2048) - A
|       TLS_RSA_WITH_AES_256_CBC_SHA (rsa 2048) - A
|       TLS_RSA_WITH_AES_256_CBC_SHA256 (rsa 2048) - A
|       TLS_RSA_WITH_AES_256_CCM (rsa 2048) - A
|       TLS_RSA_WITH_AES_256_CCM_8 (rsa 2048) - A
|       TLS_RSA_WITH_AES_256_GCM_SHA384 (rsa 2048) - A
|       TLS_RSA_WITH_ARIA_128_GCM_SHA256 (rsa 2048) - A
|       TLS_RSA_WITH_ARIA_256_GCM_SHA384 (rsa 2048) - A
|       TLS_RSA_WITH_CAMELLIA_128_CBC_SHA (rsa 2048) - A
|       TLS_RSA_WITH_CAMELLIA_128_CBC_SHA256 (rsa 2048) - A
|       TLS_RSA_WITH_CAMELLIA_256_CBC_SHA (rsa 2048) - A
|       TLS_RSA_WITH_CAMELLIA_256_CBC_SHA256 (rsa 2048) - A
|     compressors: 
|       NULL
|     cipher preference: client
|     warnings: 
|       Weak certificate signature: SHA1
|_  least strength: A
31960/tcp open  unknown
```

  \
  Send the current's level password to the correct port to get the next level password.  
  
  ```
  echo "JQttfApK4Se{REDACTED}lI9SXGR50qclOAil1" | openssl s_client -connect localhost:[port] -ign_eof
  ```
  

 The password for bandit 17 is VwOSWtCA7lRK{REDACTED}IDh6awj9RNZM5e
 
 
 
 
 
 
<br />

 ## Bandit 17
> There are 2 files in the homedirectory: passwords.old and passwords.new.   
> The password for the next level is in passwords.new and is the only line that has been changed between passwords.old and passwords.new
 

```
diff -n password.old password.new
```

 The password for bandit 18 is hga5tuuCLF{REDACTED}pnagiMN8ssu9LFrdg
 
 
 
 
 
 
<br />

 ## Bandit 18
> The password for the next level is stored in a file readme in the homedirectory.   
> Unfortunately, someone has modified .bashrc to log you out when you log in with SSH.  
  
   \
  Here we can use a `SSH` trick. The `SSH` is able to run commands when a connection is made.  

```
ssh -i key bandit18@bandit.labs.overthewire.org -p 2220 'cat /home/bandit18/readme'
```

 The password for bandit 19 is awhqfNnAbc1{REDACTED}qDYcF95h7HoMTrC

 
 
 
 
 
<br />

 ## Bandit 19
> To gain access to the next level, you should use the setuid binary in the homedirectory.   
> Execute it without arguments to find out how to use it
  
   \
  The binary found in the bandit19 home directory is able to run commands with bandit20 permissions.    
  To understand more about why this works, you can read more about SUID.  

```
./bandit20-do cat /etc/bandit_pass/bandit20
```

 The password for bandit 20 is VxCazJaVy{REDACTED}kBU0mJTCM8rR95XT


 
 
 
 
 
<br />

 ## Bandit 20
> There is a setuid binary in the homedirectory that does the following: it makes a connection to localhost on the port you specify as a commandline argument.   
> It then reads a line of text from the connection and compares it to the password in the previous level (bandit20).   
> If the password is correct, it will transmit the password for the next level (bandit21).
  
   \
  Here we'll use `netcat` once again. But this time we need to have 2 SSH instances (aka 2 terminal emulators and connect twice on the server).  
  
  \
  On the first session, we'll use `netcat` to listen on a port.  
  ```
  nc -nvlp [whatever_port_you_want(almost)]
  ```
  
  \
  Then, on the second session, we need to use the binary found for this level.  
  ```
  ./suconnect [port_used_previously]
  ```
  
  \
  We should see a established connection. Paste the password for bandit 20 in session one and press enter.  

 The password for bandit 21 is NvEJF7oVj{REDACTED}PSrdKEFOllh9V1IBcq
 
 
  
 
 
 
 
<br />

 ## Bandit 21 
> A program is running automatically at regular intervals from cron, the time-based job scheduler.   
> Look in /etc/cron.d/ for the configuration and see what command is being executed.
  
   \
  We will navigate to `/etc/cron.d` directory to see available scripts that'll be ran by `cron`.  
  
  \
  Inside `/usr/bin/cronjob_bandit22.sh`  
  ```
  #!/bin/bash
  chmod 644 /tmp/t7O6lds9S0RqQh9aMcz6ShpAoZKF7fgv
  cat /etc/bandit_pass/bandit22 > /tmp/t7O6lds9S0RqQh9aMcz6ShpAoZKF7fgv
  ```
   
   \
   This script basically just places the content of `/etc/bandit_pass/bandit22` into that tmp file.  
   
   \
   The password for bandit 22 is WdDozAdTM2z{REDACTED}2mGlwngMfj4EZff
 
 
 
<br />

 ## Bandit 22
> A program is running automatically at regular intervals from cron, the time-based job scheduler.   
> Look in /etc/cron.d/ for the configuration and see what command is being executed.
  
   \
  If we navigate to `/etc/cron.d` directory, we'll see multiple bash scripts that will run on the server.  
  However, for this particular level, we're interested by bandit23 script.  
  
  ```
  #!/bin/bash

  myname=$(whoami)
  mytarget=$(echo I am user $myname | md5sum | cut -d ' ' -f 1)

  echo "Copying passwordfile /etc/bandit_pass/$myname to /tmp/$mytarget"

  cat /etc/bandit_pass/$myname > /tmp/$mytarget
  ```
  
  \
  This is the content of the script.  
  
  \
  `myname` variable will have the value of bandit23, since the script runs with bandit23's permissions.  
  `mytarget` variable will hold the string `I am user bandit23` and then convert it to a md5 hash.  
  After that, `cut` is used to take the first part of the output (the hash).  
  
  \
  This is because if we run `md5sum` on some string, the output is similar to this: `hash -`.  
  In this case, the `cut` command will use `space` as a `delimiter (-d)` and take only the first field (the hash).   
  
  \
  Then the script will copy the password from `/etc/bandit_pass/bandit23` to `/tmp/md5sum` path.  

  \
 The password for bandit 23 is QYw0Y2aiA672{REDACTED}uTQuhoz8SyR2G

 
 
 
 
<br />

 ## Bandit 23
> A program is running automatically at regular intervals from cron, the time-based job scheduler.   
> Look in /etc/cron.d/ for the configuration and see what command is being executed.
  
   \
  Again, go to `/etc/cron.d` directory.  
  
  \
  Content of `/usr/bin/cronjob_bandit24.sh`
  
  ```
  #!/bin/bash

  myname=$(whoami)

  cd /var/spool/$myname/foo || exit 1
  echo "Executing and deleting all scripts in /var/spool/$myname/foo:"
  for i in * .*;
  do
      if [ "$i" != "." -a "$i" != ".." ];
      then
          echo "Handling $i"
          owner="$(stat --format "%U" ./$i)"
          if [ "${owner}" = "bandit23" ]; then
              timeout -s 9 60 ./$i
          fi
          rm -rf ./$i
      fi
  done
  ```
  
  \
  Shortly, `myname` variable will have the `bandit24` value.  
  So the scripts will be executed from `/var/spool/bnadit24/foo` path and then removed.  
  
  \
  We need to write our script that will copy bandit24's password from `/etc/bnaidt_pass/bandit24`.  
  
  \
  First, make a directory in `/tmp`. `mkdir /tmp/whatever`.  
  Navigate to that directory: `cd /tmp/whatever`.  
  
  \
  Once you're here, use `vim whatevernameyouwant.sh` to create a `.sh` file.  
  We'll use `cat` to redirect the content of `/etc/bandit_pass/bandit24` to a file in our `/tmp` directory.  
  <sub> NOTE: The script will run under bandit24 permissions, so it will be able to read from bandit_pass/bandit24 file </sub>  
  
  \
  The content of the script should be something like this 
  ```
  #!/bin/bash
  cat /etc/bandit_pass/bandit24 > /tmp/whatever/output
  ```
  
  \
  Exit `vim` and `chmod +x whatevernameyouwant.sh`.  
  Then, create the `output.txt` file : `touch output`.  
  
  \
  Set `read` and `write` permissions for `output` file: `chmod o+rw output`.   
  Copy the script to `/var/spool/bandit24/foo`: `cp whatever.sh /var/spool/bandit24/foo`.   
  
  \
  It'll run shortly and you will find the password in the `output` file.  
  The password for bandit 24 is VAfGXJ1PBSsP{REDACTED}I8p759leLZ9GGar
 
 
 
 
 
<br />

 ## Bandit 24
> A daemon is listening on port 30002 and will give you the password for bandit25 if given the password for bandit24 and a secret numeric 4-digit pincode.  
> There is no way to retrieve the pincode except by going through all of the 10000 combinations,
  
   \
  We need to send to `netcat` on `localhost 30002` something like `VAfGXJ1PB{REDACTED}jI8p759leLZ9GGar code`.  
  <sub> NOTE: code will actually be a 4-digit number, starting from 0000 and ending at 9999</sub>
  
  \
  Write a quick script to generate all 10k combinations  
  ```
  #!/bin/bash

  for i in $(seq 0 9999);
  do
          echo "VAfGXJ1P{REDACTED}I8p759leLZ9GGar $i" >> blabla
  done
  ```
  
  \
  Run the script. Once we have all 10k combinations, we can use the file to send content to `netcat`.  
  
  ```
  cat blabla | netcat localhost 30002 >> result
  ```

 The password for bandit 25 is p7TaowMYrmu23{REDACTED}h9UvD0O9hpx8d 

 
<br />

 ## Bandit 25
> Logging in to bandit26 from bandit25 should be fairly easy…  
> The shell for user bandit26 is not /bin/bash, but something else.  
> Find out what it is, how it works and how to break out of it.
  
 ```
-----BEGIN RSA PRIVATE KEY-----
MIIEpQIBAAKCAQEApis2AuoooEqeYWamtwX2k5z9uU1Afl2F8VyXQqbv/LTrIwdW
pTfaeRHXzr0Y0a5Oe3GB/+W2+PReif+bPZlzTY1XFwpk+DiHk1kmL0moEW8HJuT9
/5XbnpjSzn0eEAfFax2OcopjrzVqdBJQerkj0puv3UXY07AskgkyD5XepwGAlJOG
xZsMq1oZqQ0W29aBtfykuGie2bxroRjuAPrYM4o3MMmtlNE5fC4G9Ihq0eq73MDi
1ze6d2jIGce873qxn308BA2qhRPJNEbnPev5gI+5tU+UxebW8KLbk0EhoXB953Ix
3lgOIrT9Y6skRjsMSFmC6WN/O7ovu8QzGqxdywIDAQABAoIBAAaXoETtVT9GtpHW
qLaKHgYtLEO1tOFOhInWyolyZgL4inuRRva3CIvVEWK6TcnDyIlNL4MfcerehwGi
il4fQFvLR7E6UFcopvhJiSJHIcvPQ9FfNFR3dYcNOQ/IFvE73bEqMwSISPwiel6w
e1DjF3C7jHaS1s9PJfWFN982aublL/yLbJP+ou3ifdljS7QzjWZA8NRiMwmBGPIh
Yq8weR3jIVQl3ndEYxO7Cr/wXXebZwlP6CPZb67rBy0jg+366mxQbDZIwZYEaUME
zY5izFclr/kKj4s7NTRkC76Yx+rTNP5+BX+JT+rgz5aoQq8ghMw43NYwxjXym/MX
c8X8g0{REEEEEEEEEEEEEEEEEEEEEEEEEEEEEEDACCCTEEEEEEEEEEED}f3M53le
wF1rkp5SJnHRFm9IW3gM1JoF0PQxI5aXHRGHphwPeKnsQ/xQBRWCeYpqTme9amJV
tD3aDHkpIhYxkNxqol5gDCAt6tdFSxqPaNfdfsfaAOXiKGrQESUjIBcCgYEAxvmI
2ROJsBXaiM4Iyg9hUpjZIn8TW2UlH76pojFG6/KBd1NcnW3fu0ZUU790wAu7QbbU
i7pieeqCqSYcZsmkhnOvbdx54A6NNCR2btc+si6pDOe1jdsGdXISDRHFb9QxjZCj
6xzWMNvb5n1yUb9w9nfN1PZzATfUsOV+Fy8CbG0CgYEAifkTLwfhqZyLk2huTSWm
pzB0ltWfDpj22MNqVzR3h3d+sHLeJVjPzIe9396rF8KGdNsWsGlWpnJMZKDjgZsz
JQBmMc6UMYRARVP1dIKANN4eY0FSHfEebHcqXLho0mXOUTXe37DWfZza5V9Oify3
JquBd8uUptW1Ue41H4t/ErsCgYEArc5FYtF1QXIlfcDz3oUGz16itUZpgzlb71nd
1cbTm8EupCwWR5I1j+IEQU+JTUQyI1nwWcnKwZI+5kBbKNJUu/mLsRyY/UXYxEZh
ibrNklm94373kV1US/0DlZUDcQba7jz9Yp/C3dT/RlwoIw5mP3UxQCizFspNKOSe
euPeaxUCgYEAntklXwBbokgdDup/u/3ms5Lb/bm22zDOCg2HrlWQCqKEkWkAO6R5
/Wwyqhp/wTl8VXjxWo+W+DmewGdPHGQQ5fFdqgpuQpGUq24YZS8m66v5ANBwd76t
IZdtF5HXs2S5CADTwniUS5mX1HO9l5gUkk+h0cH5JnPtsMCnAUM+BRY=
-----END RSA PRIVATE KEY-----
```

\
Since we can't connect to Bandit 26 just yet, we go back to Bandit 25.  
By looking at the `/etc/passwd` file, we see that the bandit 26 has `/usr/bin/showtext` set instead of the bash shell.  

\
content of `/usr/bin/showtext`
```
#!/bin/sh

export TERM=linux

more ~/text.txt
exit 0
```

We can't read the text file but we know that `more` gets called.  
By minimizing the terminal when we try to log via `SSH`, it'll trigger the more command since the entire logo can't be displayed.  

Then, we can open `vim` by pressing `v` After that, we can enter the `:set shell=/bin/bash` command to spawn the bash shell.    
Once we have our bash shell, we can use `:!cat /etc/bandit_pass/bandit26` to get the password.     

\
 The password for bandit 26 is c7GvcKlw9m{REDACTED}aPx7nwFstuAIBw1o1
 
 
 
 
 
<br />

 ## Bandit 26
> Good job getting a shell! Now hurry and grab the password for bandit27!
  
   \
  We still can't log in to bandit 26.   
  We go back and repeat the steps from the previous level.  

  ```
  :!ls -la
  ```
  
  ```
  -rwsr-x---  1 bandit27 bandit26 7296 May  7  2020 bandit27-do
  ```

  We do have reand and execute access to a binary called bandit27-do. We might assume what this is doing from previous experience.  

  ```
  :!/home/bandit26/bandit27-do cat /etc/bandit_pass/bandit27
  ```

 The password for bandit 27 is YnQpBuifNM{REDACTED}Fk70ZmqkhUU2EuaS
 
 
 
 
 
<br />

 ## Bandit 27
> There is a git repository at ssh://bandit27-git@localhost/home/bandit27-git/repo via the port 2220.   
> The password for the user bandit27-git is the same as for the user bandit27.
  
   \
  Create a directory inside of /tmp because we don't have write access in our home directory.  

  ```
  git clone ssh://bandit27-git@localhost/home/bandit27-git/repo
  ```

\
The passowrd is inside `README.md` file  
The password for bandit 28 is AVanL161y9{REDACTED}IsFHuw35rjaOM19nR 
 
 
 
 
 
<br />

 ## Bandit 28 
> There is a git repository at ssh://bandit28-git@localhost/home/bandit28-git/repo via the port 2220.   
> The password for the user bandit28-git is the same as for the user bandit28.
  
  
  ```
  cat README.md
  ```

\
CONTENT
  ```
  ## credentials

  - username: bandit29
  - password: xxxxxxxxxx
  ```

  We can use `git log` to see the logs of the git repository.  
  We have one interesting log that caught my attention.  
  ```
  commit edd935d60906b33f0619605abd1689808ccdd5ee
  Author: Morla Porla <morla@overthewire.org>
  Date:   Thu May 7 20:14:49 2020 +0200

      fix info leak
  ```

  `git log -p` shows the logs with the differences made after each commit.
  ```
  commit edd935d60906b33f0619605abd1689808ccdd5ee
  Author: Morla Porla <morla@overthewire.org>
  Date:   Thu May 7 20:14:49 2020 +0200

      fix info leak

  diff --git a/README.md b/README.md
  index 3f7cee8..5c6457b 100644
  --- a/README.md
  +++ b/README.md
  @@ -4,5 +4,5 @@ Some notes for level29 of bandit.
   ## credentials

   - username: bandit29
  -- password: {REDACTED}
  +- password: xxxxxxxxxx
  ```


 The password for bandit 29 is tQKvmcwNY{REDACTED}HIUSI3ShmsrQZK8S
 
 
 
 
 
<br />

 ## Bandit 29
> There is a git repository at ssh://bandit29-git@localhost/home/bandit29-git/repo via the port 2220.   
> The password for the user bandit29-git is the same as for the user bandit29.
  
   \
  Here, `git log -p` doesn't seem to offer us much information at first.  
  We can check the current branch of the repository by using `git branch`.  

  ```
  * master
  ```

  Using `git branch -a` will show the other branches as well.  
  We use `git checkout [branch]` to check the other branches.  

  ```
  * master
    remotes/origin/HEAD -> origin/master
    remotes/origin/dev
    remotes/origin/master
    remotes/origin/sploits-dev
  ```

  Finally, in `/remotes/origin/dev`, if we cheeck the logs we find the password.  

  ```
  commit bc833286fca18a3948aec989f7025e23ffc16c07
  Author: Morla Porla <morla@overthewire.org>
  Date:   Thu May 7 20:14:52 2020 +0200

      add data needed for development

  diff --git a/README.md b/README.md
  index 1af21d3..39b87a8 100644
  --- a/README.md
  +++ b/README.md
  @@ -4,5 +4,5 @@ Some notes for bandit30 of bandit.
   ## credentials

   - username: bandit30
  -- password: <no passwords in production!>
  +- password: {REDACTED}
```

 The password for bandit 30 is xbhV3HpNG{REDACTED}rdAlPzc2L6y9EOnS
 
 
 
 
 
<br />

 ## Bandit 30
> There is a git repository at ssh://bandit30-git@localhost/home/bandit30-git/repo via the port 2220.  
> The password for the user bandit30-git is the same as for the user bandit30.
  
    
  Finally, inside `packet-refs` we have an interesting file.
  ```
  831aac2e2341f009e40e46392a4f5dd318483019 refs/tags/secret
  ```

  ```
  git show 831aac2e2341f009e40e46392a4f5dd318483019
  ```

 The password for bandit 31 is OoffzGDlzh{REDACTED}J2cAiz1D41JW1Mhmt
 
 
 
 
 
<br />

 ## Bandit 31
> There is a git repository at ssh://bandit30-git@localhost/home/bandit30-git/repo via the port 2220.  
> The password for the user bandit30-git is the same as for the user bandit30.
  
   \
  Create a file and add the required text.  
  Then, add the file for commit.  
  ```
  git add -f file.txt
  ```
  
  \
  Commit & push
  ```
  git commit -m [message]
  git push origin master  
  ```

 The password for bandit 32 is rmCBvG56y58B{REDACTED}yZGdO7ATVL5dW8y
 
 
 
 
 
<br />

 ## Bandit 32
> After all this git stuff its time for another escape. Good luck!
  
   \
    In linux, the current shell is held into $0 variable.  
    It seems like an interactive shell. It converts any commannd to its uppercase (and invalid) version.    
    We can execute the shell again by using the **$0** variable.   

```
$0
```

 The password for bandit 33 is odHo63fHiFq{REDACTED}rLiLDtPm45KzUKy
 
 
  
 
<br />

 ## Bandit 33 - Not available
 
