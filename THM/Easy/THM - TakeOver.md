---
parent: "[[CTFs - THM]]"
---
```bash
# PLATFORM          . THM
# CTF NAME          . TakeOver
# DESCRIPTION       . This challenge revolves around subdomain enumeration.
# DIFFICULTY        . Easy
# CTF LINK          . https://tryhackme.com/room/takeover
```

```
sudo nmap -sSVC -T5 -p- futurevera.thm -oN futurevera
```

```
PORT    STATE SERVICE  VERSION
22/tcp  open  ssh      OpenSSH 8.2p1 Ubuntu 4ubuntu0.4 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   3072 dd29a70c05691ff6260ad928cd40f020 (RSA)
|   256 cb2ea86d0366e970eb96e1f5ba25cb4e (ECDSA)
|_  256 50d34ba8a24d1d79e17dacbbff0b2413 (ED25519)
80/tcp  open  http     Apache httpd 2.4.41 ((Ubuntu))
|_http-title: Did not follow redirect to https://futurevera.thm/
|_http-server-header: Apache/2.4.41 (Ubuntu)
443/tcp open  ssl/http Apache httpd 2.4.41
|_http-title: FutureVera
| tls-alpn: 
|_  http/1.1
|_http-server-header: Apache/2.4.41 (Ubuntu)
| ssl-cert: Subject: commonName=futurevera.thm/organizationName=Futurevera/stateOrProvinceName=Oregon/countryName=US
| Not valid before: 2022-03-13T10:05:19
|_Not valid after:  2023-03-13T10:05:19
|_ssl-date: TLS randomness does not represent time
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel
```

- I have added `futurevera.thm` in `/etc/hosts`.
- After that, I've started fuzzing for subdomains

```
ffuf -H "Host: FUZZ.futurevera.thm" -u https://IP:443 -w directory-list-2.3-medium.txt -t 100 -fl 92
```

```
blog                    [Status: 200, Size: 3838, Words: 1326, Lines: 81]
support                 [Status: 200, Size: 1522, Words: 367, Lines: 34]
```

- I have chosen to use `-fl 92` to filter false positives that had a content length of 92 lines.

- I have added `blog.futurevera.thm` and `support.futurevera.thm` to `/etc/hosts`.

- I took a look around the pages, tried directory and subdomain enumeration, but I couldn't find any info.

- I have decided to fuzz for potential subdomains using another wordlist

```
ffuf -H "Host: FUZZ.futurevera.thm" -u https://IP -w subdomains-top1million-20000.txt -t 100 -fl 92
```

- Nothing new popped up, so I assumed I missed something.

- I really couldn't find anything on `blog.futurevera.thm`, but `support` had a message saying they're rebuilding the support website, so I had a feeling it must be around here.

- I spent two eternities, but I finally ran out of ideas and checked the little paddle lock in the URL bar and clicked on `Connection not secure -> More Information -> View Certificate`.

- The certificate had the a value assigned to the DNS field which pointed to another subdomain.

```
DNS Name {REDACTED}.support.futurevera.thm
```

- Then... another rabbit hole. If you connect to `https`, which I did.. there's nothing useful

- However, if you connect to `http`, you get the following message

```
We can’t connect to the server at flag{REDACTED}.s3-website-us-west-3.amazonaws.com.
```

