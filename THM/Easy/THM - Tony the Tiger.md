---
parent: "[[CTFs - THM]]"
---
```bash
# PLATFORM          . THM
# CTF NAME          . Tony the Tiger
# DESCRIPTION       . Learn how to use a Java Serialisation attack in this boot-to-root
# DIFFICULTY        . Easy
# CTF LINK          . https://tryhackme.com/room/tonythetiger
```

```bash
sudo nmap -sSVC -T5 -p- 10.10.107.237 -oN tony
```

```
PORT     STATE SERVICE     VERSION
22/tcp   open  ssh         OpenSSH 6.6.1p1 Ubuntu 2ubuntu2.13 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   1024 d6978cb974d0f39efef3a5eaf8a9b57a (DSA)
|   2048 33a47b9138585030892de457bb07bb2f (RSA)
|   256 21018b37f51e2bc557f1b042b732abea (ECDSA)
|_  256 f636073c3b3d7130c4cd2a1300b525ae (ED25519)
80/tcp   open  http        Apache httpd 2.4.7 ((Ubuntu))
|_http-server-header: Apache/2.4.7 (Ubuntu)
|_http-generator: Hugo 0.66.0
|_http-title: Tony&#39;s Blog
1090/tcp open  java-rmi    Java RMI
|_rmi-dumpregistry: ERROR: Script execution failed (use -d to debug)
1091/tcp open  java-rmi    Java RMI
1098/tcp open  java-rmi    Java RMI
1099/tcp open  java-object Java Object Serialization
| fingerprint-strings: 
|   NULL: 
|     java.rmi.MarshalledObject|
|     hash[
|     locBytest
|     objBytesq
|     #http://thm-java-deserial.home:8083/q
|     org.jnp.server.NamingServer_Stub
|     java.rmi.server.RemoteStub
|     java.rmi.server.RemoteObject
|     xpwA
|     UnicastRef2
|_    thm-java-deserial.home
3873/tcp open  java-object Java Object Serialization
4446/tcp open  java-object Java Object Serialization
4712/tcp open  msdtc       Microsoft Distributed Transaction Coordinator (error)
4713/tcp open  pulseaudio?
| fingerprint-strings: 
|   DNSStatusRequestTCP, DNSVersionBindReqTCP, FourOhFourRequest, GenericLines, GetRequest, HTTPOptions, Help, JavaRMI, Kerberos, LANDesk-RC, LDAPBindReq, LDAPSearchReq, LPDString, NCP, NULL, NotesRPC, RPCCheck, RTSPRequest, SIPOptions, SMBProgNeg, SSLSessionReq, TLSSessionReq, TerminalServer, TerminalServerCookie, WMSRequest, X11Probe, afp, giop, ms-sql-s, oracle-tns: 
|_    126a
5445/tcp open  smbdirect?
5455/tcp open  apc-5455?
5500/tcp open  hotline?
| fingerprint-strings: 
|   DNSStatusRequestTCP: 
|     GSSAPI
|     DIGEST-MD5
|     CRAM-MD5
|     NTLM
|     thm-java-deserial
|   DNSVersionBindReqTCP, GetRequest: 
|     DIGEST-MD5
|     NTLM
|     GSSAPI
|     CRAM-MD5
|     thm-java-deserial
|   GenericLines, NULL: 
|     CRAM-MD5
|     GSSAPI
|     DIGEST-MD5
|     NTLM
|     thm-java-deserial
|   HTTPOptions: 
|     DIGEST-MD5
|     CRAM-MD5
|     GSSAPI
|     NTLM
|     thm-java-deserial
|   Help, RTSPRequest: 
|     CRAM-MD5
|     DIGEST-MD5
|     NTLM
|     GSSAPI
|     thm-java-deserial
|   Kerberos: 
|     NTLM
|     CRAM-MD5
|     DIGEST-MD5
|     GSSAPI
|     thm-java-deserial
|   RPCCheck: 
|     GSSAPI
|     NTLM
|     DIGEST-MD5
|     CRAM-MD5
|     thm-java-deserial
|   SSLSessionReq: 
|     NTLM
|     GSSAPI
|     DIGEST-MD5
|     CRAM-MD5
|     thm-java-deserial
|   TLSSessionReq: 
|     DIGEST-MD5
|     GSSAPI
|     CRAM-MD5
|     NTLM
|     thm-java-deserial
|   TerminalServerCookie: 
|     DIGEST-MD5
|     NTLM
|     CRAM-MD5
|     GSSAPI
|_    thm-java-deserial
5501/tcp open  tcpwrapped
8009/tcp open  ajp13       Apache Jserv (Protocol v1.3)
| ajp-methods: 
|   Supported methods: GET HEAD POST PUT DELETE TRACE OPTIONS
|   Potentially risky methods: PUT DELETE TRACE
|_  See https://nmap.org/nsedoc/scripts/ajp-methods.html
8080/tcp open  http        Apache Tomcat/Coyote JSP engine 1.1
|_http-server-header: Apache-Coyote/1.1
|_http-title: Welcome to JBoss AS
| http-methods: 
|_  Potentially risky methods: PUT DELETE TRACE
8083/tcp open  http        JBoss service httpd
|_http-title: Site doesn't have a title (text/html).
```

#### PORT 80

- I tried enumerating the website over and over again. 
- It turns out that the flag was hidden as a string inside the image present on the first blog.

```
strings be2sOV9.jpg

THM{REDACTED}
```

#### PORT 8080

- java 8 issue

