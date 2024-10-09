---
parent: "[[CTFs - THM]]"
resources:
---

```bash
# PLATFORM          THM
# CTF NAME          Warzone 2
# DESCRIPTION       You received an IDS/IPS alert. Time to triage the alert to determine if its a true positive. 
# DIFFICULTY        Medium
# CTF LINK          https://tryhackme.com/r/room/warzonetwo
```



### What was the alert signature for **A Network Trojan was Detected**?

Load the pcap into BRIM and filter using the default "Suricata Alerts by Category". 
- Righ click on the desired category and pivot to logs.
- The field **alert.signature** is the answer to the question.

### What was the alert signature for **Potential Corporate Privacy Violation**?

- Same procedure as above.

### What was the IP to trigger either alert? Enter your answer in a **defanged** format.

- From the view(s) above, take a look at **src_ip**. 

### Provide the full URI for the malicious downloaded file. In your answer, **defang** the URI.

```
_path == "http" | id.resp_h == ip_from_above
```

- Combine **host** and **uri** columns into one string. Defang it.

### What is the name of the payload within the cab file?

- Multiple methods. I'll showcase a different method than the one suggested in the hints.
- In BRIM, use the following query.
```
_path == "files" | gap1.cab
```

- You can obtain the hash from the **sha1** column, thus not needing to download the file and get the hash yourself using `sha1sum`.

### What is the user-agent associated with this network traffic?

- Use the same query used in the question that asked full defanged URI.
- Take a look at the **user_agent** field.

### What other domains do you see in the network traffic that are labelled as malicious by VirusTotal? Enter the domains **defanged** and in alphabetical order. (**format: domain[.]zzz,domain[.]zzz**)

```
_path == "http" | sort host
```

- Take a look at the domains ad URIs. 
- Not many of them, can check them all in VT.

### There are IP addresses flagged as **Not Suspicious Traffic**. What are the IP addresses? Enter your answer in numerical order and **defanged**. (format: IPADDR,IPADDR)

```
event_type=="alert" alert.severity==3 alert.category=="Not Suspicious Traffic"
```

### For the first IP address flagged as Not Suspicious Traffic. According to VirusTotal, there are several domains associated with this one IP address that was flagged as malicious. What were the domains you spotted in the network traffic associated with this IP address? Enter your answer in a **defanged** format. Enter your answer in alphabetical order, in a defanged format. (**format: domain[.]zzz,domain[.]zzz,etc**)

- Filter using the default "Suricata Alerts by Category". 
- Righ click on the desired category and pivot to logs.
- Take notes of the IPs

```
ip | cut query
```

### Now for the second IP marked as Not Suspicious Traffic. What was the domain you spotted in the network traffic associated with this IP address? Enter your answer in a **defanged** format. (format: domain[.]zzz)

- Same as above.