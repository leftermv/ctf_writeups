---
parent: "[[CTFs - THM]]"
resources:
---

```bash
# PLATFORM          THM
# CTF NAME          Forensics
# DESCRIPTION       This is a memory dump of compromised system, do some forensics kung-fu to explore the inside.
# DIFFICULTY        Hard 
# CTF LINK          https://tryhackme.com/r/room/forensics
```

### What is the Operating System of this Dump file? (OS name)
```
vol.py imageinfo -f victim.raw 
```

```
Suggested Profile(s) : Win7SP1x64, Win7SP0x64, Win2008R2SP0x64, Win2008R2SP1x64_24000, Win2008R2SP1x64_23418, Win2008R2SP1x64, Win7SP1x64_24000, Win7SP1x64_23418
                     AS Layer1 : WindowsAMD64PagedMemory (Kernel AS)
                     AS Layer2 : FileAddressSpace (/home/sansforensics/Downloads/victim.raw)
                      PAE type : No PAE
                           DTB : 0x187000L
                          KDBG : 0xf800028420a0L
          Number of Processors : 1
     Image Type (Service Pack) : 1
                KPCR for CPU 0 : 0xfffff80002843d00L
             KUSER_SHARED_DATA : 0xfffff78000000000L
           Image date and time : 2019-05-02 18:11:45 UTC+0000
     Image local date and time : 2019-05-02 11:11:45 -0700
```

```
windows
```

### What is the PID of SearchIndexer?

```
root@siftworkstation:/home/sansforensics/Downloads# vol.py --profile=Win7SP1x64 pstree -f victim.raw 
```

```
Name                                                  Pid   PPid   Thds   Hnds Time

.. 0xfffffa8003367060:SearchIndexer.                 2180    504     11    629 2019-05-02 18:03:32 UTC+0000
```

### What is the last directory accessed by the user?

```
vol.py --profile=Win7SP1x64 -f victim.raw shellbags > bags
```

- Check the Accessed Date field

### There are many suspicious open ports; which one is it? (ANSWER format: protocol:port)

```
vol.py --profile=Win7SP1x64 netscan -f victim.raw 
```

```
UDPv4 0.0.0.0:5005  *:* 2464 wmpnetwk.exe 2019-05-02 18:05:14 
UDPv6 :::5005       *:* 2464 wmpnetwk.exe 2019-05-02 18:05:14 
```

### Vads tag and execute protection are strong indicators of malicious processes; can you find which they are? (ANSWER format: Pid1;Pid2;Pid3)

```
vol.py --profile=Win7SP1x64 malfind -f victim.raw > vad
```

- See which PIDs have Vad Tags and Protection set.

### In the previous task, you identified malicious processes, so let's dig into them and find some Indicator of Compromise (IOC). You just need to find them and fill in the blanks (You may search for them on VirusTotal to discover more details).

- I found out that we can also dump the process memory of the processes found above. 
- However, what I did was to dump the entire VAD information for all processes.

```
mkdir VADs
vol.py --profile=Win7SP1x64 vaddump -f victim.raw --dump-dir VADs
```

- Then, based on the hints, I used strings and grep to find the information.

#### `www.go****.ru` (write full url without any quotation marks)**

```
strings * | grep \www.go.....ru
```

```
www.google.ru
www.go4win.ru
www.gocaps.ru
www.goporn.ru
```

#### `www.i****.com` (write full url without any quotation marks)

```
strings * | grep \www.i.....com
```

```
www.ikaka.com
http://www.iciba.com/search?s=%si
```

#### `www.ic******.com`

```
strings * | grep \www.ic.......com
```

```
www.icsalabs.com
```

#### `202.***.233.*** (Write full IP)`

```
strings * | grep \202.....233....
```

```
202.107.233.211
```

#### `***.200.**.164 (Write full IP)`

```
strings * | grep \....200....164
```

```
phttp://209.200.12.164/drm/provider_license_v7.php
```

#### `209.190.***.***`

```
strings * | grep \209.190........
```

```
http://209.190.122.186/drm/license-savenow.asp
```