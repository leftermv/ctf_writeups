```bash
# PLATFORM          . THM
# CTF NAME          . Madness
# DESCRIPTION       . Will you be consumed by Madness?
# DIFFICULTY        . Easy
# CTF LINK          . https://tryhackme.com/room/madness
```

```bash
sudo nmap -sSVC -p- -T5 10.10.4.205 -oN Madness
```

```
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 7.2p2 Ubuntu 4ubuntu2.8 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   2048 acf9851052656e17f51c34e7d86467b1 (RSA)
|   256 dd8e5aecb195cddc4d01b3fe5f4e12c1 (ECDSA)
|_  256 e9ede3eb58773b005e3af524d858348e (ED25519)

80/tcp open  http    Apache httpd 2.4.18 ((Ubuntu))
|_http-title: Apache2 Ubuntu Default Page: It works
|_http-server-header: Apache/2.4.18 (Ubuntu)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel
```

#### PORT 80

- The default Apache website. Except ...

- Notice the icon thing in the title. That is not there by default. Checking the source code, I found the following.

```
    <img src="thm.jpg" class="floating_element"/>
<!-- They will never find me-->
```

- I tried displaying the image by navigating to `http://10.10.4.205/thm.jpg`. It didn't work.

```bash
wget http://10.10.4.205/thm.jpg
```

- I tried opening the file but it didn't work (no surprise ; the server couldn't display it either).

- I took a look at the file using `exiftool`, `hexedit` and a simple `strings` and I came to the following conclusion: this file have the header of a `.PNG` file but it's a `.JPG`

- So I've checked [this](https://en.wikipedia.org/wiki/List_of_file_signatures) page and, using `hexedit`, I've changed the `.PNG` header with that of the `.JPG`

- This gave me no results. I wasn't sure exactly why, but I then noticed that `JFIF` is still `JPG`, so I've tried using that header instead.

- We could open the photo afterwards. It contains a hidden directory.

- Navigating to that endpoint, we get the following message.

```
## Welcome! I have been expecting you!

To obtain my identity you need to guess my secret!

Secret Entered:

That is wrong! Get outta here!
```

- But there's no insert box or anything like that but I found the following comment.

```
<!-- It's between 0-99 but I don't think anyone will look here-->
```

- I was thinking to bruteforce for parameters, but it says "Secret Entered:". So I tried using `?secret=1`. And it worked. I mean, it processed `1` as the value submitted, but this wasn't the correct secret.

- I used `fuff` to fuzz through all numbers `0-99`. 

- First, I generated the wordlist using `crunch`.

```bash
crunch 1 2 0123456789 > numbers
```

```bash
fuff  -u http://10.10.4.205/{redacted}?secret=FUZZ -w=numbers -t 100 -fw 45
```

**NOTE**: `-fw 45` was used as a lot of `301s` with the word-length 45 were returned ; I wanted to get rid of them.

- After navigating to the endpoint

```
Urgh, you got it right! But I won't tell you who I am! y{REDACTED}B
```

- Alright. I was stuck for a while here and decided to think about what I've done and what not so far.

- It looked like a password, couldn't decipher it with any ROT, bases, known ciphers, etc. So it must be a password for something.

- Then, I tried running `steghide --extract -sf` on the image downloaded at the beginning on the CTF.

- Using the passphase from above, I got `hidden.txt` file.

```
Fine you found the password! 

Here's a username 

wbxre

I didn't say I would make it easy for you!
```

- I tried SSHing using `wbxre` and the passphase used for steghide thinking it might work, but it didn't. Now I really had no other ideas.

- I had to check another writeup since I was really stuck here - thing is, I've missed another stego challenge. It's the damn image on the CTF page, in the THM room. [here.](https://tryhackme.com/room/madness)  - _ - 

- OK, I'm glad I've checked another writeup. Should've done it earlier :)) 

- Anyway.. using steghide on the other image, I got `password.txt` file.

```
I didn't think you'd find me! Congratulations!

Here take my password

*a{REDACTED}P
```

- Yeah. Not really. Anyway. I also spoiled the fact that the username is actually ROT13 encoded. These two pieces of information were too close in the writeup, so yeah.

- The decoded username is `joker`.

- We can ssh into the box using `joker:*a{REDACTED}P`, but we can't run anything as `sudo`.

```
find / -type f -perm -04000 -ls 2>/dev/null

150852   1552 -rwsr-xr-x   1 root     root        1588648 Jan  4  2020 /bin/screen-4.5.0
150850   1552 -rwsr-xr-x   1 root     root        1588648 Jan  4  2020 /bin/screen-4.5.0.old
```

- I found the following two binaries with the SUID bit set ; uncommon result.

- After some googling around, I found [this](https://www.exploit-db.com/exploits/41154) script that enables `screen 4.5.0` to be leveraged to spawn a `root shell`. 

- Just copy the script to a file on the server, make it executable and run it.

- The user flag is in `/home/joker/user.txt`.
- The root flag is in `/root/root.txt`.



