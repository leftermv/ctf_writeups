```bash
# PLATFORM          . THM
# CTF NAME          . HeartBleed
# DESCRIPTION       . SSL issues are still lurking in the wild! Can you exploit this web servers OpenSSL?
# DIFFICULTY        . Easy
# CTF LINK          . https://tryhackme.com/room/heartbleed
```

```
sudo nmap -sSVC -T5 -p- 3.255.178.50 -oN hbleed
```

```
PORT      STATE    SERVICE      VERSION
22/tcp    open     ssh          OpenSSH 7.4 (protocol 2.0)
| ssh-hostkey: 
|   2048 9a0e2921e8c19cf5aa1a94ba9a54564c (RSA)
|   256 028740bd3463d1cef791ab48a36b97c2 (ECDSA)
|_  256 eba69baf40b2b2293851962e2f724143 (ED25519)
23/tcp    filtered telnet
25/tcp    filtered smtp
111/tcp   open     rpcbind      2-4 (RPC #100000)
| rpcinfo: 
|   program version    port/proto  service
|   100000  2,3,4        111/tcp   rpcbind
|   100000  2,3,4        111/udp   rpcbind
|   100000  3,4          111/tcp6  rpcbind
|   100000  3,4          111/udp6  rpcbind
|   100024  1          40295/udp6  status
|   100024  1          42513/tcp6  status
|   100024  1          48606/udp   status
|_  100024  1          52171/tcp   status
135/tcp   filtered msrpc
136/tcp   filtered profile
137/tcp   filtered netbios-ns
138/tcp   filtered netbios-dgm
139/tcp   filtered netbios-ssn
443/tcp   open     ssl/http     nginx 1.15.7
|_http-title: What are you looking for?
| ssl-cert: Subject: commonName=localhost/organizationName=TryHackMe/stateOrProvinceName=London/countryName=UK
| Not valid before: 2019-02-16T10:41:14
|_Not valid after:  2020-02-16T10:41:14
|_ssl-date: TLS randomness does not represent time
| tls-nextprotoneg: 
|_  http/1.1
|_http-server-header: nginx/1.15.7
445/tcp   filtered microsoft-ds
52171/tcp open     status       1 (RPC #100024)
```

- We can find the following in the source code

```html
<!-- don't forget to remove secret communication pages -->
```

- The Heartbleed Vulnerability is described shortly in the first task of the room along with some extra links for further reading, so I will skip saying the same information here.

- The exploit we are facing is known as **CVE-2014-0346** / **CVE-2014-0160** and can be found [here](https://www.exploit-db.com/exploits/32745)

```
...
x-www-form-urlencoded....user_name=hacker101&user_email=haxor@haxor.com&user_message=*****{REDACTED}*****..x.J"t..z.....01..Sec-Fetch-Dest:
...

```

- The flag can be retrieved by checking the message after heartbleed disclosed the information.

