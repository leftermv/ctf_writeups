---
parent: "[[CTFs - THM]]"
resources:
---

```bash
# PLATFORM          THM
# CTF NAME          Warzone 1
# DESCRIPTION       You received an IDS/IPS alert. Time to triage the alert to determine if its a true positive. 
# DIFFICULTY        Medium
# CTF LINK          https://tryhackme.com/r/room/warzoneone
```

### What was the alert signature for **Malware Command and Control Activity Detected**?

- Load the pcap into BRIM and filter using the default "Suricata Alerts by Category". 
- Righ click on the desired category and pivot to logs.
- The field **alert.signature** is the answer to the question.

![[Pasted image 20240918102032.png]]

### What is the source IP address? Enter your answer in a **defanged** format.

- From the same view as above, take a look at **src_ip** field.

### What IP address was the destination IP in the alert? Enter your answer in a **defanged** format.

- From the same view as above, take a look at **dest_ip** field.

### Still in VirusTotal, under **Community**, what threat group is attributed to this IP address?

- Search the IP from question 3 against virus total and check the comments left on Community tab.

### What is the malware family?

- The answer can be found in the same view as above.

### Do a search in VirusTotal for the domain from question 4. What was the majority file type listed under **Communicating Files**?

- You can use only the IP from question 4 and check the Relations tab.

### Inspect the web traffic for the flagged IP address; what is the **user-agent** in the traffic?

- Use the following query in BRIM

```
_path=="http" | cut id.resp_h, host, uri, user_agent
```

### Retrace the attack; there were multiple IP addresses associated with this attack. What were two other IP addresses? Enter the IP addressed **defanged** and in numerical order. (**format: IPADDR,IPADDR**)

```
_path == "http"
```

- Take a look at either **host** or **id.resp_h** columns. Double check in VT to see which one is malicious.

### What were the file names of the downloaded files? Enter the answer in the order to the IP addresses from the previous question. (**format: file.xyz,file.xyz**)

- You can see one in the **uri** column, the other in the **resp_filenames** column.
- Another hint is that they're the only entries that have **WIndows Installer** user agent.

### Inspect the traffic for the first downloaded file from the previous question. Two files will be saved to the same directory. What is the full file path of the directory and the name of the two files? (**format: C:\path\file.xyz,C:\path\file.xyz**)

- Go to wireshark and open PCAP.
- What I've done was to go to File -> Export Objects -> Click on the file found earlier and then (after being shown the packet number) right clicking on the entry and following the HTTP stream.

- In that view, I've performed a search after `C:\`. 
- You find a path and 2 files. They're both in the same path :) 

### Now do the same and inspect the traffic from the second downloaded file. Two files will be saved to the same directory. What is the full file path of the directory and the name of the two files? (format: C:\path\file.xyz,C:\path\file.xyz)

- The same steps as described above.

