---
parent: "[[CTFs - THM]]"
resources:
---

```bash
# PLATFORM          THM
# CTF NAME          Masterminds
# DESCRIPTION       Practice analyzing malicious traffic using Brim.
# DIFFICULTY        Medium
# CTF LINK          https://tryhackme.com/r/room/mastermindsxlq
```


# Infection 1

### Provide the victim's IP address.

```
_path =="conn" | cut id.orig_h, id.resp_p, id.resp_h | sort  | uniq -c | sort -r count
```

### The victim attempted to make HTTP connections to two suspicious domains with the status '404 Not Found'. Provide the hosts/domains requested.

```
_path=="http" | cut id.orig_h, id.resp_h, host, status_msg 
```

### The victim made a successful HTTP connection to one of the domains and received the response_body_len of 1,309 (uncompressed content size of the data transferred from the server). Provide the domain and the destination IP address.

```
_path == "http" | cut id.orig_h, id.resp_h, host, response_body_len
```

### How many unique DNS requests were made to cab[.]myfkn[.]com domain (including the capitalized domain)?

```
_path == "dns" | count() by query
```

### Provide the URI of the domain bhaktivrind[.]com that the victim reached out over HTTP.

```
_path == "http" | host == "bhaktivrind.com"
```

### Provide the IP address of the malicious server and the executable that the victim downloaded from the server. 

```
_path == "http"
```

- Check the only `.exe` in the URI's 

### Based on the information gathered from the second question, provide the name of the malware using [VirusTotal](https://www.virustotal.com/gui/home/upload).

- Check Community tab.

---

# Infection 2
### Provide the IP address of the victim machine.
```
_path == "conn"
```

### Provide the IP address the victim made the POST connections to. 

```
_path == "http" | cut id.orig_h, id.resp_h, method
```

### How many POST connections were made to the IP address in the previous question?

- Count :) 

### Provide the domain where the binary was downloaded from.

- Also visible from the query above. 

### Provide the name of the binary including the full URI.

- Same as above.

### Provide the IP address of the domain that hosts the binary.

- Same :| 

### There were 2 Suricata "A Network Trojan was detected" alerts. What were the source and destination IP addresses?

- Use the **Suricata Alerts by Category** built-in filter.

OR

```
event_type == "alert" alert.severity == 1 alert.category == "A network Trojan was detected"
```

### Taking a look at .top domain in HTTP requests, provide the name of the stealer (Trojan that gathers information from a system) involved in this packet capture using [URLhaus Database](https://urlhaus.abuse.ch/).

- Just search URLhaus after the domain found for question 4.

---

# Infection 3

### Provide the IP address of the victim machine.

```
_path == "conn"
```

### Provide three C2 domains from which the binaries were downloaded (starting from the earliest to the latest in the timestamp)

```
_path == "http" | sort ts
```

- There's just a subtle difference between them :) 

### Provide the IP addresses for all three domains in the previous question.

- Use the query above.

### How many unique DNS queries were made to the domain associated from the first IP address from the previous answer?

```
_path == "dns" | query == "efhoahegue.ru"
```

### How many binaries were downloaded from the above domain in total?

```
_path == "http" | host == "efhoahegue.ru
```

### Provided the user-agent listed to download the binaries.

- Also visible from the query above, bun can use the following to narrow down results

```
_path == "http" | host == "efhoahegue.ru" | cut host, uri, user_agent
```

### Provide the amount of DNS connections made in total for this packet capture.

```
_path == "dns" | count()
```

### With some OSINT skills, provide the name of the worm using the first domain you have managed to collect from Question 2. (Please use quotation marks for Google searches, don't use .ru in your search, and DO NOT interact with the domain directly).

- A simple search after the domain (without .ru) and worm will reveal some interesting results 

```
"efhoahegue" worm
```
