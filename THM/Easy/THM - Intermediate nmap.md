---
parent: "[[CTFs - THM]]"
---
```bash
# PLATFORM          . THM
# CTF NAME          . Intermediate Nmap
# DESCRIPTION       . Can you combine your great nmap skills with other tools to log in to this machine?
# DIFFICULTY        . Easy
# CTF LINK          . https://tryhackme.com/room/intermediatenmap
```

```
sudo nmap -sSVC -T5 -p- 10.10.79.144 -oN advnmap
```

```
PORT      STATE SERVICE VERSION
22/tcp    open  ssh     OpenSSH 8.2p1 Ubuntu 4ubuntu0.4 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   3072 7ddceb90e4af33d99f0b219afcd577f2 (RSA)
|   256 83a74a61ef93a3571a57385c482aeb16 (ECDSA)
|_  256 30bfef9408860700f7fcdfe8edfe07af (ED25519)
2222/tcp  open  ssh     OpenSSH 8.2p1 Ubuntu 4ubuntu0.4 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   3072 8a27bfd80f5e8ce80f46c11731aeeb40 (RSA)
|   256 8e0bbe4bbb03f30b95d6c4d95078cac8 (ECDSA)
|_  256 974391a1d604f60d965e2f47f3596a27 (ED25519)
31337/tcp open  Elite?
| fingerprint-strings: 
|   DNSStatusRequestTCP, DNSVersionBindReqTCP, FourOhFourRequest, GenericLines, GetRequest, HTTPOptions, Help, Kerberos, LANDesk-RC, LDAPBindReq, LDAPSearchReq, LPDString, NULL, RPCCheck, RTSPRequest, SIPOptions, SMBProgNeg, SSLSessionReq, TLSSessionReq, TerminalServer, TerminalServerCookie, X11Probe: 
|     In case I forget - user:pass
|_    ubuntu:{REDACTED}
```

#### PORT 31337

- The credentials are written in the fingerprint of the service. 

- I tried to connect first to ssh on port 2222, but it didn't allow password authentication.
- I was able to SSH into the box using port 22.

- Flag is located in `/home/user/flag.txt`
