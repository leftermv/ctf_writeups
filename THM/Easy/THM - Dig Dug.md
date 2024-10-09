---
parent: "[[CTFs - THM]]"
---
```bash
# PLATFORM          . THM
# CTF NAME          . Dig Dug
# DESCRIPTION       . Turns out this machine is a DNS server - it's time to get your shovels out!
# DIFFICULTY        . Easy
# CTF LINK          . https://tryhackme.com/room/digdug
```

```
Oooh, turns out, this 10.10.183.19 machine is also a DNS server! If we could dig into it, I am sure we could find some interesting records! But... it seems weird, this only responds to a special type of request for a givemetheflag.com domain?
```

- Okay. If we use dig directly on that domain, we're getting the some public IP. we don't care about that.

- Dig directly on the DNS server (our machine) gives basic info

```
dig 10.10.183.19

; <<>> DiG 9.18.24-1-Debian <<>> 10.10.183.19
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NXDOMAIN, id: 5170
;; flags: qr rd ra; QUERY: 1, ANSWER: 0, AUTHORITY: 1, ADDITIONAL: 1

;; OPT PSEUDOSECTION:
; EDNS: version: 0, flags:; udp: 4096
; COOKIE: a9434b48a313cb644cd0633f65ec701da6972e3b5c5dfdc2 (good)
;; QUESTION SECTION:
;10.10.183.19.			IN	A

;; AUTHORITY SECTION:
.			900	IN	SOA	a.root-servers.net. nstld.verisign-grs.com. 2024030900 1800 900 604800 86400

;; Query time: 20 msec
;; SERVER: 193.231.252.1#53(193.231.252.1) (UDP)
;; WHEN: Sat Mar 09 16:20:13 EET 2024
;; MSG SIZE  rcvd: 144
```

- What if we use this DNS server to query the `givemetheflag.com` domain?

```
dig @10.10.183.19 givemetheflag.com
```

```
; <<>> DiG 9.18.24-1-Debian <<>> @10.10.183.19 givemetheflag.com
; (1 server found)
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 5481
;; flags: qr aa; QUERY: 1, ANSWER: 1, AUTHORITY: 0, ADDITIONAL: 0

;; QUESTION SECTION:
;givemetheflag.com.		IN	A

;; ANSWER SECTION:
givemetheflag.com.	0	IN	TXT	"flag{REDACTED}"

;; Query time: 56 msec
;; SERVER: 10.10.183.19#53(10.10.183.19) (UDP)
;; WHEN: Sat Mar 09 16:22:06 EET 2024
;; MSG SIZE  rcvd: 86
```

- Alternatively, the flag can be retrieved by using `nslookup`.

```
nslookup givemetheflag.com 10.10.183.19


Server:		10.10.183.19
Address:	10.10.183.19#53
givemetheflag.com	text = "flag{REDACTED}"
```



