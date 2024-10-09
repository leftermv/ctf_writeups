```bash
# PLATFORM          . THM
# CTF NAME          . Ignite
# DESCRIPTION       . A new start-up has a few issues with their web server.
# DIFFICULTY        . Easy
# CTF LINK          . https://tryhackme.com/room/ignite
```

```bash
sudo nmap -sSVC -T5 10.10.189.157 -p- -oN ignite
```

```
PORT   STATE SERVICE VERSION
80/tcp open  http    Apache httpd 2.4.18 ((Ubuntu))
|_http-server-header: Apache/2.4.18 (Ubuntu)
| http-robots.txt: 1 disallowed entry 
|_/fuel/
|_http-title: Welcome to FUEL CMS
```

- If we navigate to the webpage, we see the fuel CMS default installation page. This hints us to `/fuel` page and the default credentials of `admin:admin` are working.

- This is also hinted to us by the fact that `robots.txt` file is not allowing `/fuel` to be crawled.

- There might be a way of uploading a reverse shell from the web interface. However, I checked to see if there are vulnerabilities and I found [this](https://www.exploit-db.com/exploits/50477) CVE that allowed me to obtain RCE on the webserver.

- Technically, I could get at least 1 flag using this, but I wanted to obtain a reverse shell on the server, so `wget` to download `shell.php` - which is pentestmonkey's PHP reverse shell - from my local machine after starting a web server using python.

- Then, all I had to do was to navigate to `http://ip/shell.php`

**NOTE**: I used `wget` from `/var/www/html` directory.

- First flag is in `/home/www-data/flag.txt`

- We know from the main page that the database config file is located in `fuel/application/config/database.php` but we don't have access to it from the webserver.

- However, we can read it by using `cat /var/www/html/fuel/application/config/database.php`

- There we can find the password of `root`.

- Last flag is in `/root/root.txt` :)
