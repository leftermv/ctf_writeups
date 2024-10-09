```bash
# PLATFORM          . THM
# CTF NAME          . Investigating Windows
# DESCRIPTION       . A windows machine has been hacked, its your job to go investigate this windows machine and find clues to what the hacker might have done.
# DIFFICULTY        . Easy
# CTF LINK          . https://tryhackme.com/room/investigatingwindows
```

```
CREDENTIALS

Username: Administrator  
Password: letmein123!

RDP
xfreerdp /u:Administrator /v:10.10.47.207 /dynamic-resolution /cert-ignore 
```


> 1. Whats the version and year of the windows machine?

- Running `asysteminfo.exe` from Powershell, we can find the version / year of the OS on the `OS Name:` line.

`OS Name:                   Microsoft Windows Server 2016 DatacenterOS Version:                    10.0.14393 N/A Build 14393                `

_____


> 2. Which user logged in last?

- I went to `Event Viewer -> Security ` and filtered the results only for `Event IDs 4624 and 4625`.

- Checking by the timestamp, last user logged in was `Administrator.`

____

> 3. When did John log onto the system last?
  Answer format: MM/DD/YYYY H:MM:SS AM/PM

- Still in `Event Viewer -> Security` with the same filters applied, search entries and look at `Account Name` under `New Logon` section.

- Alternatively, you can switch to `Details` tab and look at `TargetUserName`.

- The same result can be obtained by running `net user John | findstr /B /C:"Last logon"` in powershell.

____

> 4. What IP does the system connect to when it first starts?

- When you first RDP on the server, a cmd pops up running the `p.exe` file located in `/TMP`. The server is trying to connect to `10.34.2.3`

-  This can also be seen by running `regedit` in `Run` and navigating to `HKEY_LOCAL_MACHINE -> Software -> Microsoft -> Windows -> CurrentVersion -> Run`

____

> 5. What two accounts had administrative privileges (other than the Administrator user)?
     Answer format: username1, username2

- We can find this out by checking the members of the `Administrators` group: `net localgroup Administrators`

____

> 6. Whats the name of the scheduled task that is malicous.

- The task name is `Clean File System`. 

- This can be found by running `schtasks` and it's right at the top, might be hard to see because the output is very verbose.

- Under `Task To Run`, we can see that it creates a listener on port `1348`, allowing the attackers to get in.

- - Additional info can be gathered by running `schtasks /query /tn "Clean file system" /fo list 

- However, this is not the only malicious task; Take a look at `GameOver` task - we can see that it dumps the passwords to `C:\TMP\o.txt` file using mimikatz.

```bash
# Clean file system Task
Task To Run:     C:\TMP\nc.ps1 -l 1348 

# GameOver Task
Task To Run:     C:\TMP\mim.exe sekurlsa::LogonPasswords > C:\TMP\o.txt 
```

____

> 7. What file was the task trying to run daily?

- Answered in question 6.

____

> 8. What port did this file listen locally for?

- Answered in question 6.

_____

> 9. When did Jenny last logon?

- Same as question 3 - never.

__________

> 10. At what date did the compromise take place?
  Answer format: MM/DD/YYYY

- The day the malicious tasks were created. Technically, answered in question 6 as well.

___

> 11. During the compromise, at what time did Windows first assign special privileges to a new logon?
	  Answer format: MM/DD/YYYY HH:MM:SS AM/PM

- Go to `Event Viewer -> Security ` and filter by `Event ID 4672`. More details [here](https://learn.microsoft.com/en-us/windows/security/threat-protection/auditing/event-4672)

- We know the compromise started on the date found in step 10, so check for `Special Logons` from that date. Since there are a few of them, the task gives us a hint: the value for seconds is `49`.

- The value can be found by either looking at `Date and Time` in the general view or by clicking on the entry and checking `Logged:` under `General` tab.

_____

> 12. What tool was used to get Windows passwords?

- Remember `GameOver` task? Take a look under `Actions` tab :) 

_____

> 13. What was the attackers external control and command servers IP?

- Run `Get-DnsClientCache` in powershell to check the cached DNS on the server. We see that the ip assigned for `google.com` doesn't actually belong to google, so this is DNS poisoning. 

- The IP belongs to the attackers C2 infrastructure.

-----

> 14. What was the extension name of the shell uploaded via the servers website?

- We can find the files in the IIS webserver directroy, `C:\inetpub\wwwroot\`. 

------

> 15. What was the last port the attacker opened?

- For this, we can check `Inbound Firewall Rules` in Windows. The rule is named `Allow outside connections for development.`

-------

> 16. Check for DNS poisoning, what site was targeted?

- Answered in question 13.