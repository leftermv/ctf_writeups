```bash
# PLATFORM          . THM
# CTF NAME          . H4cked
# DESCRIPTION       . Find out what happened by analysing a .pcap file and hack your way back into the machine
# DIFFICULTY        . Easy
# CTF LINK          . https://tryhackme.com/room/h4cked
```

```bash
sudo nmap -sSVC -T5 10.10.255.10 -oN ~/workspace/ctf_workspace/h4cked
```

```
PORT   STATE SERVICE VERSION
21/tcp open  ftp     vsftpd 2.0.8 or later

80/tcp open  http    Apache httpd 2.4.29 ((Ubuntu))
|_http-title: Apache2 Ubuntu Default Page: It works
|_http-server-header: Apache/2.4.29 (Ubuntu)
```

- We're given a `.pcap` file that has to be analyzed in order to find out how the machine got compromised. 

- I went directly to `File -> Export Objects -> HTTP` and noticed some bits of files that gave me an idea about what was going on.

- Starting with packet 457 we can already see that the user `jenny` was compromised or at least logged on the system.

![[Pasted image 20231203174442.png]]

- Following the `TCP Stream`, we can see what user `jenny` has `password123` as a password. This is visible in `stream 20`. 

- This also granted the attacker full access to the system, as jenny was able to run anything as sudo.

```
User jenny may run the following commands on wir3:
(ALL : ALL) ALL

jenny@wir3:/$ sudo su
root@wir3:/# whoami
root
```

- In `Stream 16` we see that the attacker got access to the FTP service first using the same password. 

- Then, he uploaded a reverse shell that got accessed via the webserver available on the box.

- The reverse shell can be seen in `Stream 18`

- After the reverse shell was stabilisted, the attacker cloned the `https://github.com/f0rb1dd3n/Reptile.git` project that enabled the attacker to install a rootkit on the system.

- However, by running hydra against the FTP service we can bruteforce the new password for user `jenny`.

```
sudo hydra -l jenny -P /usr/share/wordlists/rockyou.txt IP ftp -t 16
```

- After this, we can upload our own PHP reverse shell using `put [filename]` on the FTP service.

- The shell can be accessed by navigating to `http://IP/filename.php`

- Once inside, we can su to `jenny`  and then use `sudo /bin/bash` to get a root shell.

- The final flag is in `root/Reptile/flag.txt`



