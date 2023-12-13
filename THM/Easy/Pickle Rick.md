```bash
# PLATFORM          . THM
# CTF NAME          . Pickle Rick
# DESCRIPTION       . A Rick and Morty CTF. Help turn Rick back into a human!
# DIFFICULTY        . Easy
# CTF LINK          . https://tryhackme.com/room/picklerick
```

___

- I've started this CTF by using scanning the target host.

```bash
sudo nmap -sSVC -T5 10.10.163.142 -oN ~/workspace/ctf_workspace/picklerick
```

```bash
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 7.2p2 Ubuntu 4ubuntu2.6 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey:  
|   2048 b42c0764d2ea581fe75de5eadf1e3ca7 (RSA)
|   256 f439945531b45fcf762ab190ce6a0938 (ECDSA)
|_  256 87f6bed303675adadadd6acb89772725 (ED25519)
80/tcp open  http    Apache httpd 2.4.18 ((Ubuntu))
|_http-title: Rick is sup4r cool
|_http-server-header: Apache/2.4.18 (Ubuntu)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

```

- While the scan was running, I checked the page source and I came across a hint: a username.

![[Pasted image 20231116171844.png]]

- The message found on the page suggest that we should use Burp Suite to catch the request to the webserver. 

```
I need you to *BURRRP*....Morty, logon to my computer and find the last three secret ingredients to finish my pickle-reverse potion. The only problem is, I have no idea what the *BURRRRRRRRP*, password was! Help Morty, Help!
```

- Catching the webpage request in Burp Suite did not reveal anything useful in particular.

- I've tried SSHing to the server with the username found above but the request is denied since we cannot login using a password.

- I did some fuzzing to bruteforce endpoints. Here's the command I've used and the results

```bash
ffuf -u http://10.10.163.142/FUZZ -w /usr/share/wordlists/SecLists/Discovery/Web-Content/big.txt  -t 100 -e .php
```

```bash
.htaccess.php           [Status: 403, Size: 301, Words: 22, Lines: 12]
.htaccess               [Status: 403, Size: 297, Words: 22, Lines: 12]
.htpasswd.php           [Status: 403, Size: 301, Words: 22, Lines: 12]
.htpasswd               [Status: 403, Size: 297, Words: 22, Lines: 12]
assets                  [Status: 301, Size: 315, Words: 20, Lines: 10]
denied.php              [Status: 302, Size: 0, Words: 1, Lines: 1]
login.php               [Status: 200, Size: 882, Words: 89, Lines: 26]
portal.php              [Status: 302, Size: 0, Words: 1, Lines: 1]
robots.txt              [Status: 200, Size: 17, Words: 1, Lines: 2]
	server-status           [Status: 403, Size: 301, Words: 22, Lines: 12]
```

- Robots.txt file reveals a string of text: `Wubbalubbadubdub`

- Both portal and denied.php redirect to login php. 

- We know the username; I tried brute-forcing the login form using `Hydra`, but with no success ;

- However, I tried using  the credentials `R1ckRul3s:Wubbalubbadubdub` and I got in.

![[Pasted image 20231116183531.png]]

- A simple `ls` command reveals a file supposed to contain one of the flags

![[Pasted image 20231116183821.png]]

- However, running `cat` results in a small problem :) 

- I tried different commands that can give the same result as `cat`. The command `less` seems not to be filtered.

![[Pasted image 20231116183846.png]]

- Running `whoami` and `sudo -l` reveals that we're under `www-data` account but we seem to be able to run anything as `sudo` besides the filtered commands.

```
Matching Defaults entries for www-data on ip-10-10-163-142.eu-west-1.compute.internal:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin

User www-data may run the following commands on ip-10-10-163-142.eu-west-1.compute.internal:
    (ALL) NOPASSWD: ALL
```

- The 2nd flag is found at `/home/rick/second ingredients`
- The 3rd flag is found at ``/root/3rd.txt`

