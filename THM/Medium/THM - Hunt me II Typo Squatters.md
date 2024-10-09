---
parent: "[[CTFs - THM]]"
resources:
---
Just working on a typical day as a software engineer, Perry received an encrypted 7z archive from his boss containing a snippet of a source code that must be completed within the day. Realising that his current workstation does not have an application that can unpack the file, he spins up his browser and starts to search for software that can aid in accessing the file. Without validating the resource, Perry immediately clicks the first search engine result and installs the application. 

![A screenshot of search engine results based on 7zip search.](https://tryhackme-images.s3.amazonaws.com/user-uploads/5dbea226085ab6182a2ee0f7/room-content/f556cb74ecd4a6fc10926b8fcbb9cff4.png)  

Last **September 26, 2023**, one of the security analysts observed something unusual on the workstation owned by Perry based on the generated endpoint and network logs. Given this, your SOC lead has assigned you to conduct an in-depth investigation on this workstation and assess the impact of the potential compromise.

---

### What is the URL of the malicious software that was downloaded by the victim user?

- From the scenario, we see that the user used the browser to download the file

```
http* and process.name: chrome.exe
```

- Then I've filtered after [Sysmon event ID 15](https://www.ultimatewindowssecurity.com/securitylog/encyclopedia/event.aspx?eventid=90015) to check downloaded files, as the result above didn't provide network details.

```
process.name: chrome.exe and event.code: 15
```

- Check the `winlog.event_data.Contents` field.

### What is the IP address of the domain hosting the malware?  

![[Pasted image 20241004160236.png]]

```
event.code: 22
```

- If we add the `dns.resolved_ip` and `dns.question_name` fields, we can see that the `206.189.34.218` ip is mapped to `7zipp.org`
### What is the PID of the process that executed the malicious software?  

```
"7z2301-x64.msi" and event.code: 1
```

- Add the `process.pid` field.

### Following the execution chain of the malicious payload, another remote file was downloaded and executed. What is the full command line value of this suspicious activity?

```
"http*" and process.name: 'powershell.exe'
```

![[Pasted image 20241004161833.png]]

### The newly downloaded script also installed the legitimate version of the application. What is the full file path of the legitimate installer?  

```
file.path: * and process.name: 'powershell.exe'
```

![[Pasted image 20241004162055.png]]

### What is the name of the service that was installed?

```
event.code: 1 and 7z*
```

![[Pasted image 20241004162308.png]]

- Assuming it was related to 7zip and it's a service... so I've checked process creation logs.

### The attacker was able to establish a C2 connection after starting the implanted service. What is the username of the account that executed the service?  

- Answered from the SS above. Take a look at the username.

### After dumping LSASS data, the attacker attempted to parse the data to harvest the credentials. What is the name of the tool used by the attacker in this activity?  

```
*lsass.dmp*
```

![[Pasted image 20241004162815.png]]

### What is the credential pair that the attacker leveraged after the credential dumping activity? (format: username:hash)  

```
event.code: 1 and host.name: "WKSTN-03*"
```

![[Pasted image 20241004163201.png]]


### After gaining access to the new account, the attacker attempted to reset the credentials of another user. What is the new password set to this target account?  

- Same query as above, just look through the logs.

![[Pasted image 20241004163253.png]]

### What is the name of the workstation where the new account was used?  

```
user.name: anna*
```

- Filter by her name and take a look at the workstation name :) 

### After gaining access to the new workstation, a new set of credentials was discovered. What is the username, including its domain, and password of this new account?  

```
event.code: 1 and host.name: "WKSTN-02*"
```

![[Pasted image 20241004163718.png]]

### Aside from mimikatz, what is the name of the PowerShell script used to dump the hash of the domain admin?  

```
event.code: 1 and *ps1*
```

![[Pasted image 20241004163954.png]]

### What is the AES256 hash of the domain admin based on the credential dumping output?  

```
"*Invoke-SharpKatz*" and "*hall*"
```

![[Pasted image 20241004164235.png]]

### After gaining domain admin access, the attacker popped ransomware on workstations. How many files were encrypted on all workstations?

```
bomb.exe AND winlog.event_id:11
```

